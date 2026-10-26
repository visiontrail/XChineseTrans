# Samsung TV privacy: source review

Reviewed 2026-10-26 (Asia/Singapore).

- Supplied post: https://x.com/huxlab/status/2114617661074399527
- Direct original / selected native Quote target: https://x.com/log4j/status/2113014142600953868
- Relevant author continuation: https://x.com/log4j/status/2113028209612644795
- Author describes telemetry patching as an initial plan: https://x.com/log4j/status/2113193765867516075

## Evidence and boundaries

Hux's Chinese original was read after switching off X automatic translation. The original researcher says they rooted a 2025 Samsung TV after seeing unusually targeted ads. The original post contains one terminal photograph, no video. The relevant continuation contains one security-policy.xml image and claims always-on microphone functionality, ACR, positioning, network mapping, profiling and 400 partners. Both original images were freshly downloaded and visually inspected. No relevant video was present in the original or selected continuation.

The terminal photo shows filesystem / shell output and Tizen-related desktop windows. The policy screenshot lists a package named csapi-tv-service-alwaysonvoice. These images are source-provided evidence, not tests performed by us. A package name alone cannot establish runtime recording, data transmission, consent state, or advertising causality.

Samsung's official US support page confirms that optional ACR, enabled by opting in to Viewing Information Services, generates signatures and collects information such as viewing history, device identifiers and IP address. Samsung says users may opt out via TV settings. These are vendor disclosures, not a fresh independent validation that every setting works as described:
https://www.samsung.com/us/support/answer/ANS10010616/

Samsung also documents microphone-based voice wake-up and controls; ordinary voice functionality is not itself proof of continuous surveillance for advertising:
https://www.samsung.com/ae/support/tv-audio-video/voice-assistant-issues-on-my-samsung-tv/

The final copy omits the unverified 400-partner data-flow claim, claims of frame-by-frame recording, performance causation, and any assertion that a clean replacement OS has already shipped. It treats continuous microphone surveillance as an allegation needing independent verification. The freedom to remove unwanted telemetry is an editorial judgment, not a claim that a verified tool is available.

A targeted web search found no official Samsung response to this specific log4j thread. This is a search result, not proof that no response exists. X's thread reader and author profile feed returned “Something went wrong. Try reloading.” Direct original and continuation pages loaded successfully. Latest-profile coverage is therefore limited; no claim that the full current thread has been exhaustively reviewed is made.

## Media selection

Use the native original Quote card and its one terminal photograph. Do not separately attach a duplicate image. The policy screenshot is research evidence only. No generated illustration is needed. ALT cannot be edited for another author's native quoted image.

## Publication

Prepared for @LeoGuoLabs. User approval is still required by the standing AGENTS.md final-content review rule. No submission is authorized by the bare link alone.

The live @LeoGuoLabs native Quote composer accepted all 348 characters. Its original text and terminal photo matched the selected source. The Post button was enabled. The screenshot was visually inspected. No Post click occurred.
