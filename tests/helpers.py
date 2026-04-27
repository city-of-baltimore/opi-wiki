"""Shared test helpers for MkDocs macro and repo configuration tests."""

from __future__ import annotations


class FakePageFile:
    """Minimal file object for a fake MkDocs page."""

    def __init__(self, src_path: str) -> None:
        """Store the source path used by the macros plugin."""

        self.src_path = src_path


class FakePage:
    """Minimal page object for a fake MkDocs page."""

    def __init__(self, src_path: str) -> None:
        """Create a fake page with the given source path."""

        self.file = FakePageFile(src_path)


class FakeMacroEnvironment:
    """Minimal stand-in for the MkDocs macros environment."""

    def __init__(self, page_src_path: str | None = None) -> None:
        """Initialize the fake macro registry and optional current page."""

        self.macros: dict[str, object] = {}
        if page_src_path is not None:
            self.page = FakePage(page_src_path)

    def macro(self, function: object) -> object:
        """Register a macro function and return it unchanged."""

        self.macros[getattr(function, "__name__", "unknown")] = function
        return function
