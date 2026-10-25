"""Tests for the browser redirect check's logic, driven by a fake Playwright.

The real Chromium run is ``scripts/check_browser_redirects.py`` in the
``validate`` tier. These tests pin what it asks the browser for and how it
reads the answers, without a browser.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from scripts.repo_tools import browser_redirects
from scripts.repo_tools.browser_redirects import (
    FRAGMENT,
    collect_browser_redirect_issues,
    expected_landing,
    fulfill_new_home,
    old_url,
)
from scripts.repo_tools.redirect_stubs import NEW_HOME, NEW_ORIGIN, OLD_BASE

TARGETS: dict[str, str | None] = {
    OLD_BASE: NEW_HOME,
    f"{OLD_BASE}about-us/": f"{NEW_HOME}about-us/",
}


class FakePage:
    """A page whose landing for each opened URL comes from ``land``."""

    def __init__(self, land: Callable[[str], str], links: int, log: list[str]) -> None:
        """Store how this page lands, how many home links it has, and the shared log."""
        self._land, self._links, self._log = land, links, log
        self.url = "about:blank"
        self._opened = ""

    def goto(self, url: str, wait_until: str) -> None:
        """Record the open; a 404 page stays where it was opened."""
        self._log.append(f"goto {url} ({wait_until})")
        self._opened = url
        if url.endswith("404.html"):
            self.url = url

    def wait_for_url(self, expected: str, wait_until: str) -> None:
        """Land as ``land`` says, and time out like Playwright if that isn't ``expected``."""
        self.url = self._land(self._opened)
        if self.url != expected:
            raise TimeoutError(f"Timeout 10000ms exceeded.\n=== logs ===\n{self.url}")

    def locator(self, selector: str) -> Any:
        """Return a locator that counts this page's links home."""
        return SimpleNamespace(count=lambda: self._links)


class FakeContext:
    """Records its routes and hands out one fake page."""

    def __init__(self, page: FakePage, javascript: bool, log: list[str]) -> None:
        """Store the page this context hands out and its JavaScript mode."""
        self.page, self.javascript, self.log = page, javascript, log
        self.routes: list[str] = []

    def route(self, pattern: str, handler: Any) -> None:
        """Record a route pattern in registration order."""
        self.routes.append(pattern)

    def set_default_timeout(self, timeout: int) -> None:
        """Accept the timeout; the fake never waits."""

    def new_page(self) -> FakePage:
        """Return this context's one page."""
        return self.page

    def close(self) -> None:
        """Log the close, so tests can see contexts are released."""
        self.log.append("context closed")


def _playwright(
    land: Callable[[str], str], *, links: int = 1
) -> tuple[Any, list[FakeContext], list[str]]:
    """Return a fake ``sync_playwright`` and the contexts and log it records."""

    contexts: list[FakeContext] = []
    log: list[str] = []

    def new_context(java_script_enabled: bool) -> FakeContext:
        context = FakeContext(FakePage(land, links, log), java_script_enabled, log)
        contexts.append(context)
        return context

    browser = SimpleNamespace(new_context=new_context, close=lambda: log.append("browser closed"))
    playwright = SimpleNamespace(chromium=SimpleNamespace(launch=lambda: browser))

    class Manager:
        def __enter__(self) -> Any:
            return playwright

        def __exit__(self, *exc: object) -> None:
            return None

    return (lambda: Manager()), contexts, log


def _axe(violations: list[dict[str, str]] | None = None) -> Callable[[], Any]:
    """Return a fake axe factory that reports ``violations`` for every page."""

    result = SimpleNamespace(response={"violations": violations or []})
    return lambda: SimpleNamespace(run=lambda page, options: result)


def _as_built(opened: str) -> str:
    """Land each opened address where its stub says, keeping the fragment."""

    address, _, fragment = opened.partition("#")
    target = TARGETS[address] or ""
    return f"{target}#{fragment}" if fragment else target


def test_urls_carry_the_fragment_only_with_javascript() -> None:
    """Only the script can carry a fragment; the refresh lands on the page itself."""

    assert old_url(f"{OLD_BASE}about-us/", javascript=True) == f"{OLD_BASE}about-us/#{FRAGMENT}"
    assert old_url(f"{OLD_BASE}about-us/", javascript=False) == f"{OLD_BASE}about-us/"
    assert expected_landing(NEW_HOME, javascript=True) == f"{NEW_HOME}#{FRAGMENT}"
    assert expected_landing(NEW_HOME, javascript=False) == NEW_HOME


def test_every_address_is_followed_both_ways_then_the_404_page(tmp_path: Path) -> None:
    """Two passes over every address, one with JavaScript and one without, then 404.html."""

    sync_playwright, contexts, log = _playwright(_as_built)

    issues = collect_browser_redirect_issues(sync_playwright, _axe(), tmp_path, TARGETS)

    assert issues == []
    assert [context.javascript for context in contexts] == [True, False, True]
    assert [line for line in log if line.startswith("goto")] == [
        f"goto {OLD_BASE}#{FRAGMENT} (commit)",
        f"goto {OLD_BASE}about-us/#{FRAGMENT} (commit)",
        f"goto {OLD_BASE} (commit)",
        f"goto {OLD_BASE}about-us/ (commit)",
        f"goto {OLD_BASE}404.html (load)",
    ]
    assert log[-1] == "browser closed"


def test_the_new_home_is_answered_ahead_of_the_artifact_catch_all(tmp_path: Path) -> None:
    """Playwright runs the last matching route first, so the new home must be registered last."""

    sync_playwright, contexts, _log = _playwright(_as_built)

    collect_browser_redirect_issues(sync_playwright, _axe(), tmp_path, TARGETS)

    assert all(context.routes == ["**/*", f"{NEW_ORIGIN}/**"] for context in contexts)


def test_a_wrong_landing_is_reported_by_address_and_mode(tmp_path: Path) -> None:
    """A stub that lands elsewhere is named, with the mode it failed in."""

    def drops_fragments(opened: str) -> str:
        return _as_built(opened).partition("#")[0]

    sync_playwright, _contexts, _log = _playwright(drops_fragments)

    issues = collect_browser_redirect_issues(sync_playwright, _axe(), tmp_path, TARGETS)

    assert issues == [
        f"{OLD_BASE} (with JavaScript): did not land on {NEW_HOME}#{FRAGMENT}: "
        "Timeout 10000ms exceeded.",
        f"{OLD_BASE}about-us/ (with JavaScript): did not land on "
        f"{NEW_HOME}about-us/#{FRAGMENT}: Timeout 10000ms exceeded.",
    ]


def test_an_address_without_a_clean_stub_is_reported_and_not_opened(tmp_path: Path) -> None:
    """The static check names the broken stub; the browser check doesn't guess at it."""

    sync_playwright, _contexts, log = _playwright(_as_built)
    targets = {**TARGETS, f"{OLD_BASE}about-us/": None}

    issues = collect_browser_redirect_issues(sync_playwright, _axe(), tmp_path, targets)

    assert issues == [f"{OLD_BASE}about-us/: no clean stub to follow"]
    assert not any("about-us" in line for line in log)


def test_the_404_page_must_link_home_and_pass_axe(tmp_path: Path) -> None:
    """The one page a reader can stay on is checked like any other page."""

    sync_playwright, _contexts, _log = _playwright(_as_built, links=0)
    violation = {"id": "color-contrast", "impact": "serious", "help": "Contrast"}

    issues = collect_browser_redirect_issues(sync_playwright, _axe([violation]), tmp_path, TARGETS)

    assert issues == [
        f"404.html has no single link to {NEW_HOME}",
        "404.html: axe color-contrast [serious]: Contrast",
    ]


def test_the_new_home_placeholder_never_reaches_the_network() -> None:
    """Every new-home request is fulfilled in the browser with a placeholder page."""

    calls: list[dict[str, Any]] = []
    route = SimpleNamespace(fulfill=lambda **kwargs: calls.append(kwargs))

    fulfill_new_home(route)

    assert len(calls) == 1
    assert calls[0]["status"] == 200
    assert calls[0]["content_type"] == "text/html; charset=utf-8"


def test_a_missing_built_site_is_reported(tmp_path: Path) -> None:
    """The check names the missing build rather than launching a browser at nothing."""

    issues = browser_redirects.find_browser_redirect_issues(tmp_path, Path("site"))

    assert issues == [f"{tmp_path / 'site'} is missing; run `task build` first"]


@pytest.mark.parametrize("javascript", [True, False])
def test_contexts_follow_the_requested_javascript_mode(tmp_path: Path, javascript: bool) -> None:
    """Each pass gets its own context, so a JavaScript setting never leaks between them."""

    sync_playwright, contexts, _log = _playwright(_as_built)

    collect_browser_redirect_issues(sync_playwright, _axe(), tmp_path, TARGETS)

    assert sum(1 for context in contexts[:2] if context.javascript is javascript) == 1


def test_the_cli_reports_a_missing_build_without_a_browser(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The validate step's command line fails, by name, before any browser starts."""

    from scripts import check_browser_redirects

    assert check_browser_redirects.main(["--site-dir", "no-such-site"]) == 1
    assert "no-such-site is missing; run `task build` first" in capsys.readouterr().err
