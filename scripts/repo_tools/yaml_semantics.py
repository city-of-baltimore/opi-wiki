"""Project decoded YAML scalar values back to exact authored-source offsets."""

from __future__ import annotations

from dataclasses import dataclass

import yaml
from yaml.error import MarkedYAMLError
from yaml.tokens import ScalarToken

from scripts.repo_tools.source_semantics import SemanticProjection

_DOUBLE_QUOTED_ESCAPES = {
    "0": "\0",
    "a": "\x07",
    "b": "\x08",
    "t": "\t",
    "\t": "\t",
    "n": "\n",
    "v": "\x0b",
    "f": "\x0c",
    "r": "\r",
    "e": "\x1b",
    " ": " ",
    '"': '"',
    "/": "/",
    "\\": "\\",
    "N": "\x85",
    "_": "\xa0",
    "L": "\u2028",
    "P": "\u2029",
}
_HEX_ESCAPE_LENGTHS = {"x": 2, "u": 4, "U": 8}
_YAML_LINE_BREAKS = frozenset({"\n", "\r", "\x85", "\u2028", "\u2029"})


@dataclass(frozen=True)
class YamlSemanticError(ValueError):
    """A fail-closed YAML semantic-projection error."""

    line_number: int
    detail: str

    def __str__(self) -> str:
        """Return a concise diagnostic suitable for a structural gate."""

        return self.detail


def _line_break_end(text: str, index: int) -> int:
    """Return the first offset after one YAML line break."""

    if text[index : index + 2] == "\r\n":
        return index + 2
    return index + 1


def _decode_double_quote_escape(raw: str, index: int) -> tuple[str, int] | None:
    """Decode one double-quoted YAML escape at ``index`` when complete."""

    if raw[index] != "\\" or index + 1 >= len(raw):
        return None
    marker = raw[index + 1]
    if marker in _DOUBLE_QUOTED_ESCAPES:
        return _DOUBLE_QUOTED_ESCAPES[marker], index + 2
    if marker in _HEX_ESCAPE_LENGTHS:
        length = _HEX_ESCAPE_LENGTHS[marker]
        digits = raw[index + 2 : index + 2 + length]
        if len(digits) == length:
            try:
                return chr(int(digits, 16)), index + 2 + length
            except ValueError:
                return None
    if marker in _YAML_LINE_BREAKS:
        cursor = _line_break_end(raw, index + 1)
        while cursor < len(raw) and raw[cursor] in {" ", "\t"}:
            cursor += 1
        return "", cursor
    return None


def _scalar_content_bounds(raw: str, style: str | None) -> tuple[int, int]:
    """Return the source slice that can contribute decoded scalar text."""

    if style in {"'", '"'}:
        return 1, max(1, len(raw) - 1)
    if style in {">", "|"}:
        cursor = 0
        while cursor < len(raw) and raw[cursor] not in _YAML_LINE_BREAKS:
            cursor += 1
        if cursor < len(raw):
            cursor = _line_break_end(raw, cursor)
        return cursor, len(raw)
    return 0, len(raw)


def _project_scalar(text: str, token: ScalarToken) -> SemanticProjection:
    """Map one PyYAML-decoded scalar token to absolute source offsets."""

    raw_start = token.start_mark.index
    raw = text[raw_start : token.end_mark.index]
    cursor, limit = _scalar_content_bounds(raw, token.style)
    offsets: list[int] = []

    for decoded_character in token.value:
        matched_offset: int | None = None
        while cursor < limit:
            raw_character = raw[cursor]
            if token.style == '"' and raw_character == "\\":
                decoded_escape = _decode_double_quote_escape(raw, cursor)
                if decoded_escape is not None:
                    escaped_value, escape_end = decoded_escape
                    if escaped_value == "":
                        cursor = escape_end
                        continue
                    if escaped_value == decoded_character:
                        matched_offset = cursor
                        cursor = escape_end
                        break
            if (
                token.style == "'"
                and raw_character == "'"
                and cursor + 1 < limit
                and raw[cursor + 1] == "'"
                and decoded_character == "'"
            ):
                matched_offset = cursor
                cursor += 2
                break
            if raw_character == decoded_character:
                matched_offset = cursor
                cursor += 1
                break
            if decoded_character.isspace() and raw_character.isspace():
                matched_offset = cursor
                cursor = (
                    _line_break_end(raw, cursor)
                    if raw_character in _YAML_LINE_BREAKS
                    else cursor + 1
                )
                break
            cursor += 1
        if matched_offset is None:
            raise YamlSemanticError(
                token.start_mark.line + 1,
                "could not map a decoded YAML scalar to its authored source",
            )
        offsets.append(raw_start + matched_offset)

    return SemanticProjection(token.value, tuple(offsets))


def _parse_error(error: yaml.YAMLError) -> YamlSemanticError:
    """Convert a PyYAML failure into stable line-level gate evidence."""

    if isinstance(error, MarkedYAMLError):
        mark = error.problem_mark or error.context_mark
        line_number = mark.line + 1 if mark is not None else 1
        detail = error.problem or error.context or "invalid YAML"
        return YamlSemanticError(line_number, f"invalid YAML: {detail}")
    return YamlSemanticError(1, f"invalid YAML: {error}")


def yaml_scalar_projections(text: str) -> tuple[SemanticProjection, ...]:
    """Return every decoded YAML scalar with absolute source offsets."""

    try:
        tuple(yaml.compose_all(text))
        tokens = tuple(yaml.scan(text))
    except yaml.YAMLError as error:
        raise _parse_error(error) from error

    projections: list[SemanticProjection] = []
    for token in tokens:
        if not isinstance(token, ScalarToken):
            continue
        try:
            projections.append(_project_scalar(text, token))
        except YamlSemanticError as error:
            raise YamlSemanticError(
                token.start_mark.line + 1,
                f"{error.detail} (scalar beginning on line {token.start_mark.line + 1})",
            ) from error
    return tuple(projections)
