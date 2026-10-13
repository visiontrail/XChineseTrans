# Actual iteration log

## Setup

- Read the complete source X Article in the signed-in browser after a public-fetch 403.
- Selected a 24-second conceptual routing story; wrote a six-shot brief and shared event timeline before the composition.
- Installed locally pinned Remotion 4.0.530 and React 19.2.0. Kept the work inside this output directory.
- The shell's system Python selected an Xcode stub and failed with a license message. Used the already installed Python 3.14.4 interpreter under pyenv; did not accept or change any system agreement.
- Ego Lite native UI reads timed out twice, and its browser connections returned a request-policy load error. Render work continued independently.
- Created original 48 kHz stereo soundtrack and deterministic grain. Initial audio sample peak: -2.85 dBFS.
- Started first-pass key-frame rendering; Remotion downloaded its official headless rendering dependency.

## First visual inspection

- Key frames 90 and 330 exposed a real stacking defect: the absolutely positioned paper layer was painting above the unpositioned SVG, washing out all text and strokes. Moved the SVG into an explicit positioned layer above the paper. Preserved both failed samples under research/first-pass/.
- Moved scene headings down by 33 px to give the persistent header more breathing room.
- Added a restrained rotating router arc during the decision hold, so the pause communicates ongoing rerouting rather than a frozen frame.

## Encoded export inspection

- Remotion rendered the 1,440-frame H.264/AAC draft in 38.32 seconds on this machine. This is render time only, not total production time or a speed benchmark.
- Complete decoding passed. The browser played the draft through to its ending with readyState 4 and no media error.
- FFprobe exposed full-range yuvj420p with BT.601-family matrix metadata in the raw export, plus 42.7 ms of AAC padding. Added a final FFmpeg mastering pass to convert to standard limited-range yuv420p/BT.709, retain 60 fps and trim the delivered container to 24 seconds.
- The first soundtrack measured about -25.8 LUFS with loudnorm. Added measured two-pass normalization targeting -18 LUFS and -2 dBTP, leaving space below clipping after AAC encoding. Final measurement is recorded separately; the target is not assumed to be the achieved value.
- The review page's custom play button remained labeled Pause at the end. Bound its label to actual play/pause/ended events.
- Changed the two illustrative review stills to fully readable frames 540 and 990 instead of frames sampled during title fade-ins.

## Final source and browser review

- Replaced duplicated hero-arrival and response timestamps in the composition with reads from the shared event data. The original values and resulting motion were unchanged; rerendered and mastered from the delivered source.
- Fixed numeric frame entry being overwritten by presentation updates while the field had focus. Verified direct frame entry at 540 and the next frame at 541.
- Final MP4 played from the start to ended=true at exactly 24 seconds, readyState=4, 1920×1080, with no media error.
- Checked the English article at desktop size and 390 px width. Both comparison images loaded; narrow layout had no horizontal page overflow. Reset the temporary viewport afterward.
