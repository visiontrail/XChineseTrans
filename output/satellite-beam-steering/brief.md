# Steering without turning

36 seconds, 1920×1080, 60 fps. A visual explanation of satellite phased-array pointing. English captions, original music and event sound. LeoGuoLabs warm ivory / forest green / dark gold, modern Geist typography.

The single causal chain: changing geometry → an array of radiators → relative phase → a changed main-beam direction → pointing at a terminal.

Six 6-second scenes, each with a distinct scale:
1. Satellite establishing view: rigid spacecraft, solar panels, visible planar aperture.
2. Camera closer to the aperture: identify the array while keeping the satellite context.
3. Exploded assembly: aperture, simplified feed layer, structural backing. This is a conceptual assembly, not a commercial CAD model.
4. Eight-element ideal array: all elements remain active, phase ramp changes from 0 to −90° per element, main-lobe direction changes from 0 to +30°. Display sidelobes in the normalized array factor.
5. Return to satellite and fixed terminal: panel remains rigid, pointing direction changes with satellite position.
6. Return to spacecraft hero: collect the mechanism in one sentence; no long empty title hold.

Technical stack: Three.js + React Three Fiber for real 3D geometry and lighting, Remotion for exact frame timing, SVG/HTML for crisp typography and quantitative plots, NumPy for original score, FFmpeg for mastering. All scene state is a pure function of frame index; no accumulated useFrame / wall-clock animation.

What the video proves: a deterministic, inspectable explanatory animation. It is not an orbital propagation or electromagnetic solver. Dimensions, speed, assembly layers, beam footprint and carrier period are illustrative. The ideal narrowband uniform-array factor is computed; real element patterns, coupling, losses, polarization and beam squint are outside this model.
