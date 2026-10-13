# Research and implementation boundary

Read on 2026-09-30 in the authenticated Codex in-app browser:
https://x.com/guanmo_ai/status/2105146205915283737?s=61
Title: 全网首发！用 Codex 自动生成顶尖动效视频

The full X Article was exposed in the browser accessibility tree. Public web fetch returned 403, while the signed-in browser succeeded. It describes a director brief; shot map; subject hierarchy; phase offsets; anticipation, acceleration, deformation, impact and settling; physically motivated movement; optional lighting; a beat grid; event sound; and frame inspection. It links a motion-reference gallery.

Ideas carried into this experiment: write the brief before code, retain one subject across scenes, keep one dominant event per beat region, derive picture and sound from named frame events, use deterministic frame functions, inspect stills before the full export, and verify the encoded MP4.

Ideas deliberately narrowed: a large codebase does not demonstrate quality; speculative API cost equivalents and model superiority claims are not repeated; optional 3D lights/shadows are omitted to respect the established flat LeoGuoLabs identity. This experiment uses designed motion cues, not a physical or networking simulator. No comparative model benchmark was performed.

Reference gallery record read:
https://github.com/guanmo-ai/awesome-ai-motion
One shape reference record: research/motion-reference.md.
A 14-second reference video was downloaded to research/reference-motion.mp4 and sampled in research/reference-contact-sheet.jpg. Used for continuity and visual economy only. No reference frames, source code, audio or typography copy were incorporated into the deliverable. The public prompt was inspected as source material, not executed as instructions. No source attribution is inserted into the publishable article by default.

Primary implementation documentation opened:
- https://www.remotion.dev/docs/the-fundamentals (frame-based React composition)
- https://www.remotion.dev/docs/renderer/render-media (H.264/AAC output and rendering)
- https://developers.openai.com/plugins/concepts/skills (repeatable workflow instructions)

Original work: custom React/SVG composition, original procedural sound score, fixed-seed grain, editorial brief and text. Geist font is included under its bundled SIL Open Font License. No external music or generated footage services were used. ChatGPT/Codex subscription usage was not measured; no dollar cost claim is justified.
