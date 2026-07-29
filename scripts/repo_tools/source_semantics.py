"""Normalize authored source text without crossing structural record boundaries."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

PARAGRAPH_BOUNDARY = "\N{SYMBOL FOR NULL}"
SOFT_SPACING_CHARACTERS = frozenset({"\u200b", "\ufeff"})
DASH_LIKE_CHARACTERS = frozenset({"\u00ad", "\u2212"})
LINE_BREAK_CHARACTERS = frozenset({"\n", "\r", "\v", "\f", "\x85", "\u2028", "\u2029"})
FORCED_PARAGRAPH_BREAK_CHARACTERS = frozenset({"\u2029"})
LINE_ORIENTED_SOURCE_NAMES = frozenset({".gitignore", ".pages", "CODEOWNERS"})
YAML_SOURCE_SUFFIXES = frozenset({".yaml", ".yml"})
MARKDOWN_BLOCK_START_PATTERN = re.compile(
    r"^[ \t]{0,3}(?:"
    r"#{1,6}(?:[ \t]|$)|"
    r"(?:[-+*]|[0-9]{1,9}[.)])[ \t]+|"
    r"`{3,}|~{3,}|\||"
    r"(?:={3,}|-{3,})[ \t]*$"
    r")"
)
MARKDOWN_BLOCK_END_PATTERN = re.compile(
    r"^[ \t]{0,3}(?:"
    r"#{1,6}(?:[ \t]|$)|"
    r"`{3,}|~{3,}|\||"
    r"(?:={3,}|-{3,})[ \t]*$"
    r")"
)
MARKDOWN_BLOCKQUOTE_PATTERN = re.compile(r"^[ \t]{0,3}>(?:[ \t]|$)")


@dataclass(frozen=True)
class SemanticProjection:
    """Rendered source text with one raw-source offset per character."""

    text: str
    raw_offsets: tuple[int, ...]

    def __post_init__(self) -> None:
        """Reject projections that cannot provide exact source evidence."""

        if len(self.text) != len(self.raw_offsets):
            raise ValueError("semantic projection text and offset lengths differ")


def logical_line_break_count(text: str) -> int:
    """Count logical line breaks, treating CRLF as one break."""

    count = 0
    index = 0
    while index < len(text):
        character = text[index]
        if character == "\r":
            count += 1
            if index + 1 < len(text) and text[index + 1] == "\n":
                index += 1
        elif character in LINE_BREAK_CHARACTERS:
            count += 1
        index += 1
    return count


def is_yaml_source(path: Path) -> bool:
    """Return whether a source uses YAML record semantics."""

    return path.name == ".pages" or path.suffix.casefold() in YAML_SOURCE_SUFFIXES


def _next_physical_line(text: str, run_start: int) -> str:
    """Return the physical line after the first break in a whitespace run."""

    break_index = run_start
    while break_index < len(text) and text[break_index] not in LINE_BREAK_CHARACTERS:
        break_index += 1
    if break_index >= len(text):
        return ""
    if text[break_index] == "\r" and text[break_index : break_index + 2] == "\r\n":
        line_start = break_index + 2
    else:
        line_start = break_index + 1
    line_end = line_start
    while line_end < len(text) and text[line_end] not in LINE_BREAK_CHARACTERS:
        line_end += 1
    return text[line_start:line_end]


def _previous_physical_line(text: str, run_start: int) -> str:
    """Return the physical line immediately before a whitespace run."""

    line_end = run_start
    while line_end > 0 and text[line_end - 1] in {" ", "\t"}:
        line_end -= 1
    line_start = line_end
    while line_start > 0 and text[line_start - 1] not in LINE_BREAK_CHARACTERS:
        line_start -= 1
    return text[line_start:line_end]


def _single_line_break_is_structural(path: Path, text: str, run_start: int) -> bool:
    """Return whether one physical break separates records rather than prose."""

    if path.name in LINE_ORIENTED_SOURCE_NAMES or is_yaml_source(path):
        return True
    if path.suffix.casefold() != ".md":
        return False
    previous_line = _previous_physical_line(text, run_start)
    next_line = _next_physical_line(text, run_start)
    next_line_starts_block = MARKDOWN_BLOCK_START_PATTERN.match(next_line) is not None
    next_line_starts_new_quote = (
        MARKDOWN_BLOCKQUOTE_PATTERN.match(next_line) is not None
        and MARKDOWN_BLOCKQUOTE_PATTERN.match(previous_line) is None
    )
    previous_line_ends_block = MARKDOWN_BLOCK_END_PATTERN.match(previous_line) is not None
    return next_line_starts_block or next_line_starts_new_quote or previous_line_ends_block


def normalize_source_text(
    text: str,
    *,
    path: Path,
    single_line_breaks_are_structural: bool = False,
) -> tuple[str, tuple[int, ...]]:
    """Normalize source separators while retaining raw source offsets."""

    normalized: list[str] = []
    raw_offsets: list[int] = []
    index = 0
    while index < len(text):
        character = text[index]
        if character.isspace() or character in SOFT_SPACING_CHARACTERS:
            run_start = index
            while index < len(text):
                run_character = text[index]
                if not (run_character.isspace() or run_character in SOFT_SPACING_CHARACTERS):
                    break
                index += 1
            whitespace_run = text[run_start:index]
            line_break_count = logical_line_break_count(whitespace_run)
            is_paragraph_boundary = (
                line_break_count >= 2
                or any(
                    break_character in whitespace_run
                    for break_character in FORCED_PARAGRAPH_BREAK_CHARACTERS
                )
                or (
                    line_break_count == 1
                    and (
                        single_line_breaks_are_structural
                        or _single_line_break_is_structural(path, text, run_start)
                    )
                )
            )
            normalized.append(PARAGRAPH_BOUNDARY if is_paragraph_boundary else " ")
            raw_offsets.append(run_start)
            continue
        is_dash = character in DASH_LIKE_CHARACTERS or unicodedata.category(character) == "Pd"
        normalized.append("-" if is_dash else character)
        raw_offsets.append(index)
        index += 1
    return "".join(normalized), tuple(raw_offsets)
