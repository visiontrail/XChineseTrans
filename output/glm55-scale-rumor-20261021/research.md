# GLM next-base-model scale report — preparation review

Checked on 2026-10-21 (Asia/Singapore).

## Source and format

- Supplied X post: https://x.com/leo114119/status/2112860515383066898
- Read the live Chinese original (turned off automatic translation), attached image, and relevant author replies. The post contains one Chinese news screenshot, no native quoted post and no video. The default is therefore one new standalone English post for @LeoGuoLabs.
- Source screenshot is a Gate News brief attributed to ChainCatcher and Beating AI. The selected public media is a new English scale comparison; the Chinese screenshot is retained as research only.
- ChainCatcher: https://www.chaincatcher.com/article/2297830
- ChainCatcher's own source link resolves to this public Xueqiu post: https://www.xueqiu.com/3673395034/413098252 . Read its full notes through the live browser. It contains a commentary and reproduced Q&A from an unnamed expert interview, not an official Z.ai statement or an authenticated original transcript. No primary training records were supplied.

## Claim decisions

- The notes claim a next base model with 2.5–3.5 trillion parameters, replacing an earlier 1.6T rumor. They mention GLM5.5 in the question, but do not establish the product's official name. Public text and graphic say “next GLM base model”.
- Training loss stagnation, claimed recent resolution, serving targets and predicted Fable-class performance are unconfirmed statements in the notes. The claim is Fable-class, not specifically Fable 5.1. Do not state confirmed parity or an established release date.
- Published architecture convention for GLM-5 series is about 744B total parameters; retain that baseline, not the source post's rounded 700B. Hugging Face Transformers documentation covers GLM-5/5.1/5.2/5.3 and gives 744B/40B for the architecture: https://huggingface.co/docs/transformers/en/model_doc/glm_moe_dsa . The downloaded model metadata reports 753,329,940,480 stored checkpoint elements; do not relabel that raw checkpoint count as the nominal base-model parameter convention.
- Official Z.ai model card and release blog explicitly say GLM-5.3 uses the same base as GLM-5.2, with gains from post-training: https://huggingface.co/zai-org/GLM-5.3 and https://z.ai/blog/glm-5.3 . No new benchmark values are reproduced in this package.
- Calculation: 2500 / 744 = 3.3602; 3500 / 744 = 4.7043, rounded to 3.4–4.7 times. This is a conditional comparison of total parameters, not active parameters, inference cost or measured intelligence.
- Targeted official-site search did not locate Z.ai confirmation of 2.5–3.5T or Fable parity as of this preparation. Absence in the search is not proof that a future model does not exist.
- Final paragraph about affordable coding agents is editorial judgment about the possible benefit, not a claimed test result.

## Media and UI checks

- One image generated using built-in image_gen and saved as glm-scale-comparison-v1.png; exact prompt in image-prompt-v1.txt. Visually inspected: all required labels and values readable, no clipping; rumor status clearly separated; LeoGuoLabs signature present. No UI or execution evidence is simulated.
- ALT prepared separately in alt-text-en.txt.
- Ego Lite matched to its native app and tab inventory; did not choose everyday Chrome based only on the duplicated “Chrome” label. @LeoGuoLabs verified through the live profile link and composer context.
- Empty composer opened without replacing another task's draft. Full English text filled and accepted; Post enabled with 24,509 weighted characters remaining. Post was not clicked.
- Initial file chooser attempt targeted an AX label “Choose Files” that differed from the DOM “Choose File”; recovered in place after browser runtime reset and rediscovered browser IDs.
- Actual upload menu opened and Upload selected. FileChooser.setFiles failed because the extension's “Allow access to file URLs” permission was disabled. Clipboard fallback could not complete due native-pipe disconnection; the browser connection subsequently became unavailable. No settings were changed. Image upload and ALT entry were not verified. Composer preservation could not be reconfirmed after the disconnect; local copy is authoritative.
- No publication approval, submission, scheduling, or public post exists for this task.
