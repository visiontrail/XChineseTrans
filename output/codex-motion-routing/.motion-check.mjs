// public/timeline.json
var timeline_default = {
  fps: 60,
  durationFrames: 1440,
  width: 1920,
  height: 1080,
  bpm: 120,
  seed: 260930,
  events: [
    { id: "emerge", frame: 30, kind: "bloom", pan: 0.55 },
    { id: "unfold", frame: 210, kind: "sweep", pan: -0.5 },
    { id: "launch", frame: 270, kind: "pluck", pan: -0.6 },
    { id: "router", frame: 420, kind: "tap", pan: -0.15 },
    { id: "break", frame: 480, kind: "snap", pan: 0.2 },
    { id: "alternate", frame: 720, kind: "sweep", pan: 0.1 },
    { id: "depart", frame: 750, kind: "pluck", pan: -0.1 },
    { id: "upper-a", frame: 870, kind: "tap", pan: 0.05 },
    { id: "upper-b", frame: 990, kind: "tap", pan: 0.38 },
    { id: "arrival", frame: 1110, kind: "resolve", pan: 0.65 },
    { id: "close", frame: 1230, kind: "bloom", pan: 0.5 }
  ],
  shots: [
    { id: "opening", start: 0, end: 210, title: "A route around failure" },
    { id: "path", start: 210, end: 450, title: "Start with a path" },
    { id: "break", start: 450, end: 690, title: "Then a link breaks" },
    { id: "reroute", start: 690, end: 930, title: "Change the route" },
    { id: "delivery", start: 930, end: 1170, title: "Keep the destination" },
    { id: "closing", start: 1170, end: 1440, title: "Another path, same destination" }
  ]
};

// src/motion.ts
var T = timeline_default;
var event = (id) => T.events.find((e) => e.id === id).frame;
var clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
var ease = (v) => {
  const t = clamp(v);
  return t * t * t * (t * (6 * t - 15) + 10);
};
var prog = (f, a, b) => ease((f - a) / (b - a));
var mix = (a, b, p) => a + (b - a) * p;
var lerp = (a, b, p) => ({ x: mix(a.x, b.x, p), y: mix(a.y, b.y, p) });
var bezier = (a, b, c, d, p) => {
  const q = 1 - p;
  return { x: q * q * q * a.x + 3 * q * q * p * b.x + 3 * q * p * p * c.x + p * p * p * d.x, y: q * q * q * a.y + 3 * q * q * p * b.y + 3 * q * p * p * c.y + p * p * p * d.y };
};
var impulse = (f, start, amp = 1, decay = 0.1, frequency = 0.2) => {
  const t = f - start;
  return t < 0 ? 0 : amp * Math.exp(-decay * t) * Math.sin(frequency * t);
};
var N = { source: { x: 320, y: 620 }, router: { x: 780, y: 620 }, a: { x: 1e3, y: 380 }, b: { x: 1320, y: 380 }, dest: { x: 1610, y: 620 }, lower: { x: 1110, y: 830 } };
function hero(f) {
  const unfold = event("unfold"), launch = event("launch"), router = event("router"), depart = event("depart"), a = event("upper-a"), b = event("upper-b"), arrival = event("arrival"), close = event("close");
  const opening = { x: 1430, y: 550 + 10 * Math.sin(f / 33) };
  if (f < unfold - 60) return opening;
  if (f < unfold + 30) return bezier({ x: 1430, y: 550 + 10 * Math.sin((unfold - 60) / 33) }, { x: 1410, y: 900 }, { x: 300, y: 840 }, N.source, prog(f, unfold - 60, unfold + 30));
  if (f < launch) return N.source;
  if (f < router) return lerp(N.source, N.router, prog(f, launch, router));
  if (f < depart) return N.router;
  if (f < a) return bezier(N.router, { x: 860, y: 620 }, { x: 860, y: 380 }, N.a, prog(f, depart, a));
  if (f < b) return lerp(N.a, N.b, prog(f, a, b));
  if (f < arrival) return bezier(N.b, { x: 1465, y: 380 }, { x: 1465, y: 620 }, N.dest, prog(f, b, arrival));
  if (f < close - 60) return N.dest;
  return bezier(N.dest, { x: 1610, y: 570 }, { x: 1510, y: 550 }, { x: 1430, y: 550 }, prog(f, close - 60, close + 60));
}
function heroMetrics(f) {
  const p = hero(f), a = hero(f - 0.5), b = hero(f + 0.5);
  const vx = b.x - a.x, vy = b.y - a.y, speed = Math.hypot(vx, vy);
  const radius = mix(96, 25, prog(f, event("unfold") - 75, event("unfold") + 25)) + 71 * prog(f, event("close") - 50, event("close") + 70);
  const settle = impulse(f, event("arrival"), 0.15, 0.09, 0.35);
  const stretch = 1 + Math.min(0.26, speed * 0.017) + settle;
  return { ...p, radius, angle: Math.atan2(vy, vx) * 180 / Math.PI, speed, sx: stretch, sy: 1 / stretch };
}
export {
  N,
  T,
  bezier,
  clamp,
  ease,
  event,
  hero,
  heroMetrics,
  impulse,
  lerp,
  mix,
  prog
};
