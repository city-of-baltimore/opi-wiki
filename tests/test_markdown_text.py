"""Tests for inert organization text under the real Markdown extension stack."""

from __future__ import annotations

from html.parser import HTMLParser

import pytest
from markdown import Markdown
from mkdocs.config import load_config
from scripts.repo_tools.markdown_text import render_inert_markdown_text


class _RenderedTextParser(HTMLParser):
    """Collect visible text and the complete rendered element stream."""

    def __init__(self) -> None:
        """Initialize empty evidence collections."""

        super().__init__()
        self.elements: list[tuple[str, dict[str, str | None]]] = []
        self.text: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record every element and attribute for structural assertions."""

        self.elements.append((tag, dict(attrs)))

    def handle_startendtag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record self-closing active tags such as injected images."""

        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        """Collect rendered text for visible-parity assertions."""

        self.text.append(data)


def _render(markdown_source: str) -> str:
    """Render source with the exact extension stack configured by MkDocs."""

    config = load_config(config_file="mkdocs.yml")
    renderer = Markdown(
        extensions=config["markdown_extensions"],
        extension_configs=config["mdx_configs"],
    )
    return renderer.convert(markdown_source)


@pytest.mark.parametrize(
    "value",
    [
        "**bold** and _emphasis_",
        "`inline code`",
        "[link](javascript:alert(1))",
        "<img src=x onerror=alert(1)>",
        "<https://evil.example/path>",
        "https://evil.example/path",
        "ftp://evil.example/path",
        "www.evil.example",
        "attacker@example.com",
        "@mention and #123",
        "~~deleted~~ and ~subscript~",
        "^^inserted^^ and ^superscript^",
        "==marked==",
        "++ctrl+alt++",
        "text{#danger .active}",
        '--8<-- "secrets.txt"',
        "[reference][target] and [^footnote]",
        "- [x] task",
        "#!python print('x')",
    ],
)
@pytest.mark.parametrize("surface", ["inline", "heading", "table"])
def test_inert_markdown_text_stays_visible_without_becoming_active(
    value: str,
    surface: str,
) -> None:
    """Every configured Markdown surface should preserve text without activating it."""

    inert = render_inert_markdown_text(value)
    if surface == "heading":
        source = f"## {inert}"
    elif surface == "table":
        source = f"| Value |\n| --- |\n| {inert} |"
    else:
        source = inert

    parser = _RenderedTextParser()
    parser.feed(_render(source))

    allowed_tags = {
        "inline": {"p"},
        "heading": {"h2", "a"},
        "table": {"table", "thead", "tbody", "tr", "th", "td"},
    }[surface]
    allowed_attributes = {
        "p": set(),
        "h2": {"id"},
        "a": {"class", "href", "title"},
        "table": set(),
        "thead": set(),
        "tbody": set(),
        "tr": set(),
        "th": set(),
        "td": set(),
    }
    for tag, attributes in parser.elements:
        assert tag in allowed_tags
        assert set(attributes) <= allowed_attributes[tag]
        if tag == "a":
            assert "headerlink" in (attributes.get("class") or "").split()
            assert (attributes.get("href") or "").startswith("#")
    assert value in "".join(parser.text)


def test_inert_markdown_text_preserves_ordinary_visible_copy() -> None:
    """Normal City names and prose should render with no visible encoding artifacts."""

    value = "Dartanion Swift-Williams, Executive Director & CDO."
    parser = _RenderedTextParser()
    parser.feed(_render(render_inert_markdown_text(value)))

    assert parser.elements == [("p", {})]
    assert "".join(parser.text) == value


def test_inert_markdown_text_rejects_non_string_values() -> None:
    """The output boundary should fail clearly instead of coercing an unexpected type."""

    with pytest.raises(TypeError, match="must be a string"):
        render_inert_markdown_text(123)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value",
    [
        "safe\n\n    indented code",
        "safe\rnext line",
        "safe\tindented",
        "  leading indentation",
        "trailing line break  ",
    ],
)
def test_inert_markdown_text_rejects_structural_whitespace(value: str) -> None:
    """Whitespace that can change Markdown block structure must fail explicitly."""

    with pytest.raises(ValueError, match="Markdown text value must"):
        render_inert_markdown_text(value)
