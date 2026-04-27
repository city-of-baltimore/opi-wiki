"""MkDocs macros shared across OPI documentation pages."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Protocol

from markupsafe import Markup

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DOCS_DIR = REPO_ROOT / "docs"


class MacroEnvironment(Protocol):
    """Minimal protocol for the MkDocs macros plugin environment."""

    def macro(self, function: Callable[..., Any]) -> Callable[..., Any]:
        """Register a callable as a macro."""


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
        return Markup(render_card_grid(sections[section]))
