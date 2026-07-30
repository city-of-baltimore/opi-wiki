"""Tests for repository-local links in root product contracts."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.product_contract_links import (
    find_product_contract_link_issues,
)


def _write_markdown_configuration(repo_root: Path) -> None:
    """Create the smallest fixture that preserves production link semantics."""

    (repo_root / "docs").mkdir()
    (repo_root / "mkdocs.yml").write_text(
        "site_name: Product contract test\n"
        "plugins: []\n"
        "markdown_extensions:\n"
        "  - attr_list\n"
        "  - tables\n"
        "  - toc\n"
        "  - pymdownx.superfences\n",
        encoding="utf-8",
    )


def test_product_contract_links_accept_files_directories_and_heading_fragments(
    tmp_path: Path,
) -> None:
    """The configured renderer should authorize valid targets and fragments."""

    _write_markdown_configuration(tmp_path)
    product_dir = tmp_path / "product"
    product_dir.mkdir()
    (tmp_path / "README.md").write_text("# Repository\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (product_dir / "target.md").write_text(
        "# Target\n\n"
        "## Open decisions\n\n"
        "## Repeated heading\n\n"
        "## Repeated heading\n\n"
        "## Use `task ci`\n\n"
        "## Custom fragment {#chosen-id}\n",
        encoding="utf-8",
    )
    (product_dir / "README.md").write_text(
        "# Product contracts\n\n"
        "[Target](target.md#open-decisions)\n"
        "[Duplicate](target.md#repeated-heading_1)\n"
        "[Repository](../README.md)\n"
        "[Tools](../scripts/)\n"
        "[Inline code heading](target.md#use-task-ci)\n"
        "[Custom heading](target.md#chosen-id)\n"
        "[Reference][target]\n"
        "[target]: target.md#open-decisions\n"
        "[External](https://example.org/not-checked)\n"
        "[Broken](missing.md) `but [inline code](another-missing.md)`\n"
        "```markdown\n"
        "[Fenced example](missing.md)\n"
        "```\n",
        encoding="utf-8",
    )

    issues = find_product_contract_link_issues(tmp_path)

    assert issues == [
        "product/README.md:12: relative link target does not exist 'missing.md' "
        "(resolved to 'product/missing.md')"
    ]


def test_product_contract_links_report_missing_fragment_and_escape_with_lines(
    tmp_path: Path,
) -> None:
    """Every broken target should name its contract, line, and correction seam."""

    _write_markdown_configuration(tmp_path)
    product_dir = tmp_path / "product"
    product_dir.mkdir()
    (product_dir / "target.md").write_text("# Existing heading\n", encoding="utf-8")
    (product_dir / "README.md").write_text(
        "# Contracts\n"
        "[Missing](missing.md)\n"
        "![Missing image](missing.png)\n"
        "[Missing reference][missing-ref]\n"
        "[Bad heading](target.md#missing-heading)\n"
        "[Escape](../../outside.md)\n"
        "[Unsafe](..\\outside.md)\n"
        "\n"
        "[missing-ref]: absent-via-ref.md\n",
        encoding="utf-8",
    )

    issues = find_product_contract_link_issues(tmp_path)

    assert issues == [
        "product/README.md:2: relative link target does not exist 'missing.md' "
        "(resolved to 'product/missing.md')",
        "product/README.md:3: relative link target does not exist 'missing.png' "
        "(resolved to 'product/missing.png')",
        "product/README.md:9: relative link target does not exist 'absent-via-ref.md' "
        "(resolved to 'product/absent-via-ref.md')",
        "product/README.md:5: Markdown heading fragment '#missing-heading' was not found "
        "in 'product/target.md'",
        "product/README.md:6: relative link escapes repository root '../../outside.md'",
        "product/README.md:7: unsafe relative link target '..\\\\outside.md'",
    ]


def test_product_contract_links_fail_closed_without_contract_sources(tmp_path: Path) -> None:
    """A missing or empty product contract surface must not pass vacuously."""

    assert find_product_contract_link_issues(tmp_path) == [
        "product: product contract directory was not found"
    ]

    (tmp_path / "product").mkdir()

    assert find_product_contract_link_issues(tmp_path) == [
        "product: no Markdown product contracts were found"
    ]


def test_nested_product_contracts_cannot_bypass_the_ratchet(tmp_path: Path) -> None:
    """A future nested contract should receive the same rendered-link validation."""

    _write_markdown_configuration(tmp_path)
    nested_dir = tmp_path / "product" / "decisions"
    nested_dir.mkdir(parents=True)
    (nested_dir / "record.md").write_text(
        "# Decision\n\n[Missing](missing.md)\n",
        encoding="utf-8",
    )

    assert find_product_contract_link_issues(tmp_path) == [
        "product/decisions/record.md:3: relative link target does not exist 'missing.md' "
        "(resolved to 'product/decisions/missing.md')"
    ]
