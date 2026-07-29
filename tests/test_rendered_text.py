"""Tests for source-addressable projection of generated MkDocs HTML."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from scripts.repo_tools.rendered_text import (
    RenderedOrigin,
    RenderedProjection,
    RenderedTextError,
    project_rendered_content,
)
from scripts.repo_tools.source_semantics import PARAGRAPH_BOUNDARY


def _position(html_text: str, needle: str, occurrence: int = 1) -> RenderedOrigin:
    """Return the one-based position of an occurrence in test HTML."""

    offset = -1
    for _index in range(occurrence):
        offset = html_text.index(needle, offset + 1)
    prefix = html_text[:offset]
    line = prefix.count("\n") + 1
    column = offset - prefix.rfind("\n")
    return RenderedOrigin(line, column)


def test_project_rendered_content_captures_only_the_target_article() -> None:
    """Outside chrome should be ignored while inline content stays joined."""

    html_text = """<header>Outside</header>
<article class="layout md-content__inner">
  <p>Public <em>site</em>.</p>
</article>
<footer>Ignored</footer>"""

    projection = project_rendered_content(html_text)

    assert projection.text == "Public site."
    assert projection.origins[0] == _position(html_text, "Public")
    assert projection.origins[7] == _position(html_text, "site")
    assert projection.contexts[0] == "article.md-content__inner > p:nth-of-type(1)"
    assert projection.contexts[7] == "article.md-content__inner > p:nth-of-type(1)"
    assert projection.contexts[-1] == "article.md-content__inner > p:nth-of-type(1)"


def test_block_elements_create_hard_semantic_boundaries() -> None:
    """Text from separate blocks must not form one searchable phrase."""

    projection = project_rendered_content(
        '<article class="md-content__inner">'
        "<section><p>One</p><p>Two</p></section><div>Three</div><p>Four</p>"
        "</article>"
    )

    assert projection.text == PARAGRAPH_BOUNDARY.join(("One", "Two", "Three", "Four"))
    assert len(projection.text) == len(projection.origins) == len(projection.contexts)


def test_br_creates_a_soft_separator_at_the_tag_origin() -> None:
    """A rendered line break should join words with one attributable space."""

    html_text = '<article class="md-content__inner"><p>One<br>Two</p></article>'

    projection = project_rendered_content(html_text)

    assert projection.text == "One Two"
    assert projection.origins[3] == _position(html_text, "<br>")
    assert projection.contexts[3] == "article.md-content__inner > p:nth-of-type(1)"


def test_whitespace_and_dash_variants_are_normalized() -> None:
    """Rendered spacing and dash variants should match source normalization."""

    projection = project_rendered_content(
        '<article class="md-content__inner"><p>  One\n\t— two\u200bthree  </p></article>'
    )

    assert projection.text == "One - two three"


def test_entities_decode_at_their_raw_ampersand_origin() -> None:
    """Every character produced by an entity should point to its ampersand."""

    html_text = (
        '<article class="md-content__inner"><p>A&amp;B &#x2014; C &NotEqualTilde;</p></article>'
    )

    projection = project_rendered_content(html_text)

    assert projection.text == "A&B - C ≂̸"
    amp_index = projection.text.index("&")
    long_entity_index = projection.text.index("≂")
    assert projection.origins[amp_index] == _position(html_text, "&amp;")
    assert projection.origins[long_entity_index] == _position(html_text, "&NotEqualTilde;")
    assert projection.origins[long_entity_index + 1] == _position(html_text, "&NotEqualTilde;")


def test_comments_and_nonrendered_html_subtrees_are_excluded() -> None:
    """Invisible markup must contribute neither body nor attribute text."""

    html_text = (
        '<article class="md-content__inner"><p>A'
        '<script title="script title">bad</script>B'
        "<style>bad</style>C"
        '<template><span aria-label="template label">bad</span></template>D'
        "<!-- comment text -->E</p></article>"
    )

    projection = project_rendered_content(html_text)

    assert projection.text == "ABCDE"
    assert all("[title]" not in context for context in projection.contexts)
    assert all("[aria-label]" not in context for context in projection.contexts)


def test_svg_visible_and_accessibility_text_is_projected_semantically() -> None:
    """SVG labels, titles, and visible text must participate without executable text."""

    html_text = (
        '<article class="md-content__inner"><p>Before '
        '<svg aria-label="Public site">'
        "<title>Approved version</title>"
        "<desc>Accessible detail</desc>"
        "<text>visible <tspan>words</tspan></text>"
        "<script>script text</script><style>style text</style>"
        "</svg> after</p></article>"
    )

    projection = project_rendered_content(html_text)

    assert projection.text == PARAGRAPH_BOUNDARY.join(
        (
            "Before",
            "Approved version",
            "Accessible detail",
            "visible words after",
            "Public site",
        )
    )
    title_start = projection.text.index("Approved")
    description_start = projection.text.index("Accessible")
    visible_start = projection.text.index("visible")
    label_start = projection.text.index("Public")
    assert projection.origins[title_start] == _position(html_text, "Approved")
    assert projection.origins[description_start] == _position(html_text, "Accessible")
    assert projection.origins[visible_start] == _position(html_text, "visible")
    assert projection.origins[label_start] == _position(html_text, "Public")
    assert projection.contexts[title_start].endswith("title:nth-of-type(1)")
    assert projection.contexts[description_start].endswith("desc:nth-of-type(1)")
    assert projection.contexts[visible_start].endswith("p:nth-of-type(1)")
    assert projection.contexts[label_start] == "svg[aria-label]"
    assert "script text" not in projection.text
    assert "style text" not in projection.text


def test_svg_text_spans_compose_with_surrounding_visible_prose() -> None:
    """Inline SVG text and nested spans should read as one visible phrase."""

    projection = project_rendered_content(
        '<article class="md-content__inner"><p>'
        "public <svg><text><tspan>site</tspan></text></svg>"
        "</p></article>"
    )

    assert projection.text == "public site"


@pytest.mark.parametrize(
    "container",
    (
        "clipPath",
        "defs",
        "filter",
        "linearGradient",
        "marker",
        "mask",
        "metadata",
        "pattern",
        "radialGradient",
        "symbol",
        "view",
    ),
)
def test_nonrendering_svg_definition_subtrees_are_excluded(container: str) -> None:
    """Definition and metadata containers must not leak dormant text or labels."""

    projection = project_rendered_content(
        '<article class="md-content__inner"><svg>'
        f'<{container} aria-label="Hidden label">'
        "<title>Hidden title</title><desc>Hidden description</desc>"
        "<text>Hidden text</text>"
        f"</{container}>"
        "</svg></article>"
    )

    assert projection == RenderedProjection("", (), ())


def test_svg_definition_exclusions_end_at_a_foreign_object_boundary() -> None:
    """HTML descendants of foreignObject return to ordinary rendered semantics."""

    projection = project_rendered_content(
        '<article class="md-content__inner"><svg><foreignObject>'
        "<div><metadata>Visible HTML child</metadata></div>"
        "</foreignObject></svg></article>"
    )

    assert projection.text == "Visible HTML child"


def test_inline_text_inherits_the_nearest_stable_block_context() -> None:
    """Inline formatting should not hide a phrase's shared semantic container."""

    projection = project_rendered_content(
        '<article class="md-content__inner"><section>'
        "<p>A<span>B</span></p><p>C</p>"
        "</section></article>"
    )

    assert projection.text == f"AB{PARAGRAPH_BOUNDARY}C"
    assert projection.contexts[0].endswith("section:nth-of-type(1) > p:nth-of-type(1)")
    assert projection.contexts[1] == projection.contexts[0]
    assert projection.contexts[-1].endswith("section:nth-of-type(1) > p:nth-of-type(2)")


def test_nested_nontarget_article_is_valid_content() -> None:
    """Only the target class identifies the outer capture region."""

    projection = project_rendered_content(
        '<article class="md-content__inner">'
        '<article class="opi-card"><p>Card</p></article>'
        "</article>"
    )

    assert projection.text == "Card"
    assert "article:nth-of-type(1)" in projection.contexts[0]


def test_empty_target_article_produces_an_aligned_empty_projection() -> None:
    """An empty but structurally valid target remains a valid projection."""

    projection = project_rendered_content(
        '<article class="md-content__inner"><!-- intentionally empty --></article>'
    )

    assert projection == RenderedProjection("", (), ())


def test_empty_iframe_document_attributes_remain_a_valid_empty_embed() -> None:
    """An explicitly empty embedded document has no unprojected reader text."""

    projection = project_rendered_content(
        '<article class="md-content__inner">'
        '<iframe src=" " srcdoc="   "></iframe><p>Visible page text</p>'
        "</article>"
    )

    assert projection.text == "Visible page text"


@pytest.mark.parametrize(
    ("html_text", "message"),
    [
        ("<main>Missing</main>", "found none"),
        (
            '<article class="md-content__inner">One</article>'
            '<article class="md-content__inner">Two</article>',
            "found a duplicate",
        ),
        ('<article class="md-content__inner"><p>Open</p>', "is not closed"),
        (
            '<article class="md-content__inner"><p>Mismatch</div></article>',
            "does not match",
        ),
        ('<article class="md-content__inner"/>', "self-closing"),
        (
            '<article class="md-content__inner"><svg>'
            '<defs><symbol id="label"><text>Referenced text</text></symbol></defs>'
            '<use href="#label"/>'
            "</svg></article>",
            "SVG <use> reference",
        ),
        (
            '<article class="md-content__inner"><svg><use xlink:href="#icon"/></svg></article>',
            "SVG <use> reference",
        ),
        (
            '<article class="md-content__inner"><iframe srcdoc="public site"></iframe></article>',
            "iframe embedded document",
        ),
        (
            '<article class="md-content__inner"><iframe src="/guide/"></iframe></article>',
            "iframe embedded document",
        ),
    ],
)
def test_invalid_content_regions_fail_closed(html_text: str, message: str) -> None:
    """Missing, ambiguous, and malformed target regions must raise one typed error."""

    with pytest.raises(RenderedTextError, match=message):
        project_rendered_content(html_text)


def test_projection_rejects_misaligned_evidence() -> None:
    """A projection without one origin and context per character is invalid."""

    with pytest.raises(ValueError, match="lengths differ"):
        RenderedProjection("text", (RenderedOrigin(1, 1),), ("p",))
    with pytest.raises(ValueError, match="must not be empty"):
        RenderedProjection("x", (RenderedOrigin(1, 1),), ("",))


def test_origins_are_one_based_and_frozen() -> None:
    """Source origins should reject invalid coordinates and resist mutation."""

    with pytest.raises(ValueError, match="one-based"):
        RenderedOrigin(0, 1)

    origin = RenderedOrigin(1, 1)
    with pytest.raises(FrozenInstanceError):
        origin.line = 2  # type: ignore[misc]
