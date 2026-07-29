"""Tests for the hosted browser-readiness source ratchet."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.check_browser_readiness_contract as readiness_cli
from scripts.repo_tools.browser_readiness_contract import (
    BROWSER_READINESS_SEAM,
    find_browser_readiness_contract_issues,
)
from tests.browser_readiness_fixtures import (
    VALID_CONTEXT_SEAM,
    write_runtime_sources,
)


def test_browser_readiness_contract_accepts_shared_helper_calls(tmp_path: Path) -> None:
    """Runtime modules may call helpers without owning navigation semantics."""

    write_runtime_sources(
        tmp_path,
        (
            "def run(page):\n    return navigate_to_ready_page(page)\n",
            "def run(page):\n    return navigate_to_instant_page(page)\n",
        ),
    )

    assert find_browser_readiness_contract_issues(tmp_path) == []


def test_browser_readiness_contract_reports_every_forbidden_seam(tmp_path: Path) -> None:
    """Network-idle and direct navigation must fail with file-and-line evidence."""

    write_runtime_sources(
        tmp_path,
        (
            "def run(page):\n    page.goto('https://example.test', wait_until='networkidle')\n",
            "def run(page):\n"
            "    page.wait_for_url('https://example.test')\n"
            "    page.wait_for_load_state('load')\n",
        ),
    )

    issues = find_browser_readiness_contract_issues(tmp_path)

    assert len(issues) == 4
    assert any("browser_smoke.py:2: networkidle" in issue for issue in issues)
    assert any("browser_smoke.py:2: page.goto()" in issue for issue in issues)
    assert any("browser_accessibility.py:2: page.wait_for_url()" in issue for issue in issues)
    assert any(
        "browser_accessibility.py:3: page.wait_for_load_state()" in issue for issue in issues
    )


def test_browser_readiness_contract_rejects_network_idle_inside_the_shared_seam(
    tmp_path: Path,
) -> None:
    """Centralizing a discouraged readiness signal must not make it acceptable."""

    write_runtime_sources(
        tmp_path,
        (
            "def run(page):\n    return navigate_to_ready_page(page)\n",
            "def run(page):\n    return navigate_to_instant_page(page)\n",
        ),
    )
    (tmp_path / BROWSER_READINESS_SEAM).write_text(
        "def load(page):\n"
        "    page.goto('https://example.test', wait_until='networkidle')\n"
        f"{VALID_CONTEXT_SEAM}",
        encoding="utf-8",
    )

    issues = find_browser_readiness_contract_issues(tmp_path)

    assert len(issues) == 2
    assert any("browser_routes.py:2: networkidle" in issue for issue in issues)
    assert any("must declare wait_until='load' literally" in issue for issue in issues)


def test_browser_readiness_contract_rejects_url_waits_inside_the_shared_seam(
    tmp_path: Path,
) -> None:
    """An exact-URL wait must not restore the old unreachable redirect diagnostic."""

    write_runtime_sources(
        tmp_path,
        (
            "def run(page):\n    return navigate_to_ready_page(page)\n",
            "def run(page):\n    return navigate_to_instant_page(page)\n",
        ),
    )
    (tmp_path / BROWSER_READINESS_SEAM).write_text(
        "def load(page):\n"
        "    page.goto('https://example.test', wait_until='load')\n"
        "    page.wait_for_url('https://example.test')\n"
        f"{VALID_CONTEXT_SEAM}",
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "scripts/repo_tools/browser_routes.py:3: page.wait_for_url() is not "
        "a supported browser readiness signal"
    ]


def test_browser_readiness_contract_centralizes_fail_closed_context_creation(
    tmp_path: Path,
) -> None:
    """Every browser context must inherit the canonical router and SW boundary."""

    write_runtime_sources(
        tmp_path,
        (
            "def run(browser):\n    return browser.new_context()\n",
            "def run(page):\n    return navigate_to_ready_page(page)\n",
        ),
    )
    (tmp_path / BROWSER_READINESS_SEAM).write_text(
        "def load(page):\n"
        "    page.goto('https://example.test', wait_until='load')\n"
        "def context(browser):\n"
        "    return browser.new_context()\n",
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "scripts/repo_tools/browser_routes.py: the shared seam must create exactly "
        "one browser context and install exactly one canonical artifact route and "
        "one live-preview transport route",
        "scripts/repo_tools/browser_routes.py:4: browser.new_context() must "
        "declare service_workers='block' literally",
        "scripts/repo_tools/browser_routes.py:4: browser.new_context() must set "
        "offline=target.artifact_dir is not None literally",
        "scripts/repo_tools/browser_smoke.py:2: browser.new_context() must go "
        "through scripts/repo_tools/browser_routes.py",
    ]


@pytest.mark.parametrize(
    "relative_path",
    ("scripts/rogue_browser.py", "main.py"),
)
def test_browser_readiness_contract_discovers_a_future_runtime_module(
    tmp_path: Path,
    relative_path: str,
) -> None:
    """Repo automation outside repo_tools must not escape the browser ratchet."""

    write_runtime_sources(
        tmp_path,
        (
            "def run(page):\n    return navigate_to_ready_page(page)\n",
            "def run(page):\n    return navigate_to_instant_page(page)\n",
        ),
    )
    rogue_script = tmp_path / relative_path
    rogue_script.parent.mkdir(parents=True, exist_ok=True)
    rogue_script.write_text(
        "def run(page):\n    page.goto('https://example.test', wait_until='networkidle')\n",
        encoding="utf-8",
    )

    issues = find_browser_readiness_contract_issues(tmp_path)

    assert issues == [
        f"{relative_path}:2: networkidle is not a valid readiness signal for MkDocs live preview",
        f"{relative_path}:2: page.goto() must go through scripts/repo_tools/browser_routes.py",
    ]


def test_browser_readiness_contract_fails_closed_on_an_unreadable_runtime(
    tmp_path: Path,
) -> None:
    """A missing configured module must not turn the source ratchet green."""

    with pytest.raises(RuntimeError, match="Unable to read browser runtime source"):
        find_browser_readiness_contract_issues(tmp_path)


def test_browser_readiness_cli_reports_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The thin CLI should expose a clean contract as exit zero."""

    monkeypatch.setattr(
        "scripts.repo_tools.browser_readiness_contract.find_browser_readiness_contract_issues",
        lambda _root: [],
    )

    assert readiness_cli.main() == 0
    assert capsys.readouterr().out == ("Browser readiness is centralized and live-preview safe.\n")


def test_browser_readiness_cli_reports_findings(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The thin CLI should surface contract evidence and exit nonzero."""

    monkeypatch.setattr(
        "scripts.repo_tools.browser_readiness_contract.find_browser_readiness_contract_issues",
        lambda _root: ["scripts/repo_tools/browser_smoke.py:2: direct navigation"],
    )

    assert readiness_cli.main() == 1
    assert "direct navigation" in capsys.readouterr().err
