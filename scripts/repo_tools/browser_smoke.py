"""Browser smoke checks for critical shared docs UI behaviors."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any
from urllib.parse import urljoin


class _QuietStaticSiteHandler(SimpleHTTPRequestHandler):
    """Static-site request handler without per-request console logging."""

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default request logging for local smoke-test servers."""


@dataclass(frozen=True)
class BrowserSmokeTarget:
    """A representative docs page for browser-level smoke checks."""

    section: str
    path: str
    active_link_text: str


SMOKE_TARGETS = (
    BrowserSmokeTarget("About Us", "/about-us/about-opi/operating-frame/", "Operating Frame"),
    BrowserSmokeTarget(
        "How We Work",
        "/how-we-work/operations/leadership-norms/",
        "Leadership Norms",
    ),
    BrowserSmokeTarget(
        "Our Teams",
        "/our-teams/innovation-lab/digital-product-methodology/",
        "Digital Product Methodology",
    ),
    BrowserSmokeTarget("Resources", "/resources/reference/glossary/", "Glossary"),
    BrowserSmokeTarget(
        "Public",
        "/public/website-information-architecture/",
        "Website Information Architecture",
    ),
)


def normalize_base_url(base_url: str) -> str:
    """Normalize a base URL so downstream joins are stable."""

    return base_url.rstrip("/") + "/"


@contextmanager
def local_site_server(site_dir: Path) -> Iterator[str]:
    """Serve a built static site from a temporary local HTTP server."""

    handler = partial(_QuietStaticSiteHandler, directory=str(site_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    try:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host_raw, port = server.server_address[0], server.server_address[1]
        host = host_raw.decode() if isinstance(host_raw, bytes) else host_raw
        yield f"http://{host}:{port}/"
    finally:
        server.shutdown()
        server.server_close()


def _resolve_theme_color(page: Any, css_variable: str) -> str:
    """Resolve a CSS custom property to the computed RGB value used by the page."""

    script = """
    ([variableName]) => {
      const probe = document.createElement("div");
      probe.style.color = `var(${variableName})`;
      document.body.appendChild(probe);
      const resolved = getComputedStyle(probe).color;
      probe.remove();
      return resolved;
    }
    """
    return str(page.evaluate(script, [css_variable]))


def _check_mobile_nav_state(page: Any, target: BrowserSmokeTarget, scheme: str) -> list[str]:
    """Validate mobile drawer open/close behavior and active-link styling."""

    issues: list[str] = []
    drawer_toggle = page.locator('label.md-header__button[for="__drawer"]').first
    drawer_overlay = page.locator('label.md-overlay[for="__drawer"]').first
    drawer_state = page.locator("#__drawer")

    if drawer_toggle.count() == 0:
        return [f"{target.section} ({scheme}): drawer toggle was not found."]

    drawer_toggle.click()
    if not drawer_state.is_checked():
        issues.append(f"{target.section} ({scheme}): drawer did not open.")
        return issues

    active_link = page.locator(
        ".md-nav--primary .md-nav__link--active",
        has_text=target.active_link_text,
    ).first
    if active_link.count() == 0:
        issues.append(
            f"{target.section} ({scheme}): active nav link "
            f"'{target.active_link_text}' was not found."
        )
    else:
        expected_color = _resolve_theme_color(page, "--opi-nav-accent")
        active_color = active_link.evaluate("element => getComputedStyle(element).color")
        if active_color != expected_color:
            issues.append(
                f"{target.section} ({scheme}): active nav color was {active_color}, "
                f"expected {expected_color}."
            )

    drawer_overlay.click()
    if drawer_state.is_checked():
        issues.append(f"{target.section} ({scheme}): drawer did not close.")

    return issues


def _check_card_focus_state(page: Any, scheme: str) -> list[str]:
    """Validate that shared cards still expose a visible keyboard focus treatment."""

    card_link = page.locator(".opi-card-link").first
    if card_link.count() == 0:
        return [f"Home ({scheme}): no shared card links were found."]

    card_link.focus()
    outline_style = card_link.evaluate("element => getComputedStyle(element).outlineStyle")
    card_shadow = card_link.locator("xpath=ancestor::article[1]").evaluate(
        "element => getComputedStyle(element).boxShadow"
    )

    issues: list[str] = []
    if outline_style == "none":
        issues.append(f"Home ({scheme}): focused card link lost its visible outline.")
    if card_shadow == "none":
        issues.append(f"Home ({scheme}): focused card lost its focus-within elevation state.")
    return issues


def _collect_browser_smoke_issues(sync_playwright: Any, base_url: str) -> list[str]:
    """Run the actual browser interactions against a resolved base URL."""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            issues: list[str] = []
            for scheme in ("light", "dark"):
                context = browser.new_context(
                    color_scheme=scheme,
                    viewport={"width": 390, "height": 844},
                    is_mobile=True,
                )
                context.set_default_timeout(5000)
                page = context.new_page()

                for target in SMOKE_TARGETS:
                    page.goto(urljoin(base_url, target.path.lstrip("/")), wait_until="networkidle")
                    issues.extend(_check_mobile_nav_state(page, target, scheme))

                page.goto(base_url, wait_until="networkidle")
                issues.extend(_check_card_focus_state(page, scheme))
                context.close()
            return issues
        finally:
            browser.close()


def find_browser_smoke_issues(site_dir: Path, base_url: str | None = None) -> list[str]:
    """Run lightweight browser smoke checks against the built site."""

    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Playwright is not installed. Run 'poetry install' and "
            "'poetry run playwright install chromium' first."
        ) from error

    if base_url is not None:
        return _collect_browser_smoke_issues(sync_playwright, normalize_base_url(base_url))

    if not site_dir.exists():
        raise FileNotFoundError(f"Built site directory was not found: {site_dir}")

    with local_site_server(site_dir) as server_base_url:
        return _collect_browser_smoke_issues(sync_playwright, server_base_url)
