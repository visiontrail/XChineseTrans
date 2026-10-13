# GPT-6 Sol vs Claude Opus 5.5

Checked 2026-09-28. All displayed scores use max effort. These are published system/configuration results, not an equal-compute controlled experiment or best-observed scores at any effort. Missing values mean no exact-model public score found in the checked sources, never zero.

| Benchmark and metric | GPT-6 Sol | Claude Opus 5.5 | Primary source |
| --- | ---: | ---: | --- |
| Terminal-Bench 4.0 — Pass@1 | 43.9% | 59.6% † | [Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-4-0) |
| FrontierCode v1.1 Main — Weighted rubric score | 49.3% | 54.4% | [Cognition](https://cognition.com/frontiercode) |
| CursorBench 4.0 — Task score | — | 57.8% | [Cursor](https://cursor.com/cursorbench) |
| DeepSWE v1.1 — Task score | 68.8% | — | [OpenAI-reported](https://openai.com/index/introducing-gpt-6-sol-and-luna/) |
| OSWorld 2.0 — Partial reward | 64.4% | 81.8% † | [Vendor reports](https://openai.com/index/introducing-gpt-6-sol-and-luna/) / [Anthropic](https://www.anthropic.com/claude-opus-5-5) |
| AutomationBench 1.0.6 — Strict completion | 32.0% | 42.5% † | [Zapier](https://zapier.com/benchmarks) |
| GDPval-AA v2.1 — Elo | 1487 Elo | 1846 Elo † | [Artificial Analysis](https://artificialanalysis.ai/evaluations/gdpval-aa) |
| Terminal-Bench-Science 0.1 — Pass@1 | 30.0% | 59.0% † | [Artificial Analysis](https://artificialanalysis.ai/evaluations/terminal-bench-science) |

† Default fallback configuration; these results may involve fallback models and should not be described as Opus-only results.

OSWorld 2.0 is not a matched comparison: Sol uses the offline v2026.08.08 subset; the matching Opus subset/version was not established. Both report partial reward. FrontierCode uses different harnesses (Codex versus Claude Code), and its score is a weighted rubric score.

## Row-specific notes

- **Terminal-Bench 4.0:** Same evaluator and mini-swe-agent harness; 66 tasks, 3 repeats.
- **FrontierCode v1.1 Main:** Raw scores 49.27/54.43. Different harnesses: Codex / Claude Code. Not a pass rate.
- **CursorBench 4.0:** No exact GPT-6 Sol entry found in checked owner leaderboard.
- **DeepSWE v1.1:** Not listed on checked Datacurve owner board; no public exact Opus 5.5 score found.
- **OSWorld 2.0:** Not matched: Sol offline subset v2026.08.08; Opus subset/version unconfirmed. No delta/winner claim.
- **AutomationBench 1.0.6:** Raw Opus 42.47. Current held-out private leaderboard with default fallback, not Anthropic early-access 40.0 or AutomationBench-AA partial scoring.
- **GDPval-AA v2.1:** 95% CI ±19 / ±23. DeepSeek V4.1 Flash max anchor 1600. Not percentages.
- **Terminal-Bench-Science 0.1:** Same mini-swe-agent evaluator, 70 tasks, 3 repeats; do not mix vendor 58.7 or xhigh61.9 into max snapshot.

## Selection policy

Prefer a single evaluator and the same benchmark version for each pair where available. Use max effort consistently rather than cherry-picking each model's best effort. Max effort is a setting label, not proof of equal compute or budget. Scores on different rows have different metrics and must not be averaged or put on one shared quantitative scale. Do not infer an overall winner from incomplete/heterogeneous results.

See coding-research.md and work-research.md for exact retrieval provenance and alternate effort levels.

