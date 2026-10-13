# A route around failure

A self-contained 24-second motion study made with Codex, Remotion, React/SVG and an original procedural soundtrack.

Start with `route-around-failure.mp4`. Read the making-of in `article.html` or `article.md`. Open `review.html` through the local server for event jumps, frame stepping and delivered-frame timestamps. `workflow-zh.md` records the actual process in Chinese.

## Reproduce

Requirements: Node.js (tested with 24.15.0), Python with NumPy and Pillow (tested with Python 3.14.4), and FFmpeg/FFprobe on PATH. Package versions are pinned. Remotion downloads its official headless rendering dependency if not cached; it does not use your everyday browser profile.

Run from this directory:

```sh
npm ci
python3 -m pip install -r requirements.txt
python3 scripts/soundtrack.py
npm run check
npm run stills
npm run render
npm run master
python3 scripts/build-article.py
npm run review
```

The review address is http://127.0.0.1:8743/review.html. It binds only to localhost and supports byte ranges for video seeking. Set `PORT` if 8743 is already used.

Use the Python interpreter from your environment. On the machine used for this experiment, `/usr/bin/python3` invoked an unavailable Xcode setup path; the existing `/Users/leoguo/.pyenv/shims/python3` worked. No system license or system Python was modified. The exact local interpreter path is not required elsewhere.

The delivered package already contains the WAV, fonts and final MP4, so Python is only needed to regenerate assets or documentation. `npm run render` writes the raw render as `route-around-failure-v1.mp4`; `npm run master` writes the delivered `route-around-failure.mp4`. Mastering normalizes loudness and converts the measured Remotion full-range BT.601-family render to limited-range BT.709. If you change the rendering backend, inspect its color metadata before reusing that explicit conversion.

## Edit

- `brief.md`: audience, meaning, shot sequence, art direction, motion and review rules.
- `public/timeline.json`: FPS, duration and named visual/audio events. Preserve chronological motion-event order when editing.
- `src/motion.ts`: packet path and speed-dependent deformation.
- `src/Film.tsx`: artwork, text, node responses and transitions.
- `scripts/soundtrack.py`: original score, SFX, seed and audio sample positions.
- `scripts/render.mjs`: still selection and H.264 render settings.
- `scripts/master.mjs`: measured loudness and delivery encoding.
- `scripts/validate-motion.mjs`: complete subject-path numerical check.
- `prompts.md`: reusable phased instructions.

Caption holds and introductory choreography also have deliberately authored offsets in the composition. The timeline is not a universal no-code editor. Large event changes need a fresh visual review, and a different aspect ratio needs composition work rather than a blind crop.

## Verify

```sh
ffprobe -v error -show_format -show_streams -of json route-around-failure.mp4
ffmpeg -v error -i route-around-failure.mp4 -f null -
```

Expected delivered file: 1920×1080, H.264 High, yuv420p, BT.709 limited range, 60 fps, 1,440 frames, 24 seconds, AAC stereo at 48 kHz. Review `evidence/final-report.json` for the final hash and measured audio values. These are engineering and visual checks, not a claim of independent audience testing or expert subjective sound mastering.

The film is a conceptual routing metaphor. It is not a protocol simulation or a performance benchmark. No reference video/audio is included in the project package. The included Geist files retain their bundled SIL Open Font License at `public/Geist-LICENSE.txt`.

## Satellite revision

The current article has been revised around the new 36-second 3D satellite sample in `../satellite-beam-steering/`. The original article is preserved as `article-v1.md`, `article-v1.txt`, and `article-v1.html`. The routing video and its source remain available here.
