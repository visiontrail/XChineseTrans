# Orbit — A little perspective

A self-contained, interactive solar-system webpage. No installation, build, API key, network request, or third-party library is required.

Open `index.html` directly in a modern browser. For a local preview, run this command inside this directory:

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8766`.

## Explore

- Select any of the eight planets from the strip, or click a planet or the Sun in the scene.
- Drag the sky to rotate and tilt the view. Scroll or pinch to zoom.
- Switch between perspective and top-down views.
- Pause, resume, or change time speed from 1 to 180 simulated days per second.
- Toggle labels and orbit paths; reset to the original view.
- Use Space to pause/resume, arrow keys to select a planet, +/− to zoom, and R to reset. Buttons also support standard Tab/Enter/Space interaction.

The atlas adapts to desktop and mobile layouts. Reduced-motion preferences start the simulation paused. All surfaces and stars are drawn procedurally, and all application assets work offline. The optional NASA link opens an external website.

## Model and data

The Sun and planets are intentionally enlarged and orbital distances compressed. Orbits are circular and initial positions are artistic; this is not an ephemeris or an N-body simulation. Moons are omitted. The planets use a shared elapsed-time clock with approximate relative orbital periods. Rotation statistics describe sidereal rotation, and the planetary texture drawings do not simulate actual rotation. Numeric facts are rounded; AU means Earth's mean solar distance. General reference: https://science.nasa.gov/solar-system/planets/.

## Files

- `index.html`: content, controls, and accessible dialogs.
- `styles.css`: responsive dark observatory design.
- `app.js`: planetary data, procedural surface textures, canvas renderer, simulation clock, and pointer/keyboard controls.
