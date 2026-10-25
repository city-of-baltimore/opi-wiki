# OPI wiki (retired)

**This wiki has moved.** Its content now lives in **OPI Foundations**, the knowledge base for Baltimore City's Mayor's Office of Performance and Innovation: https://opi-publications.fly.dev/foundations/

Every old address on https://city-of-baltimore.github.io/opi-wiki/ still works. It sends you to the same page in OPI Foundations and carries an old `#section` link across. Where a section was reorganized, you land at the top of its page. The Staff Guide now asks staff to sign in.

**Platform baseline:** `baltimore-patapsco==0.9.9`

## What happened

- On 3 Oct 2026, OPI Foundations was imported once into opi-publications' content management system, from this repository's `main` at `73272e255a2df95a696ff6a8cbd69a0f4c003331`. That commit stays in this repository's history as the import source.
- This repository's last GitHub Pages deploy replaced the MkDocs site with redirect stubs, one for each of the 249 addresses the wiki served. After that deploy, the repository is archived.
- To correct or suggest a change to OPI Foundations, use OPI Foundations itself, not this repository.

## What's published now

[`redirects/`](redirects/README.md) holds the whole published site: the stubs, their 404 page, the list of old addresses, and where the stubs came from. The gates check that site:

| Command | What it checks |
|---|---|
| `task ci` | Hosted, on pull requests: the policy checks, lint, types and security, plus every old address having one clean stub. |
| `task prepush` | The pre-push hook: everything in `ci`, the tests, and `site/` built from the stubs. |
| `task validate` | The deploy gate: everything in `prepush`, plus Chromium following every old address to its new page, offline, and axe on the 404 page. |

`task ci` runs two policy checkers on purpose: this repository's hosted-CI guard (`scripts/check_hosted_ci_policy.py`) and Patapsco's `platform-check`. The split is measured rather than assumed — re-measured against `platform-check` 0.9.9. The shared checker still treats a Python plan module (`verify.py --plan ci`) as an opaque leaf, it has no job-timeout rule, and it checks `run:` lines against a denylist rather than an allowlist. The "Two checkers" note in `scripts/repo_tools/hosted_ci_policy.py` has the measurements.

## What else is here

The MkDocs source, its theme and its content checks were deleted in the final commit; they stay in this repository's history, at the import commit above. The dated decisions behind the wiki are in [`MAINTAINERS.md`](MAINTAINERS.md).

## License

Content: [CC BY 4.0](LICENSE-CONTENT.md). Code and build automation: [MIT](LICENSE).
