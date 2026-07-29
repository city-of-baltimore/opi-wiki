"""Tests for the retired visibility-label ratchet."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.visibility_labels import (
    check_visibility_labels,
    find_visibility_label_issues,
)
from tests.git_fixtures import init_git_repo


def test_visibility_label_check_accepts_domain_language(tmp_path: Path) -> None:
    """The one-source checker should accept a governed-data sentence."""

    path = tmp_path / "docs" / "page.md"

    assert (
        check_visibility_labels(
            path,
            "Approved users work from approved data for public safety. "
            "The website documents internal controls, and the wiki explains public records.",
            repo_root=tmp_path,
        )
        == []
    )


def test_visibility_label_check_preserves_approved_review_action(tmp_path: Path) -> None:
    """A named actor followed by the verb approved is not a status label."""

    assert (
        check_visibility_labels(
            tmp_path / "README.md",
            "The Board approved guidance on grants.\n",
            repo_root=tmp_path,
        )
        == []
    )


def test_visibility_label_check_rejects_internal_facing_documentation(
    tmp_path: Path,
) -> None:
    """Internal-facing documentation must use a concrete reader or City system."""

    issues = check_visibility_labels(
        tmp_path / "README.md",
        "Use the internal-facing documentation.\n",
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert "internal-facing documentation" in issues[0]


def test_visibility_label_check_rejects_a_retired_phrase(tmp_path: Path) -> None:
    """The one-source checker should return exact line evidence."""

    path = tmp_path / "README.md"

    assert check_visibility_labels(
        path,
        "# Site\n\nA public-facing reference.\n",
        repo_root=tmp_path,
    ) == [
        "README.md:3:3: retired visibility label 'public-facing reference'; "
        "name the reader, review, or concrete data rule instead"
    ]


@pytest.mark.parametrize(
    "label",
    (
        "Public MkDocs site",
        "public effect",
        "public roster",
        "public operating model",
        "public template pages",
        "public summaries",
        "internal copy",
        "approved version",
        "publication posture",
        "public/private boundaries must stay explicit",
        "internal-only content",
        "public sites",
        "public repositories",
        "public-facing repositories",
        "public-facing sites",
        "internal-only repositories",
        "internal-only sites",
        "approved versions",
        "approved labels",
        "internal copies",
        "public website",
        "public wiki",
        "public documentation",
        "public-facing documentation",
        "internal website",
        "approved documentation",
    ),
)
def test_visibility_label_check_rejects_each_removed_family_once(
    tmp_path: Path,
    label: str,
) -> None:
    """Corpus-derived retired labels should produce one actionable diagnostic."""

    issues = check_visibility_labels(
        tmp_path / "README.md",
        f"{label}.\n",
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert f"retired visibility label '{label}'" in issues[0]


@pytest.mark.parametrize(
    ("text", "expected_label", "expected_line"),
    (
        ("Intro.\n\nPublic\nMkDocs site.\n", "Public MkDocs site", 3),
        ("public\u00a0site\n", "public site", 1),
        ("public\u2011site\n", "public-site", 1),
        ("public\u2015site\n", "public-site", 1),
        ("public\u2011facing copy\n", "public-facing copy", 1),
        ("public \u2014 facing reference\n", "public - facing reference", 1),
        ("internal\nworking materials\n", "internal working materials", 1),
        ("approved\nversion\n", "approved version", 1),
    ),
)
def test_visibility_label_check_normalizes_authored_separators(
    tmp_path: Path,
    text: str,
    expected_label: str,
    expected_line: int,
) -> None:
    """Line wrapping and Unicode separators must not bypass the ratchet."""

    issues = check_visibility_labels(
        tmp_path / "README.md",
        text,
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert issues[0].startswith(f"README.md:{expected_line}:")
    assert f"retired visibility label '{expected_label}'" in issues[0]


def test_visibility_label_check_preserves_markdown_paragraph_boundaries(
    tmp_path: Path,
) -> None:
    """Separate paragraphs must not be joined into a synthetic label."""

    for text in ("Public\n\nsite\n", "Public\n \nsite\n", "Public\u2029site\n"):
        assert (
            check_visibility_labels(
                tmp_path / "README.md",
                text,
                repo_root=tmp_path,
            )
            == []
        )


@pytest.mark.parametrize(
    ("relative_path", "text"),
    (
        (Path("config.yml"), "access: approved\nversion: 2026\n"),
        (Path("mkdocs.yml"), "tier: public\nsite: opi\n"),
        (Path("README.md"), "- public\n- site\n"),
    ),
)
def test_visibility_label_check_preserves_structural_record_boundaries(
    tmp_path: Path,
    relative_path: Path,
    text: str,
) -> None:
    """Separate YAML fields and Markdown list items must not become phrases."""

    assert (
        check_visibility_labels(
            tmp_path / relative_path,
            text,
            repo_root=tmp_path,
        )
        == []
    )


@pytest.mark.parametrize(
    ("text", "expected_label"),
    (
        ("summary: >\n  public\n  site\n", "public site"),
        ('summary: "approved\n  version"\n', "approved version"),
    ),
)
def test_visibility_label_check_reads_semantic_multiline_yaml_scalars(
    tmp_path: Path,
    text: str,
    expected_label: str,
) -> None:
    """A real multi-line YAML value must retain its folded text semantics."""

    issues = check_visibility_labels(
        tmp_path / "config.yml",
        text,
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert expected_label in issues[0]


@pytest.mark.parametrize(
    ("relative_path", "text"),
    (
        (Path("README.md"), "public site; public site\n"),
        (Path("README.md"), "_public site_; public site\n"),
        (Path("config.yml"), 'summary: "public site public site"\n'),
    ),
)
def test_distinct_same_line_occurrences_keep_distinct_column_evidence(
    tmp_path: Path,
    relative_path: Path,
    text: str,
) -> None:
    """Raw/decoded overlap should dedupe without hiding separate occurrences."""

    issues = check_visibility_labels(
        tmp_path / relative_path,
        text,
        repo_root=tmp_path,
    )

    assert len(issues) == 2
    assert issues[0] != issues[1]
    assert all("retired visibility label 'public site'" in issue for issue in issues)


@pytest.mark.parametrize(
    ("text", "expected_label"),
    (
        ("_public site_\n", "public site"),
        ("__approved versions__\n", "approved versions"),
        ("___publication posture___\n", "publication posture"),
    ),
)
def test_visibility_label_check_handles_underscore_emphasis(
    tmp_path: Path,
    text: str,
    expected_label: str,
) -> None:
    """Markdown emphasis must not turn a retired phrase into a false negative."""

    issues = check_visibility_labels(
        tmp_path / "README.md",
        text,
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert f"retired visibility label '{expected_label}'" in issues[0]


@pytest.mark.parametrize(
    ("relative_path", "text", "expected_label"),
    (
        (Path("README.md"), "Use the public **site**.\n", "public site"),
        (Path("README.md"), "Use the *public* site.\n", "public site"),
        (
            Path("docs/how-we-work/handbook/notes.md"),
            "Use the internal [documentation](guide.md).\n",
            "internal documentation",
        ),
        (
            Path("overrides/partials/note.html"),
            "Use the approved <em>version</em>.\n",
            "approved version",
        ),
        (
            Path(".github/ISSUE_TEMPLATE/help.yml"),
            'description: "Use the public **site**."\n',
            "public site",
        ),
        (Path("README.md"), "Use the public&nbsp;site.\n", "public site"),
    ),
)
def test_source_only_lexical_projection_closes_inline_markup_bypasses(
    tmp_path: Path,
    relative_path: Path,
    text: str,
    expected_label: str,
) -> None:
    """Source-only prose must not hide retired labels behind bounded syntax."""

    issues = check_visibility_labels(
        tmp_path / relative_path,
        text,
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert expected_label in issues[0]


def test_source_lexical_projection_preserves_domain_markup(tmp_path: Path) -> None:
    """Inline syntax must not turn legitimate civic meanings into labels."""

    assert (
        check_visibility_labels(
            tmp_path / "README.md",
            "The <em>website</em> explains public **records** to approved "
            "[users](users.md) under internal *controls*.\n",
            repo_root=tmp_path,
        )
        == []
    )


def test_canonical_markdown_defers_markup_semantics_to_built_html(tmp_path: Path) -> None:
    """Published Markdown keeps generated HTML as its semantic authority."""

    assert (
        check_visibility_labels(
            tmp_path / "docs" / "page.md",
            "Use the public **site**.\n",
            repo_root=tmp_path,
        )
        == []
    )


def test_visibility_label_check_counts_non_lf_source_lines(tmp_path: Path) -> None:
    """Line evidence must follow every line break the normalizer accepts."""

    assert check_visibility_labels(
        tmp_path / "README.md",
        "Intro.\rPublic\rMkDocs site.\r",
        repo_root=tmp_path,
    ) == [
        "README.md:2:1: retired visibility label 'Public MkDocs site'; "
        "name the reader, review, or concrete data rule instead"
    ]


def test_visibility_labels_accept_required_domain_language(tmp_path: Path) -> None:
    """Civic, legal, operational, and compatibility meanings must remain valid."""

    init_git_repo(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "page.md").write_text(
        "# Data governance\n\n"
        "The Public Innovation Toolkit supports public safety, public service, and "
        "public trust. Internal Stat and Internal Services are formal operating terms. "
        "Built-site internal links stay local. Public data may be used by approved "
        "users from approved sources. The tier is Public | Approved for publication. "
        "A Justfile may contain [private]. Public\u00a0safety and approved\u00a0users "
        "remain ordinary terms. A public-facing service must meet accessibility "
        "requirements. The public/private boundary controls disclosure. Activate an "
        "employee badge; .opi-pillar and .opi-pillow are unrelated component names. "
        "Public/private boundaries for publication define release access. "
        "Download [the brief](public-brief.pdf).\n",
        encoding="utf-8",
    )
    (tmp_path / "mkdocs.yml").write_text(
        "redirect_maps:\n  public/legacy-public-brief.md: index.md\n  public-brief.md: index.md\n",
        encoding="utf-8",
    )

    assert find_visibility_label_issues(tmp_path, docs_dir) == []


def test_product_templates_accept_required_domain_language(tmp_path: Path) -> None:
    """Template prose must retain civic-service and data-governance meanings."""

    path = tmp_path / "overrides" / "main.html"
    text = (
        "<p>A public-facing service must meet accessibility requirements. "
        "The public/private boundary controls disclosure for an internal-only dataset.</p>"
        "<code>some_public-site some_public_site</code>"
    )

    assert check_visibility_labels(path, text, repo_root=tmp_path) == []


@pytest.mark.parametrize(
    ("relative_path", "text", "expected_label"),
    (
        (Path("overrides/main.html"), "<!-- internal-only content -->", "internal-only content"),
        (
            Path("docs/assets/stylesheets/components.css"),
            "/* publication posture */",
            "publication posture",
        ),
        (Path("mkdocs.yml"), "description: public-facing wiki", "public-facing wiki"),
    ),
)
def test_repository_state_language_is_retired_across_authored_source_types(
    tmp_path: Path,
    relative_path: Path,
    text: str,
    expected_label: str,
) -> None:
    """Semantic retired phrases must not depend on a source's location or format."""

    issues = check_visibility_labels(
        tmp_path / relative_path,
        text,
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert expected_label in issues[0]


@pytest.mark.parametrize(
    ("relative_path", "text", "expected_label"),
    (
        (Path("docs/page.md"), '{{ badge("reference") }}\n', "{{ badge("),
        (Path("docs/page.md"), '{{- badge("reference") }}\n', "{{- badge("),
        (Path("docs/page.md"), '{{+ badge("reference") }}\n', "{{+ badge("),
        (Path("docs/assets/stylesheets/components.css"), ".opi-pill { color: red; }\n", "opi-pill"),
        (
            Path("docs/assets/stylesheets/components.css"),
            ".opi-pill__label { color: red; }\n",
            "opi-pill",
        ),
        (Path("overrides/main.html"), '<span class="opi-pill">Reference</span>\n', "opi-pill"),
    ),
)
def test_visibility_label_check_rejects_retired_presentation_paths_once(
    tmp_path: Path,
    relative_path: Path,
    text: str,
    expected_label: str,
) -> None:
    """Each retired rendering path should produce one actionable finding."""

    issues = check_visibility_labels(
        tmp_path / relative_path,
        text,
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert expected_label in issues[0]
