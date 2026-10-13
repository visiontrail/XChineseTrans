# A repeatable workflow for making videos with Codex

Making a video with Codex is easier to control when the work is divided into six stages: a director brief, a shot map, a shared timeline, motion and sound, review and revision, and final-file verification.

I used this six-step workflow to make *Steering without turning*, a 36-second satellite explainer. It moves from a complete spacecraft into an antenna array, shows how relative phase changes a beam's direction, then returns to a ground-pointing example. The finished video is one application of the process. The same sequence of decisions can guide a product demo, a scientific explanation, or a short visual story.

## 1. Write a director brief

Start by defining the audience and the one thing they should understand or feel when the video ends. Then set the scope, visual direction, and deliverables. Give Codex enough information to make choices that serve the same objective.

A useful brief answers five questions:

- Who is watching, and what can they already be expected to know?
- What single idea or action should remain with them?
- Which facts or events must appear, and what is outside the story?
- What should the images, typography, movement, and sound feel like?
- What must be delivered: duration, aspect ratio, resolution, language, audio, editable source, and review files?

For the satellite sample, the objective was to explain electronic pointing while the antenna panel stays fixed to the spacecraft. Link budgets, scheduling, and handover were outside that scope. The visual direction was warm ivory, forest green, restrained gold, and clear sans-serif labels.

Keep the brief short enough to consult during a revision. When a proposed effect competes with the central idea, the brief gives you a reason to remove it.

## 2. Turn the brief into a shot map

Give each shot an explanatory task. Define its subject, framing, action, text, transition, and the information the viewer should carry into the next shot. Choose the number and length of shots around those tasks.

Here is the map used for the completed sample:

| Time | Shot | Explanatory task |
|---|---|---|
| 0–6 s | Complete spacecraft | Locate the planar antenna |
| 6–12 s | Aperture close-up | Identify the repeated radiating elements |
| 12–18 s | Separated assembly layers | Expose the simplified feed structure |
| 18–24 s | Phase traces and array factor | Connect relative phase with beam direction |
| 24–30 s | Spacecraft and fixed ground terminal | Show the purpose of changing the pointing direction |
| 30–36 s | Return to the spacecraft | Reconnect the mechanism with the system |

The equal six-second sections belong to this sample. Another subject may need one long demonstration and several short connecting shots.

A transition should preserve a useful relationship: the same object, location, direction, or cause. For example, the aperture close-up retains the panel's orientation and repeated patches so the viewer can recognize what the camera has entered.

Choose the rendering tools after deciding what the shots need. This project used Three.js and React Three Fiber for geometry and cameras, Remotion for frame-based composition, and HTML/SVG for labels and plots. Remotion's [Three.js integration](https://www.remotion.dev/docs/three) supports that combination. A different shot map may call for recorded footage, flat graphics, or another renderer.

## 3. Establish a shared timeline

Assign important actions named events and frame numbers. Camera movement, object motion, text, and sound can then refer to the same schedule. Keep the timing definition in one canonical place when building a reusable implementation; separate scripts should read or receive it instead of maintaining independent copies.

This compact representation captures the timing used in the satellite sample:

```js
const fps = 60;
const totalFrames = 2160;
const shotStarts = [0, 360, 720, 1080, 1440, 1800];
const events = {
  phaseScene: 1080, // 18 s: introduce the mechanism
  sweepStart: 1140, // 19 s: start changing the angle
  sweepEnd: 1320,   // 22 s: reach 30 degrees
  tracking: 1440,   // 24 s: leave the 30-degree hold
};
```

The distinction between scene entry and action start matters. The phase scene gives the viewer one second to orient themselves, changes the angle over three seconds, then holds the result for two seconds.

For procedural animation, derive state directly from the requested frame. In this sample, camera position, layer separation, phase, and pointing are functions of local scene time. Rendering a frame directly therefore does not depend on playing every earlier frame first. That makes isolated revisions and repeatable checks much easier.

## 4. Build motion and sound around events

Choose what moves first, what follows, where it accelerates, and where it settles. An anticipation or a short pause should help the viewer read an action. Give labels enough time to be understood before asking the eye to follow something else.

For an explanatory scene, the visuals and numerical readouts should share the same underlying state. The sample's phase traces, beam-angle label, wavefront orientation, and array factor all follow one steering angle. An ideal eight-element, half-wavelength-spaced array demonstrates the relationship; all elements remain active. The model retains sidelobes and has explicit limits. The geometric principle is described in [Analog Devices' phased-array tutorial](https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part1.html).

Sound needs a comparable hierarchy. Use music for continuity and selected event sounds for emphasis. Decide whether a sound starts with an action, leads into it, or resolves afterward. A shared timestamp alone does not account for its attack and decay.

The sample uses an original Python/NumPy score at 100 BPM, with short cues around its scene changes. That tempo is a local choice. A beat grid helps organize emphasis; it does not require every object to move on every beat. The film has no narration, so captions and visuals carry the explanation when muted.

## 5. Inspect, diagnose, and revise

Render representative frames before committing to the complete video. Check each shot's opening, the moment that carries its meaning, and its exit. Add nearby samples around fast motion, overlaps, transitions, and changes in state. Look at full-size images for details and a contact sheet for the sequence.

Inspect specific things: can the subject be identified, do labels point to the right object, is the text readable at the intended viewing size, and does the visual result match the underlying state?

The first satellite stills revealed patches partly buried in a bevelled panel. Moving their geometry forward fixed the problem. A macro view also let solar wings overlap the title and sidebar; reframing around the aperture restored clearance. Those are actionable corrections, unlike asking for a vague increase in quality.

Record the defect, the change, and the frame used to verify it. Then review the changed shot and its neighbors. Numerical checks can complement visual review: this sample checks the array-factor peak against the commanded angle and the pointing line against the fixed terminal. Such checks establish internal consistency, not the validity of a complete radio system.

## 6. Verify the delivered video

Inspect the actual encoded file. Confirm duration, dimensions, frame count, codecs, color metadata, and audio streams. Decode the complete file to catch failures beyond the frames you sampled. Measure loudness on that file, then play it with sound and test seeking in a real player.

The satellite master is 1920 × 1080 at 60 fps: 2,160 decoded frames over 36.000 seconds. Its H.264 video uses 4:2:0 sampling and limited-range BT.709 color; the audio is 48 kHz stereo AAC. The final MP4 measured −18.00 LUFS integrated and −2.86 dBTP true peak. Local browser playback reached the end without a reported media error, and the review controls were checked at consecutive frames 1,320 and 1,321.

These results describe this file. They do not establish one required frame rate, loudness, or codec for every project. Set the delivery requirements for the intended destination, and preserve enough evidence to distinguish a requested setting from a measured result.

Deliver the video together with the brief, shot map, timing definitions, editable source, and a concise review record. That gives the next revision a reliable starting point.

The companion **`$video-director` Skill** packages these six steps as a separate, reusable workflow for different subjects. It was distilled from the completed work; the satellite film is its worked example. The reusable part is the progression from a clear brief to a verified file, with each creative decision represented somewhere it can be inspected and changed.
