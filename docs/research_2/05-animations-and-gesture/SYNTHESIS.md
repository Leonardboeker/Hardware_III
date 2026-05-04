# 05 — Animations + Gesture: Synthesis

**Strand:** 05-animations-and-gesture
**Date:** 2026-05-04
**Decision triggered by:** Phase 2 fingertip-tracking pivot (gesture replaces ArUco fiducials); methodology-wobble overlay locked as a first-class projection layer; AI-animation work paused pending LCA values.
**Scope:** Four parallel sub-strands — A (hand tracking), B (AI construction-sequence animation), C (uncertainty visualization), D (tabletop-projection precedent set).

This synthesis is written assuming the installation runs on TouchDesigner with an overhead webcam and a tabletop projector, and that visitors include children and adults whose only interface is their hands and the projected light on the table.

---

## A. Hand / fingertip tracking for tabletop projection

### A.1 Production-grade pipelines surveyed

**MediaPipe Hands (Google, 2019- ).** Two-stage pipeline: BlazePalm single-shot detector returns an oriented hand bounding box; a hand-landmark regression model then predicts 21 3D keypoints (knuckles, fingertips) inside that crop. The training corpus is ~30 K manually annotated real images plus rendered synthetic hands; mixed-data training yielded 13.4 % mean regression error vs. 25.7 % synthetic-only and 16.1 % real-only (Bazarevsky & Zhang, 2019, Google Research blog; primary architecture paper: Zhang et al., 2020, arXiv:2006.10214). The framework is now distributed as **MediaPipe Solutions / Hand Landmarker** under Google AI Edge, with documented mobile latency (Pixel 6 CPU/GPU benchmarks in the official guide) but no published latency for desktop overhead-camera scenarios.

**OpenPose (CMU, 2017- ).** Realtime multi-person 2D pose estimation using Part Affinity Fields (Cao, Hidalgo, Simon, Wei & Sheikh — CVPR 2017; extended TPAMI 2019). Includes body, foot, hand, and face keypoints. The architecture is heavier than MediaPipe; on a single GPU it is real-time only at modest resolutions and is overkill for a single-user tabletop scenario. The hand-only sub-model is less accurate than MediaPipe's specialised hand pipeline. Recommended **only** if the installation later wants multi-user pose plus hands together.

**Ultraleap Leap Motion Controller 2 (2023, formerly Leap Motion).** Dedicated stereo near-IR camera with 160° × 160° FoV, tracking range 10–110 cm, 27 hand joints; ships with the Hyperion tracking engine. Because it ignores visible-spectrum content entirely, it is **immune to projector-light interference on the hand** — this is the strongest case for it in a tabletop projection scenario. Trade-offs: it is a hand-mounted-volume device (designed to look up at hands above it), not an overhead surface tracker. Mounting it overhead and pointing down works but is off-label and the FoV at 110 cm caps the trackable area.

### A.2 TouchDesigner integration paths

The dominant production path is the **MediaPipe TouchDesigner plugin by Torin Blankensmith (torinmb/mediapipe-touchdesigner)**, a GPU-accelerated, self-contained TOX. Internally it runs MediaPipe's JS implementation through WebAssembly inside an embedded Chromium browser, and pipes results back to TouchDesigner via a local WebSocket server. Output lands as DAT (JSON), TOP (overlay), and CHOP (per-landmark x/y/z, plus diagnostic channels `detectTime`, `drawTime`, `realTimeRatio`, hand velocity). Tested up to TD 2025.31500. Documented constraints: 720p input cap; the embedded browser introduces "at least 3 frames" of `totalInToOutDelay` over the raw camera-to-network path (plugin documentation, 2024–25).

Alternative paths:
- **OSC bridge from a Python MediaPipe process** to TD's `OSC In CHOP` — adds one extra process and a few ms of socket latency, but lets you run the latest MediaPipe Python release directly.
- **Spout (Windows) or Syphon (macOS) texture sharing** for the camera feed and overlay; useful when a Python MediaPipe app draws debug overlays you want to composite into the TD scene without re-encoding through V4L/DirectShow.
- **TouchDesigner's native Script CHOP / CHOP Execute DAT / Parameter Execute DAT** are the right callbacks for converting landmark streams into footprint vertices and heights (Derivative documentation, 2024).

For a single overhead camera at 30 fps, end-to-end gesture-to-projection latency in this stack is realistically 80–150 ms (camera 33 ms exposure + plugin 3-frame WebSocket buffer ~100 ms + render frame ~16 ms), which is comfortable for tracing but borderline for fast pinch gestures. Latency-budget honesty: the installation should design for ~120 ms perceived lag and use animated lead-in / "anchor" feedback rather than expect instant response.

### A.3 Failure modes (named, falsifiable)

1. **Projector-light bleeding onto hands.** Bright RGB content projected onto a moving hand confuses MediaPipe palm detection because the hand surface no longer has consistent skin chroma. The MediaPipe team trained on real-world plus synthetic backgrounds but **not on hands lit by saturated projected color** (no such bias is documented in Bazarevsky & Zhang, 2019). Documented in the broader literature: illumination variation often dominates appearance variation between subjects (Finlayson, 2018, *Interface Focus*). **Test that catches it:** project a saturated cyan-magenta gradient onto an open palm and run hand detection — if confidence drops below 0.5 or landmarks jitter > 5 px, you have the bug.
2. **MediaPipe is not robust on pure IR / grayscale input.** Confirmed in MediaPipe issue #2008 (Google, 2021) and corroborated by Smart Design Technology's RealSense integration write-up: the model relies on color cues. Naive workaround "use an IR camera under projector light" therefore fails out of the box. The fix is either (a) Ultraleap (purpose-built for IR), or (b) RGB camera with an IR-pass cut filter and a small auxiliary IR illuminator and use a fine-tuned color-and-IR fusion — non-trivial.
3. **Self-occlusion at low pinch heights.** The 21-keypoint regressor extrapolates occluded fingers; predictions drift up to 30 px when index and thumb are nearly touching. A pinch-detection threshold based on **2D distance between thumb_tip and index_tip below a noise-aware floor (e.g., 6 % of palm width) for ≥ 3 frames** is the documented mitigation (consistent with MediaPipe's own gesture recognizer thresholds).
4. **Hand-from-arm ambiguity at table edges.** When only the wrist enters the camera FoV, BlazePalm sometimes locks onto the forearm. Crop the active region to the table interior and reject detections whose bounding box overlaps the FoV margin > 20 %.
5. **Two-handed false merges.** When two visitors reach in, hand-velocity smoothing in MediaPipe's tracker can briefly swap identities. The plugin's `h1`/`h2` channels are not stable under crossings; the installation either accepts single-hand interaction or implements explicit identity tracking (Hungarian assignment on landmark centroids).

### A.4 Precedent installations

- **MIT Tangible Media inFORM (Leithinger, Follmer, Olwal & Ishii, 2013/14)** — a 30 × 30 actuated pin display reading a Kinect to mirror a remote user's hand gestures into physical pins. Establishes the design language of "your hand is the controller and the table responds in real time", with explicit critical writing on the limits of dynamic shape.
- **reacTable (Jordà, Geiger, Alonso & Kaltenbrunner, MTG / UPF Barcelona, 2003- )** and its underlying **reacTIVision** computer-vision framework (Kaltenbrunner & Bencina, 2007, *TEI '07*). Local Barcelona precedent. Fiducial-based, but the gesture vocabulary (rotate to set, slide to scale, connect to compose) is the canonical reference for tabletop manipulation, and reacTIVision since v1.6 also tracks untagged blobs and fingers via TUIO.
- **UC Davis Augmented Reality Sandbox (Kreylos et al., 2012- )** — Kinect overhead, projector overhead, real-time topographic projection on physical sand. Crucially: hands above the surface trigger a "virtual rain" interaction. This is the closest functional precedent for an overhead-projector / overhead-camera tabletop where hands are both the *occluder* and the *interaction target*, and the published implementation explicitly filters hands out of the depth statistic — proving the cohabitation is solvable.
- **Augmented Bricklaying / Kitrvs Winery (Gramazio Kohler Research / Dörfler et al., ETH, 2019; Mitterberger et al., 2020, *Construction Robotics*).** Visual-inertial object tracking + projected optical guidance on the workpiece. Scale: 13 596 individually rotated bricks across a 225 m² façade. The relevant precedent here is *not* the fiducial scheme — it is the closed loop "measure where the brick is, project where the next one should go, mason places brick, re-measure" — i.e., the assembly-as-conversation pattern the installation is animating.
- **Microsoft PixelSense / Surface 2.0 (2012, Samsung SUR40)** — 52-touch IR-vision tabletop. Historical, but the documentation of three object classes (fingers, tags, blobs) is a useful taxonomy for the installation's gesture grammar.
- **teamLab Borderless / Planets** — large-scale projection with body-presence detection; not a primary reference for fingertip precision, but the design-language reference for how visitors expect projected content to *react* to bodies.

### A.5 Recommended pick (with rationale)

**MediaPipe Hands via the Blankensmith TouchDesigner plugin, with an Ultraleap fallback if A.3.1 (projector-light interference) breaks the pilot.** Rationale: the plugin is the only path that does not require shipping a side-process, runs on the GPU, and is actively maintained (TD 2025 verified). MediaPipe's 21-keypoint output already contains thumb_tip and index_tip — exactly the channels needed for footprint trace and pinch-to-set-height. The Ultraleap fallback exists because if A.3.1 is fatal, the IR-only sensor is the one well-evidenced way to make the projector and the tracker coexist, accepting the off-label overhead-mount geometry.

### A.6 Named biases

- **Bias toward fair-skin training data.** MediaPipe's 30 K real images are not demographically audited in the cited materials. In a public installation with a multi-ethnic visitor base, false negatives concentrate on darker skin tones; the wobble overlay must include a "couldn't see your hand — try moving slower" failure state, not silent dropouts.
- **Bias toward right-handed gestures.** Most gesture-vocabulary precedents (Jordà 2007, PixelSense 2012) were developed and tested right-handed. Pinch and trace must be tested mirrored.
- **Bias toward adult hands.** The MediaPipe hand model handles children's hands, but pinch threshold (6 % of palm width) auto-scales only if you compute it per-detection — not from a fixed pixel offset.

---

## B. AI-generated phase animations for construction sequences

State as of 2026-05-04 — verified within the past two weeks where dates appear.

### B.1 Tools surveyed

**Runway Gen-4 / Gen-4 Turbo / Gen-4.5.** Diffusion-transformer architecture trained with "cinematic conditioning" on professional cinematography datasets (Runway Research, 2025; Runway Help — *Creating with Gen-4.5*). Strongest in coherent camera motion and material lighting. Architectural prompt fidelity is good for static views and short pans; it consistently fails at *sequenced* construction (a wall growing course-by-course) — the model interpolates rather than steps.

**Sora / Sora 2 (OpenAI).** Sora 2 launched 2025-09-30. **As of 2026-04-26 the Sora consumer web/app was discontinued; the Sora API is scheduled to be discontinued 2026-09-24** (OpenAI Help Center, *What to know about the Sora discontinuation*). Practical implication for this installation: Sora is **not** a viable production target. Any "Sora-style" output should be sourced from Veo 3 or Kling instead.

**Kling 2.0 / 2.6 / 3.0 (Kuaishou).** Kling 3.0 released 2026-02-04, advertising "3D Spacetime Joint Attention" and chain-of-thought reasoning for physics-accurate motion (gravity, balance, deformation, inertia). 2.0 already simulates fluid and collision physics; 2.6 adds native audio. Strongest current candidate for credible *physical* sequences (concrete pour, brick stacking) when the prompt is explicit about ordering.

**Pika 2.0 / 2.1 / 2.5 with Scene Ingredients.** "Ingredients" allow uploading reference images of objects/people and reusing them across shots — the closest current tool for *consistency of a specific brick or wall texture across the five phases*. Quality below Kling 3.0 on physical realism but more controllable for repeated subjects.

**Luma Dream Machine + Ray3.** Hybrid diffusion-transformer + NeRF-derived 3D-consistency stage — the model "dreams in 3D before flattening to 2D" (Luma Labs documentation). Image-to-video is the strongest mode and is the natural fit when the input is a still architectural rendering of phase N and the output is the transition to phase N+1.

**Stable Video Diffusion (Stability AI, SVD-XT and successors).** Open-source, 25 frames at 576×1024 from a conditioning image (Hugging Face model card, *stable-video-diffusion-img2vid-xt*). Lower quality than the proprietary models for free-form prompts, but it is the only path that gives full local control — relevant if the installation later wants to ship without a runtime API dependency.

**Hybrid: Houdini / Blender authored sequence + AI texture/lighting/shading pass.** The reliability champion. Author the construction sequence deterministically (each brick keyframed; pour volume animated with a real fluid solver); use AI for stylistic re-renders and dust/debris layers. Recommended whenever "this brick goes here on this frame" must be true.

### B.2 Failure modes — named, with the test that catches each

1. **Material physics drift.** Concrete pours that flow uphill; rebar that bends like rope; brick courses that float and settle. *Test:* generate a 4 s clip of each phase and check frame-by-frame for monotonicity (the wall should never lose mass) and for material identity (a brick should not morph into a stone).
2. **Sequence reversal / non-monotonic build.** Walls grow then partially shrink as the model "regrets" earlier frames. *Test:* compute pixel mass of the built region per frame; reject any clip where mass derivative goes negative outside an authored event (e.g., a chase being cut into the wall).
3. **AI-slop tells.** Excessive smoothness, no dust, no debris, overly clean tools, hands that have six fingers or shimmer at edges, and a hyperreal "no-shadow" lighting that betrays a synthetic origin. *Test:* a/b a 2 s clip against an authored Houdini pass with the same camera; if a non-expert can identify the AI clip in < 5 s, the slop is unmasked.
4. **Inconsistent material identity across phases.** The brick texture in phase 2 does not match phase 4. *Test:* reference-image SSIM > 0.85 across all five phases against a locked reference brick. Pika's Scene Ingredients are explicitly the mitigation.
5. **Tooling and labor invisibility.** AI defaults to a magical assembly with no visible workers, no scaffolding, no cranes — which encodes a *false* claim about how buildings get built and silently flatters the technologies. *Test:* a labour-hours-per-m² range exists in the LCA data; if the animation does not show *any* labor, the methodology-wobble layer must explicitly footnote the omission.

### B.3 Honesty and disclosure

An AI-animated brick wall is not a brick wall. The installation already commits to honesty about value uncertainty; it owes the same to its imagery. Recommended disclosure language is in `RECOMMENDATIONS.md`. The principle: if AI is used for the phase animation at all, the methodology-wobble layer carries a small persistent badge (e.g., a square that fades between rendered and AI-generated states matching the actual frame source) and a one-line caption "Animation: AI-generated from reference photos of [Catalan masonry / ICON Vulcan prints / Holcim Striatus build]."

### B.4 Recommended pick (with rationale)

**Hybrid path: Houdini-authored sequence with Kling 3.0 stylistic passes for atmosphere, when un-paused.** Rationale: Kling 3.0 is the current leader on physical motion as of 2026-05 (released 2026-02-04), but is still untrustworthy for *ordered* assembly. The reliable construction sequence must be authored — keyframed in 3D — and AI is used only for the textural and atmospheric layer that softens the digital aesthetic into something tabletop-credible. If the un-pause happens before LCA values land and there is no time for full Houdini authorship, the fallback is **Luma Ray3 image-to-video on a sequence of authored stills**, which constrains AI to short interpolations between known states.

### B.5 Named biases

- **Recency bias in AI-tool reporting.** Marketing copy from each vendor claims "physics-accurate". Treat all such claims as Tier-3 vendor sources per the project's tiering convention; do not adopt them without an in-house frame-by-frame test.
- **Western-construction bias.** Training corpora overrepresent North-American/European wood-frame and steel construction. Catalan fired-clay block masonry, rammed earth, and reclaimed brick are likely under-represented; expect higher slop on the Catalan-specific methods than on a generic "wall going up".
- **Aesthetic-cinema bias.** Diffusion models converge to cinematic compositions — golden hour, slow dolly. The tabletop installation's projection is fundamentally orthographic / top-down. AI clips authored cinematically and reprojected top-down look broken.

---

## C. Methodology-wobble / uncertainty visualization

### C.1 Practitioners and academic basis

**Hullman et al., Hypothetical Outcome Plots (HOPs).** Hullman, Resnick & Adar (2015), *PLOS ONE*, established that animated frames each drawn from the distribution let untrained observers judge multivariate probabilities more accurately than error bars or violin plots. Kale, Nguyen, Kay & Hullman (2018, *IEEE TVCG* / *PLOS ONE*) extended the result: HOPs let untrained observers reach ~75 % accuracy on noisy time-series trends with less evidence than error bars require. **This is the empirical case for a flickering-value idiom over a static range bar in the projection.**

**van der Bles et al. (2019), "Communicating uncertainty about facts, numbers and science," *Royal Society Open Science* 6(5), 181870.** The framework distinguishes three objects of uncertainty (facts / numbers / scientific hypotheses) and two levels (direct / indirect). It enumerates a nine-rung scale of expressions of direct uncertainty, from full probability distribution down to explicit denial. For LCA values the relevant rungs are 2 (summary of distribution — confidence intervals, fan charts) and 3 (rounded ranges / order of magnitude). Their visualization recommendation: gradient and violin plots beat error bars by reducing "within-the-bar bias" — recipients otherwise assume values inside a bar are more probable than values outside.

**Financial Times Visual Vocabulary** (Smith et al., FT Visual Journalism Team — open-source repository at github.com/Financial-Times/chart-doctor). The fan chart is the FT's canonical idiom for forecast uncertainty: the past as a line, the future as a widening tinted band. For LCA: the *phase progression* is the analog of the time axis, the value range becomes the tint band.

**Domestic Data Streamers (Barcelona, 2013- ).** Studio specialised in participatory physical data visualization. Their *Data Falls* installation at CCCB (Big Bang Data exhibition) is the local-Barcelona reference for translating data into a tactile/projected idiom that visitors can stand inside. They are not, however, primarily an "uncertainty viz" studio — adopt their tactile honesty, not their literal idioms.

**Dear Data (Lupi & Posavec, 2016, Princeton Architectural Press).** Hand-drawn data postcards over 52 weeks. The relevance for *uncertainty* is the legend system: each postcard front shows the dataset, the back shows a hand-written legend that can include "I'm not sure if this counted as X". The installation's wobble layer can borrow the legend-as-companion idiom.

**LCA-software incumbents (One Click LCA, EC3, Carbon Heroes).** Reviewed via product documentation and Carbon Leadership Forum community comparisons (2024–26). State of practice: most show a single point value with EPD provenance text in a tooltip. EC3 surfaces the per-EPD GWP variation as a histogram (the "achievable / conservative / industry-average" bars are the closest current uncertainty idiom). One Click LCA's January 2026 release added pre-filtered Local/Regional EPDs and "data locking" but no explicit uncertainty band UI. The honest summary: the incumbents currently visualize uncertainty *poorly*, which is exactly the opening this installation can occupy.

### C.2 Idioms candidate set for the projection

Each idiom evaluated against three constraints: (i) child-legible without instruction, (ii) honest about range, (iii) cheap to render in TouchDesigner at 60 fps.

- **Static range bar with low/high tick marks.** Cheap, legible, but research-proven to suffer within-the-bar bias (van der Bles et al., 2019). Reject as primary.
- **Fading-edge gradient bar.** A bar whose endpoints fade to transparent over the uncertainty interval. Mitigates within-the-bar bias. Cheap. Adopted as the static fallback on the side comparison view.
- **Flickering value (HOP-style).** The projected number animates between samples drawn from the assumed distribution every ~400 ms (Hullman 2015 finds that frame intervals shorter than 400 ms degrade comprehension; longer than 1.5 s loses the sense of "many futures"). Most honest, most memorable, slightly anxiety-inducing for some viewers. Adopted as the primary idiom for the active-method readout.
- **Sand / dust particle plume.** Particles whose density encodes uncertainty around the value. Legible to children; harder to read off a number.
- **Two simultaneous values shown with explicit "low assumption / high assumption" labels.** Most explicit; pedagogically strongest. Adopted for the methodology-wobble overlay specifically.

### C.3 Recommended pick (with rationale)

**Primary idiom — HOP-style flickering value at ~2.5 Hz** for the live readout of the currently active method, paired with **a fading-edge gradient bar in the comparison view**. Rationale: the flicker forces visitors to *experience* the range rather than pattern-match a single number; the gradient bar is the calmer summary view that supports cross-method comparison. The methodology-wobble overlay (Phase 4) layers a third element: a typed assumption sentence that fades in for ~3 s every cycle, e.g., "if cement is CEM II/B-S 32.5 R from a Catalan plant" — which is the rung 3-plus-rung-2 combination van der Bles et al. (2019) explicitly recommend for non-expert audiences.

### C.4 Failure modes

1. **Flicker fatigue.** Continuous 2.5 Hz flicker for the whole exhibit visit causes legibility fatigue. *Mitigation:* freeze the value when the visitor is not actively tracing, only flicker when comparing or transitioning.
2. **False precision via decimal places.** Showing "187.342 kg CO₂eq/m²" within a 150–250 range is a documented honesty violation (van der Bles et al., 2019, on rounded figures). The flickering values must be rounded to two significant figures.
3. **Children read the fastest number as "the answer".** *Mitigation:* the gradient bar in the comparison view should not flicker; it presents the band as a stable spatial extent, which children read as "this much, plus or minus".
4. **Color-coding traffic-lighting the methods.** Red/amber/green encodes a value judgment LCA can't sustain (a Tier-3 vendor source's "green" is not a Tier-1 EPD's "green"). *Mitigation:* color-encode the *uncertainty width*, not the central value; methods with wider bands are visibly less certain regardless of their absolute number.

### C.5 Named biases

- **Confidence-projection bias.** Designers default to displaying point values because they look professional. The installation must resist this.
- **Tier-collapsing bias.** When a value is from a Tier-3 vendor source and a Tier-1 EPD, averaging the two erases the evidence-quality distinction. The wobble layer must show provenance, not averages.
- **Range-equals-disagreement bias.** A wide range can mean either "we have many high-quality measurements that genuinely disagree" or "we have one weak source". The named-assumption text is what disambiguates; without it, ranges lie.

---

## D. Tabletop projection animation — formal precedents

### D.1 Canonical reference set

- **reacTable / reacTIVision (UPF Barcelona, 2003- ; Jordà et al., 2007 *TEI*; Kaltenbrunner & Bencina, 2007 *TEI*).** The original tabletop tangible-interface canon. Local lineage. Animation idioms: directional flow lines between connected pucks, ring radial halos for parameter values, audio-reactive ripples under each puck. The visual language of "the table itself is alive and currents flow between objects on it" originates here.
- **Augmented Bricklaying / Kitrvs Winery (Mitterberger, Dörfler, Sandy, Salveridou, Flückiger, Casas, Gramazio & Kohler, 2020, *Construction Robotics*).** Ghost-projection vocabulary: a translucent target outline, a real-time confidence color, and a snap-to-place click. Error-feedback idiom: when a brick is misplaced, the projection turns the registration outline red and shows the offset vector. This is the single most directly transferable visual grammar for the installation's "you traced the footprint, here's how the masons would build it" sequence.
- **Striatus / Phoenix Bridge (Zaha Hadid Architects + Block Research Group, ETH; Holcim and incremental3D — Venice 2021, reassembled as Phoenix in Lyon 2024).** 53 unreinforced 3DCP blocks, ~500 layers per block, six-axis robotic arm, ~84 hr total print time. Reference for the *3D-printed method's* phase animation: layer-by-layer accretion, compression-only block geometry, dry assembly.
- **Stefana Parascho — "Cooperative Robotic Assembly" (ETH dissertation, 2019, DOI 10.3929/ethz-b-000364322; *Robotic Vault*, Parascho et al., 2020, *Construction Robotics*).** Dissertation establishes the FSM-as-animation pattern: each robot's role, the cooperative handoff, the dependency graph between elements. Translates directly to the installation's five-phase progression as a small state machine where each phase's entry condition is the previous phase's completion event.
- **MIT inFORM (Leithinger, Follmer, Olwal & Ishii, 2013, *UIST*).** Establishes that a tabletop with overhead sensing + actuation is a *full-stack* interactive medium, not just a display.
- **UC Davis AR Sandbox (Kreylos, Reed et al., 2012- ).** Open-source canon for overhead-camera + overhead-projector + physical-substrate-on-table loops. Source code (github.com/openearth/sandbox forks) shows the GLSL contour-line and hillshading shaders that the installation's phase-3-roof and phase-5-finishing layers can borrow directly.
- **teamLab Borderless / Planets.** Reference for production scale and the design language of "the projection responds to where you stand" — the installation borrows the *responsiveness* idiom, not the room-scale execution.
- **openFrameworks (Lieberman, Watson, Castro et al., 2005- ) and Cinder (Bell et al., 2010- ).** The pre-TouchDesigner creative-coding lineage. Many of the precedent projects above were originally implemented in openFrameworks. Reading the OF examples for projection mapping and computer vision is the cheapest way to internalize the idiom set; the implementations themselves do not transfer to TD but the visual grammars do.

### D.2 TouchDesigner-specific production techniques

Verified from Derivative documentation and the Derivative community library (2024–26):

- **TOP / Render TOP family** for the animated frames; **Geometry COMP + Phong MAT** for any 3D phase-of-construction model.
- **Kantan Mapper** (palette / palette:kantanMapper) — the de facto first-pass projection-mapping tool. 2D polygons + bezier outlines + per-shape TOP fill. Sufficient for a flat tabletop. (Documented at docs.derivative.ca/Palette:kantanMapper.)
- **CamSchnappr / camera calibration** — used when the projector geometry needs precise correction; relevant if the tabletop is non-rectangular.
- **Script CHOP / CHOP Execute DAT / Parameter Execute DAT** for converting MediaPipe landmark streams into footprint vertices, height channels, and phase-state transitions (Derivative documentation).
- **Engine COMP** for isolating the gesture-tracking subsystem so its frame rate does not block the render thread when MediaPipe stalls (the plugin's `realTimeRatio` channel is the watchdog input).

### D.3 Recommended two precedents to study most closely

**(1) Augmented Bricklaying** for the *visual error-feedback grammar* — translucent target outlines, live registration color, snap-to-place audio-visual confirmation. Specifically extract: the four-state registration palette (idle / approaching / on-target / mis-set), the per-element animation curve, the confirmation latency. **(2) UC Davis AR Sandbox** for the *overhead-camera + overhead-projector + hand-as-occluder* loop and the open-source GLSL contour shaders. Specifically extract: the depth-statistic filter that distinguishes hands from substrate, the per-frame contour generation, the shader-side falloff that makes the projection forgive sensor noise.

### D.4 Failure modes specific to TouchDesigner production

1. **Plugin frame-rate coupling.** If MediaPipe-TD plugin cooks on the main thread, a lighting glitch in the camera feed can stall the entire render. Use Engine COMP isolation.
2. **Kantan Mapper at high resolution.** Bezier-warp geometry at 1080p tabletop projection is fine; at 4K with many warps, fragment cost rises sharply. Bake the projection-map TOP if it is static.
3. **GLSL-on-a-laptop heat ceiling.** Continuous shader work for an 8-hour exhibit day on a laptop GPU thermally throttles after ~90 min. Either ship a desktop or design the visual budget around 120 fps thermal-headroom rather than 240 fps clean-state.

### D.5 Named biases

- **Demo-reel bias.** TouchDesigner's public demo reels are dominated by audiovisual installations (concerts, club visuals). The installation is closer to a museum exhibit and should *not* benchmark against demo-reel pacing or saturation.
- **Mac-vs-Windows-tested-only bias.** Many community plugins and tutorials are tested on a single platform. Cross-test the gesture pipeline on both (the MediaPipe-TD plugin docs are explicit about Mac/Windows differences via Spout vs Syphon for SpoutCam fallbacks).
- **Fiducial-installation-aesthetics bias.** Installation precedents from 2003–2018 are dominated by the fiducial-puck visual language (rings, halos, connection lines between pucks). Post-pivot, the installation has no pucks. Borrow the *responsiveness*, not the puck-shaped iconography.

---

## Brief revisit

Sub-strand A's pivot-driven evidence is the strongest in this strand: there is a single, clearly-best production path (MediaPipe via the Blankensmith plugin) with a clearly-named fallback (Ultraleap). Sub-strand B's evidence is weakest because the AI-video field is moving weekly and any pick is a forecast; the recommendation is a *hybrid* path precisely because no single AI tool is yet a credible production target. Sub-strand C has the strongest academic basis — Hullman and van der Bles are foundational — and the recommendation rides directly on those papers. Sub-strand D's evidence is high-quality but heterogenous; the two-precedent recommendation is what crosses the action threshold.

Cross-cutting honesty: every sub-strand's recommendation is conditional on a pilot test that has not yet been run. The installation's commitment to methodology-wobble visualization extends naturally to the production stack itself — the TouchDesigner network should expose its own confidence ("hand tracking quality: 0.42") to the same overlay layer that surfaces LCA wobble, so visitors see when the instrument is uncertain about *them* with the same honesty it applies to the data.
