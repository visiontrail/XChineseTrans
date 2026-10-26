# Qwen4-Exp release-watch preparation

Checked on 2026-10-26 (Asia/Singapore). State: pending final content review; not published.

## Source chain and format

- Supplied post: https://x.com/leo114119/status/2114660267514634652
- The live post contains a reused image with X's “From Salio” link, rather than a full text Quote card. That link resolves to https://x.com/Mr_Salio/status/2114651829476762060.
- Selected format: native Quote of Salio's post with fresh English commentary for @LeoGuoLabs. This preserves the relevant original media under the project's original-source default.
- Salio is the earliest accessible source of this image in the observed chain. The cropped code image has no repository/client identity; its creator and underlying software are not established.
- Both live posts were read in Ego Lite. The Chinese source was switched from automatic translation to its original text. Full source text is saved in research/source-live.txt and research/original-live.txt. Public FxTwitter responses are retained only as source-text/media retrieval evidence.
- The source contains one English code image, showing a model list with qwen4-exp and qwen3.8-flash-next; neither selected post contains video. The original image is downloaded and visually inspected. It stays in the native Quote card; no duplicate upload or new graphic is needed.
- Existing Qwen lineup and RSI records concern different older stories. No existing record matched either current post ID.

## Verified claims and limits

1. Official model configuration: https://huggingface.co/Qwen/Qwen3.8-Flash-Next/raw/main/config.json. The downloaded file declares model_type = qwen4_exp and architecture = Qwen4ExpForConditionalGeneration. Saved as research/qwen-flash-next-config.json.
2. Official model card: https://huggingface.co/Qwen/Qwen3.8-Flash-Next. It describes Flash-Next as an experimental preview of the architecture that will underpin Qwen4 and provides weights and usage instructions. This supports the public copy's practical observation that a preview can already be inspected and run; we did not run or benchmark the model.
3. Transformers documentation: https://huggingface.co/docs/transformers/main/en/model_doc/qwen4_exp. It documents the architecture and lists a contribution date of 2026-08-26. The identifier is not evidence by itself of an imminent new launch.
4. Alibaba's 2026-09-22 announcement states Qwen 4 was in training: https://www.alibabacloud.com/en/press-room/alibaba-unveils-roadmap-on-full-stack-ai-strategy.
5. QwenCloud model changelog checked: https://docs.qwencloud.com/changelog/models. The most recent visible entry was 2026-10-22; no Qwen4 launch entry was found in this check. Targeted searches did not establish an official October 29 launch date or an Arena confirmation that Kalmia is Qwen4. Search absence is not proof none exists, so the copy only says this identifier alone cannot confirm those claims.
6. The screenshot's hyphenated qwen4-exp string and the official underscored qwen4_exp architecture key should not be silently equated as a verified client routing alias. The screenshot's application/repository was not identified.

The final copy avoids claiming a release date, anonymous-model identity, model superiority, or personal testing. Source/production notes remain outside the publishable text.

## Media

- Selected media: original post's one native image, preserved in its original colors.
- Local original: source-image.jpg, 1280 × 411.
- Retrieval URL, timestamp, byte size and SHA-256: research/media-record.json.
- No separate attachment; ALT on someone else's quoted image cannot be edited. Internal description: “Code snippet listing qwen4-exp and qwen3.8-flash-next, with qwen4-exp highlighted.”

## Review and publication

- Publishable text: post.txt.
- Target account confirmed in the live browser: @LeoGuoLabs.
- No publication authorization yet. The standing final-content review rule applies.
- Publication submitted: false. Public URL: none.

- Live composer verified: complete text exactly matches post.txt, correct Salio Quote card and source image are displayed, Post is enabled, and @LeoGuoLabs is the active account. Evidence: research/composer-check.json and composer-review.png. The composer remains unsubmitted for review.
