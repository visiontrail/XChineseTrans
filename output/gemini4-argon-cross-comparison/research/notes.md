# Gemini 4 Argon comparison research
Checked 1 October 2026.

## Publication scope
Requested adaptation of https://x.com/dotey/status/2105396970772942935 into one fresh standalone English LeoGuoLabs post with one newly generated cross-comparison image. The user permitted either Fable or Opus; Opus 5.5 is chosen to preserve continuity with the previous images. Final publication review is still required by AGENTS.md.

## Visual references
- output/agent-benchmarks-comparison/gpt6-astra-vs-opus55-grouped-v3.png
- output/agent-benchmarks-comparison/gpt6-sol-vs-opus55-grouped-v4.png
- assets/brand/leoguolabs-light-v1/reference-infographic-paper-v2.png
All three were visually inspected. They supply style and structure, not scores.

## Primary evidence
- Google benchmark table: https://deepmind.google/models/gemini/
- Google methodology PDF: https://deepmind.google/models/evals-methodology/gemini-4-argon
- Google announcement: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
- GPT-6 Astra model documentation: https://developers.openai.com/api/docs/models/gpt-6-astra
- Opus announcement/pricing: https://www.anthropic.com/claude-opus-5-5
- Opus system card: https://anthropic.com/claude-opus-5-5-system-card
- Zapier leaderboard: https://zapier.com/benchmarks
- Independent analysis: https://artificialanalysis.ai/articles/gemini-4-argon-google-top-three-labs

## Scope of scores
The figure selects 12 rows from Google's 19-row published comparison. It is a compiled comparison of published configurations, not a matched equal-compute experiment. Google's methodology defaults to maximum thinking/reasoning where reported and otherwise best available reasoning results. No aggregate ranking, overall-winner count, normalized radar plot, or cross-benchmark average is calculated.

Four groups preserve the old figures' engineering-oriented structure while adding the new model's long-context and video strengths. OSWorld is excluded because Google omits Claude: Anthropic reports online/offline aggregates while Google uses the offline subset. The old 81.8% Claude result must not be inserted.

## Changes from old images
Old Astra max AA mini-swe-agent Terminal score59.1 and AA coding-agent DeepSWE67.6 are not Google's current source choices58.2 and74.1. Likewise Opus59.6/68.4 are not66.4/74.2 from the new compilation. Different setups explain the difference; this does not measure temporal model improvement.
Old Science63.3 Astra/59.0 Opus is replaced by Google's current compiled68.1/63.3. Do not mix the AA and Google rows.

## Confirmed fallback marks
- Opus Terminal66.4: downloaded system-card page178 explicitly reports66.36 with safeguards and default server-side fallback; same rounded66.4 in Google's table. This is a confirmed vendor configuration. Do not infer routing or fallback frequency for Google's other source scores.
- Opus Automation42.5: Zapier version1.0.6 explicitly labels42.47 default fallbacks/max; refused tasks rerun through provider fallback routing.
- Only these two selected cells carry daggers.
- Other selected Claude results have no current row-specific fallback confirmation in the accessed evidence. Missing a dagger is not evidence that fallback was disabled.
- DeepSWE74.2 is independently visible in the system card page175, averaged over five trials.
- Anthropic's own Science58.7 fallback result is a different result and must not be substituted for Google's official-leaderboard63.3.

## Comparability details
- DeepSWE: Gemini self-computed with mini-swe-agent; Astra from official leaderboard; Claude from system cards.
- Terminal: Gemini self-computed; competitors from official leaderboard, highest-scoring thinking levels.
- PostTrainBench v1.1: all models computed by Google with OpenCode,10-hour budget, one H100, weighted aggregate across four base models/seven benchmarks.
- Science0.1: Argon verifier timeout increased6x; competitors from official public leaderboard.
- GraphWalks: all models computed by Google; selected256k–1M subset has200 problems; BFS F1.
- LVBench: without tools; Gemini1fps; Astra800frames; Opus600frames. Sampling differs because of API limitations.
- CWE-bench v1: official leaderboard pass@1 with pass@4 tie-break; both Argon/Astra score68% on the displayed metric.

## Editorial corrections
- Introductory token prices2/10 are20% of Astra10/50. Standard4/20 are40%, not20%. Standard pricing equals Opus5.5. No claim that standard Argon is one-fifth of Astra.
- The announced1M output limit can use Long Decode Continuation across API calls. Do not promise one uninterrupted HTTP response or1M visible answer tokens.
- AA measured1.99/task versus Astra3.26 at discounted prices; Argon used more output tokens. This is task cost on the Intelligence Index, not universal task cost.
- Google reports300+TiB already freed after deployment;500TiB–1PiB remains an estimate and is omitted.
- libgav1 improvement is2.7x versus an existing Rust port, not2.7x versus optimized C++.
- Large migrations remain under automated/manual auditing and testing before deployment.
- Staged access currently begins with trusted cyber defenders; wider paidAPI/AIUltra rollout is planned, with no dated public release.

## Browser access
Codex in-app browser successfully read the source post and confirmed the LeoGuoLabs session. Its Show original action did not visibly change the automatically translated body; official sources ground the rewritten factual claims.
Ego native app connection timed out. Ego CLI exists but the installed runtime returned taskSpace is not defined; no replacement browser was used for that research. Public official research was completed with the web tool and direct PDF download.
The system card exceeded web-tool content limits but curl downloaded its17.8MB PDF; PyMuPDF extracted it and rendered pages175/178 for visual inspection.

## Production
Built-in image_gen is used with three inspected image references. Exact prompt: image-prompt-v1.txt.
Status: image generated and copied into the project; all36 values visually checked; body accepted by the LeoGuoLabs Premium composer; one image attached;811-character ALT saved; normalized composer body matches the final draft. Publication not submitted; awaiting explicit final-content approval. The browser tab is retained for the next turn.
