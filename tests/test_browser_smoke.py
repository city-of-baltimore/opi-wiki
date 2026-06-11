"""Tests for browser smoke configuration helpers."""

from __future__ import annotations

from scripts.repo_tools.browser_smoke import SMOKE_TARGETS, normalize_base_url


def test_smoke_targets_cover_each_major_section() -> None:
    """Browser smoke coverage should keep one representative page per major section."""

    assert [target.section for target in SMOKE_TARGETS] == [
        "About Us",
        "How We Work",
        "Our Teams",
        "Resources",
        "Public",
    ]


def test_normalize_base_url_enforces_trailing_slash() -> None:
    """Base URLs should normalize so joined paths stay stable."""

    assert normalize_base_url("http://127.0.0.1:8000") == "http://127.0.0.1:8000/"
    assert normalize_base_url("http://127.0.0.1:8000/") == "http://127.0.0.1:8000/"
