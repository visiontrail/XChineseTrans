# Claude Code context management — 2026-10-10 SGT

Supplied source: https://x.com/dotey/status/2094964831061155845 (Sep 2, 2026).
Source says disabling 1M context made usage last longer, especially on Fable 5.1. Attached media is a code screenshot; no video.

Live authenticated X conversation loaded after one Retry. Account shown: @LeoGuoLabs. It contains a later author correction:
https://x.com/dotey/status/2108669281802289375 (Oct 9 21:21:48 UTC)
https://x.com/dotey/status/2108669008283402744 (Oct 9 21:20:43 UTC)
Author now recommends deleting the old disable flag and trying auto-compaction around 300–400K. His chosen threshold is 300K, an anecdotal preference rather than a universal optimum.

Primary documentation checked live:
https://code.claude.com/docs/en/model-config#turn-off-1m-context
The disable flag is still supported and restricts native-1M models to a 200K window. A larger auto-compact setting cannot override this.
https://code.claude.com/docs/en/model-config#context-window-and-auto-compaction
/autocompact accepts k/M suffixes and saves the current model's window on recent versions. Higher-priority settings or environment overrides can prevent the requested value from applying.
https://code.claude.com/docs/en/costs#reduce-token-usage
Cost depends on actual context processed, caching, model and workload. Do not promise a savings percentage or imply 1M is billed when empty. Compaction summarizes history and may lose earlier detail.

Editorial decision: one standalone English post about the corrected method with one newly authored English tip image. No personal test claims, model-specific savings claims or unofficial source attribution in public copy. The old screenshot includes unrelated permission settings; it is research evidence, not selected attachment.

Later correction quotes https://x.com/lydiahallie/status/2108624109538291901 . Live full post read. Its seven-second English animation compares default ~967K versus /autocompact 400k and is relevant, so freshly downloaded it. Final media selected: tip-v1.png then lydia-original.mp4. X composer accepted both and video reported Ready. Source 60fps file needed no transcode.
Generated infographic used the built-in imagegen tool; prompt saved in image-prompt-v1.txt, exact command spelling and all text visually inspected.
Review endpoint: http://172.16.10.59:65224/review.html . Only review.html, tip-v1.png and lydia-original.mp4 are served. LAN endpoint checked; remote phone playback not claimed.
