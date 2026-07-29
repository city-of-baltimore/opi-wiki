"""Tests for the page consistency linter."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.check_consistency as consistency_cli
from scripts.repo_tools import consistency
from scripts.repo_tools.consistency import (
    DOCS,
    SERVICE_REQUIRED,
    TOC_REQUIRED,
    ConsistencyScan,
    acronym_report,
    check_citistat_narrative,
    check_duplicate_blockquotes,
    check_empty_headings,
    check_glossary_taxonomy,
    check_retired_page_decoration,
    check_service_sections,
    check_toc_sections,
    format_consistency_report,
    load_acronym_allowlist,
    scan_consistency,
)

# Display paths resolve against the repository root, so these fixture paths do
# not need to exist on disk.
PAGE = DOCS / "example" / "page.md"


def test_empty_heading_before_same_level_sibling_is_flagged() -> None:
    """A heading immediately followed by a same-level heading is empty."""

    lines = ["## First", "", "## Second", "Body text."]

    issues = check_empty_headings(PAGE, lines)

    assert len(issues) == 1
    assert "empty heading '## First'" in issues[0]


def test_heading_with_content_or_subsection_is_not_empty() -> None:
    """Body text and deeper subsections both make a section non-empty."""

    assert check_empty_headings(PAGE, ["## Parent", "", "Body text."]) == []
    assert check_empty_headings(PAGE, ["## Parent", "", "### Child", "Body text."]) == []


def test_trailing_empty_heading_is_flagged() -> None:
    """A heading at end-of-file with no body should be reported."""

    issues = check_empty_headings(PAGE, ["Body.", "", "## Dangling"])

    assert len(issues) == 1
    assert "end of file" in issues[0]


def test_repeated_long_blockquote_is_flagged() -> None:
    """The same long blockquote twice on one page indicates copy drift."""

    quote = "> " + "Respond when necessary. Build so we do not have to respond again. " * 2

    issues = check_duplicate_blockquotes(PAGE, [quote, "Body.", quote])

    assert len(issues) == 1
    assert "repeated 2x" in issues[0]


def test_short_or_unique_blockquotes_are_not_flagged() -> None:
    """Only repeated long blockquotes should produce findings."""

    long_quote = "> " + ("A sufficiently long reader summary sentence. " * 2)

    assert check_duplicate_blockquotes(PAGE, ["> Short.", long_quote]) == []


def test_service_pages_require_the_shared_skeleton() -> None:
    """Direct service pages missing required sections should be reported."""

    service_page = DOCS / "what-we-do" / "services" / "example.md"
    text = "## What this service does\n\ncontent\n"

    issues = check_service_sections(service_page, text)

    assert any("## The goal" in issue for issue in issues)
    assert not any("## What this service does" in issue for issue in issues)


def test_nested_service_landing_pages_require_the_shared_skeleton() -> None:
    """A service represented by a directory index must not bypass validation."""

    service_page = DOCS / "what-we-do" / "services" / "example" / "index.md"

    issues = check_service_sections(service_page, "## What this service does\n\ncontent\n")

    assert any("## The goal" in issue for issue in issues)
    assert not any("## What this service does" in issue for issue in issues)


def test_complete_service_page_and_supporting_pages_pass() -> None:
    """Complete summaries pass while section and detail pages stay out of scope."""

    service_page = DOCS / "what-we-do" / "services" / "example.md"
    section_landing = DOCS / "what-we-do" / "services" / "index.md"
    detail_page = DOCS / "what-we-do" / "services" / "example" / "method.md"
    complete_text = "\n\n".join(SERVICE_REQUIRED)

    assert check_service_sections(service_page, complete_text) == []
    assert check_service_sections(section_landing, "# Services\n") == []
    assert check_service_sections(detail_page, "# Method\n") == []


def test_acronym_report_respects_allowlist_expansion_headings_and_stopwords() -> None:
    """Known, expanded, heading-only, and stopword tokens should not be reported."""

    text = (
        "# ABCD\n"
        "The XYZQ pipeline feeds OPI dashboards.\n"
        "We coordinate with the Department of General Services (DGSX).\n"
    )

    findings = acronym_report(PAGE, text, allow={"OPI"})

    tokens = {token for _path, token in findings}
    assert tokens == {"XYZQ"}


def test_acronym_report_returns_no_findings_for_plain_copy() -> None:
    """A page without unknown acronyms should produce no informational findings."""

    assert acronym_report(PAGE, "Plain site copy for everyone.", allow=set()) == []


def test_theory_of_change_pages_require_the_shared_skeleton() -> None:
    """A named theory-of-change page should report every missing section."""

    toc_page = DOCS / "example-theory-of-change.md"

    issues = check_toc_sections(toc_page, "## NORTH STAR\n\nOutcome\n")

    assert any("### 1. Service overview" in issue for issue in issues)
    assert not any("## NORTH STAR" in issue for issue in issues)


def test_complete_or_unrelated_theory_of_change_pages_pass() -> None:
    """A complete theory page and unrelated content should produce no findings."""

    toc_page = DOCS / "example-theory-of-change.md"

    assert check_toc_sections(toc_page, "\n\n".join(TOC_REQUIRED)) == []
    assert check_toc_sections(DOCS / "ordinary.md", "# Ordinary\n") == []


def test_glossary_taxonomy_rejects_verified_stale_classifications() -> None:
    """Known team/service and role-placement contradictions must not return."""

    glossary = DOCS / "resources" / "reference" / "glossary.md"
    text = (
        "**Data and Analytics.** OPI’s service for analytics.\n"
        "| **TPM** | Technical Program Manager (a Data and Analytics role) |\n"
    )

    issues = check_glossary_taxonomy(glossary, text)

    assert len(issues) == 2
    assert "Data and Analytics is a team" in issues[0]
    assert "Technical Program Manager is a Director's Office role" in issues[1]


def test_glossary_taxonomy_accepts_canonical_language_and_other_pages() -> None:
    """Canonical glossary language should pass without policing unrelated prose."""

    glossary = DOCS / "resources" / "reference" / "glossary.md"
    canonical = (
        "**Data and Analytics.** OPI’s team that delivers the Citywide Data and "
        "Analytics service.\n"
        "| **TPM** | Technical Program Manager (a Director's Office role) |\n"
    )

    assert check_glossary_taxonomy(glossary, canonical) == []
    assert check_glossary_taxonomy(DOCS / "ordinary.md", canonical) == []


def test_citistat_narrative_rejects_verified_portfolio_and_ownership_drift() -> None:
    """Agency-only labels and team-level program ownership must not return."""

    citistat_page = DOCS / "what-we-do" / "programs" / "citistat" / "index.cards.yml"
    performance_page = DOCS / "about-us" / "our-teams" / "performance" / "index.md"
    innovation_page = DOCS / "about-us" / "our-teams" / "innovation-lab" / "about-innovation-lab.md"

    portfolio_issues = check_citistat_narrative(
        citistat_page,
        "The 19 agency briefs form the agency portfolio and current schedule of active Stats.",
    )
    ownership_issues = check_citistat_narrative(
        performance_page,
        "The Performance team owns how the city reviews performance. "
        "The team owns the CitiStat program.",
    )
    boundary_issues = check_citistat_narrative(
        innovation_page,
        "Performance routines and CitiStat belong to the Performance team.",
    )

    assert len(portfolio_issues) == 3
    assert "mixes agency and thematic Stats" in portfolio_issues[0]
    assert "calendar details are maintained separately" in portfolio_issues[2]
    assert len(ownership_issues) == 2
    assert all("Executive Director" in issue for issue in ownership_issues)
    assert len(boundary_issues) == 1
    assert "operates CitiStat" in boundary_issues[0]


def test_citistat_narrative_accepts_canonical_language_and_other_pages() -> None:
    """Canonical ownership and register wording pass without policing other pages."""

    citistat_page = DOCS / "what-we-do" / "programs" / "citistat" / "index.md"
    canonical = (
        "The Executive Director owns CitiStat as CitiStat Director. "
        "Performance operates it day to day. The Stat portfolio is a register."
    )

    assert check_citistat_narrative(citistat_page, canonical) == []
    assert check_citistat_narrative(DOCS / "ordinary.md", "Agency briefs.") == []


def test_retired_page_decoration_rejects_macro_and_raw_markup() -> None:
    """Both legacy rendering paths must fail with line-level evidence."""

    text = '# Page\n\n{{ badge("reference") }}\n\n<span class="opi-pill neutral">Reference</span>\n'

    issues = check_retired_page_decoration(PAGE, text)

    assert len(issues) == 2
    assert issues[0].startswith("docs/example/page.md:3:")
    assert "Inline badge macros are retired" in issues[0]
    assert issues[1].startswith("docs/example/page.md:5:")
    assert "Raw pill markup is retired" in issues[1]


def test_retired_page_decoration_ignores_domain_language() -> None:
    """Physical credentials and operational wording remain ordinary prose."""

    text = "Activate your building badge and review the service-request status."

    assert check_retired_page_decoration(PAGE, text) == []


def test_allowlist_combines_curated_and_glossary_terms(tmp_path: Path) -> None:
    """The acronym allowlist should include built-ins and glossary terms."""

    docs_dir = tmp_path / "docs"
    glossary = docs_dir / "resources" / "reference" / "glossary.md"
    glossary.parent.mkdir(parents=True)
    glossary.write_text("# Glossary\n\nABCD is a fixture term.\n", encoding="utf-8")

    allow = load_acronym_allowlist(docs_dir)

    assert {"OPI", "ABCD"} <= allow


def test_allowlist_reports_an_unreadable_glossary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A glossary IO failure should become a contextual runtime error."""

    docs_dir = tmp_path / "docs"
    glossary = docs_dir / "resources" / "reference" / "glossary.md"
    glossary.parent.mkdir(parents=True)
    glossary.touch()
    original_read_text = Path.read_text

    def fail_glossary(path: Path, *, encoding: str) -> str:
        if path == glossary:
            raise OSError("read failed")
        return original_read_text(path, encoding=encoding)

    monkeypatch.setattr(Path, "read_text", fail_glossary)

    with pytest.raises(RuntimeError, match="Unable to read acronym glossary"):
        load_acronym_allowlist(docs_dir)


def test_scan_consistency_collects_a_clean_page(tmp_path: Path) -> None:
    """The repository scan should return an empty result for clean Markdown."""

    repo_root = tmp_path / "repo"
    docs_dir = repo_root / "docs"
    page = docs_dir / "guide" / "page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Page\n\nPlain site copy.\n", encoding="utf-8")

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result == ConsistencyScan(structural_issues=(), acronyms=())


def test_scan_consistency_integrates_visibility_ratchet_across_sources(tmp_path: Path) -> None:
    """Root guidance, Markdown, and either YAML suffix must share the CI ratchet."""

    repo_root = tmp_path / "repo"
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(parents=True)
    (repo_root / "README.md").write_text("Public-facing guide.\n", encoding="utf-8")
    (docs_dir / "page.md").write_text("# Page\n\nInternal-only copy.\n", encoding="utf-8")
    (docs_dir / "page.yaml").write_text(
        'summary: "Approved audience label."\n',
        encoding="utf-8",
    )

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert len(result.structural_issues) == 3
    assert any(
        "README.md:1:" in issue and "Public-facing" in issue for issue in result.structural_issues
    )
    assert any(
        "docs/page.md:3:" in issue and "Internal-only" in issue
        for issue in result.structural_issues
    )
    assert any(
        "docs/page.yaml:1:" in issue and "Approved audience" in issue
        for issue in result.structural_issues
    )


def test_scan_consistency_collects_citistat_card_narrative_drift(tmp_path: Path) -> None:
    """The integrated scan must inspect the card source that held the original drift."""

    repo_root = tmp_path / "repo"
    docs_dir = repo_root / "docs"
    cards = docs_dir / "what-we-do" / "programs" / "citistat" / "index.cards.yml"
    cards.parent.mkdir(parents=True)
    cards.write_text('body: "The full agency portfolio: 19 agency briefs."\n', encoding="utf-8")

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert len(result.structural_issues) == 2
    assert all("index.cards.yml:1" in issue for issue in result.structural_issues)
    assert any("agency and thematic Stats" in issue for issue in result.structural_issues)


def test_scan_consistency_collects_an_unreadable_citistat_card_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A card-source IO failure should retain its path and cause."""

    repo_root = tmp_path / "repo"
    docs_dir = repo_root / "docs"
    cards = docs_dir / "what-we-do" / "programs" / "citistat" / "index.cards.yml"
    cards.parent.mkdir(parents=True)
    cards.touch()
    original_read_text = Path.read_text

    def fail_cards(path: Path, *, encoding: str) -> str:
        if path == cards:
            raise OSError("card read failed")
        return original_read_text(path, encoding=encoding)

    monkeypatch.setattr(Path, "read_text", fail_cards)

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result.structural_issues == (
        "docs/what-we-do/programs/citistat/index.cards.yml: "
        "unable to read card source: card read failed",
    )


def test_scan_consistency_collects_an_unreadable_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page read failure should be collected instead of raising a traceback."""

    repo_root = tmp_path / "repo"
    docs_dir = repo_root / "docs"
    page = docs_dir / "guide" / "page.md"
    page.parent.mkdir(parents=True)
    page.touch()
    original_read_text = Path.read_text

    def fail_page(path: Path, *, encoding: str) -> str:
        if path == page:
            raise OSError("read failed")
        return original_read_text(path, encoding=encoding)

    monkeypatch.setattr(Path, "read_text", fail_page)

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result.acronyms == ()
    assert result.structural_issues == (
        "docs/guide/page.md: unable to read Markdown source: read failed",
    )


def test_format_consistency_report_formats_clean_results() -> None:
    """A clean result should retain the established success output."""

    assert format_consistency_report(
        ConsistencyScan(structural_issues=(), acronyms=()),
        show_acronyms=False,
    ) == ("Consistency checks passed.", 0)


def test_format_consistency_report_formats_summary_and_structural_failure() -> None:
    """Hidden acronym details and hard findings should retain the established layout."""

    scan = ConsistencyScan(
        structural_issues=("docs/example.md: fixture failure",),
        acronyms=(("docs/a.md", "ABCD"), ("docs/b.md", "ABCD"), ("docs/b.md", "WXYZ")),
    )

    report, exit_code = format_consistency_report(scan, show_acronyms=False)

    assert exit_code == 1
    assert report == (
        "[consistency] 2 distinct possibly-undefined acronyms — "
        "run with --acronyms to list them.\n"
        "\n"
        "[consistency] 1 structural issue(s):\n"
        "  docs/example.md: fixture failure"
    )


def test_format_consistency_report_lists_acronyms_by_frequency() -> None:
    """The opt-in acronym report should sort by frequency and then token."""

    scan = ConsistencyScan(
        structural_issues=(),
        acronyms=(("docs/a.md", "WXYZ"), ("docs/b.md", "ABCD"), ("docs/c.md", "ABCD")),
    )

    report, exit_code = format_consistency_report(scan, show_acronyms=True)

    assert exit_code == 0
    assert report == (
        "[consistency] 2 distinct possibly-undefined acronym(s) "
        "(informational — add to the glossary or expand on first use):\n"
        "  ABCD (2 use(s))\n"
        "  WXYZ (1 use(s))\n"
        "Consistency checks passed."
    )


def test_main_reports_success_when_no_pages_have_findings(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The consistency CLI should return zero after a clean scan."""

    monkeypatch.setattr(
        consistency,
        "scan_consistency",
        lambda: ConsistencyScan(structural_issues=(), acronyms=()),
    )

    assert consistency_cli.main([]) == 0
    assert capsys.readouterr().out == "Consistency checks passed.\n"


def test_main_reports_structural_findings(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI should print structural evidence and return failure."""

    monkeypatch.setattr(
        consistency,
        "scan_consistency",
        lambda: ConsistencyScan(
            structural_issues=("docs/example/page.md: fixture failure",),
            acronyms=(),
        ),
    )

    assert consistency_cli.main([]) == 1
    assert capsys.readouterr().out == (
        "\n[consistency] 1 structural issue(s):\n  docs/example/page.md: fixture failure\n"
    )


def test_main_honors_the_short_acronym_flag(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The short flag should request the detailed informational report."""

    monkeypatch.setattr(
        consistency,
        "scan_consistency",
        lambda: ConsistencyScan(structural_issues=(), acronyms=(("docs/page.md", "ABCD"),)),
    )

    assert consistency_cli.main(["-a"]) == 0
    output = capsys.readouterr().out
    assert "ABCD (1 use(s))" in output
    assert output.endswith("Consistency checks passed.\n")


def test_main_reports_an_allowlist_load_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A glossary failure should become a concise CLI error."""

    def fail_scan() -> ConsistencyScan:
        raise RuntimeError("Unable to read acronym glossary")

    monkeypatch.setattr(consistency, "scan_consistency", fail_scan)

    assert consistency_cli.main([]) == 1
    assert capsys.readouterr().out == "[consistency] Unable to read acronym glossary\n"
