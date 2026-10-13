# Production notes

Generated with the built-in image_gen tool on 2026-09-28. Image prompt: image-prompt.txt. Style reference: assets/brand/leoguolabs-light-v1/reference-infographic-paper-v2.png. Final file: gpt6-sol-vs-opus55.png. Research: coding-research.md, work-research.md; selected data: scores.json and comparison.md. No publication performed.

Style: warm ivory fine paper texture, modern sans-serif, forest green and restrained dark gold, simple table, no decorative icons or winner totals.

All reported values use max effort. Display percentages rounded to one decimal, Elo as integers. Explicit missing entries, OSWorld unmatched setup warning, and fallback daggers preserved. This is a comparison of published configurations, not an equal-compute experiment or a pure single-model claim for fallback results.

## Retained Sol grouped version

Retained prior deliverable: gpt6-sol-vs-opus55-grouped-v2.png. Generated with the built-in image_gen tool using image-prompt-grouped-v2.txt and the previous comparison image as a reference. Original tool output: /Users/leoguo/.codex/generated_images/01a0e6b0-8921-73c3-ae17-d2e663f1181d/exec-e21e638c-2d6f-42bd-b23b-87b455b94e1f.png.

Grouped into the field guide's three categories: Code & software engineering (4 rows), Computer use & business workflows (2 rows), Knowledge work & science (2 rows). All scores are unchanged. Visual and independent review confirmed all 8 score pairs, 5 fallback daggers, Elo units, both missing entries, and the complete caveats. Prior image retained. ALT text: alt-text-grouped-v2.txt. No publication performed.

## Current Astra version

Current deliverable: gpt6-astra-vs-opus55-grouped-v3.png. The user replaced GPT-6 Sol with GPT-6 Astra; all Astra scores were researched anew. Research: astra-coding-research.md and astra-work-research.md. Selected data and links: scores-astra-v3.json and comparison-astra-v3.md. ALT: alt-text-astra-v3.txt.

Generated with the built-in image_gen tool using image-prompt-astra-v3.txt and the Sol grouped version as the edit target. Original output retained at /Users/leoguo/.codex/generated_images/01a0e6b0-8921-73c3-ae17-d2e663f1181d/exec-8cb36d38-6507-4fa8-93bc-f1ac468d232c.png. The three categories and established paper/green/gold/sans-serif style are preserved.

DeepSWE now uses the same-evaluator AA Coding Agents pair, with Codex and Claude Code disclosed, rather than the older unmatched Sol vendor report. One missing Astra CursorBench value remains. Six Opus values carry a dagger. The user-specified explanation is reproduced exactly: “† Fallback enabled: some tasks may be handled by other Claude models.” This wording and the non-inference rule were also recorded in AGENTS.md.

Visual and independent QA passed for all eight score pairs, 4/2/2 grouping, six daggers, one missing value, Elo units, and caveats. No leftover Sol label, clipping or extra decoration was found. No publication performed.

## Current three-image publication package

The user requested both model comparisons alongside the benchmark field guide. publication-review-three-images.md and publication-manifest-three-images.json now define the pending approval package: field guide, Sol grouped v4, Astra grouped v3, in that order. The exact body is x-post-three-images-final.txt. Earlier one-image approval packages are superseded.

Sol grouped v4 uses the user-approved fallback footnote and the newly located AA Coding Agents DeepSWE pair: 69.0% / 68.4%†. The prior vendor-only 68.8% / missing row is retained only in older versions. Data and evidence: scores-sol-v4.json, comparison-sol-v4.md and sol-deepswe-refresh.md. Built-in image_gen prompt: image-prompt-sol-v4.txt. Final image: gpt6-sol-vs-opus55-grouped-v4.png. ALT: alt-text-sol-v4.txt.

Sol v4 passed visual and independent QA for all scores, six daggers, one missing entry, units, updated source/harness notes, three sections and existing style. All three images are saved. Awaiting user approval; no publication performed.
