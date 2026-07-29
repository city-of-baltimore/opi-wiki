# Accessibility

{{ page_header(summary="What OPI Foundations promises, how we test it, and how to report a barrier.", category="OPI FOUNDATIONS · SERVICE STANDARD") }}

OPI Foundations is designed and tested against
[WCAG 2.2 Level AA](https://www.w3.org/TR/WCAG22/). Accessibility is part of
the definition of done for the site, not a review added after publication.

This is a service commitment, not a claim that an automated tool can prove
perfect conformance. Automated checks catch repeatable failures. Human review
is still required for meaning, reading order, keyboard experience, zoom,
screen-reader clarity, and the quality of alternative text.

## What we promise

| Promise | How it is proven |
| --- | --- |
| Pages use meaningful headings, landmarks, names, and native HTML semantics. | Every generated page receives static semantic checks and a full-browser axe scan. |
| Text, controls, links, and focus indicators remain perceivable in both color schemes. | Axe evaluates every canonical route in light and dark modes; focused cards, tables, and the skip link receive browser checks. |
| The site works without a mouse. | Browser tests operate navigation, search, skip links, and horizontally scrollable tables with keyboard-accessible controls. |
| Content reflows without page-level horizontal scrolling. | Every canonical route is measured at a 320 CSS-pixel viewport in both color schemes. Data tables may scroll inside their labeled region, as WCAG permits. |
| Responsive and interactive states receive the same standard as a direct page load. | The browser audit covers desktop, 320px reflow, the open mobile navigation drawer, open search, and pages reached through instant navigation. |
| Accessibility failures stop a release. | `task prepush` holds generated semantic checks; `task validate` adds the real-browser matrix and must pass before deployment. |

## What the automated gate covers

The local release gate scans every URL in the generated sitemap with
[axe-core](https://github.com/dequelabs/axe-core). The rule engine is pinned so
its behavior cannot change silently. The matrix covers:

- 1440 × 900 desktop in light and dark modes;
- 320 × 800 reflow in light and dark modes;
- WCAG A and AA rules, plus axe accessibility best practices;
- document-level horizontal overflow;
- the first-focus skip link;
- the mobile navigation drawer and search after they are opened; and
- runtime errors, canonical routes, focus treatments, and instant navigation
  through the companion browser smoke suite.

Run the complete local proof with:

```bash
uv run playwright install chromium  # one-time browser install
task validate
```

## What still requires people

Before a structural navigation, template, or shared-component release, the
reviewer should:

1. Travel through the changed experience with only a keyboard.
2. Check the page at 200% and 400% zoom.
3. Apply increased line, paragraph, letter, and word spacing.
4. Spot-check the changed experience with a screen reader.
5. Confirm that headings, link text, alternative text, and reading order still
   make sense without visual context.

The pull request should name the pages and states reviewed. “The automated
check passed” is not a substitute for that evidence.

## Report an accessibility barrier

Email [opi@baltimorecity.gov](mailto:opi@baltimorecity.gov) or
[open a GitHub issue](https://github.com/city-of-baltimore/opi-wiki/issues/new).
Include the page address, what you were trying to do, what happened, and the
browser or assistive technology you were using. Do not include sensitive
personal information.
