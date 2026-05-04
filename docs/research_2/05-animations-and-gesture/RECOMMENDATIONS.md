# 05 — Animations + Gesture: Recommendations

**Strand:** 05-animations-and-gesture
**Date:** 2026-05-04
**Audience:** Phase 2 implementation (TouchDesigner + gesture pivot), Phase 4 (methodology-wobble overlay), and the un-pause decision for the AI-animation track.

---

## A. Hand / fingertip tracking pipeline

**Pick: MediaPipe Hands via the Blankensmith TouchDesigner plugin (`torinmb/mediapipe-touchdesigner`).** Fall back to Ultraleap Leap Motion Controller 2 only if the projector-light interference test (defined below) fails.

**TouchDesigner topology:** `Video Device In TOP` (720p) → `mediaPipeTOX` (Hand Landmarker only, face/pose deselected to keep `realTimeRatio` < 0.5) → plugin CHOP exposing `h1:index_finger_tip:tx/ty`, `h1:thumb_tip:tx/ty`, `h1:wrist:*`, plus `detectTime`/`realTimeRatio`. A `Script CHOP` converts the index_tip stream into a footprint polyline; a `CHOP Execute DAT` watches for pinch onset (thumb-to-index 2D distance < 6 % of palm width for ≥ 3 frames) and emits phase-state changes. Wrap the whole subsystem in an `Engine COMP` so a tracking stall cannot block the render thread; watchdog on `realTimeRatio > 0.9` for > 10 frames triggers a "system catching up" overlay rather than a freeze.

**Latency budget: design for ~120 ms.** Camera 33 ms + plugin ~3-frame WebSocket buffer ~100 ms + render ~16 ms. Use animated lead-in feedback rather than expecting instant response.

**Mandatory pre-pilot test:** project a saturated cyan-magenta gradient onto an open palm at the planned table position. If MediaPipe confidence drops below 0.5 or landmark jitter exceeds 5 px, the RGB path is non-viable and the Ultraleap fallback is required. Without this test, the pivot is unverified.

---

## B. AI animation tool — first un-pause test

**Pick when un-paused: Hybrid path. Author the construction sequence in Houdini/Blender (deterministic, frame-exact); use Kling 3.0 for stylistic / atmospheric passes (dust, lighting, weather) over authored stills.** If un-pause arrives before authoring time exists, the fallback is **Luma Ray3 image-to-video** restricted to short interpolations between two locked authored stills — never free-form text-to-video for sequenced construction.

**Why not pure-AI:** Sora is discontinued. Runway Gen-4.5 is good at single shots, bad at *ordered* assembly. Kling 3.0 has the strongest physics as of 2026-05 but still produces non-monotonic builds (walls grow then partially shrink). Pika Ingredients gives texture consistency but not sequence integrity.

**First test:** generate a 3-second Kling 3.0 clip of a single brick course being laid on a previously authored wall still. Score: (i) no brick out of order; (ii) wall mass monotonically increases per frame; (iii) brick texture matches reference SSIM > 0.85; (iv) non-expert cannot identify the AI-generated 1-second slice in < 5 s a/b against authored frames. Pass = adopt; fail = restrict to atmospheric overlays only.

**Mandatory disclosure if any AI is used:** persistent badge in the wobble layer reading "Animation: AI-generated atmosphere over a hand-authored construction sequence", and on long-look the longer note "Phase frames are authored from reference photos of [Catalan masonry / Striatus 3DCP / the specific prefab system]; weather and dust are AI-generated and do not depict actual construction." Without this, the installation is implicitly claiming to show a real building going up.

---

## C. Methodology-wobble overlay — uncertainty-visualization idiom

**Pick: HOP-style flickering value at ~2.5 Hz for the active method's live readout, paired with a fading-edge gradient bar for the side-by-side comparison view.** The methodology-wobble layer (Phase 4) adds a third element: a typed assumption sentence — for example "if cement is CEM II/B-S 32.5 R from a Catalan plant" — that fades in for ~3 s every cycle.

**Why:** Hullman et al. (2015) and Kale et al. (2019) show animated distribution samples beat error bars and violin plots for untrained-observer accuracy; van der Bles et al. (2019) recommend rung-3 (rounded range) + rung-2 (summary distribution) for non-experts. The flicker forces visitors to *experience* the range; the gradient bar supports cross-method comparison without flicker fatigue; the assumption sentence turns a range into an honest claim.

**Mandatory rules:** round flickering values to two significant figures (false precision like "187.342 kg CO₂eq/m²" inside a 150–250 range is a documented honesty violation); do not color-code methods red/amber/green by central value — color-encode the *uncertainty width* instead; freeze the readout when the visitor is not tracing or pinching (continuous 2.5 Hz flicker for an 8-hour day causes legibility fatigue); show provenance (Tier 1 / 2 / 3) inline with each value, not buried in a tooltip.

---

## D. Two precedent projects to study most closely

**(1) Augmented Bricklaying / Kitrvs Winery (Mitterberger et al., 2020, *Construction Robotics*).** Extract the *visual error-feedback grammar*: the four-state registration palette (idle / approaching / on-target / mis-set), the per-element animation curve as the brick approaches its target, and the snap-to-place audio-visual confirmation. The masons-following-projected-targets loop is the same loop the installation animates, just rendered from above instead of in-eye.

**(2) UC Davis AR Sandbox (Kreylos et al., open source, 2012-).** Extract the overhead-camera + overhead-projector + hand-as-occluder loop and the open-source GLSL contour shaders: (a) the depth-statistic filter that distinguishes hands from substrate, (b) per-frame contour generation, (c) shader-side falloff that makes the projection forgive sensor noise. The geometric setup is identical to the installation's tabletop, the code is auditable, and the same shader pattern transfers to the phase-3-roof and phase-5-finishing layers.

Secondary one-read-each: **reacTable / reacTIVision** (gesture-vocabulary lineage); **Striatus** (layer-by-layer accretion for the 3DCP phase); **Parascho's dissertation** (FSM-as-animation, phase-as-state with named entry conditions).

---

## Cross-cutting

Surface the gesture subsystem's own confidence (`realTimeRatio`, `detectTime`, MediaPipe detection confidence) into the same wobble layer that surfaces LCA uncertainty. When the system is uncertain about the visitor, the projection should say so — same idiom, same restraint — rather than silently dropping frames.
