# GibberLink mode — preparation, 2026-10-19

User: supplied Hux post and requested slightly deeper coverage of Gibberlink mode itself. Prepared English native Quote for @LeoGuoLabs; final review required, no submission authorized yet.

## Source chain and target

- Supplied: https://x.com/huxlab/status/2112123190667542846 ; live full Chinese text read in authenticated built-in browser. Embedded video attribution points to Luqman Ali.
- Intermediary: https://x.com/luqman_talks/status/2111790481759945007 ; live full post and Community Note read. The note corrects the spontaneous-switch claim; primary sources below independently establish the mechanism.
- Selected native Quote target: https://x.com/ggerganov/status/1894057587441566081 . Linked by ElevenLabs' official retrospective. Gerganov created ggwave, NOT GibberLink; his post explicitly says the demo was sent to him. Live post and relevant author continuations verified. Same hotel/wedding demo, published February 2025, earlier than October 2026 reposts. Do not claim this is the demo creators' own original X upload.
- GibberLink creators: Anton Pidkuiko and Boris Starkov. Repository links creator's original YouTube upload: https://www.youtube.com/watch?v=EtNagNezo8w . Author X search yielded no result; do not invent an original creator status.

## Primary evidence

1. https://github.com/PennyroyalTea/gibberlink — explicit prompts to switch after identifying AI; decoder demo; authors and original video.
2. https://github.com/PennyroyalTea/gibberlink/wiki/Repro-steps-for-demo — gibbMode tool requires recognizing an AI AND confirmation to switch.
3. https://github.com/PennyroyalTea/gibberlink/blob/main/hackathon_demo/src/components/ConvAI.tsx — gibbMode ends voice session; normal text chat continues through genMyNextMessage and /api/chat; replies passed to sendAudioMessage. System prompts request short English messages. No learned secret language or latent-state exchange.
4. https://github.com/PennyroyalTea/gibberlink/blob/main/hackathon_demo/src/utils/audioUtils.ts — ggwave.encode on message string; AUDIBLE_FAST or AUDIBLE_FASTEST; ggwave.decode and UTF-8 TextDecoder; no encryption layer in these operations. Snapshot retained in research/audioUtils.ts with trailing whitespace normalized.
5. https://github.com/PennyroyalTea/gibberlink/blob/main/hackathon_demo/src/app/api/chat/route.ts — ordinary model completion still performed. Do not claim removing LLM inference cost.
6. https://github.com/ggerganov/ggwave — FSK, Reed-Solomon ECC, documented 8–16 bytes/sec depending on parameters. Rate belongs to library documentation, not measured benchmark of this video.
7. https://elevenlabs.io/blog/what-happens-when-two-ai-voice-assistants-have-a-conversation — official demo history and links to early X uploads.
8. Relevant author continuation: https://x.com/ggerganov/status/1894099024715636811 — demo can be decoded using Waver.

## Editorial judgment and limits

- API/direct-network preference, deployment testing of codecs/noise suppression, and readable booking records are engineering judgment; no claimed local deployment, real hotel booking, universal phone compatibility, or measured savings.
- Omitted ungrounded 80% efficiency, universal error-proof communication, instantaneous coordination, AI awakening, autonomous invention, and secret/encrypted language claims.
- Public copy explains the technology itself; research process, download provenance, review state, and limitations of source attribution stay here.
- No added infographic: the actual demo carries the useful visual information.
- Account session visibly @LeoGuoLabs. Exact Quote target must retain native video. No redundant separate upload.

## Media verification

Fresh source download: 3,393,365 bytes, 1280×720 H.264 video, stereo AAC at 48 kHz, 69.696 seconds. Full audio/video decode completed with zero errors. Representative beginning/middle/end frames inspected; native source playback advanced from 0:16 to 0:01 remaining. No listening-based audio quality assessment is claimed. The file preserves the source video and native English on-screen text. SHA-256 and retrieval time are in publication-record.json.

Composer retained the complete text and the native Quote target, with 23,410 characters remaining. Screenshots show the text and the expanded original video card. Awaiting final content review; no Post click performed.

## Revision 2

User requested simplification and their personal impression of AI feeling increasingly like another intelligent species. Removed modulation details, rate figures, and deployment/audit digression; retained text-to-tones mechanism, prompted switch, and ongoing LLM generation. Final paragraph is explicitly subjective. Previous text preserved in post.v1.en.txt; revised text awaits review. Same Quote target and verified video.

## Approved scheduled publication

User approved revision 2 for US West Coast morning 08:20. Scheduled the next occurrence, 2026-10-19 08:20 America/Los_Angeles (PDT, UTC-7), equal to 2026-10-19 23:20 Asia/Singapore and 15:20 UTC. X schedule UI explicitly showed Singapore Standard Time. Submitted using X native Schedule, then verified the queue and reopened the scheduled item to confirm the complete approved text, personal reflection, GitHub link, and native Quote target. No public URL exists yet. One-time heartbeat gibberlink is set for 23:25 Singapore time to verify publication and advancing video playback, reconcile existing post before any action, avoid duplicates, and pause after the check. Screenshots and AX records are in research/.

## Public publication verified

Actual public URL: https://x.com/LeoGuoLabs/status/2112202109550559588 . Live page shows @LeoGuoLabs and 11:20 PM Oct 19, 2026 Singapore time, matching 08:20 America/Los_Angeles. Complete English body matches approved revision 2 after whitespace normalization, including the personal reflection. Followed the native Quote card to https://x.com/ggerganov/status/1894057587441566081 and returned to the public post. The GitHub shortlink resolved to the correct repository in the built-in browser. Refreshed native scheduled queue no longer contains GibberLink. The public post contains one native quoted video; read-only DOM samples show playback from 39.876045 to 58.072476 seconds, paused=false, readyState=4, no media error. Initial page player required scrolling into view and starting playback; no content was edited or reposted. One-time automation gibberlink paused after successful verification.

The same public video subsequently reached its natural end: currentTime=duration=69.695999 seconds, ended=true, readyState=4, error=null. Completion screenshot and DOM sample retained.
