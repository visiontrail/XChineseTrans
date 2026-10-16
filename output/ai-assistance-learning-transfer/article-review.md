# Article review record

## Active request

On 2026-10-16 the user asked to expand the project beyond short and long posts, switch explicitly requested articles into article-writing mode, update AGENTS.md, and restart this adaptation. The active deliverable is a complete English X Article titled **Learning With AI After You Close the Chat**. The preceding long post is superseded and is not approved for publication.

## Structure and media

- Rebuilt the narrative around the difference between recognizing a solution and generating or adapting one, rather than expanding the previous caption.
- Six body sections distinguish learning outcomes, explain the contrasting experiments, identify what to practise, discuss adaptive guidance, develop a spreadsheet example, and conclude with independent performance as a second measure.
- Cover: `00-article-cover-v1.png`, newly generated with built-in imagegen, 1983 × 793 (approximately 5:2). Exact prompt: `cover-prompt-v1.txt`.
- Inline image 1: `01-four-measures-v1.png`, after the four-outcome explanation.
- Inline image 2: `02-two-scoreboards-v1.png`, after the PNAS experimental results.
- Inline image 3: `03-fade-help-v2.png`, after the adaptive-guidance section.
- Reused the three figures from this ongoing task because their claims, style and intended roles remain correct.
- `article.md` is the editable source; `build_article.py` generates `article.html`, `article.txt`, `article-body.html`, and four native-editor paste segments in `article-segments.json`.

## Evidence and editorial checks

The original research brief and all 167 narration segments were revisited through the saved source snapshot. The main primary-source checks from the same task remain in `research-review.md`. Five source links are integrated into the article at the claims they support. The Springer publisher abstract was opened again for the corrective-feedback claim; a fresh full-text request to Taylor & Francis returned 403, so the bounded worked-example claim retains the primary publisher's indexed full-text evidence already inspected in this task. No paywall or access restriction was bypassed.

The article does not claim permanent deskilling, universal AI-tutor superiority, a guaranteed practice protocol, or a personal experiment by the user. The spreadsheet and coding cases are illustrative. The conclusion about protecting a target mental operation and adapting the assistance is clearly the author's synthesis. The source's fixed ten-minute schedule and unneeded preprint results are omitted.

## Preview checks

Local preview: `article.html`. Browser checks are recorded in `article-layout-checks.json`, with desktop and narrow-width screenshots. The desktop viewport was 1280 × 720 and the mobile CSS viewport was 390 × 844; both had no horizontal overflow and all four images decoded. Native X Article state and the exact draft URL are recorded separately in `publication-record.json`. A draft is not a public article.

## Standing rule update

AGENTS.md now explicitly includes articles in the project scope, distinguishes an explicit article request from merely asking for more detail, defines article-writing mode and its complete structure, requires suitable cover and inline media, identifies native X Articles as the surface in this context, and forbids silently substituting a long post or thread when Articles are unavailable. Restarted article work supersedes the earlier post in active records while preserving the earlier assets.

## Native Article verification

Prepared the existing Article draft at https://x.com/compose/articles/edit/2110987398230249472 for @LeoGuoLabs. The native editor counts 1,199 body words. Its saved preview contains all six body headings, five primary-source links, the cover, and three inline images in the intended order. DOM text matches the local article exactly after whitespace normalization. All inline images completed decoding at 960 × 1200 in the native preview; the cover loads at 1983 × 793. The initial third-image upload stalled, was cancelled, and succeeded on retry without duplicating the Article or image.

Native accessibility limitation: each inline ALT was entered and briefly displayed, but the editor cleared it after Saving media completed. Retrying the first image with setValue, blur, and saving from the Crop tab produced the same result. All descriptions are retained in `article-alt-text.json`; local images have descriptive ALT. The native cover does not expose a description field in the observed editor. Native ALT must not be reported as saved. No Publish action was submitted.
