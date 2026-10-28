# GPT-6.1 Terra Computer Use delegation

- Source: https://x.com/xiangning0/status/2115108633755398186
- Published: https://x.com/LeoGuoLabs/status/2115258799133163982
- Observed: 2026-10-28 Asia/Singapore
- Format: standalone English post, including an adapted reusable prompt.
- Source: The author reports Terra is faster than Astra for computer use and prefers not to use it for coding; this is an individual experience, not a controlled benchmark. The author's reply says Astra is better in effect but slower. No independent speed test was performed.
- Screenshot, paraphrased: default to delegating UI work to a single gpt-6.1-terra subagent at xhigh; reuse it within a task, coordinate and verify through the parent agent; select model and effort in the delegation call; prefer suitable dedicated tools; apply existing permission rules and the user's current instructions. The screenshot uses fork_turns=none and requests sufficient task context.
- Global instruction location: ~/.codex/AGENTS.md. Project scope: project AGENTS.md. Higher-priority runtime instructions can restrict delegation.
- Verification: X composer returned a sent receipt and post URL; FxTwitter retrieved the exact full text and @LeoGuoLabs identity. Direct web access returned HTTP 403, and the authenticated browser page did not finish loading before its task space was closed. Public browser rendering was not verified.
