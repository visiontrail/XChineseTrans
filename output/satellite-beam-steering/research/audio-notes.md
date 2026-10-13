# Original satellite-film audio

## Delivery

- Source: `scripts/soundtrack.py`; deterministic Python standard library + NumPy synthesis.
- Audio: `public/soundtrack.wav`, exactly 36.000 seconds, 48 kHz, stereo, 24-bit PCM.
- Original composition and synthesized editorial effects; no downloaded music, recordings, sample packs, sound fonts or TTS.
- Sounds express transitions and the film's rhythm. They are not physical sounds recorded in space or from antenna hardware.

## Musical direction

The pulse is 100 BPM (one beat every 0.6 seconds). Each six-second scene contains ten beats, arranged as five 2/4 bars. A recurring D–F#–E figure ties the six scenes together. The harmony moves through Dmaj9, Bm11, Gmaj9, Aadd9, Gmaj9 and D6/9. The opening is sparse; the middle adds small percussive subdivisions and slightly wider pitch movement; the last section withdraws the rhythm.

Low notes and a soft heartbeat remain near the center. Struck-string-like tones use a decaying harmonic spectrum, with upper partials disappearing faster than the fundamental. Quiet sine-based pads use minute detuning. Band-shaped noise provides air and brushed percussion. Equal-power panning and low-level cross-fed delay taps create space while preserving a stable low end and substantial mono compatibility.

## Picture-synchronized cues

| Time | Picture beat | Designed cue |
| --- | --- | --- |
| 0.00–0.12 s | Establish the satellite | Soft bass/pad entry, then a quiet D5 shimmer |
| 6.00 s | Array macro | Brief breath ending in an A5 glass-like point |
| 12.00 s | Separate array layers | Three short descending wooden notes moving left to right |
| 18.00 s | Change phase and direction | Smooth D5-to-F#5 gesture with a small left-to-right pan |
| 24.00 s | Ground tracking view | Open four-note harmonic bloom with a wider tail |
| 30.00 s | Return and resolve | Rising D chord, reduced percussion, final D5 note at 32.40 s |
| 33.50–35.50 s | Closing hold | Smooth fade; exact silence from 35.50 to 36.00 s |

The soundtrack can be regenerated with:

```bash
python3 scripts/soundtrack.py
```

## Technical verification

The WAV was decoded by FFmpeg and independently inspected as 24-bit PCM. The completed file has 1,728,000 samples per channel, no non-finite values, and no clipped samples. The largest adjacent-sample step is 0.04686 full scale. Endpoint envelopes prevent intentional step discontinuities; that numerical check does not replace listening in the final picture context.

Measured using FFmpeg `loudnorm` analysis:

| Measure | Unmastered source |
| --- | --- |
| Integrated loudness | −20.16 LUFS |
| True peak | −5.00 dBTP |
| Loudness range | 3.60 LU |
| Gating threshold | −30.39 LUFS |
| Sample peak | −5.0000 dBFS |
| Stereo correlation | 0.9465 |
| Last nonzero sample | 35.499875 s |

The score is deliberately delivered with headroom. The film's final master target is **−18 LUFS**. A static gain of approximately **+2.16 dB** should reach that target while retaining a true peak near −2.84 dBTP, before codec changes; measure the encoded final film again. If using two-pass `loudnorm`, use the measured source values above and `linear=true`, then verify the final output rather than treating the first-pass prediction as evidence.

Raw source segment RMS levels are −22.14, −20.57, −21.58, −19.24, −19.56 and −22.94 dBFS. The rise in the phase-control and tracking chapters and the softer resolution are intentional. No compressor, peak limiter or hard clipping is baked into the WAV.

Audio has been technically checked, but no claim of subjective listening approval is made here. Final acceptance should include listening with the rendered picture, checking that all five transition cues line up and that the final tail ends naturally.
