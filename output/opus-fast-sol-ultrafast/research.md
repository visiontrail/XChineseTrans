# Opus Fast vs Sol Ultrafast

Checked 2026-10-10, Singapore time. Source: https://x.com/leo114119/status/2108723129485041932. Quoted chart: https://x.com/chetaslua/status/2108722464218116115.

Live authenticated source page read under @LeoGuoLabs. Source has one relevant comparison image and no relevant video. No prior matching source record found locally.

Corrections: supplied text says Sol Ultrafast is API-only; official OpenAI Docs establishes Codex and ChatGPT Work access on Pro $500 and eligible Enterprise/Edu. The supplied chart itself says no published Sol Ultrafast throughput and labels its approximate 280 figure unmeasured. Do not treat it as an observed speed tie. Peripheral evaluation rows are omitted.

Primary sources:
- https://platform.claude.com/docs/en/build-with-claude/fast-mode : Opus 5.5 Fast $8 input / $40 output per 1M; up to 2.5x output throughput; caching multipliers stack.
- https://www.anthropic.com/claude/opus : Fast available in Claude Code and Claude Platform.
- https://developers.openai.com/api/docs/models/gpt-6.1-sol : Standard $2 input / $10 output, Ultrafast 6x; long context above 272K input costs more; global rates exclude regional premium.
- https://developers.openai.com/api/docs/guides/ultrafast-mode : API availability.
- https://learn.chatgpt.com/docs/agent-configuration/speed : Codex/ChatGPT Work plan eligibility.
- https://vercel-docs.vercel.sh/ai-gateway/models/claude-opus-5.5-fast : retrieved page provider table 273 tps, 2.6 s latency; P50 on live traffic. Earlier search extraction returned 297; dynamic snapshots differ. Selected final snapshot 273. This is Vercel measurement, not our test or a vendor guarantee.

Price comparison: 8/12 and 40/60 imply about 33% lower input/output rates; not equivalent task cost. Cached input omitted because Vercel displayed base cache price while Anthropic documentation applies fast multiplier.

Authored comparison: imagegen built-in, comparison-v2.png. V1 retained; V2 changes snapshot 297 to 273, uses [1] for access, and narrows conclusion to input/output rates. Reviewed generated image for numbers, model names, footnotes, color, spelling, clipping and readability.

Pending final-content approval under AGENTS.md. No submission authorized yet.
