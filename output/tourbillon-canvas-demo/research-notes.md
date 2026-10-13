# Tourbillon Canvas demo — research notes

Checked on 2026-10-06, Asia/Singapore.

- Supplied post: https://x.com/leo114119/status/2107100744742760846
- Original embedded video post: https://x.com/Inmerson/status/2107036480917160250
- Shared app link: https://share.gemini.google/hHCZZhDoSLsA
- Shared link redirected to https://gemini.google.com/share/d39410262ad1?skid=ccca4cae-223e-4357-a8f3-13d8e8372482 but remained blank in the built-in browser. A web-tool read of the share page was also inaccessible. No live app execution was verified.
- Read the supplied post in its original Chinese using Show original; read the original Inmersion post in the authenticated built-in browser.
- Original video playback was observed: duration 156.866 seconds, currentTime 34.46513, paused false, readyState 4, error null. The video showed a mechanical visualization with on-screen controls and black/gold styling. This confirms the recording played; it does not validate mechanical accuracy or the app's live controls.
- The supplied post describes five chapters, three view modes and an acoustic oscilloscope. These details are retained as its description of the demo; not every mode or chapter was independently tested.
- Both posts label the model Gemini 4 Argon. The exact model identity was not independently established, so post-en-v1.txt uses Gemini Canvas without that model-version claim.
- Omitted the supplied post's assertion that the horological parameters are real and individually verifiable; no technical accuracy audit was performed.
- Initial draft format was a standalone English post, text only. After the user's follow-up requiring fresh downloads whenever a source post contains video, the original video was downloaded and prepared as the default direct attachment for this draft. The user subsequently approved publication of the displayed text and video. No source attribution added to publishable copy, following project instructions.

## Fresh video download

- Project `AGENTS.md` was updated to require fresh video downloads even during draft preparation, direct video attachments by default for standalone adaptations, and a local download while preserving native media for explicitly requested Repost or Quote Post formats.
- Built-in-browser `downloadMedia` located the correct video but timed out after 55 seconds. The page asset inventory exposed no video file asset.
- FxTwitter metadata for the already verified original status identified video ID `2107035822830596096`. The actual media bytes were downloaded directly from X's `video.twimg.com` CDN using sequential HTTP byte ranges.
- Download: `tourbillon-source-v1.mp4`, 27,107,204 bytes, SHA-256 `56ba97aa5a8ee8499389430e764a76cf05457ebdea5a3044a9169069a9ec0549`.
- Actual downloaded file: 1152 x 720 H.264 video, AAC stereo audio at 48 kHz, container duration 156.928 seconds. Selected the highest-bitrate MP4 variant listed in the metadata. The metadata's larger source dimensions are not the downloaded file's dimensions.
- Full video and audio decode passed using FFmpeg. Three extracted preview frames were inspected and matched the mechanical visualization, controls, oscilloscope, and black/gold presentation of the source recording.
- Records: `source-media-metadata-v1.json`, `video-download-record-v1.json`, `video-probe-v1.json`, `video-decode-v1.log`, and `video-preview-v1.jpg`.

## Publication

- User approval: `按照这个要求发布吧`, after the complete standalone English draft and downloaded video had been displayed in the conversation.
- Published under the live authenticated `@LeoGuoLabs` account as a standalone English post with the downloaded video directly attached. Text: `post-en-v1.txt`.
- Actual URL: https://x.com/LeoGuoLabs/status/2107144691791892905
- The composer accepted 368 characters and showed the attached file as Ready before submission.
- Reopened the actual status page and read the complete published text; it matched the approved draft exactly. One direct video attachment was present; no quoted source card was used.
- Public video duration 156.933 seconds, resolution 1152 x 720. Playback advanced from 29.613039 to 63.795437 seconds with paused false, readyState 4, and error null. The player was muted during this check.
- Publication evidence: `publication-record-v1.json` and visually inspected `published-post-v2.jpg`. The first screenshot used fullPage plus clip and was misaligned; v2 is the correct screenshot containing the author, complete text, and video.

## Supplied Chinese text

Gemini 4 Argon 生成的双轴陀飞轮机械模拟

是一支完整的奢侈品腕表品牌广告片—— 5 章分镜 + 3 种视图模式 + 声学示波器，而且片子里塞满了真到可以逐条查证的钟表学参数。

还是 Gemini Canvas 交互应用，不是文生视频
但它的呈现形态是"广告片"：黑底、金色机构、白色大字标题、章节卡
