# DeepSeek and Ascend — publication record

- Source: https://x.com/0xLogicrw/status/2115018092317401488
- Native Quote target: https://x.com/SemiAnalysis_/status/2112965533754675280
- Primary report: https://newsletter.semianalysis.com/p/huawei-deepseek (21 October 2026)
- Supporting repository: https://github.com/tile-ai/tilelang
- Published: https://x.com/LeoGuoLabs/status/2115259336230584746 (28 October 2026, Singapore)
- Status: publicly verified in Ego Lite: account, full text, image loading and ALT, and quoted SemiAnalysis card. Original target has a report link card and no video.

## Published text

DeepSeek is adapting its software to make better use of Huawei Ascend: fewer data transfers, overlapping work, and more efficient communication between experts.

The next question is how much those changes improve full-model performance. A faster individual operation is only part of the picture.

## Evidence and limits

SemiAnalysis tested 1,055 BF16 GEMM shapes with stock Huawei kernels on the 950PR_9579. It says AutoSchedule reduced execution time by up to 40% for a single operation, especially at smaller sizes. This is not an end-to-end model benchmark. The report describes FlashMLA's co-location of cached values and scales, TileLang's overlapping transfers and computation, and shared resource contention in expert communication. The original article identifies 950PR as a prefill and recommendation chip; its result cannot be treated as a 950DT training result. Reported chip-comparison figures in the intermediary's post were omitted because their detailed calculation is presented in the source figures and is unnecessary to the point.

Image: explainer.svg and explainer.svg.png. The raster was visually inspected and uploaded with descriptive ALT.
