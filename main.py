"""MkDocs macros shared across OPI documentation pages."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, Protocol

from markupsafe import Markup

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DOCS_DIR = REPO_ROOT / "docs"

# Canonical single-source people directory, relative to DOCS_DIR.
PEOPLE_DATA_PATH = "_data/people.yml"


class PageFile(Protocol):
    """Minimal protocol for the current MkDocs page file."""

    src_path: str


class Page(Protocol):
    """Minimal protocol for the current MkDocs page object."""

    file: PageFile


class MacroEnvironment(Protocol):
    """Minimal protocol for the MkDocs macros plugin environment."""

    page: Page

    def macro(self, function: Callable[..., Any]) -> Callable[..., Any]:
        """Register a callable as a macro."""


def _render_markup(rendered: str) -> Markup:
    """Wrap rendered HTML or Markdown in a Markup object for MkDocs."""

    # S704: the wrapped string is always HTML this repository's own renderers
    # built from tracked docs/ data at build time. There is no request, no user
    # input, and no runtime template rendering anywhere in a static docs build.
    return Markup(rendered)  # nosec B704  # noqa: S704


def _render_docs_markup(
    relative_path: str,
    *,
    load_data: Callable[[Path, str], Any],
    render_data: Callable[..., str],
    render_args: tuple[Any, ...] = (),
) -> Markup:
    """Load docs-adjacent structured data and render it as markup."""

    return _render_markup(render_data(load_data(DOCS_DIR, relative_path), *render_args))


def define_env(env: MacroEnvironment) -> None:
    """Register shared macros for the MkDocs macros plugin."""

    @env.macro
    def card_grid_from(relative_path: str, section: str = "default") -> Markup:
        """Render a card grid from shared YAML data."""

        from scripts.repo_tools.cards import load_card_sections, render_card_grid

        sections = load_card_sections(DOCS_DIR, relative_path)
        if section not in sections:
            available_sections = ", ".join(sorted(sections))
            raise ValueError(
                f"Card section '{section}' was not found in '{relative_path}'. "
                f"Available sections: {available_sections}"
            )
        return _render_markup(render_card_grid(sections[section]))

    @env.macro
    def badge(value: str) -> Markup:
        """Render a shared display badge by token."""

        from scripts.repo_tools.badges import render_badge

        return _render_markup(render_badge(value))

    @env.macro
    def page_badge() -> Markup:
        """Render the current page's configured display badge."""

        from scripts.repo_tools.badges import render_badge, resolve_page_badge_value
        from scripts.repo_tools.metadata import resolve_page_metadata

        page_path = DOCS_DIR / env.page.file.src_path
        metadata = resolve_page_metadata(DOCS_DIR, page_path)
        return _render_markup(render_badge(resolve_page_badge_value(metadata)))

    @env.macro
    def page_header(
        summary: str = "",
        category: str = "",
        tagline: str = "",
    ) -> Markup:
        """Render the current page's canonical header from metadata and args."""

        from scripts.repo_tools.badges import resolve_optional_page_badge_value
        from scripts.repo_tools.metadata import resolve_page_metadata
        from scripts.repo_tools.page_header import render_page_header

        page_path = DOCS_DIR / env.page.file.src_path
        metadata = resolve_page_metadata(DOCS_DIR, page_path)
        badge_value = resolve_optional_page_badge_value(metadata)
        return _render_markup(
            render_page_header(
                badge_value,
                summary=summary,
                category=category,
                tagline=tagline,
            )
        )

    @env.macro
    def org_structure_from(relative_path: str, section: str) -> Markup:
        """Render a structured org-structure section from shared YAML data."""

        from scripts.repo_tools.org_structure import load_org_structure, render_org_structure

        return _render_docs_markup(
            relative_path,
            load_data=load_org_structure,
            render_data=render_org_structure,
            render_args=(section,),
        )

    @env.macro
    def people(section: str) -> Markup:
        """Render a section of the canonical people directory (_data/people.yml)."""

        from scripts.repo_tools.people import load_people, render_people

        return _render_docs_markup(
            PEOPLE_DATA_PATH,
            load_data=load_people,
            render_data=render_people,
            render_args=(section,),
        )

    @env.macro
    def role_holder(title: str) -> str:
        """Return the name of the staff member holding the given working title."""

        from scripts.repo_tools.people import find_role_holder, load_people

        return find_role_holder(load_people(DOCS_DIR, PEOPLE_DATA_PATH), title)
