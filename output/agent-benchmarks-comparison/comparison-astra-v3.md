# GPT-6 Astra vs Claude Opus 5.5

Checked 28 September 2026. Published max-effort configurations, not an equal-compute controlled experiment. Original Sol files are retained separately.

## Code & software engineering

| Benchmark / metric | GPT-6 Astra | Claude Opus 5.5 | Primary source |
| --- | ---: | ---: | --- |
| Terminal-Bench 4.0 — Pass@1 | 59.1% | 59.6%† | [Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-4-0) |
| FrontierCode v1.1 Main — Weighted rubric score | 53.3% | 54.4% | [Cognition](https://cognition.com/frontiercode) |
| CursorBench 4.0 — Task score | — | 57.8% | [Cursor](https://cursor.com/cursorbench) |
| DeepSWE v1.1 — Pass@1 | 67.6% | 68.4%† | [Artificial Analysis coding agents](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex) |

## Computer use & business workflows

| Benchmark / metric | GPT-6 Astra | Claude Opus 5.5 | Primary source |
| --- | ---: | ---: | --- |
| OSWorld 2.0* — Partial reward | 73.5% | 81.8%† | [Separate vendor reports](https://openai.com/index/introducing-gpt-6-sol-and-luna/) / [Anthropic](https://www.anthropic.com/claude-opus-5-5) |
| AutomationBench 1.0.6 — Strict completion | 41.4% | 42.5%† | [Zapier](https://zapier.com/benchmarks) |

## Knowledge work & science

| Benchmark / metric | GPT-6 Astra | Claude Opus 5.5 | Primary source |
| --- | ---: | ---: | --- |
| GDPval-AA v2.1 — Elo | 1542 Elo | 1846 Elo† | [Artificial Analysis](https://artificialanalysis.ai/evaluations/gdpval-aa) |
| Terminal-Bench-Science 0.1 — Pass@1 | 63.3% | 59.0%† | [Artificial Analysis](https://artificialanalysis.ai/evaluations/terminal-bench-science) |

— No public score found in checked sources. Missing is not zero.

† Fallback enabled: some tasks may be handled by other Claude models. This identifies a tested configuration, not necessarily a pure Opus-only result. It does not establish routing or how often fallback occurred. Missing † is not confirmation that fallback was disabled.

* OSWorld is not a matched comparison: Astra uses offline v2026.08.08; Opus subset/version is unconfirmed. Both are vendor-reported partial-reward scores; no direct winner or delta is asserted.

Max effort does not mean equal compute. Agent setups differ. FrontierCode and DeepSWE use Codex vs Claude Code. DeepSWE uses AA Coding Agents, whereas the selected Terminal-Bench row uses AA's mini-swe-agent model evaluation. Do not mix scores from those tracks.

## Row-specific notes

- **Terminal-Bench 4.0:** Same mini-swe-agent model evaluation; 66 tasks, three trials. Astra max 59.1 differs from xhigh 59.6.
- **FrontierCode v1.1 Main:** Raw max scores 53.26/54.43%; Codex vs Claude Code. Not pass rates.
- **CursorBench 4.0:** No exact GPT-6 Astra result found on checked official leaderboard.
- **DeepSWE v1.1:** AA coding-agent evaluation, datacurve/deep-swe-1-1@1, 113 tasks with three trials; Codex 0.153.4 vs Claude Code 2.1.280. Raw 0.675516224188791/0.684365781710915. Opus fallback is recorded in evaluation data. Do not substitute Datacurve mini-swe-agent Astra 73.2%.
- **OSWorld 2.0:** Not matched: Astra offline v2026.08.08, raw 0.7349; Opus subset/version unconfirmed. No delta/winner claim.
- **AutomationBench 1.0.6:** Both max; current held-out leaderboard, raw Opus 42.47%; different from AA partial-credit implementation.
- **GDPval-AA v2.1:** 95% CIs ±25/±23; 220 tasks. Not percentages.
- **Terminal-Bench-Science 0.1:** Same mini-swe-agent, 70 tasks with three trials. Opus xhigh61.9 is excluded.

See astra-coding-research.md and astra-work-research.md for exact primary-source evidence, effort sweeps and excluded alternate scores. Do not average metrics or claim an overall winner.

