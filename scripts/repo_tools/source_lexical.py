"""Project bounded source-only inline markup without rendering Markdown."""

from __future__ import annotations

import html
import re

from scripts.repo_tools.source_semantics import PARAGRAPH_BOUNDARY, SemanticProjection

_BLOCK_HTML_TAGS = frozenset(
    (
        "address article aside blockquote dd details dialog div dl dt fieldset "
        "figcaption figure footer form h1 h2 h3 h4 h5 h6 header hr li main nav ol p "
        "pre section summary table tbody td tfoot th thead tr ul"
    ).split()
)
_ENTITY_PATTERN = re.compile(
    r"(?:&(?:#[0-9]+;?|#[xX][0-9A-Fa-f]+;?|[A-Za-z][A-Za-z0-9]+;)"
    r"|&nbsp(?![A-Za-z0-9=]))"
)
_INLINE_LINK_PATTERN = re.compile(
    r"(?P<image>!)?\[(?P<label>[^\]\r\n]+)\]"
    r"\((?P<destination>(?:[^()\r\n]|\([^()\r\n]*\))*)\)"
)
_EMPHASIS_TOKEN_PATTERN = re.compile(
    r"(?<!\\)(?P<delimiter>\*{1,3}|_{1,3})"
    r"(?P<token>[A-Za-z0-9][A-Za-z0-9'’/-]*)"
    r"(?P=delimiter)"
)
_TAG_OPEN_PATTERN = re.compile(r"</?([A-Za-z][A-Za-z0-9:-]*)")


def _tag_end(text: str, start: int) -> int | None:
    """Return the end of one quote-aware HTML tag, if it is complete."""

    quote: str | None = None
    cursor = start
    while cursor < len(text):
        character = text[cursor]
        if quote is None and character in {"'", '"'}:
            quote = character
        elif quote == character:
            quote = None
        elif quote is None and character == ">":
            return cursor + 1
        cursor += 1
    return None


def _mark_html_markup(
    text: str,
    removed: set[int],
    replacements: dict[int, str],
) -> None:
    """Remove complete comments and tags while retaining block boundaries."""

    cursor = 0
    while cursor < len(text):
        start = text.find("<", cursor)
        if start == -1:
            return
        if text.startswith("<!--", start):
            end = text.find("-->", start + 4)
            if end == -1:
                cursor = start + 1
                continue
            removed.update(range(start, end + 3))
            cursor = end + 3
            continue

        tag_match = _TAG_OPEN_PATTERN.match(text, start)
        if tag_match is None:
            cursor = start + 1
            continue
        tag_name_end = tag_match.end()
        if (
            tag_name_end < len(text)
            and not text[tag_name_end].isspace()
            and text[tag_name_end] not in {"/", ">"}
        ):
            cursor = start + 1
            continue
        tag_end = _tag_end(text, tag_name_end)
        if tag_end is None:
            cursor = start + 1
            continue

        tag = tag_match.group(1).casefold()
        removed.update(range(start, tag_end))
        if tag == "br":
            replacements[start] = " "
        elif tag in _BLOCK_HTML_TAGS:
            replacements[start] = PARAGRAPH_BOUNDARY
        cursor = tag_end


def _mark_inline_links(text: str, removed: set[int]) -> None:
    """Remove bounded inline-link syntax and destinations, retaining labels."""

    for match in _INLINE_LINK_PATTERN.finditer(text):
        if any(index in removed for index in range(match.start(), match.end())):
            continue
        image_start = match.start("image")
        if image_start != -1:
            removed.add(image_start)
        removed.add(match.start("label") - 1)
        removed.add(match.end("label"))
        removed.update(range(match.start("destination") - 1, match.end()))


def _mark_emphasis_tokens(text: str, removed: set[int]) -> None:
    """Remove paired emphasis around one lexical token only."""

    for match in _EMPHASIS_TOKEN_PATTERN.finditer(text):
        if any(index in removed for index in range(match.start(), match.end())):
            continue
        removed.update(range(match.start("delimiter"), match.start("token")))
        removed.update(range(match.end("token"), match.end()))


def _mark_entities(
    text: str,
    removed: set[int],
    replacements: dict[int, str],
) -> None:
    """Decode complete entities with every replacement mapped to its ampersand."""

    for match in _ENTITY_PATTERN.finditer(text):
        if any(index in removed for index in range(match.start(), match.end())):
            continue
        decoded = html.unescape(match.group(0))
        if decoded == match.group(0):
            continue
        removed.update(range(match.start(), match.end()))
        replacements[match.start()] = decoded


def source_lexical_projection(text: str) -> SemanticProjection:
    """Return a source-mapped projection for a closed set of inline syntax.

    This is deliberately lexical, not a Markdown renderer. It handles only
    complete HTML tags/comments, bounded inline links, single-token emphasis,
    and character references needed by source-only repository surfaces.
    Canonical published pages continue to use generated HTML as authority.
    """

    if not isinstance(text, str):
        raise TypeError("source lexical projection requires text")

    removed: set[int] = set()
    replacements: dict[int, str] = {}
    _mark_html_markup(text, removed, replacements)
    _mark_inline_links(text, removed)
    _mark_emphasis_tokens(text, removed)
    _mark_entities(text, removed, replacements)

    projected_text: list[str] = []
    raw_offsets: list[int] = []
    for index, character in enumerate(text):
        replacement = replacements.get(index)
        if replacement is not None:
            projected_text.extend(replacement)
            raw_offsets.extend(index for _character in replacement)
        elif index not in removed:
            projected_text.append(character)
            raw_offsets.append(index)
    return SemanticProjection("".join(projected_text), tuple(raw_offsets))
