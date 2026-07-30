"""Validate repository-local links in root product contracts."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from typing import cast
from urllib.parse import unquote, urlsplit

# Python-Markdown does not publish typing metadata; it is the canonical renderer here.
import markdown  # type: ignore[import-untyped]
from mkdocs.config import load_config

_REQUIRED_RENDER_EXTENSIONS = frozenset({"attr_list", "tables", "toc", "pymdownx.superfences"})
_UNSAFE_PATH_CHARACTER = re.compile(r"[\x00-\x1f\x7f]")


@dataclass(frozen=True, slots=True)
class _RenderedDocument:
    """References and element IDs produced by the configured Markdown renderer."""

    source: str
    targets: tuple[str, ...]
    element_ids: frozenset[str]


class _RenderedContractParser(HTMLParser):
    """Collect link targets, image targets, and fragment authorities from HTML."""

    def __init__(self) -> None:
        """Initialize empty rendered-semantic collections."""

        super().__init__(convert_charrefs=True)
        self.targets: list[str] = []
        self.element_ids: set[str] = set()

    def _record(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record relevant attributes from one rendered element."""

        attributes = {name.casefold(): value for name, value in attrs}
        element_id = attributes.get("id")
        if element_id:
            self.element_ids.add(element_id)

        target_attribute = {"a": "href", "img": "src"}.get(tag.casefold())
        if target_attribute is None:
            return
        target = attributes.get(target_attribute)
        if target is not None:
            self.targets.append(target.strip())

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record ordinary start tags."""

        self._record(tag, attrs)

    def handle_startendtag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record self-closing elements such as rendered images."""

        self._record(tag, attrs)


@cache
def _markdown_configuration(
    config_path: Path,
) -> tuple[tuple[str, ...], dict[str, dict[str, object]]]:
    """Load the live Markdown extension stack instead of copying its semantics."""

    try:
        config = load_config(config_file=str(config_path))
    # MkDocs and third-party plugins raise heterogeneous exceptions while loading.
    except Exception as error:  # noqa: BLE001
        raise RuntimeError(f"Unable to load Markdown configuration: {config_path}") from error

    extensions = tuple(str(name) for name in config["markdown_extensions"])
    missing = sorted(_REQUIRED_RENDER_EXTENSIONS.difference(extensions))
    if missing:
        missing_list = ", ".join(missing)
        raise RuntimeError(
            f"Markdown configuration is missing required link semantics: {missing_list}"
        )
    extension_configs = cast(
        dict[str, dict[str, object]],
        dict(config["mdx_configs"] or {}),
    )
    return extensions, extension_configs


def _read_markdown(path: Path) -> str:
    """Read one UTF-8 Markdown source with contextual failures."""

    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise RuntimeError(f"Unable to read product contract: {path}") from error


def _render_document(path: Path, config_path: Path) -> _RenderedDocument:
    """Render one source with the production Markdown dialect and inspect its HTML."""

    source = _read_markdown(path)
    extensions, extension_configs = _markdown_configuration(config_path)
    try:
        rendered = markdown.Markdown(
            extensions=extensions,
            extension_configs=extension_configs,
        ).convert(source)
        parser = _RenderedContractParser()
        parser.feed(rendered)
        parser.close()
    # Markdown extensions and HTMLParser can raise heterogeneous parsing errors.
    except Exception as error:  # noqa: BLE001
        raise RuntimeError(f"Unable to render product contract: {path}") from error

    return _RenderedDocument(
        source=source,
        targets=tuple(parser.targets),
        element_ids=frozenset(parser.element_ids),
    )


def _repository_relative(path: Path, repo_root: Path) -> str:
    """Return a stable repository-relative display path."""

    return path.relative_to(repo_root).as_posix()


def _source_line_number(source: str, rendered_target: str) -> int:
    """Locate a rendered target in source for an actionable diagnostic."""

    normalized_target = unquote(html.unescape(rendered_target))
    if normalized_target:
        for line_number, line in enumerate(source.splitlines(), start=1):
            if rendered_target in line:
                return line_number
            if normalized_target in unquote(html.unescape(line)):
                return line_number
    return 1


def _fragment_target(path: Path) -> Path | None:
    """Return the Markdown source that owns fragments for one resolved target."""

    if path.is_file() and path.suffix.casefold() == ".md":
        return path
    if not path.is_dir():
        return None
    for name in ("index.md", "README.md"):
        candidate = path / name
        if candidate.is_file():
            return candidate
    return None


def find_product_contract_link_issues(repo_root: Path) -> list[str]:
    """Return unsafe, missing, or fragment-invalid links in ``product/*.md``."""

    resolved_root = repo_root.resolve()
    product_dir = resolved_root / "product"
    if not product_dir.is_dir():
        return ["product: product contract directory was not found"]

    sources = tuple(sorted(path for path in product_dir.rglob("*.md") if path.is_file()))
    if not sources:
        return ["product: no Markdown product contracts were found"]

    config_path = resolved_root / "mkdocs.yml"
    rendered_cache: dict[Path, _RenderedDocument] = {}

    def rendered_document(path: Path) -> _RenderedDocument:
        if path not in rendered_cache:
            rendered_cache[path] = _render_document(path, config_path)
        return rendered_cache[path]

    issues: list[str] = []
    for source in sources:
        document = rendered_document(source)
        source_label = _repository_relative(source, resolved_root)
        for target in document.targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith("//"):
                continue

            line_number = _source_line_number(document.source, target)
            decoded_path = unquote(parsed.path)
            if "\\" in decoded_path or _UNSAFE_PATH_CHARACTER.search(decoded_path):
                issues.append(
                    f"{source_label}:{line_number}: unsafe relative link target {target!r}"
                )
                continue

            target_path = source if not decoded_path else source.parent / decoded_path
            resolved_target = target_path.resolve()
            if not resolved_target.is_relative_to(resolved_root):
                issues.append(
                    f"{source_label}:{line_number}: relative link escapes repository root "
                    f"{target!r}"
                )
                continue
            if not resolved_target.exists():
                target_label = _repository_relative(resolved_target, resolved_root)
                issues.append(
                    f"{source_label}:{line_number}: relative link target does not exist "
                    f"{target!r} (resolved to {target_label!r})"
                )
                continue

            if not parsed.fragment:
                continue
            markdown_target = _fragment_target(resolved_target)
            if markdown_target is None:
                continue
            fragment = unquote(parsed.fragment)
            if fragment not in rendered_document(markdown_target).element_ids:
                target_label = _repository_relative(markdown_target, resolved_root)
                issues.append(
                    f"{source_label}:{line_number}: Markdown heading fragment "
                    f"'#{fragment}' was not found in {target_label!r}"
                )

    return issues
