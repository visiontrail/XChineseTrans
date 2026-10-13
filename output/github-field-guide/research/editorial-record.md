# Editorial and verification record

Prepared 27 September 2026 for LeoGuoLabs.

## Source retrieval and editorial treatment

The user-supplied X article at https://x.com/xaiwind/status/2104039563719262546?s=61 was read in the signed-in Codex in-app browser. The source DOM is retained in `source-x-dom.txt` for private research. No source-post credit, handle, or URL was added to the reader-facing article or imagery.

The adaptation reorganizes the material around a single path: understand a project, make a small change, establish what was checked, review a PR, deploy, and verify the result. It introduces a runnable two-page practice project, a local checker with clear scope, staging semantics, conflict handling, state-specific recovery, and agent task boundaries. First-person passages express editorial judgment; they do not claim the user performed the source author's tests or deployments.

## Corrections and added detail

| Topic | Checked statement | Primary reference |
|---|---|---|
| Free repositories | Unlimited public/private repositories and collaborators; feature differences remain | https://docs.github.com/en/get-started/learning-about-github/githubs-plans |
| Codespaces | 120 core-hours and 15 GB-month for personal Free accounts; 2-core compute uses allowance in about 60 running hours | https://docs.github.com/en/billing/concepts/product-billing/github-codespaces |
| Actions | 2,000 included minutes for applicable Free private-repository use; standard public runners free; larger runners and storage separately governed | https://docs.github.com/en/billing/concepts/product-billing/github-actions |
| Actions versions | Official examples used checkout v7 and setup-python v7 at verification | https://github.com/actions/checkout and https://github.com/actions/setup-python |
| Authentication | HTTPS Git does not accept account passwords; CLI/GCM, tokens and SSH have different roles | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github |
| Identity | Commit metadata differs from authentication; usernames can change with side effects | https://docs.github.com/en/account-and-profile/concepts/username-changes |
| Search | Repository, issue and code search have distinct syntax; symbol search finds definitions | https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax |
| Reading code | Shortcuts and github.dev editor distinguished from Codespaces compute | https://docs.github.com/en/get-started/accessibility/keyboard-shortcuts and https://docs.github.com/en/codespaces/the-githubdev-web-based-editor |
| Pages | Static hosting; user/org root site and project subpath; main/docs supported as branch publishing source | https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages and https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site |
| Large files | Regular Git files above 100 MiB are blocked | https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github |
| Rulesets | Applicability depends on plan/visibility; enforcement and target need checking | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| Undo | Restore --staged and revert operate at different layers | https://git-scm.com/docs/git-restore and https://git-scm.com/docs/git-revert |
| Secret exposure | Revoke/rotate first; removing a current file does not remove historical copies | https://docs.github.com/en/code-security/tutorials/remediate-leaked-secrets/remediating-a-leaked-secret |
| Public code | Visibility does not replace a license or dependency checks | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository |

Additional directly linked primary references are preserved in `article.md`. No claim of hosted Actions execution, a new PR, or public deployment was made.

## Screenshots and generated assets

Ego Lite's native connection timed out, and similarly named extension connections could not be reliably mapped. The user explicitly approved Codex's in-app browser as the replacement for local GitHub captures. No everyday Chrome session was used for the completed captures. A blocked browser-internal page was not retried or bypassed.

| Original capture | URL and observed content |
|---|---|
| 01-repository.png | https://github.com/pallets/flask — root file list, src/flask, tests, PR tab and license |
| 02-code-search.png | https://github.com/search?q=repo%3Apallets%2Fflask%20symbol%3AFlask&type=code — loaded code results |
| 03-pull-request.png | https://github.com/pallets/flask/pull/6013/changes — filename.lower() diff and changelog; merged status observed separately in page UI |
| 04-pages.png | https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#types-of-github-pages-sites — repository names and URL patterns |

Original bytes are kept under `screenshots/originals/`; their SHA-256 values are in `artifact-verification.json`. Figures 04, 05 and 07 are direct copies. Figure 03 is an AI-assisted annotated derivative: it is explicitly identified as such, and the raw image remains accessible. The first annotation draft's overbroad license sentence was corrected to “Public does not mean unrestricted.” The cover is explicitly conceptual. Figures 02 and 06 are vector diagrams, not interface evidence.

## Local validation

`companion-verification.json` records 35 command results from a temporary Git repository. All pushes targeted a temporary local bare repository. Three deliberately broken link cases exited nonzero; restoration passed. No global Git configuration was changed. The temporary sandbox was removed by the test runner.

Desktop and 390 × 844 responsive QA checked all figures, 15 headings, anchors, responsive table scrolling, image enlargement, Escape/close, and unedited-capture viewing. The viewport override was reset. QA captures are saved in this directory. Diagram theme controls and export menu were inspected in the local browser.

The article is a local deliverable. Publication was not requested and was not performed.
