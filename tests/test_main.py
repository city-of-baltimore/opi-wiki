"""Tests for shared MkDocs macro registration."""

from __future__ import annotations

from tests.helpers import register_macros


def test_shared_macro_registry_stays_explicit() -> None:
    """The shared macros module should expose the expected public macro surface."""

    env = register_macros("how-we-work/operations/charter-template.md")

    assert set(env.macros) == {
        "card_grid_from",
        "badge",
        "page_badge",
        "org_structure_from",
    }
