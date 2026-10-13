# Steering without turning

36-second, 1080p/60fps satellite phased-array explainer for LeoGuoLabs.

- `steering-without-turning.mp4`: mastered delivery file
- `article.html` / `article.md`: six-step English workflow article
- `article-review-zh.html` / `article-review-zh.md`: complete Chinese review translation
- `video-director.zip`: separate reusable Codex Skill
- `article-v2.*`: retained earlier article revision
- `review.html`: MP4 playback and frame viewer
- `workflow-zh.md`: Chinese production and review record
- `research/frame-audit-zh.md`: detailed reference analysis
- `src/`: deterministic Three.js / React Three Fiber / Remotion source
- `evidence/`: numerical, decode, render and playback evidence

## Reproduce

Tested with Node 24.15.0 and Python 3.14.4 on macOS ARM64. Install FFmpeg separately (the mastering script uses `/opt/homebrew/bin/ffmpeg` on this machine). The renderer reuses the prior experiment's headless Chromium if present; otherwise Remotion can provision its supported browser.

```bash
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

Open http://127.0.0.1:8744/review.html. The local server supports HTTP byte ranges for seeking. No API key or paid video-generation service is required to render this source project. npm package and font licences still apply to their respective components.

## Technical scope

The ideal 8-element narrowband uniform linear array factor is calculated. Spacecraft geometry, its 64 illustrated patches, the exploded assembly, ground path, wavefront period and beam footprint are schematic. This is neither a commercial spacecraft CAD model nor an orbital/RF simulator. Real element patterns, coupling, losses, polarization, wideband squint, link budgets and handover are not simulated. All elements remain active; phase steering is not sequential element switching.

The reference video is retained only in the local research directory and excluded from the portable project ZIP. Its frames are analysed, not included in the new film.
