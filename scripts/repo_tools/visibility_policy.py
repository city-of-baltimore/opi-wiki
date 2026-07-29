"""Typed policy matchers for retired repository labels and presentation hooks."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final, Literal

type VisibilityPolicyKind = Literal["visibility_label", "presentation_hook"]

VISIBILITY_LABEL_KIND: Final[VisibilityPolicyKind] = "visibility_label"
PRESENTATION_HOOK_KIND: Final[VisibilityPolicyKind] = "presentation_hook"

_RETIRED_TERM_START = r"(?<![A-Za-z0-9_/-])_{0,3}"
_RETIRED_TERM_END = r"_{0,3}(?![A-Za-z0-9_/-]|\.[A-Za-z0-9][A-Za-z0-9_-]*\b)"
_SEPARATOR = r"[- ]+"
_MARKDOWN_DECORATION = r"[*_]{0,3}"
_REPOSITORY_SURFACE_NOUN = (
    rf"(?:briefs?|cop(?:y|ies)|content(?:{_SEPARATOR}reviews?)?|"
    rf"docs?(?:{_SEPARATOR}sites?)?|documentation|guidance|guides?|materials?|"
    rf"pages?|publications?|references?|repositor(?:y|ies)|sites?|versions?|"
    rf"websites?|wikis?)"
)
_PUBLIC_INTERNAL_STATE_PREFIX = (
    rf"(?:public(?:{_SEPARATOR}facing)?|"
    rf"internal(?:{_SEPARATOR}(?:facing|only))?)"
)
_APPROVED_LABEL_CONTEXT = re.compile(
    r"(?:\A|"
    r"(?:[\N{SYMBOL FOR NULL}:;,(]|"
    r"\b(?:a|an|the|this|that|these|those|our|your|their|its|"
    r"as|be|been|being|is|are|was|were|"
    r"use|uses|using|used|keep|keeps|keeping|kept|"
    r"mark|marks|marking|marked|call|calls|calling|called|"
    r"publish|publishes|publishing|published|only))"
    r"[ \t]*)\Z",
    re.IGNORECASE,
)
_DIRECTOR_HEADING_LABEL = (
    rf"{_MARKDOWN_DECORATION}Public{_MARKDOWN_DECORATION}"
    rf"[^\S\r\n]+"
    rf"{_MARKDOWN_DECORATION}Purpose{_MARKDOWN_DECORATION}"
)
_DIRECTOR_HEADING_CONTENT = (
    rf"(?:{_DIRECTOR_HEADING_LABEL}|"
    rf"\[[ \t]*{_DIRECTOR_HEADING_LABEL}[ \t]*\]\([^)\r\n]*\))"
)


@dataclass(frozen=True)
class VisibilityPolicyMatch:
    """One deterministic policy match within the supplied text."""

    kind: VisibilityPolicyKind
    start: int
    end: int
    text: str


@dataclass(frozen=True)
class _PolicyRule:
    """One private regex rule with an optional canonical diagnostic label."""

    pattern: re.Pattern[str]
    diagnostic_text: str | None = None
    canonical_director_heading: bool = False
    predicate: Callable[[str, re.Match[str]], bool] | None = None


def _approved_match_is_label(text: str, match: re.Match[str]) -> bool:
    """Require bounded grammatical evidence that ``approved`` is a state label."""

    return _APPROVED_LABEL_CONTEXT.search(text[: match.start()]) is not None


_RETIRED_REPOSITORY_STATE_RULES = (
    _PolicyRule(
        re.compile(
            rf"{_RETIRED_TERM_START}{_PUBLIC_INTERNAL_STATE_PREFIX}{_SEPARATOR}"
            rf"{_REPOSITORY_SURFACE_NOUN}"
            rf"{_RETIRED_TERM_END}",
            re.IGNORECASE,
        )
    ),
    _PolicyRule(
        re.compile(
            rf"{_RETIRED_TERM_START}approved{_SEPARATOR}"
            rf"{_REPOSITORY_SURFACE_NOUN}"
            rf"{_RETIRED_TERM_END}",
            re.IGNORECASE,
        ),
        predicate=_approved_match_is_label,
    ),
    _PolicyRule(
        re.compile(
            rf"{_RETIRED_TERM_START}publication{_SEPARATOR}posture{_RETIRED_TERM_END}",
            re.IGNORECASE,
        )
    ),
    _PolicyRule(
        re.compile(
            rf"{_RETIRED_TERM_START}public/private{_SEPARATOR}"
            rf"boundar(?:y|ies){_SEPARATOR}"
            rf"must{_SEPARATOR}(?:remain|stay){_SEPARATOR}explicit\b",
            re.IGNORECASE,
        )
    ),
)

_RETIRED_VISIBILITY_LABEL_RULES = (
    _PolicyRule(
        re.compile(
            rf"{_RETIRED_TERM_START}(?:public|internal|approved){_SEPARATOR}"
            rf"(?:audiences?|badges?|labels?|languages?)"
            rf"{_RETIRED_TERM_END}",
            re.IGNORECASE,
        )
    ),
    _PolicyRule(
        re.compile(
            rf"{_RETIRED_TERM_START}public{_SEPARATOR}(?:"
            rf"effects?|"
            rf"Foundations{_SEPARATOR}sites?|leadership"
            rf"(?:{_SEPARATOR}(?:charts?|names))?|MkDocs{_SEPARATOR}sites?|"
            rf"operating{_SEPARATOR}models?|org{_SEPARATOR}charts?|"
            rf"organization{_SEPARATOR}data|role{_SEPARATOR}summar(?:y|ies)|rosters?|"
            rf"staff(?:{_SEPARATOR}rosters?)?|summar(?:y|ies)|"
            rf"template{_SEPARATOR}pages?){_RETIRED_TERM_END}",
            re.IGNORECASE,
        )
    ),
    _PolicyRule(
        re.compile(
            rf"{_RETIRED_TERM_START}internal{_SEPARATOR}(?:"
            rf"companion{_SEPARATOR}documents?|guidance|"
            rf"onboarding(?:{_SEPARATOR}working)?{_SEPARATOR}materials?|"
            rf"operating{_SEPARATOR}guidance|"
            rf"operations{_SEPARATOR}and{_SEPARATOR}communications|SOPs?|"
            rf"working{_SEPARATOR}materials?){_RETIRED_TERM_END}",
            re.IGNORECASE,
        )
    ),
    _PolicyRule(
        re.compile(
            rf"{_RETIRED_TERM_START}approved{_SEPARATOR}(?:"
            rf"engineering{_SEPARATOR}stack|PRs?|short{_SEPARATOR}form)"
            rf"{_RETIRED_TERM_END}",
            re.IGNORECASE,
        )
    ),
    _PolicyRule(re.compile(r"\b(?:ED/CDO|section owner) approves?\b", re.IGNORECASE)),
    _PolicyRule(re.compile(r"\bED/CDO approval\b", re.IGNORECASE)),
)

_DIRECTOR_LETTER_LABEL_RULES = (
    _PolicyRule(
        re.compile(
            rf"(?<![A-Za-z0-9]){_MARKDOWN_DECORATION}A{_MARKDOWN_DECORATION}"
            rf"[^\S\r\n]+{_MARKDOWN_DECORATION}public{_MARKDOWN_DECORATION}"
            rf"[^\S\r\n]+{_MARKDOWN_DECORATION}letter{_MARKDOWN_DECORATION}"
            rf"(?![A-Za-z0-9])",
            re.IGNORECASE,
        ),
        diagnostic_text="A public letter",
    ),
)

_DIRECTOR_LETTER_HEADING_RULES = (
    _PolicyRule(
        re.compile(
            rf"^[ \t]{{0,3}}#{{1,6}}[^\S\r\n]+{_DIRECTOR_HEADING_CONTENT}"
            rf"[ \t]*:?[ \t]*(?:(?:#+|\{{[^{{}}\r\n]*\}})[ \t]*)*\r?$",
            re.IGNORECASE | re.MULTILINE,
        ),
        canonical_director_heading=True,
    ),
    _PolicyRule(
        re.compile(
            rf"^[ \t]{{0,3}}{_DIRECTOR_HEADING_CONTENT}[ \t]*:?[ \t]*"
            rf"(?:\{{[^{{}}\r\n]*\}})?[ \t]*"
            rf"(?:\r\n|[\n\r\x85\u2028\u2029])"
            rf"[ \t]{{0,3}}(?:=+|-+)[ \t]*\r?$",
            re.IGNORECASE | re.MULTILINE,
        ),
        canonical_director_heading=True,
    ),
    _PolicyRule(
        re.compile(
            r"^[ \t]*Public[^\S\r\n]+Purpose[ \t]*:?[ \t]*$",
            re.IGNORECASE,
        ),
        canonical_director_heading=True,
    ),
)

_RETIRED_PRESENTATION_RULES = (
    _PolicyRule(re.compile(r"\{\{[-+]?\s*badge\s*\(", re.IGNORECASE)),
    _PolicyRule(re.compile(r"(?<![A-Za-z0-9])opi-pill(?![A-Za-z0-9])", re.IGNORECASE)),
)


def _find_matches(
    text: str,
    rules: tuple[_PolicyRule, ...],
    *,
    kind: VisibilityPolicyKind,
) -> tuple[VisibilityPolicyMatch, ...]:
    """Return stable, occurrence-deduplicated matches for one policy family."""

    matches: list[VisibilityPolicyMatch] = []
    seen: set[tuple[int, int, str]] = set()
    for rule in rules:
        for match in rule.pattern.finditer(text):
            if rule.predicate is not None and not rule.predicate(text, match):
                continue
            diagnostic_text = rule.diagnostic_text or match.group(0)
            if rule.canonical_director_heading:
                atx_prefix = re.match(r"^[ \t]{0,3}(#{1,6})", match.group(0))
                diagnostic_text = (
                    f"{atx_prefix.group(1)} Public Purpose"
                    if atx_prefix is not None
                    else "Public Purpose"
                )
            occurrence = (match.start(), match.end(), diagnostic_text.casefold())
            if occurrence in seen:
                continue
            seen.add(occurrence)
            matches.append(
                VisibilityPolicyMatch(
                    kind=kind,
                    start=match.start(),
                    end=match.end(),
                    text=diagnostic_text,
                )
            )
    return tuple(
        sorted(
            matches,
            key=lambda item: (
                item.start,
                item.end,
                item.kind,
                item.text.casefold(),
                item.text,
            ),
        )
    )


def find_visibility_label_matches(
    text: str,
    *,
    director_letter: bool = False,
    heading: bool = False,
) -> tuple[VisibilityPolicyMatch, ...]:
    """Return retired label matches for raw or already-rendered text.

    Callers set ``director_letter`` only for the canonical director-letter
    section, and set ``heading`` only when the supplied text is known to be a
    heading. This keeps ordinary civic and governance prose out of the policy.
    """

    rules: tuple[_PolicyRule, ...] = (
        *_RETIRED_VISIBILITY_LABEL_RULES,
        *_RETIRED_REPOSITORY_STATE_RULES,
    )
    if director_letter:
        rules = (*rules, *_DIRECTOR_LETTER_LABEL_RULES)
        if heading:
            rules = (*rules, *_DIRECTOR_LETTER_HEADING_RULES)
    return _find_matches(text, rules, kind=VISIBILITY_LABEL_KIND)


def find_presentation_hook_matches(text: str) -> tuple[VisibilityPolicyMatch, ...]:
    """Return retired macro and CSS-hook matches in deterministic source order."""

    return _find_matches(
        text,
        _RETIRED_PRESENTATION_RULES,
        kind=PRESENTATION_HOOK_KIND,
    )
