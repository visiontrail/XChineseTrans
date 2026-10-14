# When code outruns the plumbing

An original English Scion explainer for LeoGuoLabs, made with the established six-stage video-director workflow.

## Deliverables

- `scion-explained.mp4`: final video, 1920 × 1080, 30 fps, English narration and burned-in English subtitles.
- `review.html`: local player, chapter jumps, full narration, and source references.
- `captions.srt`: separately editable English subtitle file.
- `director-brief.md`, `shot-plan.md`, `script.json`, `public/timeline.json`: creative and timing source.
- `src/`: deterministic SVG/React motion graphics.
- `evidence/`: reference verification, revisions, render and final-file checks.

## Reproduce

Requires Node 24, Python 3, FFmpeg/ffprobe, and network access for initial dependency installation and optional speech regeneration. Pinned Node dependencies are in `package-lock.json`; speech dependency is in `requirements.txt`. Existing `public/voice` assets let you render without resynthesizing speech.

Run from this directory:

```sh
npm ci
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm run narrate
python3 scripts/sound.py
npm run stills
npm run render
python3 scripts/master.py
python3 scripts/build-review.py
npm run review
```

Open http://127.0.0.1:8756/review.html. The review server serves an explicit file allowlist and supports byte ranges.

The installed `video-director/scripts/check_delivery.py` was used for full decode, timeline, cadence, streams, and loudness inspection. Its results do not substitute for visual review or actual player checks.

## Media and sources

The source reference includes two complete freshly downloaded videos from the supplied X post. They are preserved under `source/`, with URLs, retrieval times, bytes and SHA-256 in `research/source-media.json`. Both exceed the project’s 50 MiB Git video threshold and are kept locally. They are reference material and are not composited into the new film. Intermediate render files are likewise preserved locally and excluded from Git.

Primary factual sources are linked in `research/claim-checks.json` and in the review page. Performance figures remain Anthropic-reported and use separate infrastructure/CI denominators. Animations are conceptual examples rather than measured traces or product UI.

Geist’s license is in `public/Geist-LICENSE.txt`. Voice uses Microsoft’s Andrew neural voice through edge-tts; no cloned voice. The short transition cue is original synthesis from `scripts/sound.py`.

Published to @LeoGuoLabs after user approval: https://x.com/LeoGuoLabs/status/2110407310346788915. The reopened public post contains the complete title and one 3:06 video. Playback advanced from 10.26 to 27.94 seconds with no media error. `publication-record.json` and `evidence/public-playback.json` record the result.
