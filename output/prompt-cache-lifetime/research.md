# Prompt-cache lifetime adaptation

Source: https://x.com/jakevin7/status/2109605283236553163
Prepared on 2026-10-12 for @LeoGuoLabs as one standalone English text post.

The live authenticated source was read in its original Chinese, after disabling automatic translation. No video, image, quoted post, or external link is attached to the source. The source account is an independent commentator; provider documentation is the authoritative source for the proposed API claims.

## Original source text

很多人都不知道但是却极其重要的一个事情：模型的缓存过期时间（TTL）

deepseek 官方说的是几小时~几天；
Codex 则是5–10 分钟，也就是 5 分钟一过，你没有接上继续使用，Cache 就当做不命中了。
Claude默认 5 分钟、命中刷新，然后可以付费可提至 1 小时；
Gemini 默认 1 小时；阿里/Kimi 默认 5 分钟；智谱约 1 小时。

可以看到大部分模型厂商的过期时间都是 5 分钟，而 DeepSeek 则是可以长至几天。
deepseek 的 infra 确实太牛逼了。

## Relevant author replies

- https://x.com/jakevin7/status/2109636325594796210 — author acknowledges the five-minute Claude value may refer to the API.
- https://x.com/jakevin7/status/2109648994016391176 — author writes: 我的问题，之前应该每个都查证下的.
- https://x.com/jakevin7/status/2109637022340284483 — author links DeepSeek API pricing to cache implementation; this causal magnitude was not verified and is not asserted in the adaptation.

## Primary verification

| Provider | Verified scope and policy | Official source |
| --- | --- | --- |
| DeepSeek | Current guide says unused cache is cleared usually within a few hours to a few days and cache hits are best effort. This is typical eviction behavior, not a guaranteed multi-day TTL. | https://api-docs.deepseek.com/guides/kv_cache/ |
| OpenAI | GPT-5.6 and later use a 30-minute minimum from the latest write or reuse. Earlier-model policies vary: in-memory typical inactivity 5–10 minutes (up to one hour); supported extended retention up to 24 hours. These API settings do not establish one subscription-Codex TTL. | https://developers.openai.com/api/docs/guides/prompt-caching |
| Claude | API default five minutes, refresh on reuse. One-hour option charges more for cache writes. Current docs retrieved through web tool; direct shell retrieval redirected to a regional availability page and was not used as a documentation source. | https://platform.claude.com/docs/en/build-with-claude/prompt-caching |
| Gemini | generateContent explicit caching defaults to one hour when unset, is configurable, and charges for storage duration. Implicit caching is separate. The current Interactions API only supports implicit caching. | https://ai.google.dev/gemini-api/docs/generate-content/caching ; https://ai.google.dev/gemini-api/docs/caching |
| Qwen | Alibaba Model Studio explicit caching lasts five minutes with hits resetting the period. Implicit caching has no fixed validity period and is managed by the system. Applies to supported models and the documented interface. | https://www.alibabacloud.com/help/en/model-studio/context-cache |

Kimi and Zhipu timing claims were omitted because the focused primary-source lookup did not establish comparable policies. No universal provider ranking or guarantee of lower total cost is proposed. The final paragraph is a technical opinion and suggests measuring actual usage; it does not claim personal testing.

## Delivery

No new graphic is necessary for this short text comparison. No source video exists, so no video download is required. No ALT is applicable.
Final English copy: post-en-v1.txt. The user approved the exact final copy with “确认发布”. Published and publicly verified: https://x.com/LeoGuoLabs/status/2109655219059699978 . The reopened page shows @LeoGuoLabs, the exact 1,038-character approved text, standalone format, and zero media attachments. Evidence is saved in public-verification.json, public-page-dom.txt, and public-page.jpg.
