# When AI becomes the research team

An English narrated motion explainer and a standalone X post prepared for final review. The video uses the six-stage video-director workflow previously used for the satellite explainer; all narrative and scenes here are new.

## Deliverables

- `when-ai-becomes-the-research-team.mp4`: final normalized H.264/AAC export.
- `post.txt`: complete proposed English post.
- `review.html`: local review player and exact proposed text.
- `captions.srt`: English captions, also burned into the video.
- `poster.jpg`: preview frame.
- `brief.md`, `shot-plan.md`, `script.json`, `public/timeline.json`: brief, shot map, script and authoritative timeline.
- `src/`: editable deterministic React/SVG animation.
- `public/voice/`: generated audio and word-boundary timing, retained for reproduction without synthesizing again.
- `evidence/`: delivery measurements and review record. See QA record for which checks were performed.

## Reproduce

Node.js 24; Remotion 4.0.530; React 19.2.0. Geist font files and license are bundled. FFmpeg and ffprobe must be on PATH.

```sh
npm ci
node scripts/render.mjs --stills
node scripts/render.mjs
ffmpeg -i research-feedback-v1.mp4 -vf 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p' -c:v libx264 -preset fast -crf 18 -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -ac 2 -c:a aac -b:a 192k -t 218.466667 -map_metadata -1 -movflags +faststart when-ai-becomes-the-research-team.mp4
PORT=8753 node scripts/review-server.mjs
```

To rewrite and synthesize the narration, edit `script.json`, install `edge-tts==7.2.8` in a Python environment, and run `scripts/narrate.py`. The script reuses existing clips, so deliberately move the corresponding clip and JSON aside if replacing its text. It uses Microsoft Edge's generic `en-US-AndrewMultilingualNeural` voice at -3% speed; this is not a cloned person. External service availability is required only for new synthesis. Regeneration rewrites the timeline and SRT before rendering. `scripts/build-review.py` updates the review page and shot table.

## Evidence boundaries

Reported automation data and conditional research scenarios are not our own measurements. Diagram particles, curves and bars explain the argument; the curves are labelled schematic. The approved-code and autonomous-R&D percentages retain different denominators and dates. The tenfold result is conditional after full automation, not an 18-month forecast starting now. Research citations are kept in `research/verification.md`.

No source-video frames or audio are reused in the final film. Shapes are authored in React/SVG. Paper texture and licensed Geist files are reused from the established brand assets. The final mix contains narration only.

Publication is separate from artifact completion. The project AGENTS.md requires review of the exact final text and video before clicking Post.
