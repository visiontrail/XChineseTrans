# AI-native revision record

Revision date: 27 September 2026. Previous deliverable: adjacent `github-field-guide/`; that directory was preserved.

## Editorial scope

The 15 sections of the previous English article were rebuilt into 16 sections with 28 prompts. Operational work is assigned to a tool-enabled AI agent. The diagrams explain command effects, direction, and evidence rather than presenting manual terminal recipes. The practice site's checklist explicitly addresses the release agent. Owner-only authentication or platform-required interaction is identified honestly.

The public package contains no original X author, handle, or source-post attribution. It retains links to relevant official technical references. Voice and paragraph structure follow the current project guidelines.

## Assets

One new cover was generated with built-in ImageGen; its full prompt is in `image-prompts.json`. Eleven new SVG diagrams were laid out using Archify and refined as native SVG, with PNG exports. These are labeled conceptual diagrams. They are not product screenshots or claimed execution evidence. No prior article figure is reused in this revision.

All 12 images were visually inspected. Archify layout validation passed for all 11 diagrams. The standalone staging diagram was inspected in light and dark themes; its export menu exposes PNG, JPEG, WebP, and SVG formats. The supplied SVG/PNG files were generated directly; each browser download path was not separately exercised.

## Technical verification

- `git-state-verification.json`: 8 scenarios, 79 actual Git commands in disposable local repositories, including a local bare remote. Staged content, worktree isolation, stash behavior, fetch boundaries, merge parents, rebase identity, merge abort, and revert history were checked.
- `companion-verification.json`: 35 command checks in a disposable copy, including baseline/branch/commit/local push/revert and three deliberate checker failures (missing target, missing fragment, root-relative URL).
- After the final explanatory text edits to the practice pages, the supplied checker passed again.
- `coverage-audit.json`: all 15 previous article sections map to new prompts, and every prior Git command family has a diagram index entry. The article contains no manual shell recipe blocks.

The local tests do not establish model compliance with every prompt, hosted Actions execution, public repository creation, PR merge, or Pages deployment. No GitHub writes were performed for this revision.

## Browser QA

Browser: Codex in-app browser on the user's computer, as explicitly approved in the conversation. Local preview: `http://127.0.0.1:8769/article.html`.

- Desktop: 1280 px viewport, 1265 px document width; no horizontal document overflow. All 12 embedded images loaded. All 16 section anchors and 28 prompt cards existed; no missing local anchor targets.
- Mobile: 390 px viewport, 375 px document width. All prompt blocks fit without horizontal overflow; the table of contents starts collapsed. The full-learning-prompt link reached Prompt 28 near the top of the viewport.
- Figure enlargement and close controls worked. Screenshots are in `qa/`.
- The copy button's Clipboard API write resolved and displayed its success state. The automation clipboard read interface returned an empty value; a separate browser clipboard-read probe did not resolve during the check. An exact pasted-content comparison was therefore not established. The article includes a selection fallback when clipboard writes are rejected, and all prompts are also supplied in Markdown/plain text.
- The final rebuilt article displayed the revised agent-operated checklist prompt, all images remained loaded, and the article console showed no captured errors.

## Packaging

`prepare_delivery.py` derives the prompt library and plain text from the current article, checks image and prompt counts, packages the companion's hidden ignore/workflow files, and validates every ZIP member using CRC and SHA-256. The latest counts and file hashes are in `delivery-validation.json` and `delivery-manifest.json`.
