"""Lightweight accessibility smoke checks for generated site HTML."""

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


@dataclass
class _DetailsBlock:
    """Relevant content captured from one details element."""

    index: int
    summary_seen: bool = False
    summary_text: list[str] = field(default_factory=list)


@dataclass
class _Card:
    """Relevant content captured from one shared card article."""

    index: int
    link_text: list[list[str]] = field(default_factory=list)


@dataclass
class _Heading:
    """Text captured from one first-level heading."""

    text: list[str] = field(default_factory=list)


@dataclass
class _OrgChartNode:
    """Public leadership node captured from the semantic org chart."""

    level: str
    name: list[str] = field(default_factory=list)


@dataclass
class _OrgChart:
    """Accessible content captured from one public leadership chart."""

    index: int
    caption_seen: bool = False
    caption_text: list[str] = field(default_factory=list)
    nodes: list[_OrgChartNode] = field(default_factory=list)


class _AccessibilityParser(HTMLParser):
    """Capture accessibility invariants from semantic generated markup."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.details: list[_DetailsBlock] = []
        self.cards: list[_Card] = []
        self.headings: list[_Heading] = []
        self.org_charts: list[_OrgChart] = []
        self._details_stack: list[_DetailsBlock] = []
        self._summary_stack: list[_DetailsBlock] = []
        self._card_stack: list[_Card] = []
        self._card_link_stack: list[list[str]] = []
        self._heading_stack: list[_Heading] = []
        self._org_chart_stack: list[_OrgChart] = []
        self._org_caption_stack: list[_OrgChart] = []
        self._org_node_stack: list[_OrgChartNode] = []
        self._org_name_stack: list[_OrgChartNode] = []

    @staticmethod
    def _classes(attributes: list[tuple[str, str | None]]) -> set[str]:
        """Return the whitespace-delimited class tokens from attributes."""

        return {
            token
            for name, value in attributes
            if name == "class" and value is not None
            for token in value.split()
        }

    @staticmethod
    def _attribute(attributes: list[tuple[str, str | None]], name: str) -> str:
        """Return one string attribute value, or an empty string when absent."""

        return next((value or "" for key, value in attributes if key == name), "")

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Start capturing relevant semantic elements."""

        classes = self._classes(attrs)
        if tag == "details":
            block = _DetailsBlock(index=len(self.details) + 1)
            self.details.append(block)
            self._details_stack.append(block)
        elif tag == "summary" and self._details_stack:
            block = self._details_stack[-1]
            block.summary_seen = True
            self._summary_stack.append(block)

        if tag == "article" and "opi-card" in classes:
            card = _Card(index=len(self.cards) + 1)
            self.cards.append(card)
            self._card_stack.append(card)
        elif tag == "a" and "opi-card-link" in classes and self._card_stack:
            link_text: list[str] = []
            self._card_stack[-1].link_text.append(link_text)
            self._card_link_stack.append(link_text)

        if tag == "h1":
            heading = _Heading()
            self.headings.append(heading)
            self._heading_stack.append(heading)

        if tag == "figure" and "opi-org-chart" in classes:
            chart = _OrgChart(index=len(self.org_charts) + 1)
            self.org_charts.append(chart)
            self._org_chart_stack.append(chart)
        elif tag == "figcaption" and "opi-org-chart__caption" in classes and self._org_chart_stack:
            chart = self._org_chart_stack[-1]
            chart.caption_seen = True
            self._org_caption_stack.append(chart)

        if "opi-org-chart__node" in classes and self._org_chart_stack:
            node = _OrgChartNode(level=self._attribute(attrs, "data-org-level"))
            self._org_chart_stack[-1].nodes.append(node)
            self._org_node_stack.append(node)
        elif "opi-org-chart__name" in classes and self._org_node_stack:
            self._org_name_stack.append(self._org_node_stack[-1])

    def handle_endtag(self, tag: str) -> None:
        """Stop capturing a relevant semantic element."""

        if tag == "summary" and self._summary_stack:
            self._summary_stack.pop()
        elif tag == "details" and self._details_stack:
            self._details_stack.pop()

        if tag == "a" and self._card_link_stack:
            self._card_link_stack.pop()
        elif tag == "article" and self._card_stack:
            self._card_stack.pop()

        if tag == "h1" and self._heading_stack:
            self._heading_stack.pop()

        if tag == "strong" and self._org_name_stack:
            self._org_name_stack.pop()
        elif tag == "div" and self._org_node_stack:
            self._org_node_stack.pop()

        if tag == "figcaption" and self._org_caption_stack:
            self._org_caption_stack.pop()
        elif tag == "figure" and self._org_chart_stack:
            self._org_chart_stack.pop()

    def handle_data(self, data: str) -> None:
        """Capture visible text inside relevant elements."""

        if self._summary_stack:
            self._summary_stack[-1].summary_text.append(data)
        if self._card_link_stack:
            self._card_link_stack[-1].append(data)
        if self._heading_stack:
            self._heading_stack[-1].text.append(data)
        if self._org_caption_stack:
            self._org_caption_stack[-1].caption_text.append(data)
        if self._org_name_stack:
            self._org_name_stack[-1].name.append(data)


def _has_visible_text(chunks: list[str]) -> bool:
    """Return whether captured HTML text contains non-whitespace content."""

    return bool("".join(chunks).strip())


def find_accessibility_issues(site_dir: Path) -> list[str]:
    """Return basic accessibility issues from generated site HTML."""

    issues: list[str] = []

    for html_file in sorted(site_dir.rglob("*.html")):
        try:
            html = html_file.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Unable to read built HTML file: {html_file}") from error

        relative_file = html_file.relative_to(site_dir)
        parser = _AccessibilityParser()
        parser.feed(html)
        parser.close()

        for details_block in parser.details:
            if not details_block.summary_seen or not _has_visible_text(details_block.summary_text):
                issues.append(
                    f"{relative_file}: details block #{details_block.index} "
                    "is missing a summary label"
                )

        for card in parser.cards:
            for link_text in card.link_text:
                if not _has_visible_text(link_text):
                    issues.append(
                        f"{relative_file}: card #{card.index} is missing visible link text"
                    )

        meaningful_headings = [
            heading for heading in parser.headings if _has_visible_text(heading.text)
        ]
        if len(meaningful_headings) > 1:
            issues.append(
                f"{relative_file}: page has {len(meaningful_headings)} visible h1 headings; "
                "expected at most one"
            )

        if relative_file == Path("how-we-work/organization/org-structure/index.html"):
            if len(parser.org_charts) != 1:
                issues.append(
                    f"{relative_file}: expected one semantic public leadership chart, "
                    f"found {len(parser.org_charts)}"
                )
                continue

            chart = parser.org_charts[0]
            if not chart.caption_seen or not _has_visible_text(chart.caption_text):
                issues.append(f"{relative_file}: public leadership chart is missing its caption")

            levels = [node.level for node in chart.nodes]
            # The chart is the reporting spine only (City Administrator ->
            # Executive Director); teams and reports live in the adjacent table.
            expected_counts = {"city": 1, "executive": 1}
            for level, expected_count in expected_counts.items():
                actual_count = levels.count(level)
                if actual_count != expected_count:
                    issues.append(
                        f"{relative_file}: public leadership chart has {actual_count} "
                        f"'{level}' nodes; expected {expected_count}"
                    )

            empty_names = [
                index
                for index, node in enumerate(chart.nodes, start=1)
                if not _has_visible_text(node.name)
            ]
            for index in empty_names:
                issues.append(
                    f"{relative_file}: public leadership chart node #{index} "
                    "is missing a visible name"
                )

    return issues
