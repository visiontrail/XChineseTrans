# GPT-6 Sol vs Claude Opus 5.5 — work benchmark evidence

Checked 2026-09-28. Primary publishers/evaluators only. This is research evidence, not publication copy. Exact requested models were preserved; GPT-6 Astra and GPT-5.6 Sol were not substituted.

## Recommended comparison data

| Benchmark | GPT-6 Sol | Claude Opus 5.5 | Interpretation |
| --- | --- | --- | --- |
| OSWorld 2.0 | 64.4% (max; offline v2026.08.08; partial reward) | 81.8% (max; partial reward; matching subset/version not established) | Separate vendor-reported setups; no like-for-like delta or winner claim |
| AutomationBench 1.0.6 | 33.2% (xhigh) | 42.47% (max, default fallbacks) | Zapier public leaderboard; held-out private evaluation split; strict task completion |
| GDPval-AA v2.1 | 1487 Elo (max; CI ±19) | 1846 Elo (max, default fallback; CI ±23) | Same Artificial Analysis evaluation, 220 tasks; Elo is not a percentage |
| Terminal-Bench-Science 0.1 | 30.0% (max) | 61.9% (xhigh, default fallback) | Same Artificial Analysis mini-swe-agent evaluation; mean pass@1 over 3 repeats |

These are each model's best observed score in the cited effort sweep, not a fixed-effort, fixed-cost comparison. For a max-only policy, AutomationBench Sol is 32.0%; Terminal-Bench-Science Opus 5.5 is 59.0%. The word “fallback” must remain visible in any compact table or be explained in a linked footnote.

## OSWorld 2.0 evidence and comparability limit

Source: https://openai.com/index/introducing-gpt-6-sol-and-luna/

OpenAI's interactive chart is titled OSWorld 2.0, offline set. Its caption specifies partial reward on v2026.08.08. Browser extraction of the embedded chart data confirmed these GPT-6 Sol points:

| Effort | Raw score | Display score | Cost per task, USD |
| --- | --- | --- | --- |
| low | 0.439 | 43.9% | 0.9675 |
| medium | 0.54 | 54.0% | 1.3169 |
| high | 0.5829 | 58.3% | 1.6379 |
| xhigh | 0.6054 | 60.5% | 2.2127 |
| max | 0.6443 | 64.4% | 3.2543 |

Source: https://www.anthropic.com/claude-opus-5-5

Anthropic's launch table lists Opus 5.5 at 81.8% partial, with adaptive thinking/max effort by default and production safeguards/default model fallbacks. It does not establish the matching subset/version for this row. The system-card link https://anthropic.com/claude-opus-5-5-system-card exceeded web-tool content limits; a direct download returned HTTP 403. Do not assume the 81.8% result covers the same offline subset. The benchmark publisher's current page https://osworld-v2.xlang.ai/ and its chart source list older models, not the exact requested pair.

## AutomationBench evidence

Source: https://zapier.com/benchmarks

Live leaderboard version 1.0.6: Sol xhigh 33.2%/$0.27, Sol max 32.0%/$0.34, Opus 5.5 max with default fallbacks 42.47%/$1.44, xhigh with fallbacks 35.77%/$0.89, high with fallbacks 33.03%/$0.71. Refused tasks were rerun through the provider's default fallback routing. The leaderboard uses a held-out private set and strict completion: every scored assertion must pass. Its public 600-task set is for experimentation. API mode offers search and execute tools, capped at 50 steps.

Anthropic's 40.0% launch result is a separate early-access Zapier evaluation without fallback models, counting safeguard interventions as failures. Do not label 40.0% as the current default-fallback leaderboard score.

AutomationBench-AA is a different scoring implementation. AA uses a private 657-task split of version 1.0.6 and awards partial objective credit unless a guardrail is violated. It must not replace Zapier's strict headline score without changing the row's name and metric.

AA methodology: https://artificialanalysis.ai/methodology/intelligence-benchmarking#automationbench-aa

## GDPval-AA v2.1 evidence

Sources:
- https://artificialanalysis.ai/evaluations/gdpval-aa
- https://artificialanalysis.ai/models/comparisons/gpt-6-sol-high-vs-gpt-6-sol
- https://artificialanalysis.ai/methodology/intelligence-benchmarking#gdpval-aa

Live DOM table confirms Sol max 1487 (95% CI ±19), xhigh 1437 (±17), high 1376 (±18), medium 1320 (±16), non-reasoning 1225 (±14), low 1176 (±16). Opus 5.5 default-fallback entries: max 1846 (±23), xhigh 1820 (±22), high 1692 (±20), medium 1576 (±19), low 1224 (±18). The chart anchor is DeepSeek V4.1 Flash max = 1600. AA runs the 220 tasks independently with its Stirrup agent loop, shell and web browsing. Ratings come from anonymized pairwise comparisons, not task-pass percentages or human win rates.

## Terminal-Bench-Science 0.1 evidence

Sources:
- https://artificialanalysis.ai/evaluations/terminal-bench-science
- https://artificialanalysis.ai/methodology/intelligence-benchmarking#terminal-bench-science

The browser-rendered chart confirms Sol max 30.0%, xhigh 17.6%; Opus 5.5 default-fallback xhigh 61.9%, max 59.0%, high 49.0%, medium 43.3%, low 24.3%. AA uses all 70 tasks from release 0.1.0, the mini-swe-agent harness, and pass@1 averaged over three repeats per task. Every task test must pass. Agent cap is 1000 steps; timeouts/resources follow upstream task definitions.

This matched evaluation is preferable to mixing Anthropic's own 58.7% result with Sol's AA score. The Anthropic result uses a different setup. No overall aggregate score should combine Elo and percentages, and scores across different benchmarks should not share a misleading common scale.

## Retrieval notes

Web search/open located primary URLs; Ego Lite task space 208 verified JavaScript-rendered charts and tables. In particular, web text extraction omitted several OpenAI rows that the live DOM displayed. OSWorld's OpenAI figure data was extracted from its public page-embedded Vega-Lite specification, keeping the title/caption attached to the values. No estimate or secondary-site score was promoted to a primary-source result.
