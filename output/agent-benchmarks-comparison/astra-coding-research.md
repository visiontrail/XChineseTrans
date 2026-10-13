# GPT-6 Astra vs Claude Opus 5.5: coding benchmark evidence

Verified on 2026-09-28. This supersedes the model choice in `coding-research.md` for the Astra comparison; that older Sol research remains unchanged. Exact model and effort selection is **GPT-6 Astra (max)** and **Claude Opus 5.5 (max)**. No Astra Pro, xhigh, Sol, or unofficial estimates are substituted.

## Recommended image values

| Benchmark / evaluator | GPT-6 Astra (max) | Claude Opus 5.5 (max) | Metric and setup |
| --- | ---: | ---: | --- |
| Terminal-Bench 4.0 / Artificial Analysis model evaluation | 59.1% | 59.6%† | pass@1; mini-swe-agent for both; 66 tasks, 3 attempts per task |
| FrontierCode v1.1 Main / Cognition | 53.3% | 54.4% | Weighted rubric score; Codex vs Claude Code; Main only |
| CursorBench 4.0 / Cursor | — | 57.8% | Owner-reported score; no Astra row found |
| DeepSWE v1.1 / Artificial Analysis Coding Agents | 67.6% | 68.4%† | pass@1; Codex vs Claude Code; 113 tasks, 3 attempts per task |

Approved public footnote: **† Fallback enabled: some tasks may be handled by other Claude models.** Do not infer fallback model identities, trigger rules, or frequency from another evaluator's results. The dagger is evidenced for Terminal-Bench and DeepSWE here. FrontierCode and Cursor do not disclose a fallback field in the inspected rows; absence of a field is not evidence that fallback was disabled.

Suggested harness footnote: **FrontierCode & DeepSWE use Codex vs Claude Code.** The rows measure configurations, with different agents where indicated; they are not a controlled model-only experiment. A shared effort name does not establish equal compute budgets. Do not total or average unrelated benchmark scores.

## Terminal-Bench 4.0: same-harness model evaluation

Primary evaluator: https://artificialanalysis.ai/evaluations/terminalbench-4-0

Live SVG/DOM chart, read in Ego Lite, pairs the following ordered labels and values:

```text
Claude Opus 5.5 (max with fallback)  59.6%
Claude Opus 5.5 (xhigh with fallback) 59.6%
GPT-6 Astra (xhigh)                59.6%
GPT-6 Astra (max)                  59.1%
```

Use the max entries. The Astra xhigh score is deliberately excluded. The page's methodology identifies mini-swe-agent, 66 tasks and pass@1 averaged over three repeated attempts per task. This is the AA **model evaluation** track, separate from its Coding Agents track.

The separately inspected AA Coding Agents comparison has Terminal-Bench rewards `0.555555555555555` for Astra/Codex and `0.631313131313131` for Opus/Claude Code. These are **55.6% and 63.1% in another harness track** and must not replace one side of the selected 59.1%/59.6% pair. Anthropic's vendor-reported 66.4% xhigh is also excluded.

## FrontierCode v1.1 Main: owner data

Primary owner page: https://cognition.com/frontiercode

Page data endpoint: https://cognition.com/data/frontiercode-leaderboard/data.json

Parsed from `v1_1.harness[model]` and `v1_1.data[model].max.main`:

```json
{
  "GPT-6 Astra": {
    "harness": "codex",
    "effort": "max",
    "main": {"correct": 0.5875, "new_score": 0.5326, "tokens": 30144, "cost": 4.586, "flagged_rate": null}
  },
  "Claude Opus 5.5": {
    "harness": "claude-code",
    "effort": "max",
    "main": {"correct": 0.6, "new_score": 0.5443, "tokens": 165811, "cost": 6.191, "flagged_rate": 0.008}
  }
}
```

Use `new_score`, the weighted rubric score: **53.26% vs 54.43%**, rounded to 53.3% vs 54.4%. `correct` is a different metric and is not the reported combined score. Main contains 100 tasks; Extended contains 150. Extended max scores are 64.48% and 63.58%, respectively, and are not substituted into Main. Opus medium is also excluded despite a slightly higher Main score. The owner's fairness policy zeros runs that use the internet unfairly.

## CursorBench 4.0: incomplete pair

Primary owner page: https://cursor.com/cursorbench

Live owner table contains `Opus 5.5 Max`, score **57.8%**, cost/task $13.43, 218,363 tokens, 185 steps. Other Opus effort levels are separate rows. The page's 52 configurations contain no GPT-6 Astra: a live document text search for `Astra` returns false. No exact Astra result was found on this owner board.

An external GitHub report assigns Astra an estimated score around 54%; its author describes inference from other benchmarks. It is not a measured CursorBench result and is not used. Missing is **not zero**.

## DeepSWE v1.1: a same-evaluator agent comparison is available

Primary evaluator comparison: https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex

Primary evaluator methodology: https://artificialanalysis.ai/methodology/coding-agents-benchmarking/

The rendered table rounds both DeepSWE results to 68%. Exact values are present in that same page's public Next.js server-rendered data. Decode the JSON arguments in `self.__next_f.push(...)` script tags, then inspect the highlighted `rows` and their `evals` array for `datasetIndexName == "deep-swe-v1.1"`.

Selected data excerpt, fetched and parsed twice on the verification date:

```json
[
  {
    "displayLabel": "Codex - GPT-6 Astra (max)",
    "agentName": "Codex",
    "datasetIndexName": "deep-swe-v1.1",
    "refDatasetName": "datacurve/deep-swe-1-1@1",
    "mean.reward": 0.675516224188791,
    "safety.attemptCount": 339,
    "safety.fallbackAttemptCount": 0,
    "versions.deep-swe-v1.1.min.version": "0.153.4",
    "versions.deep-swe-v1.1.max.version": "0.153.4"
  },
  {
    "displayLabel": "Claude Code - Opus 5.5 (max)",
    "agentName": "Claude Code",
    "datasetIndexName": "deep-swe-v1.1",
    "refDatasetName": "datacurve/deep-swe-1-1@1",
    "mean.reward": 0.684365781710915,
    "safety.attemptCount": 339,
    "safety.fallbackAttemptCount": 2,
    "versions.deep-swe-v1.1.min.version": "2.1.280",
    "versions.deep-swe-v1.1.max.version": "2.1.280"
  }
]
```

Dots in the excerpt denote nested field paths; this is a compact factual projection rather than the entire original JSON object. Scores are **67.5516224188791%** and **68.4365781710915%**, rounded to **67.6% vs 68.4%†**. Both exact labels state max, the dataset references match, and both have 339 scored attempts, corresponding to 113 tasks × 3. Harnesses differ. The Opus row's display label omits a fallback suffix, but the actual per-benchmark data positively records fallback, supporting the dagger. The internal counts are retained only as an audit record; the user-approved public note does not speculate about routing or proportions.

AA's September 2026 Coding Agent Index v1.5 methodology uses DeepSWE v1.1 with isolated verification of committed patches. It averages three attempt scores per task, then averages equally across tasks. DeepSWE network access is restricted except the model API; provider browsing/search is disabled. Timeouts and completed safety refusals receive zero, with specific provider-error retry handling. Each public row represents an agent variant.

### Datacurve owner's separate mini-swe-agent board

Owner page: https://deepswe.datacurve.ai/

Owner raw leaderboard: https://deepswe.datacurve.ai/artifacts/v1.1/leaderboard-live.json

Owner repository: https://github.com/datacurve-ai/deep-swe

The raw leaderboard was generated at `2026-09-22T06:27:15.860279+00:00`. Astra max has:

```json
{
  "model": "gpt-6-astra",
  "harness": "mini-swe-agent",
  "reasoning_effort": "max",
  "config": "mini_swe_agent_gpt_6_astra_max",
  "pass_rate": 0.7323008849557522,
  "pass_at_1": 0.7323008849557522,
  "n_passed": 331,
  "n_attempted": 452,
  "n_tasks_attempted": 113,
  "n_runs": 4
}
```

This is **73.2%**, not the 74.1% Astra xhigh result shown by the default owner view. A scan of every owner JSON model row finds Opus 5 and Opus 4.8 but **no Claude Opus 5.5**. Therefore there is no matched Opus 5.5 mini-swe-agent result on that owner snapshot. Do not pair the owner's Astra 73.2% with AA's Opus 68.4%; that would mix evaluator, agent, and repeat count. Use the AA pair above, with a clear Codex vs Claude Code qualifier.

## Retrieval notes

All numerical selections were checked against benchmark-owner or original evaluator pages/data. Ego Lite task space 210 was used to read live rendered tables and obtain each page's public data. Browser-only static rendering sometimes prevented tabs from updating; exact DeepSWE values were consequently verified in the page's public server-rendered payload. No unpublished score was inferred. No image, draft, or existing data file was changed by this research.
