# GPT-6 Astra vs Claude Opus 5.5 — work benchmark evidence

Verified 2026-09-28. Scope: GPT-6 Astra (not Astra Pro), max effort, compared with Claude Opus 5.5 max effort. This is a fresh primary-source check rather than a model-name substitution in the Sol results.

## Recommended values

| Benchmark | GPT-6 Astra max | Claude Opus 5.5 max | Matched evaluator / qualification |
| --- | --- | --- | --- |
| OSWorld 2.0 | 73.5% | 81.8% | Separate vendor reports; matching task subset, harness and grading not established. Astra: offline v2026.08.08 partial reward. No winner/delta claim. |
| AutomationBench 1.0.6 | 41.4% | 42.47%, default fallbacks | Same Zapier public leaderboard, held-out private task set, strict completion |
| GDPval-AA v2.1 | 1542 Elo, CI ±25 | 1846 Elo, CI ±23, default fallback | Same Artificial Analysis evaluation and Elo scale |
| Terminal-Bench-Science 0.1 | 63.3% | 59.0%, default fallback | Same Artificial Analysis mini-swe-agent evaluation; mean pass@1 across three trials per task |

Do not use Opus 5.5 xhigh 61.9% for a max-versus-max chart. The default-fallback qualifier means the evaluated provider configuration may route refused work to other Anthropic models; these are not guaranteed pure single-model runs. Max effort is not an equal-compute or equal-cost budget across vendors.

## AutomationBench 1.0.6

Primary source: https://zapier.com/benchmarks

The live leaderboard explicitly labels GPT 6 Astra (Max) at 41.4%, $1.73/task; Claude Opus 5.5 (default fallbacks, Max) at 42.47%, $1.44/task. The score is `task_completed_correctly`: every scored assertion must pass. This is a held-out private set; the public 600-task release is for research. The API-mode agent uses search and execute tools with a 50-step ceiling. Refused Opus tasks were rerun with the provider's default fallback routing.

Do not substitute AutomationBench-AA, whose score gives partial objective credit subject to guardrails. Do not replace Opus's current 42.47% with the Anthropic launch figure 40.0%, which was an early-access Zapier run without fallback models.

## GDPval-AA v2.1

Primary sources:
- https://artificialanalysis.ai/evaluations/gdpval-aa
- https://artificialanalysis.ai/models/comparisons/gpt-6-astra-high-vs-gpt-6-astra
- https://artificialanalysis.ai/methodology/intelligence-benchmarking#gdpval-aa

Re-read live DOM table via Ego Lite because text-only web extraction omitted some OpenAI rows. Exact rows: GPT-6 Astra (max), rank 31, Elo 1542, CI -25/+25; Claude Opus 5.5 (Adaptive Reasoning, Max Effort, Default Fallback), rank 1, Elo 1846, CI -23/+23. Both are September 2026 releases. This scale is anchored to DeepSeek V4.1 Flash max = 1600. AA runs 220 tasks using Stirrup with shell and browsing, then scores anonymized pairwise deliverable comparisons. Elo must not be displayed as a percentage or combined numerically with success rates.

## Terminal-Bench-Science 0.1

Primary sources:
- https://artificialanalysis.ai/evaluations/terminal-bench-science
- https://artificialanalysis.ai/methodology/intelligence-benchmarking#terminal-bench-science

The current page summary and live chart both show GPT-6 Astra max = 63.3%; Opus 5.5 max with default fallback = 59.0%. Opus xhigh = 61.9% is a different effort setting, excluded from the selected pair. AA evaluates all 70 tasks in release 0.1.0 with mini-swe-agent, pass@1 averaged across three repeats, and a 1000-step cap. A task passes only if every test passes. Timeouts/resources follow task definitions.

The vendors' launch figures, Astra 64.6% and Opus 58.7%, are not the matched AA results and are not selected. A 4.3-point observed margin is not proof of a statistically significant advantage; no confidence interval for this pair was exposed in the inspected summary.

## OSWorld 2.0: newer chart values and unmatched setup

Primary newer source: https://openai.com/index/introducing-gpt-6-sol-and-luna/

On the September 22 launch page, the embedded Vega-Lite chart is titled OSWorld 2.0, offline set. Its caption specifies partial reward on v2026.08.08. Read directly from page-embedded chart data:

| Astra effort | Raw score | Display, percent | Raw cost, USD/task |
| --- | --- | --- | --- |
| low | 0.6217 | 62.2 | 2.5457 |
| medium | 0.6925 | 69.3 | 5.1009 |
| high | 0.7002 | 70.0 | 6.6024 |
| xhigh | 0.7127 | 71.3 | 7.1744 |
| max | 0.7349 | 73.5 | 9.0733 |

Every row explicitly says GPT-6 Astra; no Pro label is used. Thus 73.5% is the appropriate value for the requested current max-effort row. The earlier primary source https://openai.com/index/gpt-6-astra/ still reports 72.6% and says its scores are maximum across efforts. Do not silently equate that older number to the newer effort-tagged chart.

Primary Opus source: https://www.anthropic.com/claude-opus-5-5

The launch table gives Opus 5.5 = 81.8% partial; default evaluation setting is adaptive thinking/max with production safeguards and fallbacks. It does not establish the same offline subset, version, harness or graders used by OpenAI. OpenAI's Astra page explicitly distinguishes its official OSWorld settings from modified tasks/grading in the Fable 5.1 system card, so shared benchmark name alone is insufficient. The Opus 5.5 system-card fetch previously exceeded the web-tool size limit; a direct retry returned HTTP 403. No identical-setup comparison was found. Keep this row under “Separate reported setups” or mark it not directly comparable; do not bold a winner or calculate an 8.3-point comparative advantage.

## Verification log

- Web opened the primary pages anew on 2026-09-28.
- Ego Lite task space 212 re-read AA rows and the Science chart, and extracted OpenAI's public page-embedded OSWorld chart specification.
- Browser values and primary page text agree on the three matched rows.
- No other project artifacts or source score files were edited for this research subtask.
