# The wiki's final site

The wiki retired into **OPI Foundations**, the knowledge base in opi-publications, at https://opi-publications.fly.dev/foundations/. Its content was imported once, from this repository's `main` at `73272e255a2df95a696ff6a8cbd69a0f4c003331`. This directory is everything GitHub Pages now publishes.

| Path | What it is |
|---|---|
| `stubs/` | The published site, deployed as it is. One `index.html` per old address (249), plus `404.html`. |
| `old-addresses.txt` | The 249 addresses the wiki served at `73272e25`: its 88 sitemap pages and its 161 `redirect_maps` entries. |

## Where the stubs come from

The 249 stubs are the unedited output of opi-publications' `scripts/build_wiki_redirect_stubs.py` (WIKI-14). It was run at opi-publications commit `634d930a67165e6ccdcc1cf36134e3d4dbcd45a8`:

```bash
uv run python scripts/build_wiki_redirect_stubs.py https://opi-publications.fly.dev <empty dir>
```

| Input | sha256 |
|---|---|
| `scripts/build_wiki_redirect_stubs.py` | `8631d44602d781de90579319728fc3f2c1f514698bfde7e617df30120b34d6ec` |
| `content_fixtures/opi_foundations/manifest.json` | `ebc928410a7a4b3fbbfe8a6061ea805d854ef064ed6acda27dde52948fd6f194` |

- **What a stub does:** it sends the reader to the old page's new page and carries any `#section` across. Without JavaScript, its refresh still lands on the page.
- **`404.html` is written here,** not by the builder. GitHub Pages serves it for every address that has no stub.
- **Don't edit a stub by hand.** To change the stubs, rebuild them all from opi-publications and replace `stubs/` whole, keeping `404.html`.

`old-addresses.txt` comes from the wiki itself, not from opi-publications' import manifest. So the checks compare two independent sources: `scripts/check_redirect_stubs.py` statically, and `scripts/check_browser_redirects.py` in a browser.
