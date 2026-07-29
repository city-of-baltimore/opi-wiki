"""Stable pages and selectors exercised by the browser smoke suite."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BrowserSmokeTarget:
    """A representative docs page for browser-level smoke checks."""

    section: str
    path: str
    active_link_text: str


SMOKE_TARGETS = (
    BrowserSmokeTarget(
        "About Us",
        "/about-us/operating-principles-and-culture/",
        "Operating Principles and Culture",
    ),
    BrowserSmokeTarget(
        "How We Work",
        "/how-we-work/how-work-moves-through-opi/",
        "How Work Moves Through OPI",
    ),
    BrowserSmokeTarget(
        "What We Do",
        "/what-we-do/services/cross-agency-delivery/",
        "Cross-Agency Delivery",
    ),
    BrowserSmokeTarget("Resources", "/resources/reference/glossary/", "Glossary"),
)
TABLE_FOCUS_SOURCE_PATH = "/what-we-do/services/cross-agency-delivery/"
TABLE_FOCUS_TARGET_PATH = "/what-we-do/services/cross-agency-delivery/service-definition/"
TABLE_READY_SELECTOR = '.md-typeset__scrollwrap[tabindex="0"]'
ORG_SOURCE_PATH = "/how-we-work/organization/"
ORG_TARGET_PATH = "/how-we-work/organization/org-structure/"
ORG_READY_SELECTOR = ".opi-org-chart"
SEARCH_TARGET_SELECTOR = "h1#citistat"
ORG_CHART_NAMES = (
    "Brandon M. Scott",
    "Faith P. Leach",
    "Dartanion Swift-Williams",
    "Rakeim Young",
    "Danny Heller",
    "Jason Howard, PhD",
    "Gabriel Watson",
    "Xander Jake de los Santos",
)
REPOSITORY_URL = "https://github.com/city-of-baltimore/opi-wiki"
REPOSITORY_NAME = "city-of-baltimore/opi-wiki"
