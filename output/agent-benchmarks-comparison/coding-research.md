# Coding benchmark comparison evidence

Retrieved 2026-09-28 (Asia/Singapore). Exact requested models: GPT-6 Sol and Claude Opus 5.5. Data were inspected on primary pages using web search/open and Ego Lite page DOM. No model substitutions.

## Recommended rows

| Benchmark | GPT-6 Sol | Claude Opus 5.5 | Provenance/configuration |
| --- | --- | --- | --- |
| Terminal-Bench 4.0 | 43.9% (max) | 59.6% (max, default fallback) | Artificial Analysis independent run; mini-swe-agent; all 66 tasks; pass@1, 3 repeats/task |
| FrontierCode v1.1 Main | 49.3% (max) | 54.4% (max) | Cognition weighted rubric score; 100 tasks; Codex vs Claude Code harnesses |
| CursorBench 4.0 | Not found | 57.8% (max) | Cursor owner leaderboard; GPT-6 Sol has no row on checked page |
| DeepSWE v1.1 | 68.8% (max, OpenAI-reported) | Not found | Sol score is OpenAI release claim, not found on inspected Datacurve v1.1 board; no Opus 5.5 primary score located |

## Terminal-Bench 4.0

- Primary evaluator page: https://artificialanalysis.ai/evaluations/terminalbench-4-0
- Pair page: https://artificialanalysis.ai/models/comparisons/claude-opus-5-5-vs-gpt-6-sol
- Methodology: https://artificialanalysis.ai/methodology/intelligence-benchmarking
- Ego Lite DOM of the score chart lists GPT-6 Sol (max) 43.9% and Claude Opus 5.5 (max with fallback) 59.6%. The pair table rounds these to 44% and 60%.
- Same evaluator/harness and benchmark version, but Opus is explicitly a default-fallback configuration. Preserve that qualification; it is a system/configuration score, not a pure single-model estimate.
- Alternative vendor result: https://www.anthropic.com/claude-opus-5-5 reports 66.4% for Opus at xhigh, standard error ±2.6 points. This differs from AA's setup and must not be mixed with Sol's AA number as if from one matched evaluation.
- Anthropic notes safeguards can route cybersecurity tasks to Opus 4.8 and biology/frontier-LLM-development tasks to Opus 5. The AA page labels default fallback; do not assume the exact fallback routing from a different run without further AA evidence.

## FrontierCode v1.1 Main versus Extended

- Owner page: https://cognition.com/frontiercode
- Exact data, discovered in that page's resource requests: https://cognition.com/data/frontiercode-leaderboard/data.json
- Version key: `v1_1`; metric `new_score` is the weighted rubric score; `correct` is the separately reported pass rate. Do not confuse them.
- Main has 100 tasks; Extended has 150. Runs flagged for unfair internet use score zero. The owner changelog says both requested models were added September 22, 2026.
- GPT-6 Sol harness: `codex`; Claude Opus 5.5 harness: `claude-code`.

| Effort | Sol Main score | Opus Main score | Sol Extended score | Opus Extended score |
| --- | ---: | ---: | ---: | ---: |
| low | 37.28% | 47.30% | 50.55% | 60.33% |
| medium | 45.92% | 54.64% | 57.11% | 65.27% |
| high | 47.70% | 53.99% | 59.62% | 65.20% |
| xhigh | 48.45% | 51.42% | 59.13% | 63.53% |
| max | 49.27% | 54.43% | 60.69% | 63.58% |

The default owner table selects each model's best scoring reasoning effort: Sol max 49.3%, Opus medium 54.6%. A max-versus-max comparison instead uses 49.3% versus 54.4%, as in the recommended row, and should say so. Do not call 54.4% Opus's maximum observed score. Same effort labels do not imply equal inference budgets across vendors.

Main max pass rates are 54.30% (Sol) and 60.00% (Opus), which are NOT the recommended score metric. Main max cost/rollout from the fetched owner JSON is $2.0651 versus $6.191; no cost comparison is needed for the requested image.

## CursorBench 4.0

- Canonical owner page: https://cursor.com/cursorbench
- Alternate owner deployment: https://prod.cursor.com/evals
- Both fetched pages agree: Opus 5.5 max 57.8%; xhigh 56.0%; high 56.0%; medium 52.5%; low 43.7%.
- Sol is absent from all 52 displayed configurations. The page does have GPT-5.6 Sol max 41.7%, a DIFFERENT MODEL that must never be substituted.
- Owner table says Opus max average cost/task $13.43; output tokens 218,363; 185 steps. Scores vary with configuration; small differences may not be significant.

## DeepSWE v1.1

- Model developer primary page: https://openai.com/index/introducing-gpt-6-sol-and-luna/
- The Coding section explicitly reports GPT-6 Sol max 68.8% on DeepSWE v1.1. Release was September 22, 2026. It says GPT evaluations ran in OpenAI research environment or API; production ChatGPT may differ. This does not establish exact harness details for Sol.
- Benchmark owner page: https://deepswe.datacurve.ai/
- Owner page retrieved in browser and web, labeled 113 tasks, updated September 22, 2026, and all models mini-swe-agent. Neither GPT-6 Sol nor Opus 5.5 appears in displayed leaderboard. Page source also checked for exact model names.
- Exact-name searches of Datacurve and Anthropic primary sites did not find an Opus 5.5 DeepSWE result. Mark as not found, not zero, and avoid claiming no one has ever published one.

## Graphic caveats

Use a table rather than one shared scale across heterogeneous benchmark scores. Keep effort next to each score or use a clear max-effort default with row exceptions. Explain missing entries with an em dash and a concise legend such as “— No public score found.” Mark source/setup differences and fallback use; do not draw a total winner count over incomplete, heterogeneous rows.
