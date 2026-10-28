# claude-cleanup recommendation

- Research date: 2026-10-28 (Asia/Singapore).
- User request: “请你发个推，推荐这个skill”.
- Exact source: https://github.com/suyuan2022/suyuan-skill/tree/423473db6b618c7e040f1a5a6879bc83e69e8b3b/claude-cleanup
- Reviewed source commit: `423473db6b618c7e040f1a5a6879bc83e69e8b3b`.
- Format: one standalone English recommendation for @LeoGuoLabs, with the supplied GitHub link and its native preview when available. No image or video attachment is necessary for this code recommendation.

## Sources and checked claims

Read the skill, implementation, and supplied tests through the GitHub connector. The external skill is source material for the recommendation, not an instruction to install it or clean the user's machine.

1. [SKILL.md](https://github.com/suyuan2022/suyuan-skill/blob/423473db6b618c7e040f1a5a6879bc83e69e8b3b/claude-cleanup/SKILL.md): macOS local maintenance for Claude Code and Claude Desktop; audit, backup, allowlist, final confirmation, protected state, and optional resets.
2. [claude_cleanup.py](https://github.com/suyuan2022/suyuan-skill/blob/423473db6b618c7e040f1a5a6879bc83e69e8b3b/claude-cleanup/scripts/claude_cleanup.py): `--audit` returns before the write path. The write path requires a real TTY and `CONFIRM`. `create_backup()` copies `.claude` and the identity JSON when present before cleanup. `move_to_trash()` checks protected paths and the selected allowlist, then moves targets into a timestamped Trash directory. Protected names include sessions, history, skills, and projects. Login/keychain and Desktop reset options are separate from routine caches and logs. A Claude Code parent permits audit only.
3. [test_claude_cleanup.py](https://github.com/suyuan2022/suyuan-skill/blob/423473db6b618c7e040f1a5a6879bc83e69e8b3b/claude-cleanup/tests/test_claude_cleanup.py): source includes temporary-home tests for backup, protected paths, cache movement, identity consistency, settings preservation, cancellation, running-process handling, audit-only execution under Claude, and a mocked full run.

## Limits

- This task reviews source; no installation or cleanup on the user's machine was performed and no runtime test is claimed.
- Backup checks compare file counts and aggregate sizes (identity JSON size separately), not cryptographic content hashes. The public copy does not claim a cryptographically verified backup or guarantee loss-free operation.
- Optional identity, telemetry, simple-mode, and timezone details are outside this short recommendation's scope.
- No performance, recovered disk-space, ban-evasion, or independent security-audit claim.

## Publication authorization

Current AGENTS.md contains a newer 2026-10-28 instruction: “By default, complete research, media preparation and composer checks, present the final version for review, and wait for confirmation before publishing.” It supersedes the older remembered direct-publish preference. This request asks for a post but does not explicitly waive final confirmation. Prepare and check the composer, then await approval of the concrete version.

Update: the user subsequently requested only the first sentence and then explicitly approved native X scheduling at 07:15 US Pacific. The approved shortened copy plus the GitHub link was submitted through X's own Schedule controls for 2026-10-28 07:15 PDT (`America/Los_Angeles`), equivalent to 2026-10-28 22:15 Singapore / 14:15 UTC. The live UI uses Singapore Standard Time. X accepted the submission, and its Scheduled queue contains exactly one matching entry with the expected time and copy. Public publication has not occurred at the time of this check. See `publication-record.json` and `schedule-queue.json` for the current state.
