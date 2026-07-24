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
from urllib.parse import urljoin, urlsplit, urlunsplit

from scripts.repo_tools.built_links import discover_site_base_path, load_sitemap_locations


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
    BrowserSmokeTarget(
        "About Us",
        "/about-us/operating-principles-and-culture/",
        "Operating Principles and Culture",
    ),
    BrowserSmokeTarget(
        "How We Work",
        "/how-we-work/how-work-moves-through-opi/",
        "How Work Moves Through OPI",
    ),
    BrowserSmokeTarget(
        "What We Do",
        "/what-we-do/services/cross-agency-delivery/",
        "Cross-Agency Delivery",
    ),
    BrowserSmokeTarget("Resources", "/resources/reference/glossary/", "Glossary"),
)
TABLE_FOCUS_SOURCE_PATH = "/what-we-do/services/cross-agency-delivery/"
TABLE_FOCUS_TARGET_PATH = "/what-we-do/services/cross-agency-delivery/service-definition/"
ORG_SOURCE_PATH = "/how-we-work/organization/"
ORG_TARGET_PATH = "/how-we-work/organization/org-structure/"
ORG_EXPECTED_NAMES = (
    "Faith P. Leach",
    "Dartanion Swift-Williams",
    "Rakeim Young",
    "Danny Heller",
    "Jason Howard, PhD",
    "Gabriel Watson",
)
REPOSITORY_URL = "https://github.com/city-of-baltimore/opi-wiki"
REPOSITORY_NAME = "city-of-baltimore/opi-wiki"


def normalize_base_url(base_url: str) -> str:
    """Normalize a base URL so downstream joins are stable."""

    return base_url.rstrip("/") + "/"


def normalize_page_url(url: str) -> str:
    """Normalize a page URL for redirect-sensitive final-URL comparisons."""

    parsed = urlsplit(url)
    path = parsed.path or "/"
    if not Path(path).suffix:
        path = path.rstrip("/") + "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def canonical_route_paths(site_dir: Path) -> list[str]:
    """Return deployment-relative canonical routes from the built sitemap."""

    base_path = discover_site_base_path(site_dir)
    routes: set[str] = set()
    for location in load_sitemap_locations(site_dir):
        path = urlsplit(location).path
        if base_path != "/":
            if not path.startswith(base_path):
                continue
            path = path[len(base_path) :]
        route = "/" + path.lstrip("/")
        if not Path(route).suffix:
            route = route.rstrip("/") + "/"
        routes.add(route)
    return sorted(routes, key=lambda route: (route != "/", route))


@contextmanager
def local_site_server(site_dir: Path) -> Iterator[str]:
    """Serve a built static site from a temporary local HTTP server."""

    handler = partial(_QuietStaticSiteHandler, directory=str(site_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    try:
        thread.start()
        host_raw, port = server.server_address[0], server.server_address[1]
        host = host_raw.decode() if isinstance(host_raw, bytes) else host_raw
        yield f"http://{host}:{port}/"
    finally:
        if thread.is_alive():
            server.shutdown()
            thread.join(timeout=5)
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

    issues.extend(_check_repository_link_state(page, target.section, scheme))

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

    overlay_bounds = drawer_overlay.bounding_box()
    if overlay_bounds is None:
        issues.append(f"{target.section} ({scheme}): drawer overlay had no visible bounds.")
        return issues
    page.mouse.click(
        overlay_bounds["x"] + overlay_bounds["width"] - 8,
        overlay_bounds["y"] + (overlay_bounds["height"] / 2),
    )
    if drawer_state.is_checked():
        issues.append(f"{target.section} ({scheme}): drawer did not close.")

    return issues


def _check_repository_link_state(page: Any, section: str, scheme: str) -> list[str]:
    """Keep the visible repository link without Material's network-backed widget."""

    issues: list[str] = []
    repository_link = page.locator(f'.md-nav__source a.md-source[href="{REPOSITORY_URL}"]').first
    if repository_link.count() == 0 or not repository_link.is_visible():
        issues.append(f"{section} ({scheme}): visible repository link was not found.")
    elif REPOSITORY_NAME not in repository_link.inner_text():
        issues.append(f"{section} ({scheme}): repository name was not visible in its link.")

    if page.locator('[data-md-component="source"]').count() != 0:
        issues.append(f"{section} ({scheme}): repository stats component was still active.")
    return issues


def _check_page_load(
    page: Any,
    response: Any,
    requested_url: str,
    label: str,
    scheme: str,
) -> list[str]:
    """Validate the HTTP status and final URL for one canonical page load."""

    if response is None:
        return [f"{label} ({scheme}): navigation returned no HTTP response."]

    issues: list[str] = []
    if response.status != 200:
        issues.append(f"{label} ({scheme}): returned HTTP {response.status}, expected 200.")

    final_url = str(page.url)
    if normalize_page_url(final_url) != normalize_page_url(requested_url):
        issues.append(
            f"{label} ({scheme}): ended at {final_url}, expected canonical URL {requested_url}."
        )
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


def _check_table_focus_state(page: Any, scheme: str, navigation: str) -> list[str]:
    """Validate keyboard focusability and focus styling on a generated table wrapper."""

    result = page.evaluate(
        """
        () => {
          const region = document.querySelector(".md-typeset__scrollwrap");
          if (!region) return null;
          region.focus();
          const style = getComputedStyle(region);
          return {
            tabIndex: region.tabIndex,
            outlineStyle: style.outlineStyle,
            outlineWidth: style.outlineWidth,
          };
        }
        """
    )
    label = f"Table scroll region ({scheme}, {navigation})"
    if result is None:
        return [f"{label}: generated scroll wrapper was not found."]

    issues: list[str] = []
    if result["tabIndex"] != 0:
        issues.append(f"{label}: tabIndex was {result['tabIndex']}, expected 0.")
    if result["outlineStyle"] == "none" or result["outlineWidth"] == "0px":
        issues.append(f"{label}: keyboard focus outline was not visible.")
    return issues


def _check_table_focus_after_instant_navigation(page: Any, base_url: str, scheme: str) -> list[str]:
    """Navigate through Material's instant loader and validate its document hook."""

    source_url = urljoin(base_url, TABLE_FOCUS_SOURCE_PATH.lstrip("/"))
    target_url = urljoin(base_url, TABLE_FOCUS_TARGET_PATH.lstrip("/"))
    response = page.goto(source_url, wait_until="networkidle")
    issues = _check_page_load(page, response, source_url, "Table focus source", scheme)

    target_link = page.locator('.md-content a[href*="service-definition/"]').first
    if target_link.count() == 0:
        issues.append(f"Table scroll region ({scheme}, instant navigation): link was not found.")
        return issues

    target_link.click()
    page.wait_for_url(target_url)
    page.wait_for_load_state("networkidle")
    if normalize_page_url(str(page.url)) != normalize_page_url(target_url):
        issues.append(
            f"Table scroll region ({scheme}, instant navigation): ended at {page.url}, "
            f"expected {target_url}."
        )
        return issues
    issues.extend(_check_table_focus_state(page, scheme, "instant navigation"))
    return issues


def _check_org_chart_state(page: Any, scheme: str, navigation: str) -> list[str]:
    """Validate the visible semantic hierarchy and public leadership names."""

    result = page.evaluate(
        """
        () => {
          const chart = document.querySelector(".opi-org-chart");
          if (!chart) return null;
          const isVisible = (element) => {
            const style = getComputedStyle(element);
            const rect = element.getBoundingClientRect();
            return style.display !== "none" && style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
          };
          const nodes = [...chart.querySelectorAll(".opi-org-chart__node")];
          return {
            chartVisible: isVisible(chart),
            visibleNames: nodes
              .filter(isVisible)
              .map((node) => node.querySelector(".opi-org-chart__name")?.textContent?.trim())
              .filter(Boolean),
            cityCount: chart.querySelectorAll(
              ".opi-org-chart__root > .opi-org-chart__node[data-org-level='city']"
            ).length,
            executiveCount: chart.querySelectorAll(
              ".opi-org-chart__executive > .opi-org-chart__node[data-org-level='executive']"
            ).length,
            teamCount: chart.querySelectorAll(
              ".opi-org-chart__team-item > .opi-org-chart__node" +
              "[data-org-level='team'][data-org-key]"
            ).length,
          };
        }
        """
    )
    label = f"Organization chart ({scheme}, {navigation})"
    if result is None:
        return [f"{label}: semantic chart container was not found."]

    issues: list[str] = []
    if not result["chartVisible"]:
        issues.append(f"{label}: chart container had no visible dimensions.")
    missing_names = [name for name in ORG_EXPECTED_NAMES if name not in result["visibleNames"]]
    if missing_names:
        issues.append(f"{label}: public leadership names were not visible: {missing_names}.")
    expected_counts = (1, 1, 4)
    actual_counts = (result["cityCount"], result["executiveCount"], result["teamCount"])
    if actual_counts != expected_counts:
        issues.append(
            f"{label}: hierarchy counts were city/executive/team {actual_counts}, "
            f"expected {expected_counts}."
        )
    return issues


def _check_org_chart_after_instant_navigation(page: Any, base_url: str, scheme: str) -> list[str]:
    """Navigate to the organization chart through Material's instant loader."""

    source_url = urljoin(base_url, ORG_SOURCE_PATH.lstrip("/"))
    target_url = urljoin(base_url, ORG_TARGET_PATH.lstrip("/"))
    response = page.goto(source_url, wait_until="networkidle")
    issues = _check_page_load(page, response, source_url, "Organization source", scheme)
    target_link = page.locator('.md-content a[href*="org-structure/"]').first
    if target_link.count() == 0:
        issues.append(f"Organization chart ({scheme}, instant navigation): link was not found.")
        return issues

    target_link.click()
    page.wait_for_url(target_url)
    page.wait_for_load_state("networkidle")
    issues.extend(_check_org_chart_state(page, scheme, "instant navigation"))
    return issues


def _check_search_workflow(page: Any, base_url: str, scheme: str) -> list[str]:
    """Search for a stable public term and navigate to an accessible result."""

    response = page.goto(base_url, wait_until="networkidle")
    issues = _check_page_load(page, response, base_url, "Search home", scheme)
    search_toggle = page.locator('label.md-header__button[for="__search"]').first
    if search_toggle.count() == 0:
        return [*issues, f"Search ({scheme}): search toggle was not found."]
    search_toggle.click()

    search_input = page.locator("input.md-search__input").first
    # Material 9.6 listens to key events, so fill() changes the value without
    # starting a search. Real keystrokes exercise the user-facing contract.
    search_input.press_sequentially("CitiStat", delay=20)
    result_link = page.locator("a.md-search-result__link", has_text="CitiStat").first
    result_link.wait_for(state="visible")
    accessible_name = result_link.inner_text().strip()
    href = result_link.get_attribute("href")
    if not accessible_name or href is None:
        issues.append(f"Search ({scheme}): result link had no accessible name or target.")
        return issues

    target_url = urljoin(str(page.url), href)
    result_link.click()
    page.wait_for_url(target_url)
    page.wait_for_load_state("networkidle")
    target_response = page.request.get(target_url)
    try:
        issues.extend(_check_page_load(page, target_response, target_url, "Search result", scheme))
    finally:
        target_response.dispose()
    return issues


def _crawl_canonical_routes(browser: Any, base_url: str, routes: tuple[str, ...]) -> list[str]:
    """Load every canonical route and capture status, redirect, and runtime errors."""

    if not routes:
        return []
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    context.set_default_timeout(5000)
    page = context.new_page()
    issues: list[str] = []
    current_route = {"value": "/"}

    def record_console(message: Any) -> None:
        if message.type == "error":
            issues.append(f"Canonical {current_route['value']}: console error: {message.text}")

    def record_page_error(error: Any) -> None:
        issues.append(f"Canonical {current_route['value']}: page error: {error}")

    page.on("console", record_console)
    page.on("pageerror", record_page_error)
    try:
        for route in routes:
            current_route["value"] = route
            requested_url = urljoin(base_url, route.lstrip("/"))
            response = page.goto(requested_url, wait_until="networkidle")
            issues.extend(
                _check_page_load(page, response, requested_url, f"Canonical {route}", "desktop")
            )
    finally:
        context.close()
    return issues


def _collect_browser_smoke_issues(
    sync_playwright: Any,
    base_url: str,
    routes: tuple[str, ...] = (),
) -> list[str]:
    """Run the actual browser interactions against a resolved base URL."""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            issues = _crawl_canonical_routes(browser, base_url, routes)
            for scheme in ("light", "dark"):
                context = browser.new_context(
                    color_scheme=scheme,
                    viewport={"width": 390, "height": 844},
                    is_mobile=True,
                )
                context.set_default_timeout(5000)
                page = context.new_page()

                for target in SMOKE_TARGETS:
                    requested_url = urljoin(base_url, target.path.lstrip("/"))
                    response = page.goto(requested_url, wait_until="networkidle")
                    issues.extend(
                        _check_page_load(page, response, requested_url, target.section, scheme)
                    )
                    issues.extend(_check_mobile_nav_state(page, target, scheme))

                table_url = urljoin(base_url, TABLE_FOCUS_TARGET_PATH.lstrip("/"))
                response = page.goto(table_url, wait_until="networkidle")
                issues.extend(_check_page_load(page, response, table_url, "Table focus", scheme))
                issues.extend(_check_table_focus_state(page, scheme, "direct load"))
                issues.extend(_check_table_focus_after_instant_navigation(page, base_url, scheme))

                org_url = urljoin(base_url, ORG_TARGET_PATH.lstrip("/"))
                response = page.goto(org_url, wait_until="networkidle")
                issues.extend(
                    _check_page_load(page, response, org_url, "Organization chart", scheme)
                )
                issues.extend(_check_org_chart_state(page, scheme, "direct load"))
                issues.extend(_check_org_chart_after_instant_navigation(page, base_url, scheme))
                issues.extend(_check_search_workflow(page, base_url, scheme))

                response = page.goto(base_url, wait_until="networkidle")
                issues.extend(_check_page_load(page, response, base_url, "Home", scheme))
                issues.extend(_check_card_focus_state(page, scheme))
                context.close()
            return issues
        finally:
            browser.close()


def find_browser_smoke_issues(site_dir: Path, base_url: str | None = None) -> list[str]:
    """Run lightweight browser smoke checks against the built site."""

    if base_url is None and not site_dir.is_dir():
        raise FileNotFoundError(f"Built site directory was not found: {site_dir}")

    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Playwright is not installed. Run 'uv sync' and "
            "'uv run playwright install chromium' first."
        ) from error

    routes = tuple(canonical_route_paths(site_dir)) if site_dir.is_dir() else ()
    if base_url is not None:
        return _collect_browser_smoke_issues(
            sync_playwright,
            normalize_base_url(base_url),
            routes,
        )

    with local_site_server(site_dir) as server_base_url:
        return _collect_browser_smoke_issues(sync_playwright, server_base_url, routes)
