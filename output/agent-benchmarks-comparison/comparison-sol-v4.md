# GPT-6 Sol vs Claude Opus 5.5 — final Sol v4

Checked 28 September 2026. Published max-effort configurations; not an equal-compute controlled experiment.

| Benchmark / metric | GPT-6 Sol | Claude Opus 5.5 | Primary source |
| --- | ---: | ---: | --- |
| Terminal-Bench 4.0 — Pass@1 | 43.9% | 59.6%† | [Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-4-0) |
| FrontierCode v1.1 Main — Weighted rubric score | 49.3% | 54.4% | [Cognition](https://cognition.com/frontiercode) |
| CursorBench 4.0 — Task score | — | 57.8% | [Cursor](https://cursor.com/cursorbench) |
| DeepSWE v1.1 — Pass@1 | 69.0% | 68.4%† | [Artificial Analysis coding agents](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex) |
| OSWorld 2.0 — Partial reward | 64.4% | 81.8%† | [Vendor reports](https://openai.com/index/introducing-gpt-6-sol-and-luna/) / [Anthropic](https://www.anthropic.com/claude-opus-5-5) |
| AutomationBench 1.0.6 — Strict completion | 32.0% | 42.5%† | [Zapier](https://zapier.com/benchmarks) |
| GDPval-AA v2.1 — Elo | 1487 Elo | 1846 Elo† | [Artificial Analysis](https://artificialanalysis.ai/evaluations/gdpval-aa) |
| Terminal-Bench-Science 0.1 — Pass@1 | 30.0% | 59.0%† | [Artificial Analysis](https://artificialanalysis.ai/evaluations/terminal-bench-science) |

— No public score found in checked sources. Missing is not zero.

† Fallback enabled: some tasks may be handled by other Claude models. The symbol does not identify routing or frequency. Missing a dagger is not confirmation that fallback was disabled.

OSWorld is not a matched comparison: Sol uses offline v2026.08.08; Opus subset/version is unconfirmed. Max effort does not mean equal compute. FrontierCode and DeepSWE use Codex vs Claude Code.

DeepSWE replaces the old vendor-only 68.8% / missing pair with the AA Coding Agents pair. See sol-deepswe-refresh.md for exact evidence; other rows retain the verified source choices in coding-research.md and work-research.md. Terminal-Bench still uses AA mini-swe-agent; do not mix the Coding Agents Terminal scores into it.
