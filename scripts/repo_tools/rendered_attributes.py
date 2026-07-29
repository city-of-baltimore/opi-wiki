"""Project selected HTML attribute values back to raw start-tag offsets."""

from __future__ import annotations

import html
import re
from collections.abc import Mapping
from dataclasses import dataclass
from html.entities import html5 as HTML5_ENTITIES
from typing import Final

_ATTRIBUTE_REFERENCE = re.compile(r"&(#[0-9]+|#[xX][0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*)[;=]?")
# This table is intentionally closed: ``None`` means a global prose attribute,
# while a tag set limits an attribute to elements where HTML gives it reader
# meaning. ARIA states and ID-reference relationships are deliberately absent.
_READER_FACING_ATTRIBUTE_TAGS: Final[Mapping[str, frozenset[str] | None]] = {
    "abbr": frozenset({"th"}),
    "alt": frozenset({"area", "img", "input"}),
    "aria-braillelabel": None,
    "aria-brailleroledescription": None,
    "aria-description": None,
    "aria-label": None,
    "aria-placeholder": None,
    "aria-roledescription": None,
    "aria-valuetext": None,
    "label": frozenset({"optgroup", "option", "track"}),
    "placeholder": frozenset({"input", "textarea"}),
    "title": None,
    "value": frozenset({"input"}),
}
_READER_FACING_ATTRIBUTE_NAMES = frozenset(_READER_FACING_ATTRIBUTE_TAGS)


@dataclass(frozen=True)
class _AttributeSegment:
    """Decoded attribute text aligned to offsets within one raw start tag."""

    name: str
    text: str
    raw_offsets: tuple[int, ...]

    def __post_init__(self) -> None:
        """Reject attribute evidence that cannot map every decoded character."""

        if len(self.text) != len(self.raw_offsets):
            raise ValueError("attribute text and raw offsets differ in length")


def _decoded_reference(reference: str) -> tuple[str, bool] | None:
    """Return decoded attribute text and whether a trailing equals sign is literal."""

    if reference.startswith("&#"):
        trailing_equals = reference.endswith("=")
        encoded = reference[:-1] if trailing_equals else reference
        return html.unescape(encoded), trailing_equals
    if reference.endswith("=") or reference[1:] not in HTML5_ENTITIES:
        return None
    return html.unescape(reference), False


def _decode_attribute_value(raw: str, *, start_offset: int) -> tuple[str, tuple[int, ...]]:
    """Decode HTML attribute references with one raw offset per output character."""

    text: list[str] = []
    offsets: list[int] = []
    index = 0
    while index < len(raw):
        if raw[index] != "&":
            text.append(raw[index])
            offsets.append(start_offset + index)
            index += 1
            continue

        match = _ATTRIBUTE_REFERENCE.match(raw, index)
        if match is None:
            text.append("&")
            offsets.append(start_offset + index)
            index += 1
            continue

        reference = match.group()
        decoded = _decoded_reference(reference)
        if decoded is None:
            text.extend(reference)
            offsets.extend(range(start_offset + index, start_offset + match.end()))
        else:
            value, trailing_equals = decoded
            text.extend(value)
            offsets.extend(start_offset + index for _character in value)
            if trailing_equals:
                text.append("=")
                offsets.append(start_offset + match.end() - 1)
        index = match.end()
    return "".join(text), tuple(offsets)


def _attribute_segments(
    raw_tag: str,
    selected_names: frozenset[str],
) -> tuple[_AttributeSegment, ...]:
    """Extract selected decoded attributes and their raw start-tag offsets."""

    segments: list[_AttributeSegment] = []
    cursor = 1
    while cursor < len(raw_tag) and not raw_tag[cursor].isspace():
        cursor += 1
    while cursor < len(raw_tag):
        while cursor < len(raw_tag) and raw_tag[cursor].isspace():
            cursor += 1
        if cursor >= len(raw_tag) or raw_tag[cursor] == ">":
            break
        if raw_tag.startswith("/>", cursor):
            break

        name_start = cursor
        while cursor < len(raw_tag) and not (raw_tag[cursor].isspace() or raw_tag[cursor] in "=/>"):
            cursor += 1
        if cursor == name_start:
            cursor += 1
            continue
        name = raw_tag[name_start:cursor].casefold()

        while cursor < len(raw_tag) and raw_tag[cursor].isspace():
            cursor += 1
        if cursor >= len(raw_tag) or raw_tag[cursor] != "=":
            continue
        cursor += 1
        while cursor < len(raw_tag) and raw_tag[cursor].isspace():
            cursor += 1
        if cursor >= len(raw_tag):
            break

        quote = raw_tag[cursor] if raw_tag[cursor] in {"'", '"'} else None
        if quote is not None:
            cursor += 1
            value_start = cursor
            while cursor < len(raw_tag) and raw_tag[cursor] != quote:
                cursor += 1
            value_end = cursor
            cursor += cursor < len(raw_tag)
        else:
            value_start = cursor
            while cursor < len(raw_tag) and not (
                raw_tag[cursor].isspace() or raw_tag[cursor] == ">"
            ):
                cursor += 1
            value_end = cursor

        if name in selected_names:
            text, raw_offsets = _decode_attribute_value(
                raw_tag[value_start:value_end],
                start_offset=value_start,
            )
            segments.append(_AttributeSegment(name, text, raw_offsets))
    return tuple(segments)


def _reader_facing_attribute_segments(
    raw_tag: str,
    tag: str,
    attrs: list[tuple[str, str | None]],
) -> tuple[_AttributeSegment, ...]:
    """Return only attributes with reader-facing meaning on this element."""

    input_type = (
        next(
            (
                value.strip().casefold()
                for name, value in attrs
                if name == "type" and value is not None
            ),
            "",
        )
        or "text"
    )
    segments: list[_AttributeSegment] = []
    for segment in _attribute_segments(raw_tag, _READER_FACING_ATTRIBUTE_NAMES):
        allowed_tags = _READER_FACING_ATTRIBUTE_TAGS[segment.name]
        if allowed_tags is not None and tag not in allowed_tags:
            continue
        if tag == "input" and segment.name == "alt" and input_type != "image":
            continue
        if tag == "input" and segment.name == "value" and input_type == "hidden":
            continue
        segments.append(segment)
    return tuple(segments)
