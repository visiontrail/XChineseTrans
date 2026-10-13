# Shared timeline conventions

Use a small timing object/module that both picture and sound consume. Don't introduce a second hand-maintained schedule just to satisfy this format. Export a JSON manifest for the checker if the authoring source is a code module or editor timeline.

This example uses 30 fps and 12 seconds solely to demonstrate the contract. Choose values for the user's film.

```json
{
  "fps": 30,
  "duration_frames": 360,
  "shots": [
    {"id": "establish", "start": 0, "end": 120},
    {"id": "change", "start": 120, "end": 270},
    {"id": "resolve", "start": 270, "end": 360}
  ],
  "events": [
    {"id": "title-in", "frame": 12},
    {"id": "main-action", "frame": 150},
    {"id": "response", "frame": 166},
    {"id": "resolution", "frame": 286}
  ]
}
```

## Semantics

- Frame zero is the first displayed frame; `duration_frames - 1` is the last.
- Shot intervals are half-open: `start <= frame < end`. This simple manifest describes ordered primary shots covering the whole composition. Crossfades can be described in extra transition fields without changing primary-shot ownership.
- Event frames are absolute composition frames. Compute local scene time explicitly: `(frame - shot.start) / fps`.
- For rate `fps`, convert an audio event frame to a sample using `round(frame * sample_rate / fps)`. Keep the integer frame as the authoritative event coordinate.
- Beat duration is `60 / bpm` seconds. Beat positions need not land on integer frames; round once for rendering and retain the beat index if useful.
- Use descriptive event names. Readout values, camera targets, and sound accents may refer to the same event without duplicating its numeric timestamp.
- A retime must update downstream visual and audio consumers. Don't round each track independently.
- The helper accepts positive numeric fps (including rates such as `30000 / 1001` expressed as a JSON number), an integer duration, ordered contiguous shots, and optional events. It is a delivery interchange format, not a restriction on editor internals.

## Code illustration

```js
const frame = useCurrentFrame();
const shot = timeline.shots.find(s => frame >= s.start && frame < s.end);
const localFrame = frame - shot.start;
const state = modelAtFrame(frame);
// Camera, geometry, and displayed values consume state.
// Offline audio placement consumes timeline.events using the same fps.
```

## Delivery helper

```bash
python3 scripts/check_delivery.py final.mp4 --out review-evidence
python3 scripts/check_delivery.py final.mp4 --timeline timeline.json --out review-evidence --extract
```

Run the script from wherever the skill's folder is installed, or use its absolute path. `--extract` saves every shot midpoint plus frames immediately around shot boundaries and named events, and the first/last frame. Inspect these files; the script does not assess them. It selects frames by decoded index, not approximate fast seeks. Large timelines can yield many images, so use an appropriately scoped manifest.

The report includes full-decode status, measured stream metadata, optional timeline comparison including each presentation timestamp against the frame grid, selected review-frame indices, and integrated audio loudness/true peak when audio exists. Loudness targets are deliberately not built in. A nonzero exit means an available check failed or the manifest is invalid; a missing tool produces a concrete error rather than a fabricated pass.

With a manifest, presentation times relative to the first video frame must follow `n / fps` within one stream time-base tick plus rounding allowance. This catches variable-rate timing that average fps alone can miss. Without a manifest, cadence is reported as unchecked. This does not verify that a particular sound accent matches a visible action.

`checks_passed` covers decoding and the supplied timing contract only. Dimensions, color metadata, audio presence, and loudness are reported, not compared against a delivery brief. Compare those fields with the requested format separately; a passing report is not a complete delivery verdict.
