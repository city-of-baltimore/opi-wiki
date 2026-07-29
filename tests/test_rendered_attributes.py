"""Tests for source-addressable user-facing HTML attribute projection."""

from __future__ import annotations

import pytest
from scripts.repo_tools.rendered_text import (
    RenderedOrigin,
    RenderedProjection,
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


def test_user_facing_attributes_are_isolated_semantic_segments() -> None:
    """Attributes should be searchable without interrupting visible body flow."""

    html_text = (
        '<article class="md-content__inner"><p>Before '
        "<img alt=\"Public&nbsp;site\" title='Tooltip'> after</p>"
        '<input aria-label="Search" value=Go></article>'
    )

    projection = project_rendered_content(html_text)

    assert projection.text == PARAGRAPH_BOUNDARY.join(
        ("Before after", "Public site", "Tooltip", "Search", "Go")
    )
    alt_start = projection.text.index("Public site")
    alt_space = alt_start + len("Public")
    assert projection.origins[alt_space] == _position(html_text, "&nbsp;")
    assert set(projection.contexts[alt_start : alt_start + len("Public site")]) == {"img[alt]"}
    assert projection.contexts[projection.text.index("Tooltip")] == "img[title]"
    assert projection.contexts[projection.text.index("Search")] == "input[aria-label]"
    assert projection.contexts[projection.text.rindex("Go")] == "input[value]"


def test_reader_facing_attribute_allowlist_covers_descriptions_and_control_labels() -> None:
    """Visible and accessibility prose should project with exact attribute evidence."""

    html_text = (
        '<article class="md-content__inner">'
        '<input placeholder="Find&nbsp records" '
        'aria-description="Approved&#160 version" '
        'aria-placeholder="Search records" '
        'aria-roledescription="Performance dial" '
        'aria-valuetext="75 percent" '
        'aria-braillelabel="Find data" '
        'aria-brailleroledescription="Search control">'
        '<input type="image" alt="Submit report">'
        '<select><optgroup label="Agency group">'
        '<option label="Current choice" value="machine-choice"></option>'
        "</optgroup></select>"
        '<track label="English captions">'
        '<table><tr><th abbr="Case volume"></th></tr></table>'
        "</article>"
    )

    projection = project_rendered_content(html_text)

    assert projection.text == PARAGRAPH_BOUNDARY.join(
        (
            "Find records",
            "Approved version",
            "Search records",
            "Performance dial",
            "75 percent",
            "Find data",
            "Search control",
            "Submit report",
            "Agency group",
            "Current choice",
            "English captions",
            "Case volume",
        )
    )
    expected_contexts = {
        "Find": "input[placeholder]",
        "Approved": "input[aria-description]",
        "Search": "input[aria-placeholder]",
        "Performance": "input[aria-roledescription]",
        "75": "input[aria-valuetext]",
        "data": "input[aria-braillelabel]",
        "control": "input[aria-brailleroledescription]",
        "Submit": "input[alt]",
        "Agency": "optgroup[label]",
        "Current": "option[label]",
        "English": "track[label]",
        "Case": "th[abbr]",
    }
    for text, context in expected_contexts.items():
        index = projection.text.index(text)
        assert projection.origins[index] == _position(html_text, text)
        assert projection.contexts[index] == context
    find_space = projection.text.index(" ")
    assert projection.origins[find_space] == _position(html_text, "&nbsp")


def test_state_id_reference_and_wrong_element_attributes_are_not_projected() -> None:
    """ARIA mechanics and lookalike attributes are not reader-facing text."""

    projection = project_rendered_content(
        '<article class="md-content__inner">'
        '<div id="machine-id" aria-activedescendant="active-id" '
        'aria-controls="panel-id" aria-describedby="description-id" '
        'aria-details="details-id" aria-expanded="true" aria-flowto="next-id" '
        'aria-labelledby="label-id" aria-owns="owned-id" aria-pressed="mixed" '
        'aria-selected="true" alt="Not alternative text" value="machine-value" '
        'label="Not an option" placeholder="Not a control">'
        "</div>"
        '<input type="hidden" alt="Not an image" value="Hidden machine value">'
        '<input type="text" alt="Not an image">'
        "</article>"
    )

    assert projection == RenderedProjection("", (), ())


@pytest.mark.parametrize("reference", ("&nbsp", "&#160", "&#xA0"))
def test_semicolonless_attribute_references_decode_at_their_ampersand_origin(
    reference: str,
) -> None:
    """HTML attribute references accepted without semicolons must retain evidence."""

    html_text = f'<article class="md-content__inner"><img alt="Public{reference} site"></article>'

    projection = project_rendered_content(html_text)

    assert projection.text == "Public site"
    space_index = projection.text.index(" ")
    assert projection.origins[space_index] == _position(html_text, reference)
    assert projection.contexts[space_index] == "img[alt]"


def test_ambiguous_semicolonless_attribute_references_remain_literal() -> None:
    """A name followed by a letter or equals sign is not an attribute reference."""

    projection = project_rendered_content(
        '<article class="md-content__inner"><img alt="A&nbspx &copy= B"></article>'
    )

    assert projection.text == "A&nbspx &copy= B"


def test_numeric_attribute_reference_preserves_a_literal_trailing_equals_origin() -> None:
    """Numeric decoding must not attribute an adjacent equals sign to the entity."""

    html_text = '<article class="md-content__inner"><img alt="A&#160=B"></article>'

    projection = project_rendered_content(html_text)

    assert projection.text == "A =B"
    equals_index = projection.text.index("=")
    assert projection.origins[equals_index] == _position(html_text, "=B")


def test_attribute_segments_do_not_split_inline_body_text() -> None:
    """An inline title is independent evidence rather than a body separator."""

    projection = project_rendered_content(
        '<article class="md-content__inner"><p>public<a title="help">site</a></p></article>'
    )

    assert projection.text == f"publicsite{PARAGRAPH_BOUNDARY}help"


def test_multiline_attribute_positions_remain_exact() -> None:
    """Literal attribute characters after a newline need line-accurate origins."""

    html_text = """<article class="md-content__inner">
<img
 alt="Line
two">
</article>"""

    projection = project_rendered_content(html_text)

    assert projection.text == "Line two"
    assert projection.origins[0] == _position(html_text, "Line")
    assert projection.origins[5] == _position(html_text, "two")
    assert set(projection.contexts) == {"img[alt]"}
