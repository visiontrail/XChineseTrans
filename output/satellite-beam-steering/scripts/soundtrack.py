#!/usr/bin/env python3
"""Original deterministic 36 s score and designed effects for the satellite film.

Only Python standard library + NumPy. No recordings, sound fonts, loops or models.
Render: python3 scripts/soundtrack.py
The sounds are editorial music/sonification, not physical sounds in space.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import wave
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
DURATION = 36.0
BPM = 100
BEAT = 60 / BPM
SEED = 260930
N = round(SR * DURATION)
RNG = np.random.default_rng(SEED)
MIX = np.zeros((N, 2), dtype=np.float64)
SEND = np.zeros_like(MIX)
EVENTS = []


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def timebase(duration):
    return np.arange(round(duration * SR), dtype=np.float64) / SR


def edge(signal, attack=0.008, release=0.04):
    """Raised-cosine endpoints prevent synthesizer clicks."""
    s = np.asarray(signal).copy()
    a = min(round(attack * SR), len(s) // 2)
    r = min(round(release * SR), len(s) // 2)
    if a:
        s[:a] *= np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    if r:
        s[-r:] *= np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return s


def place(signal, at, gain=1.0, pan=0.0, wet=0.0):
    """Equal-power pan; pan can be one value or a sample-accurate trajectory."""
    start = round(at * SR)
    source_start = max(0, -start)
    start = max(0, start)
    count = min(len(signal) - source_start, N - start)
    if count <= 0:
        return
    s = signal[source_start:source_start + count]
    p = np.asarray(pan)
    if p.ndim:
        p = p[source_start:source_start + count]
    angle = (np.clip(p, -1, 1) + 1) * np.pi / 4
    stereo = np.column_stack((s * np.cos(angle), s * np.sin(angle))) * gain
    MIX[start:start + count] += stereo
    SEND[start:start + count] += stereo * wet


def air(duration, center=1100, width=1000):
    """A fresh band-shaped noise texture, with no external samples."""
    n = round(duration * SR)
    noise = RNG.normal(0, 1, n)
    bins = np.fft.rfftfreq(n, 1 / SR)
    spectrum = np.exp(-0.5 * ((bins - center) / width) ** 2)
    spectrum *= 1 - np.exp(-(bins / 250) ** 2)
    result = np.fft.irfft(np.fft.rfft(noise) * spectrum, n=n)
    return result / max(np.std(result), 1e-8)


def pluck(midi, duration=1.8, softness=1.0):
    """A warm struck-string hybrid: fundamental sustains; upper partials fall away."""
    t = timebase(duration)
    f = hz(midi)
    result = np.zeros(len(t))
    for k, (weight, decay) in enumerate([(1, 2.5), (.34, 5.0), (.12, 7.8), (.035, 11)], 1):
        # Tiny stable inharmonicity adds material character without a detuned chorus.
        result += weight * np.sin(2 * np.pi * f * k * (1 + .0001 * k * k) * t) * np.exp(-t * decay / softness)
    result *= 1 - np.exp(-t * 650)
    return edge(result, .003, .05)


def pad(midi, duration=7.6, phase=0):
    t = timebase(duration)
    f = hz(midi)
    # Very restrained beating, no conspicuous cinematic oscillation.
    result = (.61 * np.sin(2 * np.pi * f * t + phase)
              + .25 * np.sin(2 * np.pi * f * 1.0010 * t + phase + .2)
              + .09 * np.sin(2 * np.pi * 2 * f * t + phase)
              + .025 * np.sin(2 * np.pi * 3 * f * t))
    result *= .94 + .06 * np.sin(2 * np.pi * .19 * t + phase)
    return edge(result, .80, 1.65)


def bass(midi, duration=1.65):
    t = timebase(duration)
    f = hz(midi)
    result = np.sin(2 * np.pi * f * t) + .13 * np.sin(4 * np.pi * f * t)
    result *= np.exp(-t * 1.35)
    return edge(result, .030, .20)


def low_pulse(duration=.34):
    t = timebase(duration)
    f = 49 + 18 * np.exp(-t * 28)
    signal = np.sin(2 * np.pi * np.cumsum(f) / SR)
    signal *= np.exp(-t * 13)
    return edge(signal, .012, .06)


def rim(duration=.075):
    t = timebase(duration)
    signal = .18 * air(duration, 2600, 1500) + .38 * np.sin(2 * np.pi * 740 * t)
    return edge(signal * np.exp(-t * 55), .002, .015)


def brush(duration=.15):
    t = timebase(duration)
    return edge(air(duration, 4900, 2300) * np.exp(-t * 32), .007, .045)


def bell(midi, duration=2.8):
    t = timebase(duration)
    f = hz(midi)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.6)
    s += .22 * np.sin(2 * np.pi * f * 2.005 * t) * np.exp(-t * 4.8)
    s += .055 * np.sin(2 * np.pi * f * 3.97 * t) * np.exp(-t * 8)
    return edge(s, .010, .12)


def log_event(seconds, name, description):
    EVENTS.append({'seconds': seconds, 'sample': round(seconds * SR), 'name': name, 'description': description})


# 6 seconds = 10 quarter-note beats. Each chapter is intentionally a five-bar
# 2/4 phrase, so all scene cuts are downbeats without pretending they are 4/4 bars.
# The recurring D / F# / E motif is original to this score.
chords = [
    {'name': 'Dmaj9', 'root': 38, 'notes': [57, 61, 64, 66], 'motif': [74, 78, 76, 69]},
    {'name': 'Bm11',  'root': 35, 'notes': [54, 57, 62, 64], 'motif': [74, 78, 81, 76]},
    {'name': 'Gmaj9', 'root': 31, 'notes': [55, 59, 62, 66], 'motif': [74, 71, 69, 78]},
    {'name': 'Aadd9', 'root': 33, 'notes': [57, 59, 61, 64], 'motif': [73, 76, 78, 81]},
    {'name': 'Gmaj9', 'root': 31, 'notes': [55, 59, 62, 66], 'motif': [74, 78, 81, 78]},
    {'name': 'D6/9',  'root': 38, 'notes': [57, 59, 64, 66], 'motif': [78, 76, 74, 69]},
]

for chapter, chord in enumerate(chords):
    start = chapter * 6.0
    intensity = [.74, .83, .78, .95, 1.0, .70][chapter]
    duration = 7.3 if chapter < 5 else 5.45
    for i, note in enumerate(chord['notes']):
        place(pad(note, duration, i * .73), start, .030 * intensity,
              [-.48, .32, -.20, .51][i], wet=.25)
    # Bass and gentle heartbeat. Final section withdraws, leaving the cadence tail.
    beats = [0, 2, 4, 6, 8] if chapter < 5 else [0, 2, 4]
    for beat in beats:
        at = start + beat * BEAT
        place(bass(chord['root']), at, .114 * intensity, 0, wet=.015)
        place(low_pulse(), at, .061 * intensity, 0)
    for beat in ([3, 7] if chapter < 5 else [3]):
        place(rim(), start + beat * BEAT, .026 * intensity, -.18, wet=.12)
    # The plucked figure is sparse at the opening, denser when phase control is shown.
    positions = ([1.5, 4.5, 7.5] if chapter == 0 else
                 [1, 3.5, 6, 8.5] if chapter in [1, 2] else
                 [1, 2.5, 4.5, 6, 8.5] if chapter in [3, 4] else [1, 3, 5])
    for i, beat in enumerate(positions):
        note = chord['motif'][i % len(chord['motif'])]
        place(pluck(note), start + beat * BEAT, .051 * intensity,
              [-.28, .31, -.12, .39][i % 4], wet=.31)
    # Soft ghost subdivisions add life without a prominent drum track.
    if chapter in [1, 2, 3, 4]:
        for i, beat in enumerate([.5, 2.5, 4.5, 5.5, 7.5, 9.5]):
            place(brush(), start + beat * BEAT, (.0046 if i % 2 else .0061) * intensity,
                  .27 if i % 2 else -.31, wet=.09)
    log_event(start, 'chapter_' + str(chapter + 1), chord['name'] + ' harmonic chapter')

# Six different restrained editorial cues, synchronized to the visual chapter edges.
# 0 s: warm low onset with soft upper shimmer, no abrupt trailer impact.
place(bell(74, 3.0), .12, .043, -.10, wet=.46)
log_event(.12, 'opening_shimmer', 'Quiet D5 shimmer over the first harmonic bed')

# 6 s: macro focus — a breath rising into a single small glass point.
t = timebase(.75)
place(air(.75, 1400, 950) * np.sin(np.pi * t / .75) ** 2,
      5.56, .011, np.linspace(-.42, .30, len(t)), wet=.2)
place(bell(81, 2.15), 6.0, .080, .26, wet=.44)
log_event(6, 'macro_focus', 'Short breath and clean A5 glass point')

# 12 s: array layers — quiet, spaced wooden clicks; each reveal gets its own pitch.
for offset, note, p in [(0, 74, -.42), (.09, 71, 0), (.18, 66, .42)]:
    place(pluck(note, 1.35, .63), 12 + offset, .075, p, wet=.28)
place(rim(.095), 12, .030, -.2, wet=.15)
log_event(12, 'layer_separation', 'Three short descending wood-like notes moving left to right')

# 18 s: phase gradient — smooth, small pitch rise and sideways movement.
t = timebase(.76)
f = hz(74) * 2 ** ((4 * (.5 - .5 * np.cos(np.pi * t / .76))) / 12)
phase = 2 * np.pi * np.cumsum(f) / SR
s = (np.sin(phase) + .13 * np.sin(2 * phase)) * np.sin(np.pi * t / .76) ** 2
place(s, 17.81, .062, np.linspace(-.50, .50, len(t)), wet=.38)
place(bell(78, 1.8), 18.0, .044, .24, wet=.3)
log_event(18, 'phase_steer', 'A smooth D5-to-F#5 gesture with a left-to-right pan')

# 24 s: tracking view — broader, lower harmonic bloom, not a second loud impact.
for i, note in enumerate([62, 69, 74, 78]):
    place(bell(note, 3.0), 24 + i * .035, .061, [-.35, .3, -.1, .37][i], wet=.48)
log_event(24, 'tracking_bloom', 'Four-note open voicing with a wider stereo tail')

# 30 s: return / resolve — cadence played as a soft rising broken chord.
for i, note in enumerate([62, 69, 74, 78, 81]):
    place(pluck(note, 3.0, 1.32), 30 + i * .06, .064 - i * .003,
          [-.27, .15, -.1, .3, .08][i], wet=.43)
place(bell(74, 2.8), 32.4, .036, 0, wet=.38)
log_event(30, 'closing_cadence', 'D major/add9 resolution, withdrawing percussion, sustained tail')

# Fixed cross-fed multitap space. Low-frequency layers have almost no send, keeping
# bass steady and centered. Prime-like delay offsets prevent an obvious repeating echo.
for delay, gain, cross in [(.139, .21, True), (.283, .16, False), (.431, .13, True),
                           (.617, .10, True), (.887, .078, False), (1.193, .056, True),
                           (1.571, .036, False), (2.039, .020, True)]:
    offset = round(delay * SR)
    src = SEND[:-offset, ::-1] if cross else SEND[:-offset]
    MIX[offset:] += src * gain

# Overall entrance and a smooth musical fade; exact silence from 35.5 s onward.
entrance = round(.16 * SR)
MIX[:entrance] *= np.sin(np.linspace(0, np.pi / 2, entrance))[:, None] ** 2
end_start, end_stop = round(33.50 * SR), round(35.50 * SR)
MIX[end_start:end_stop] *= np.cos(np.linspace(0, np.pi / 2, end_stop - end_start))[:, None] ** 2
MIX[end_stop:] = 0
# Remove tiny numerical DC before final tapered endpoints. No limiter or hard clipping.
MIX -= MIX.mean(axis=0)[None, :]
MIX[:entrance] *= np.sin(np.linspace(0, np.pi / 2, entrance))[:, None] ** 2
MIX[end_start:end_stop] *= np.cos(np.linspace(0, np.pi / 2, end_stop - end_start))[:, None] ** 2
MIX[end_stop:] = 0
MIX *= (10 ** (-5 / 20)) / np.max(np.abs(MIX))

# 24-bit PCM with fixed-seed triangular dither, while preserving the silent handle.
dither = (RNG.random(MIX.shape) - RNG.random(MIX.shape)) / (2 ** 23 - 1)
dither[end_stop:] = 0
pcm = np.rint(np.clip(MIX + dither, -1, 1) * (2 ** 23 - 1)).astype(np.int32)
flat = pcm.reshape(-1)
packed = np.empty((len(flat), 3), dtype=np.uint8)
packed[:, 0] = flat & 255
packed[:, 1] = (flat >> 8) & 255
packed[:, 2] = (flat >> 16) & 255
out = ROOT / 'public' / 'soundtrack.wav'
out.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(out), 'wb') as wav:
    wav.setnchannels(2)
    wav.setsampwidth(3)
    wav.setframerate(SR)
    wav.writeframes(packed.tobytes())

peak = float(20 * np.log10(np.max(np.abs(MIX))))
rms = float(20 * np.log10(np.sqrt(np.mean(MIX ** 2))))
correlation = float(np.corrcoef(MIX.T)[0, 1])
report = {'file': str(out), 'durationSeconds': DURATION, 'sampleRate': SR,
          'channels': 2, 'bitsPerSample': 24, 'bpm': BPM, 'seed': SEED,
          'samplePeakDbfs': peak, 'rmsDbfs': rms, 'stereoCorrelation': correlation,
          'samplesPerChannel': N, 'silentFromSeconds': 35.5, 'events': EVENTS}
print(json.dumps(report, indent=2))
