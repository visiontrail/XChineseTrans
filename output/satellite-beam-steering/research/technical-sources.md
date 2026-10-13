# Satellite sample: technical source record

Reviewed 2026-09-30. This is a generic explanation of electronic beam steering on a satellite. The spacecraft is illustrative, without a commercial product identity, claimed orbit, RF link budget, or measured performance.

## Primary evidence and claim boundaries

- **Electronic steering:** antenna elements can be controlled in phase and amplitude to direct a radio beam without mechanically turning the panel. This supports the fixed-panel / moving-main-beam contrast in the sample. It does not imply the entire spacecraft has no attitude control. [ESA: The silicon brains steering next-generation antennas](https://www.esa.int/ESA_Multimedia/Images/2026/07/The_silicon_brains_steering_next-generation_antennas).
- **Real satellite applicability:** SpaceX documents phased-array antennas on Starlink spacecraft. Use this only as proof that the concept has a real LEO application; the sample should not borrow hardware counts or performance figures. Its report also treats motion, Doppler, timing and handoff as system challenges. [SpaceX: Starlink Progress 2024](https://starlink.com/public-files/starlinkProgressReport_2024.pdf).
- **Geometric principle:** for uniformly spaced elements, adjacent far-field paths differ by `d sin(theta)`. Relative phase compensates that difference. Real patterns combine the element pattern and array factor, with sidelobes and reduced performance away from broadside. [Analog Devices: Part 1](https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part1.html).
- **Limits:** large element spacing can produce grating lobes; practical planar-array scan range is finite. Phase-shifter steering is frequency-dependent, producing beam squint over bandwidth. [Analog Devices: Part 2](https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part2.html).

## Signed formula for the animation

This sign is our derivation under the conventions below, not a universal sign convention:

- Uniform linear array: `x_n = n d`, normal along `+z`.
- `theta` is measured from `+z`; positive angles lean toward `+x`.
- Use time phasor `exp(+i omega t)` and outgoing propagation `exp(-i k r)`.
- To steer toward `theta_0`: `w_n = exp(-i k n d sin(theta_0))`.
- Adjacent feed-phase step: `delta_phi = -2 pi (d/lambda) sin(theta_0)`.
- Thus `d = lambda/2`, `theta_0 = +30 degrees` gives `delta_phi = -90 degrees`.
- First four feed phases: `0, -90, -180, -270 degrees` (equivalently `0, 270, 180, 90`).

For the ideal array factor, use

```text
AF(theta) = (1/N) sum_n exp(i n k d [sin(theta) - sin(theta_0)])
```

This is a narrowband far-field model. Show simultaneous emission with different phase, not elements firing one after another. See the source derivation of path difference and angle convention in [Analog Devices Part 1](https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part1.html).

## Suggested screen copy

1. A moving satellite.
2. A changing look angle.
3. One array. Controlled phase.
4. Shift the phase. Steer the beam.
5. Keep the beam on the terminal.

The last line describes the concept for the depicted interval; it is not a guarantee of continuous service throughout a pass.

## Optional narration

A satellite moves across the sky, and the direction to a ground terminal keeps changing. A phased array can steer its main beam without rotating the antenna panel. Each element contributes a radio wave. Change the relative phase, and those waves add most strongly in a new direction. The result is electronic pointing, within the antenna’s scan range. Real arrays still have sidelobes and losses.

## Direction for accurate visuals

Use the spacecraft and ground terminal to establish changing geometry; then move into a flat array with visible elements. Keep the panel fixed relative to the spacecraft. At broadside use aligned phases; for steering use a phase ramp and rotate the wavefront normal consistently. Return to the satellite shot and show the beam axis following the terminal while the spacecraft moves.

A translucent beam cone and footprint can explain pointing, but they are not a complete radiation pattern. Do not imply that energy exists only inside a hard-edged cone. A separate small pattern inset can show the main lobe with lower sidelobes if it improves understanding. Keep distances, sizes and animation timing diagrammatic. No claim about exact RF propagation speed should be inferred from decorative pulse motion.

## Claims to avoid

No universal statement that all LEO systems use this architecture. No unlimited scan angle, equal gain at all angles, zero sidelobes, arbitrary-spacing freedom from grating lobes, or broadband perfection from one phase setting. Do not equate steering with a completed link or instantaneous, lossless handover. Do not call this measured hardware performance, a full RF simulation, or a validated orbital simulation.

## Useful article wording

> The satellite sequence explains one mechanism: changing the relative phase across an array changes the direction in which the signals combine most strongly. The beam geometry is illustrative. The antenna remains fixed to the spacecraft in the shot, while its electronic pointing changes; that does not remove the need for spacecraft attitude control or other parts of a communications system.

The article can put the source links near the technical explanation. Production caveats belong in the method discussion, not as repeated labels over every shot.
