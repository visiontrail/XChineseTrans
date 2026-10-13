# Sol DeepSWE v1.1 refresh for the three-image publishing package

Verified 2026-09-28 against Artificial Analysis's original evaluator page and its public server-rendered data. Research only; no image or existing data file was modified.

## Selected replacement pair

**DeepSWE v1.1: GPT-6 Sol (max) 69.0% vs Claude Opus 5.5 (max) 68.4%†.**

Primary source: https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex

Methodology: https://artificialanalysis.ai/methodology/coding-agents-benchmarking/

These are the AA Coding Agents track, using Codex and Claude Code respectively. The main representative comparison defaults to Astra, but the same page's **Model Variants** table explicitly includes Sol. Its live DOM displays Sol max DeepSWE 69% and Opus max 68%, with more precise values present in the page's Next.js data. Both were checked twice.

| Field | GPT-6 Sol | Claude Opus 5.5 |
| --- | --- | --- |
| `displayLabel` | `Codex - GPT-6 Sol (max)` | `Claude Code - Opus 5.5 (max)` |
| `hostModelSlug` | `openai_gpt-6-sol` | `anthropic_claude-opus-5-5` |
| `datasetIndexName` | `deep-swe-v1.1` | `deep-swe-v1.1` |
| `refDatasetName` | `datacurve/deep-swe-1-1@1` | `datacurve/deep-swe-1-1@1` |
| `mean.reward` | `0.690265486725664` | `0.684365781710915` |
| Percentage before display rounding | `69.0265486725664` | `68.4365781710915` |
| Image display | **69.0%** | **68.4%†** |
| Agent version, min and max | Codex `0.154.0` | Claude Code `2.1.280` |
| `safety.attemptCount` | 337 | 339 |
| `safety.fallbackAttemptCount` | 0 | 2 |

The numeric data comes from each variant's `evals` entry for `deep-swe-v1.1`. To inspect it, decode the JSON arguments in the page's `self.__next_f.push(...)` script tags, find the exact `displayLabel`, then read that object's DeepSWE `mean.reward` and version fields.

AA's published methodology averages attempts within each task, then averages across tasks equally. It targets three attempts per task for the 113-task DeepSWE v1.1 set. The live Sol row records 337 safety-counted attempts versus Opus's 339; do not claim that both have exactly 339, or replace the evaluator's published task-weighted score with a ratio inferred from this count. The inspected payload does not explain the two-attempt discrepancy. Both results belong to the same AA dataset and methodology but use different harnesses and agent versions; they are not a controlled model-only experiment.

## Required corrections to the older Sol graphic

- Replace the DeepSWE **68.8% / —** row with **69.0% / 68.4%†**. The former 68.8% is an OpenAI vendor result from another setup; do not pair it with AA's Opus result.
- Remove any DeepSWE implication that Opus has no publicly available result. The earlier search missed AA's Coding Agents track.
- Add/retain the harness clarification: **FrontierCode & DeepSWE use Codex vs Claude Code.**
- Use the user-approved dagger text exactly: **† Fallback enabled: some tasks may be handled by other Claude models.** The Opus DeepSWE data positively records fallback even though its visible variant name does not append a fallback label. Internal counts are audit evidence only; do not infer routing identities, triggers, or public frequency claims.
- Preserve the Terminal-Bench row's AA **model-evaluation/mini-swe-agent** numbers. The AA Coding Agents track has different Terminal-Bench numbers and must not silently replace just one side.

If retaining a vendor-only DeepSWE row for a deliberate editorial reason, an accurate missing marker would mean **No matched result in this source/setup**, not **No public score found**. The same-evaluator AA pair above is preferable and removes that avoidable missing entry.
