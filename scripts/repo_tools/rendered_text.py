"""Project trusted MkDocs HTML into normalized, source-addressable text."""

from __future__ import annotations

import html
import unicodedata
from dataclasses import dataclass, field
from html.parser import HTMLParser

from scripts.repo_tools.rendered_attributes import _reader_facing_attribute_segments
from scripts.repo_tools.source_semantics import (
    DASH_LIKE_CHARACTERS,
    PARAGRAPH_BOUNDARY,
    SOFT_SPACING_CHARACTERS,
)

_TARGET_CLASS = "md-content__inner"
_EXCLUDED_TAGS = frozenset({"script", "style", "template"})
_NON_RENDERING_SVG_SUBTREES = frozenset(
    {
        "clippath",
        "defs",
        "filter",
        "lineargradient",
        "marker",
        "mask",
        "metadata",
        "pattern",
        "radialgradient",
        "symbol",
        "view",
    }
)
_VOID_TAGS = frozenset(
    "area base br col embed hr img input link meta param source track wbr".split()
)
_BLOCK_TAGS = frozenset(
    (
        "address article aside blockquote dd desc details dialog div dl dt fieldset "
        "figcaption figure footer form h1 h2 h3 h4 h5 h6 header hr li main nav ol p "
        "optgroup option pre section summary table tbody td tfoot th thead title tr ul"
    ).split()
)


class RenderedTextError(ValueError):
    """Report HTML that cannot yield one trustworthy content projection."""


@dataclass(frozen=True)
class RenderedOrigin:
    """Exact one-based source location for one projected character."""

    line: int
    column: int

    def __post_init__(self) -> None:
        """Reject positions that cannot address HTML source."""

        if self.line < 1 or self.column < 1:
            raise ValueError("rendered-text origins must be one-based")


@dataclass(frozen=True)
class RenderedProjection:
    """Normalized text with aligned source origins and semantic contexts."""

    text: str
    origins: tuple[RenderedOrigin, ...]
    contexts: tuple[str, ...]

    def __post_init__(self) -> None:
        """Reject projections that cannot provide per-character evidence."""

        if len(self.text) != len(self.origins) or len(self.text) != len(self.contexts):
            raise ValueError("rendered projection text, origin, and context lengths differ")
        if any(not context for context in self.contexts):
            raise ValueError("rendered projection contexts must not be empty")


@dataclass
class _Frame:
    """One open element in the captured content region."""

    tag: str
    context: str
    excluded: bool
    svg_namespace: bool = False
    child_counts: dict[str, int] = field(default_factory=dict)


@dataclass
class _Characters:
    """Mutable, aligned character evidence used while parsing."""

    text: list[str] = field(default_factory=list)
    origins: list[RenderedOrigin] = field(default_factory=list)
    contexts: list[str] = field(default_factory=list)

    def append(self, text: str, origin: RenderedOrigin, context: str) -> None:
        """Append characters that share one source origin and context."""

        self.text.extend(text)
        self.origins.extend(origin for _character in text)
        self.contexts.extend(context for _character in text)


def _advance_positions(raw: str, start: RenderedOrigin) -> tuple[RenderedOrigin, ...]:
    """Return the source position of every character in a raw HTML fragment."""

    positions: list[RenderedOrigin] = []
    line = start.line
    column = start.column
    for character in raw:
        positions.append(RenderedOrigin(line, column))
        if character == "\n":
            line += 1
            column = 1
        else:
            column += 1
    return tuple(positions)


def _normalize(characters: _Characters) -> RenderedProjection:
    """Normalize spacing and dashes without losing character evidence."""

    normalized = _Characters()
    for character, origin, context in zip(
        characters.text,
        characters.origins,
        characters.contexts,
        strict=True,
    ):
        if character == PARAGRAPH_BOUNDARY:
            if normalized.text and normalized.text[-1] == " ":
                normalized.text.pop()
                normalized.origins.pop()
                normalized.contexts.pop()
            if normalized.text and normalized.text[-1] != PARAGRAPH_BOUNDARY:
                normalized.append(PARAGRAPH_BOUNDARY, origin, context)
            continue
        if character.isspace() or character in SOFT_SPACING_CHARACTERS:
            if normalized.text and normalized.text[-1] not in {" ", PARAGRAPH_BOUNDARY}:
                normalized.append(" ", origin, context)
            continue
        is_dash = character in DASH_LIKE_CHARACTERS or unicodedata.category(character) == "Pd"
        normalized.append("-" if is_dash else character, origin, context)
    while normalized.text and normalized.text[-1] in {" ", PARAGRAPH_BOUNDARY}:
        normalized.text.pop()
        normalized.origins.pop()
        normalized.contexts.pop()
    return RenderedProjection(
        "".join(normalized.text),
        tuple(normalized.origins),
        tuple(normalized.contexts),
    )


class _RenderedContentParser(HTMLParser):
    """Capture one generated MkDocs content article and its source evidence."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.body = _Characters()
        self.attributes: list[_Characters] = []
        self.frames: list[_Frame] = []
        self.target_seen = False
        self.target_closed = False

    @staticmethod
    def _is_target(tag: str, attrs: list[tuple[str, str | None]]) -> bool:
        """Return whether a start tag is the generated content container."""

        classes = {
            token
            for name, value in attrs
            if name == "class" and value is not None
            for token in value.split()
        }
        return tag == "article" and _TARGET_CLASS in classes

    def _origin(self) -> RenderedOrigin:
        """Return the current parser position as a one-based origin."""

        line, zero_based_column = self.getpos()
        return RenderedOrigin(line, zero_based_column + 1)

    def _context_for_child(self, tag: str) -> str:
        """Return a deterministic DOM-like context for a new child element."""

        parent = self.frames[-1]
        count = parent.child_counts.get(tag, 0) + 1
        parent.child_counts[tag] = count
        return f"{parent.context} > {tag}:nth-of-type({count})"

    def _capture_attributes(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
        origin: RenderedOrigin,
        *,
        svg_namespace: bool = False,
    ) -> None:
        """Capture user-facing attributes from the current raw start tag."""

        if tag == "iframe" and any(
            name in {"src", "srcdoc"} and value is not None and value.strip()
            for name, value in attrs
        ):
            raise RenderedTextError(
                "unable to project a nonempty iframe embedded document; move its content "
                "into the canonical page"
            )
        if (
            svg_namespace
            and tag == "use"
            and any(
                name in {"href", "xlink:href"} and value is not None and value.strip()
                for name, value in attrs
            )
        ):
            raise RenderedTextError(
                "unable to project SVG <use> reference; inline the referenced SVG content"
            )
        raw_tag = self.get_starttag_text()
        if raw_tag is None:
            raise RenderedTextError("malformed content region: start tag source is unavailable")
        positions = _advance_positions(raw_tag, origin)
        for segment in _reader_facing_attribute_segments(raw_tag, tag, attrs):
            context = f"{tag}[{segment.name}]"
            characters = _Characters()
            for character, raw_offset in zip(
                segment.text,
                segment.raw_offsets,
                strict=True,
            ):
                characters.append(character, positions[raw_offset], context)
            self.attributes.append(characters)

    def _start(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
        *,
        self_closing: bool,
    ) -> None:
        """Handle ordinary and explicitly self-closing start tags."""

        origin = self._origin()
        if self._is_target(tag, attrs):
            if self.target_seen:
                raise RenderedTextError(
                    "expected exactly one md-content__inner article; found a duplicate"
                )
            if self_closing:
                raise RenderedTextError("malformed content region: target article is self-closing")
            self.target_seen = True
            self.frames.append(_Frame(tag, "article.md-content__inner", False))
            self._capture_attributes(tag, attrs, origin)
            return
        if not self.frames:
            return
        parent = self.frames[-1]
        element_context = self._context_for_child(tag)
        context = element_context if tag in _BLOCK_TAGS else parent.context
        svg_namespace = tag == "svg" or (parent.svg_namespace and parent.tag != "foreignobject")
        excluded = (
            parent.excluded
            or tag in _EXCLUDED_TAGS
            or (svg_namespace and tag in _NON_RENDERING_SVG_SUBTREES)
        )
        if not excluded:
            if tag in _BLOCK_TAGS:
                self.body.append(PARAGRAPH_BOUNDARY, origin, context)
            elif tag == "br":
                self.body.append(" ", origin, context)
            self._capture_attributes(
                tag,
                attrs,
                origin,
                svg_namespace=svg_namespace,
            )
        if tag not in _VOID_TAGS and not self_closing:
            self.frames.append(
                _Frame(
                    tag=tag,
                    context=context,
                    excluded=excluded,
                    svg_namespace=svg_namespace,
                )
            )
        elif tag in _BLOCK_TAGS and not excluded:
            self.body.append(PARAGRAPH_BOUNDARY, origin, context)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Capture a normal start tag."""

        self._start(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Capture an explicitly self-closing tag without opening a frame."""

        self._start(tag, attrs, self_closing=True)

    def handle_endtag(self, tag: str) -> None:
        """Close a captured element, rejecting structurally ambiguous markup."""

        if not self.frames:
            return
        frame = self.frames[-1]
        if frame.tag != tag:
            raise RenderedTextError(
                f"malformed content region: closing </{tag}> does not match <{frame.tag}>"
            )
        origin = self._origin()
        if tag in _BLOCK_TAGS and not frame.excluded:
            self.body.append(PARAGRAPH_BOUNDARY, origin, frame.context)
        self.frames.pop()
        if not self.frames:
            self.target_closed = True

    def handle_data(self, data: str) -> None:
        """Capture visible character data with exact source positions."""

        if not self.frames or self.frames[-1].excluded:
            return
        context = self.frames[-1].context
        positions = _advance_positions(data, self._origin())
        for character, origin in zip(data, positions, strict=True):
            self.body.append(character, origin, context)

    def handle_entityref(self, name: str) -> None:
        """Decode a named entity at the entity's source ampersand."""

        if self.frames and not self.frames[-1].excluded:
            self.body.append(html.unescape(f"&{name};"), self._origin(), self.frames[-1].context)

    def handle_charref(self, name: str) -> None:
        """Decode a numeric entity at the entity's source ampersand."""

        if self.frames and not self.frames[-1].excluded:
            self.body.append(html.unescape(f"&#{name};"), self._origin(), self.frames[-1].context)

    def projection(self) -> RenderedProjection:
        """Build the final projection after structural validation."""

        if not self.target_seen:
            raise RenderedTextError("expected exactly one md-content__inner article; found none")
        if self.frames or not self.target_closed:
            raise RenderedTextError("malformed content region: target article is not closed")
        segments = [_normalize(self.body)]
        segments.extend(_normalize(attribute) for attribute in self.attributes)
        nonempty = [segment for segment in segments if segment.text]
        combined = _Characters()
        for segment in nonempty:
            if combined.text:
                combined.append(PARAGRAPH_BOUNDARY, segment.origins[0], segment.contexts[0])
            combined.text.extend(segment.text)
            combined.origins.extend(segment.origins)
            combined.contexts.extend(segment.contexts)
        return RenderedProjection(
            "".join(combined.text),
            tuple(combined.origins),
            tuple(combined.contexts),
        )


def project_rendered_content(html_text: str) -> RenderedProjection:
    """Return normalized visible text from exactly one MkDocs content article."""

    parser = _RenderedContentParser()
    try:
        parser.feed(html_text)
        parser.close()
    except RenderedTextError:
        raise
    except (AssertionError, ValueError) as error:
        raise RenderedTextError(f"malformed HTML content region: {error}") from error
    return parser.projection()
