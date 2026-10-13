---
name: video-director
description: "Create an actual video from a topic, story, or creative brief using a director brief, shot plan, shared timeline, coordinated motion and sound, visual revisions, and delivery checks. Use for original explainers, motion graphics, product films, narrative shorts, and similar authored sequences. Simple trimming, transcription, and format conversion do not need this workflow."
---

# Video Director

Turn an idea into a watchable video and an editable project. Use the six stages below as the production workflow. They are **not** a requirement for six shots, equal scene lengths, any particular topic, or a fixed visual style.

Honor the user's topic, audience, language, brand, aspect ratio, tools, existing project, and deliverables. Derive missing low-risk details from context and state practical assumptions; ask only for missing inputs that materially block the work. When asked to make a video, continue through the actual render and delivery rather than stopping with a plan or prompt.

## 1. Director brief

Write a compact brief before building scenes. Capture:

- Audience and the single idea, feeling, action, or change the viewer should take away.
- Content scope: what the film shows, what it leaves out, and which claims or depictions need sources.
- Narrative spine: a causal chain, emotional arc, transformation, contrast, or demonstration appropriate to the topic.
- Visual language: subject hierarchy, palette, typography, framing, motion character, and any supplied identity.
- Delivery intent: runtime or useful range, aspect ratio, resolution, frame rate, sound/voice/subtitles, output format, and editable assets.

Keep concept, illustration, simulation, captured evidence, and measured performance distinct where that distinction affects the story. For fiction or expressive work, don't impose engineering explanation or unnecessary fact-checking.

Choose the implementation after understanding the shots. 2D vectors suit clear graphics; 3D suits spatial structure and camera movement; recorded media suits real demonstrations; generated assets can suit illustration or atmosphere. Combine them when useful. Verify the tools available in the current environment. Do not make a particular renderer or paid service a dependency of this skill.

## 2. Shot plan

Give each shot a viewer-facing purpose. Record its duration, framing or scale, main action, text, entrance/exit, continuity anchor, and sound role. Scene count and timing follow the content.

A cut, push-in, reveal, or exploded view should reveal a relationship or advance the story. Keep the subject identifiable across scale changes. Plan readable attention windows; do not make the viewer decode several new relationships at once. Establish a text-safe region in the actual delivery aspect ratio.

For supplied references, extract useful visual constraints and techniques only as needed. Do not reproduce the whole reference analysis in the finished article or infer its software stack from appearance. Use original or appropriately sourced assets for the new film.

## 3. Shared timeline

Make one timing definition authoritative for shots, actions, titles, camera moves, voice cues, and sound events. For a new code-rendered project, use integer frames, zero-based indexing, and half-open intervals `[start, end)`. Existing projects may keep another explicit convention if used consistently.

Read [references/timeline.md](references/timeline.md) when implementing the timing layer or using the bundled delivery checker. It includes an adaptable JSON example and timing semantics.

For procedural animation, derive scene state directly from the requested frame: `state = f(frame)`. Do not accumulate wall-clock deltas or depend on playback history. Numeric readouts and the behavior they describe should use the same model state. In edited/generated footage workflows, keep trims, overlays, captions, and sound synchronized to the edit timeline; deterministic code does not make generated content physically correct.

Keep factual quantities separate from presentation timing. A beat may select when to start a reveal; it must not change the equation or invent a measurement.

## 4. Motion and sound

Give motion a purpose and a suitable response. Use anticipation, acceleration, deformation, impact, overshoot, and settling selectively. Rigid hardware, type, organic subjects, and signals should not all share one spring preset. Offset secondary actions so the intended subject remains dominant.

If music is useful, define a beat grid at the selected tempo and place accents intentionally. Cue sound from named timeline events rather than an independently typed list of approximate seconds. Allow pauses and off-beat events when the story needs them. Do not move every object on every beat.

Choose silence, music, narration, ambience, and event sound to fit the brief. If using speech, leave reading/breathing time and keep other audio from masking it. Use original or licensed audio. Document provenance with the project, not as unnecessary on-screen production labels.

## 5. Inspect and revise

Render representative frames early, before the expensive full export. Cover every planned shot and dense or important transitions. Inspect the actual images at delivery size and a practical viewing size, not only the source code.

Check composition, hierarchy, clipping, contrast, object thickness/occlusion, text readability, continuity, timing, and any domain-specific causal relationships. Then inspect short motion segments around important events; one attractive still does not prove the movement works. For speech/audio, listen when playback is available. Signal measurements alone cannot establish a good mix or intelligible narration.

Record concrete defects and the change that addresses each. Preserve useful before/after evidence when it helps explain a revision. Change the relevant geometry, timing, framing, or mix rather than hiding defects with effects. For quantitative subjects, validate meaningful invariants against the actual production functions; don't replace visual review with tests or write tests that only mirror implementation wording.

Do not label a sample-based visual review as manual inspection of every frame. Keep automated coverage, visual coverage, and audio listening coverage explicit.

## 6. Verify the delivered file

Render the final video, then check the **encoded delivery file**. Verify the requested dimensions, rate, duration, decoded frame count, streams, color handling, and playback. Check the audio from the final file if it contains audio. Select loudness and peak targets for the actual destination rather than enforcing one universal value.

The optional standard-library helper `scripts/check_delivery.py` uses installed FFmpeg/ffprobe to fully decode a video, report stream metadata, measure audio loudness when present, compare an optional timing manifest, and extract review frames. It does not certify visual quality or listen to audio. Use it when useful, or retain an existing checker that already provides equivalent evidence. If a tool is unavailable, preserve the result and report exactly which check remains incomplete.

Play the final file through the intended player or delivery surface when available, including the end and a seek. Verify a replacement export again where a change invalidates earlier evidence. Once relevant checks pass, stop adding tests without a new reason.

Deliver the actual video, requested text, and the editable project/resources needed to reproduce it. Record relevant dependency versions and reproduce commands. Keep source media, intermediate exports, and final exports distinguishable. Report timings only for the steps actually measured, and distinguish assets prepared from publicly published content. Publishing follows the user's chosen destination and its existing authorization requirements; it is not implied by making a local video.
