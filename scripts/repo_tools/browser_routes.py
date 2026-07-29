"""Resolved browser targets and page-readiness navigation helpers."""

from __future__ import annotations

import re
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit, urlunsplit

from scripts.repo_tools.browser_artifact_routes import install_canonical_artifact_route
from scripts.repo_tools.browser_route_manifest import (
    canonical_route_manifest,
    canonical_route_manifest_from_preview,
)
from scripts.repo_tools.site_urls import (
    normalize_base_url,
    normalize_page_url,
    validate_http_location,
)

PAGE_CONTENT_SELECTOR = "article.md-content__inner"
_FONTS_READY_EXPRESSION = "() => document.fonts.status === 'loaded'"
_LIVE_RELOAD_PATH = re.compile(r"/livereload/\d+/\d+")


@dataclass(frozen=True)
class BrowserTarget:
    """One immutable browser target and its authoritative artifact, if static."""

    base_url: str
    routes: tuple[str, ...]
    artifact_dir: Path | None = None


def browser_route_url(base_url: str, route: str) -> str:
    """Join one decoded absolute route without changing its URL identity."""

    if not route.startswith("/") or route.startswith("//") or "\\" in route:
        raise ValueError(
            "browser route must be an absolute path with one leading slash and no backslashes"
        )
    if any(
        character.isspace() or ord(character) < 32 or ord(character) == 127 for character in route
    ):
        raise ValueError("browser route must not contain whitespace or control characters")

    normalized_base_url = normalize_base_url(
        base_url,
        label="Browser target base URL",
    )
    browser_url = f"{normalized_base_url}{quote(route[1:], safe='/')}"
    try:
        validate_http_location(browser_url, "Browser route URL")
    except RuntimeError as error:
        raise ValueError(str(error)) from error
    return browser_url


def browser_target_owns_url(target: BrowserTarget, url: str) -> bool:
    """Return whether one request belongs to the target's canonical URL space."""

    try:
        base_origin, base_path = validate_http_location(
            normalize_base_url(target.base_url),
            "Browser target base URL",
        )
        parsed = urlsplit(url)
        queryless_url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
        request_origin, request_path = validate_http_location(
            queryless_url,
            "Browser target request URL",
            allow_empty_path=True,
        )
    except (RuntimeError, ValueError):
        return False
    if request_origin != base_origin:
        return False
    root_without_slash = base_path.rstrip("/") or "/"
    return request_path == root_without_slash or request_path.startswith(base_path)


def browser_target_owns_live_reload_url(target: BrowserTarget, url: str) -> bool:
    """Return whether one URL is the selected live preview's exact reload poll."""

    if target.artifact_dir is not None:
        return False
    try:
        target_origin, _target_path = validate_http_location(
            target.base_url,
            "Browser target base URL",
        )
        request_origin, request_path = validate_http_location(
            url,
            "MkDocs live-reload request URL",
        )
    except (RuntimeError, ValueError):
        return False
    return target_origin == request_origin and _LIVE_RELOAD_PATH.fullmatch(request_path) is not None


def _install_live_preview_transport_route(context: Any, target: BrowserTarget) -> None:
    """Keep MkDocs' 60-second reload poll from accumulating during route crawls."""

    def abort_live_reload(route: Any) -> None:
        if browser_target_owns_live_reload_url(target, route.request.url):
            route.abort(error_code="aborted")
        else:
            route.continue_()

    context.route("**/livereload/**", abort_live_reload)


@contextmanager
def resolved_browser_target(
    site_dir: Path,
    base_url: str | None = None,
) -> Iterator[BrowserTarget]:
    """Resolve one live preview or exact canonical build-artifact target."""

    if base_url is not None:
        normalized_base_url = normalize_base_url(base_url)
        manifest = canonical_route_manifest_from_preview(normalized_base_url)
        if not manifest.routes:
            raise RuntimeError(
                f"Sitemap contains no canonical routes: {normalized_base_url}sitemap.xml"
            )
        yield BrowserTarget(normalized_base_url, manifest.routes)
        return

    if not site_dir.is_dir():
        raise FileNotFoundError(f"Built site directory was not found: {site_dir}")

    manifest = canonical_route_manifest(site_dir)
    if not manifest.routes:
        raise RuntimeError(f"Sitemap contains no canonical routes: {site_dir / 'sitemap.xml'}")
    yield BrowserTarget(
        manifest.canonical_base_url,
        manifest.routes,
        site_dir.resolve(),
    )


def create_browser_context(
    browser: Any,
    target: BrowserTarget,
    **options: Any,
) -> Any:
    """Create one fail-closed context for a live or canonical artifact target."""

    context_options = dict(options)
    context_options.pop("service_workers", None)
    context_options.pop("offline", None)
    context = browser.new_context(
        service_workers="block",
        offline=target.artifact_dir is not None,
        **context_options,
    )
    try:
        if target.artifact_dir is not None:
            install_canonical_artifact_route(
                context,
                canonical_base_url=target.base_url,
                site_dir=target.artifact_dir,
            )
        else:
            _install_live_preview_transport_route(context, target)
        context.set_default_timeout(5000)
    except Exception:
        context.close()
        raise
    return context


def check_page_load(
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


def navigate_to_ready_page(
    page: Any,
    requested_url: str,
    label: str,
    scheme: str,
    *,
    ready_selector: str = PAGE_CONTENT_SELECTOR,
) -> list[str]:
    """Navigate to one URL and require its canonical content to be visible."""

    response = page.goto(requested_url, wait_until="load")
    issues = check_page_load(page, response, requested_url, label, scheme)
    if issues:
        return issues

    page.locator(ready_selector).first.wait_for(state="visible")
    page.wait_for_function(_FONTS_READY_EXPRESSION)
    return []


def navigate_to_instant_page(
    page: Any,
    link: Any,
    requested_url: str,
    label: str,
    scheme: str,
    *,
    ready_selector: str,
) -> list[str]:
    """Click a link and prove Material replaced content without reloading the document."""

    transition = page.evaluate(
        """
        () => {
          const content = document.querySelector("article.md-content__inner");
          if (!content) return null;
          const token = crypto.randomUUID();
          window.__opiBrowserInstantProbe = token;
          content.dataset.opiBrowserInstantProbe = token;
          return {
            token,
            sourceUrl: window.location.href,
            timeOrigin: performance.timeOrigin,
          };
        }
        """
    )
    if transition is None:
        return [f"{label} ({scheme}): source content was unavailable before instant navigation."]

    link.click()
    page.wait_for_function(
        "(sourceUrl) => window.location.href !== sourceUrl",
        arg=transition["sourceUrl"],
    )
    final_url = str(page.url)
    if normalize_page_url(final_url) != normalize_page_url(requested_url):
        return [
            f"{label} ({scheme}): ended at {final_url}, expected canonical URL {requested_url}."
        ]

    same_document = page.evaluate(
        """
        (expected) =>
          window.__opiBrowserInstantProbe === expected.token &&
          performance.timeOrigin === expected.timeOrigin
        """,
        transition,
    )
    if not same_document:
        return [
            f"{label} ({scheme}): loaded a new document instead of using "
            "Material instant navigation."
        ]

    page.wait_for_function(
        """
        (token) =>
          !document.querySelector(
            `[data-opi-browser-instant-probe="${CSS.escape(token)}"]`
          )
        """,
        arg=transition["token"],
    )
    page.locator(ready_selector).first.wait_for(state="visible")
    page.wait_for_function(_FONTS_READY_EXPRESSION)
    final_url = str(page.url)
    if normalize_page_url(final_url) == normalize_page_url(requested_url):
        return []
    return [f"{label} ({scheme}): ended at {final_url}, expected canonical URL {requested_url}."]
