# Updated article consistency check

- Draft: `../article.md`; public-facing English, production workflow is the subject.
- Preserves previous article untouched; uses new sample as a targeted second experiment.
- Describes old React/SVG routing film and new Three.js + React Three Fiber + Remotion stack accurately.
- Uses the actual six 6-second scenes from the current brief and source, 36 seconds / 2,160 frames at 60 fps.
- Reference evidence is correctly separated: 12,543 automated frames, 67 distinct visually reviewed sampled frames, 720p analysis copy. No assertion that every frame was manually inspected or that the 1080p copy had received equivalent review.
- No attribution/link to the supplied source author in reader-facing copy; reference retained in research records.
- No inference about the reference creator's software stack.
- Phase convention is explicit: array along +x, broadside +z, exp(+iωt), outgoing exp(−ikr); −90-degree adjacent phase step steers +30 degrees for d = λ/2.
- Eight elements stay active; equal amplitude, normalized magnitude array factor, sidelobes remain. Formula agrees with `src/motion.ts`.
- Names numerical check and its scope: 360 phase frames, scan resolution 0.1 degrees, peak error at most 0.05 degrees; independent geometry check for tracking scene.
- RF/orbit model limitations retained; no claim of continuous service, measured performance, full RF solver, or real propagation time.
- Real iteration issues included: bevel occlusion, macro solar-wing overlap, tracking heading clearance.
- Source WAV measurements retained as source-only; no listening-quality or encoded-file measurement claims.
- One `[FINAL_QA]` placeholder remains for root to replace with verified final output specifications, encoded loudness, full decode/playback, and any limitations.
- Commands assume parent will provide `scripts/master.mjs`; package.json already declares it. Do not ship command without that file.
- No cost, total production duration, benchmark, universal best-tool, or final quality claim invented.
