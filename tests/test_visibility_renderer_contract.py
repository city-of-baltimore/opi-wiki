"""Differential visibility-policy tests against the configured Markdown renderer."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import markdown
import pytest
from mkdocs.config import load_config
from scripts.repo_tools.rendered_text import RenderedTextError, project_rendered_content
from scripts.repo_tools.visibility_policy import find_visibility_label_matches

REPO_ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=1)
def _markdown_configuration() -> tuple[tuple[str, ...], dict[str, object]]:
    """Load the production extension names and settings without duplicating them."""

    config = load_config(config_file=str(REPO_ROOT / "mkdocs.yml"))
    return tuple(config["markdown_extensions"]), dict(config["mdx_configs"] or {})


def _render_projection(source: str) -> str:
    """Render one fixture with the production dialect and project its page content."""

    extensions, extension_configs = _markdown_configuration()
    renderer = markdown.Markdown(
        extensions=extensions,
        extension_configs=extension_configs,
    )
    page_html = (
        f'<article class="md-content__inner md-typeset">{renderer.convert(source)}</article>'
    )
    return project_rendered_content(page_html).text


@pytest.mark.parametrize(
    "source",
    (
        "public **site**",
        "public **website**",
        "public [wiki](guide.md)",
        "public <em>documentation</em>",
        "public-*facing* documentation",
        "internal **website**",
        "approved <em>documentation</em>",
        "approved *version*",
        "public _site_",
        "internal _working_ materials",
        "public-*facing* copy",
        "[public site](guide.md)",
        "Read the public [site](guide.md).",
        "[public](one.md) [site](two.md)",
        "[public][a] [site][b]\n\n[a]: /a\n[b]: /b",
        "public ==site==",
        "public ~~site~~",
        "public ^^site^^",
        "public&nbsp;site",
        "public&#160;site",
        "public&hyphen;site",
        "public <!-- harmless --> site",
        "public <!-- harmless > still comment --> site",
        'public <span title="context">site</span>',
        "public<br>site",
        "*public*{.x} site",
        "[public](x){.x} site",
        "public ++s++ite",
        'public ++"site"++',
        "public `#!text s`ite",
        "public ++s++{.x}ite",
        "public `s`{.x}ite",
        '[public](x "title)") site',
        '[public](x "title ( test") site',
        "literal < unmatched\n\npublic <strong>site</strong>",
    ),
)
def test_configured_renderer_cannot_hide_a_retired_label(source: str) -> None:
    """Every phrase produced by valid configured syntax must reach the policy."""

    rendered_text = _render_projection(source)

    assert find_visibility_label_matches(rendered_text)


@pytest.mark.parametrize(
    "source",
    (
        "The **website** publishes public data for approved users.",
        "The documentation describes internal controls and approved access.",
        "The [wiki](guide.md) explains public records disclosure requirements.",
    ),
)
def test_configured_renderer_preserves_legitimate_surface_and_domain_language(
    source: str,
) -> None:
    """Rendering must not turn legitimate civic and governance prose into a label."""

    assert find_visibility_label_matches(_render_projection(source)) == ()


def test_configured_renderer_preserves_approved_review_action() -> None:
    """Rendered civic prose must retain approved as a past-tense review action."""

    assert (
        find_visibility_label_matches(
            _render_projection("The Board approved **guidance** on grants.")
        )
        == ()
    )


def test_configured_renderer_rejects_internal_facing_documentation() -> None:
    """Inline rendering cannot hide the internal-facing repository posture."""

    assert find_visibility_label_matches(
        _render_projection("Use the internal-*facing* documentation.")
    )


@pytest.mark.parametrize(
    "source",
    (
        "public == site ==",
        "public ~~ site ~~",
        "public ^^ site ^^",
        "public ++site++",
        "++public++ site",
        "`public **site**`",
        "~~~html\npublic <strong>site</strong>\n~~~",
        "> ~~~html\n> public <strong>site</strong>\n> ~~~",
        "    public <strong>site</strong>",
        "[guide](public-site)",
        "Public_Purpose",
        r"public \*\*site\*\*",
        "public_*facing*",
        "# Public\nsite",
        "Public\n# site",
        "public\n> site",
        "public\n<div>site</div>",
    ),
)
def test_configured_renderer_does_not_join_literal_or_separate_text(source: str) -> None:
    """Literal syntax and distinct rendered blocks must not create a policy match."""

    rendered_text = _render_projection(source)

    assert find_visibility_label_matches(rendered_text) == ()


@pytest.mark.parametrize(
    "source",
    (
        "public\n    **site**\n",
        "public\n    <strong>site</strong>\n",
        "- public\n    **site**\n",
        "> public\n    **site**\n",
    ),
)
def test_configured_renderer_keeps_four_indented_prose_continuations(
    source: str,
) -> None:
    """Indentation within prose must not create a false code boundary."""

    assert find_visibility_label_matches(_render_projection(source))


@pytest.mark.parametrize(
    "source",
    (
        "> public\nsite\n",
        "> public\n> site\n",
        ">> public\n> site\n",
    ),
)
def test_configured_renderer_keeps_three_lazy_blockquote_continuations(
    source: str,
) -> None:
    """All configured lazy blockquote forms should remain one rendered phrase."""

    assert find_visibility_label_matches(_render_projection(source))


@pytest.mark.parametrize(
    "source",
    (
        "> public\n>> site\n",
        "> public\n> > site\n",
    ),
)
def test_configured_renderer_separates_nested_blockquote_blocks(source: str) -> None:
    """Increasing quote depth creates a hard semantic block boundary."""

    assert find_visibility_label_matches(_render_projection(source)) == ()


@pytest.mark.parametrize(
    "source",
    (
        "[public] [site]\n\n~~~\n[public]: /x\n[site]: /y\n~~~\n",
        "[public] [site]\n\n> ~~~\n> [public]: /x\n> [site]: /y\n> ~~~\n",
        "[public] [site]\n\n<!--\n[public]: /x\n[site]: /y\n-->\n",
    ),
)
def test_hidden_reference_definitions_cannot_change_visible_link_semantics(
    source: str,
) -> None:
    """Code and comments must not resolve otherwise literal reference labels."""

    assert find_visibility_label_matches(_render_projection(source)) == ()


def test_configured_renderer_projects_image_alt_text() -> None:
    """Reader-facing image alternatives participate in rendered policy checks."""

    assert find_visibility_label_matches(_render_projection("![public site](image.png)"))


def test_configured_renderer_fails_closed_on_malformed_quoted_tag_output() -> None:
    """A quoted greater-than edge case must fail rather than weaken the ratchet."""

    with pytest.raises(RenderedTextError, match="malformed content region"):
        _render_projection('public <span title=">">site</span>')


def test_renderer_contract_reads_the_live_mkdocs_extension_configuration() -> None:
    """The differential oracle must use the production dialect, not a copied list."""

    extensions, extension_configs = _markdown_configuration()

    assert "attr_list" in extensions
    assert "pymdownx.keys" in extensions
    assert "pymdownx.superfences" in extensions
    assert extension_configs["pymdownx.highlight"] == {
        "anchor_linenums": True,
        "line_spans": "__span",
        "pygments_lang_class": True,
    }
