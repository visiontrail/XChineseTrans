# A route around failure

## Intended result

A 24-second, 1920×1080, 60 fps motion film. Audience: technical readers who enjoy clear visual explanations. One gold packet follows a green path; a link breaks; an alternate route carries it to its destination. This is a conceptual routing metaphor, not a packet trace, a measured failover demonstration, or a protocol simulation.

## Art direction

LeoGuoLabs Light v1. Warm ivory #FDFBF7, fine stationary paper grain, forest green #1A4A3A, muted green #426454, dark gold #80601B and small gold/yellow fills. Geist sans serif, generous margins, no cards, no gradients, no glows, no shadows, no stock icons. One persistent gold circular subject; network lines support it. Flat graphic motion takes precedence over the reference article's optional photorealistic lighting.

## Timing and staging

120 BPM; 60 fps; 30 frames per beat. Six shots with a shared coordinate system and continuous subject identity. Text enters after its visual premise. Connection ends react to the break with damped motion; neighboring nodes respond later. The packet deforms with its speed and settles at the destination. Important events, music accents and SFX derive from `public/timeline.json`.

| Frames | Seconds | Main event | On-screen copy |
|---|---|---|---|
| 0–209 | 0–3.5 | A gold subject emerges within a moving path | A route / around failure. |
| 210–449 | 3.5–7.5 | Network unfolds; packet travels to the router | Start with a path. |
| 450–689 | 7.5–11.5 | Direct link breaks at frame 480; packet waits at router | Then a link breaks. |
| 690–929 | 11.5–15.5 | Alternate route draws; packet takes the upper branch | Change the route. |
| 930–1169 | 15.5–19.5 | Packet crosses the second node and reaches destination | Keep the destination. |
| 1170–1439 | 19.5–24 | Network yields to the persistent subject and closing thought | Another path. / Same destination. |

## Motion rules

All visual state is a deterministic function of frame. No elapsed-time CSS transitions, `Math.random()`, timers or mutable simulation state. Smooth paths preserve position across shot boundaries. The hero uses speed-dependent squash/stretch; cables use a localized damped impulse. These are designed physical cues, not a numerical physics simulation. No whole-frame shaking. Static text is allowed to hold for reading; motion should serve the story.

## Sound

Original synthesized stereo bed and event sounds. No external songs, voice cloning or narration. Sparse plucked tones, restrained pulse, a cable snap, path sweeps and a resolved arrival chord. The scene text carries the meaning with sound off. Soundtrack rendered at 48 kHz; final audio AAC.

## Acceptance

Inspect a beat contact sheet, full-size key frames and the break/arrival frame neighborhoods. Check for overlap, clipping, safe margins, text dwell time, discontinuities, and restrained subject deformation. Export H.264/yuv420p + AAC with fast start. Fully decode the final file; measure duration, frame count and audio peak/loudness; play and seek the final MP4 in a real player. Keep actual correction history in `research/iteration-log.md`.
