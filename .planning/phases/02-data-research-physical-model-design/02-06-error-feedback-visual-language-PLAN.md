---
phase: 2
plan: 06
title: Error-feedback visual language specification (lock the green/red/ghost grammar)
owner: _TBD_
wave: 1
depends_on: []
files_modified:
  - touchdesigner/ERROR-FEEDBACK-SPEC.md
  - touchdesigner/error-feedback-palette.png
  - touchdesigner/error-feedback-mockup.png
autonomous: false
requirements:
  - MOD-03
estimated_effort_hours: 3
---

<objective>
Lock the visual language for closed-loop feedback in the FSM: what does "valid placement" look like, what does "invalid placement" look like, and what does the "ghost of the correct position" look like when the user is wrong. This is a design + curation decision, NOT an implementation task — Plan 07 (one-puck closed-loop CV vertical slice) IMPLEMENTS this language in TouchDesigner. This plan PRODUCES THE SPEC so Plan 07 has zero design ambiguity. The reference pattern, per locked decision and lit review (`docs/research/lit-review/02-augmented-assembly.md`), is Augmented Bricklaying (Mitterberger et al. 2020): when wrong position detected, project the CORRECT position as a transparent ghost so the user can self-correct without text instructions. This plan also addresses the lit-review's accessibility critique (`OVERVIEW.md` "What the literature says fails" item 3): "red-green color coding without secondary cues fails ~4.5% of viewers and conflates good/bad with technical magnitude" — so the spec mandates redundant visual cues (motion, line weight, fill pattern) on top of colour. Addresses MOD-03 (connection valid vs invalid states defined: what makes a placement correct — the spec gives the user-visible criteria for "correct"; numeric tolerance is set in Plan 07 tuning).
</objective>

<must_haves>
- `touchdesigner/ERROR-FEEDBACK-SPEC.md` exists and defines the visual states (valid / pending / invalid-with-ghost / disconnected/no-marker) with concrete RGB values, line weights, and animation parameters that Plan 07 reads VERBATIM and implements in TouchDesigner.
- The spec includes the redundancy rule: every state distinguishable by AT LEAST 2 cues (colour + form/motion/line-style) so colour-blind users still get the signal.
- The spec includes a "ghost of correct position" pattern definition (alpha, line style, line weight) per Augmented Bricklaying.
- The spec is colour-blind-safe — no pure red/green pairing as the SOLE distinguisher; the IPCC AR6 colourblind-safe palette (or equivalent — viridis-derived) is referenced.
- Two visual aids exist: (a) `touchdesigner/error-feedback-palette.png` showing the chosen colours as swatches with hex codes; (b) `touchdesigner/error-feedback-mockup.png` showing what the projection looks like in each state (can be a simple GIMP/Figma/Photoshop mockup — even a hand-drawn PNG is acceptable for v1).
- The spec links back to `docs/research/lit-review/02-augmented-assembly.md` and `docs/research/lit-review/05-lca-visualization.md` for the source-research justification.
- An "audio cue" decision is made and locked: either "no audio in Phase 2 vertical slice" OR "specific WAV / synth tone" — Phase 4 is when sound becomes a first-class layer; Phase 2 may opt out, but the spec records the decision.
</must_haves>

<tasks>

<task type="checkpoint:decision">
  <name>Task 6.1: Pick the colour palette + redundancy strategy (Curation + TD owners)</name>
  <decision>Lock the 4-state colour palette and the secondary cue strategy for distinguishing states beyond colour.</decision>
  <context>
    The lit review is explicit: "Red-green color coding without secondary cues fails ~4.5% of viewers and conflates 'good/bad' with technical magnitude" (`OVERVIEW.md` "What the literature says fails", item 3). So the spec MUST use:
    1. A colourblind-safe base palette (IPCC AR6, viridis, or a custom 4-state palette with ΔE > 30 between any two states under projector light).
    2. AT LEAST one secondary cue per state — line style (solid/dashed/dotted), line weight, fill pattern (filled/outline/hatch), animation (pulse/static/strobe), or shape (circle/square/diamond).

    The 4 visual states the FSM needs (locked in this Phase 2 vertical slice; Phase 3 may add more):
    - **VALID**: puck centre is within tolerance T of the projected target zone. Means "transition can fire / state advances".
    - **PENDING**: a puck is detected, system is computing the comparison, < ~50 ms transitional state.
    - **INVALID-WITH-GHOST**: puck centre is OUTSIDE tolerance. The projection shows the puck WHERE IT IS (annotated as wrong) AND a ghost of the correct position (faded outline of where the puck SHOULD be) so the user can self-correct without text instructions.
    - **DISCONNECTED / NO-MARKER**: no ArUco detected at all. Means "place a puck somewhere on the table; nothing detected".
  </context>
  <options>
    <option id="ipcc-ar6-with-secondary-cues">
      <name>IPCC AR6 colourblind-safe palette + secondary cue per state</name>
      <pros>Most cited as the colourblind-safe choice in scientific data viz; well-tested under projector light; secondary cues (motion + line style) make the palette robust without needing colour to do all the work.</pros>
      <cons>The palette defaults to muted earth-tone hues — less "punchy" than a saturated green/red, which means the projection may need higher absolute brightness to read at exhibition distance.</cons>
    </option>
    <option id="viridis-with-secondary-cues">
      <name>Viridis-derived 4-state palette + secondary cue per state</name>
      <pros>Highest perceptual uniformity across colour-blindness types; the matplotlib default for a reason. Strong recognition in academic audiences.</pros>
      <cons>Viridis is a CONTINUOUS gradient — picking 4 discrete states from it is somewhat arbitrary. Less semantic mapping ("yellow = good" is cultural; viridis doesn't enforce that).</cons>
    </option>
    <option id="custom-4-state-saturated">
      <name>Custom 4-state palette: cyan/teal=VALID, neutral grey=PENDING, magenta=INVALID, dark blue=DISCONNECTED + secondary cues</name>
      <pros>Cyan vs magenta is colourblind-safe (no red-green axis); high saturation reads well under projector light; intuitive valid/invalid mapping without using the failing red/green pair.</pros>
      <cons>Requires user education (initial brief 5-second projection legend at IDLE state; doesn't map to traffic-light intuition).</cons>
    </option>
  </options>
  <resume-signal>Reply with one of: "ipcc-ar6-with-secondary-cues", "viridis-with-secondary-cues", "custom-4-state-saturated", or "custom: <hex_valid>+<hex_pending>+<hex_invalid>+<hex_disconnected>" with rationale. Whichever is chosen, Task 6.2 writes the spec around it.</resume-signal>
</task>

<task type="auto">
  <name>Task 6.2: Write touchdesigner/ERROR-FEEDBACK-SPEC.md</name>
  <action>Create `touchdesigner/ERROR-FEEDBACK-SPEC.md` using the chosen palette from Task 6.1. Use this exact structure (replace `<HEX>` placeholders with the chosen values; if `custom-4-state-saturated` was chosen, the values are: VALID=#00B4B4, PENDING=#888888, INVALID=#D946EF, DISCONNECTED=#1E3A8A; if `ipcc-ar6-with-secondary-cues` chosen, use IPCC AR6 categorical palette — primary categorical hex codes from the IPCC visual style guide; if viridis chosen, sample at 0.0/0.33/0.67/1.0 of the viridis colormap):

  ```markdown
  # Error-feedback visual language (LOCKED 2026-05-03)

  This spec is the source of truth for how the projection responds to detected vs expected puck positions. Plan 07 (one-puck closed-loop CV vertical slice) implements this in TouchDesigner verbatim — no design ambiguity at execution time. Phase 3 + Phase 4 inherit and extend this grammar.

  Reference: Augmented Bricklaying (Mitterberger et al. 2020) interaction loop — `docs/research/lit-review/02-augmented-assembly.md`. Accessibility constraint: `docs/research/lit-review/OVERVIEW.md` "What the literature says fails" item 3 (red-green colour coding without secondary cues fails ~4.5% of viewers).

  ## States

  Four visible states, distinguished by AT LEAST 2 cues each. Colour alone is never the only cue.

  | State | Colour | Secondary cue 1 | Secondary cue 2 | Meaning |
  |---|---|---|---|---|
  | VALID | <HEX_VALID> | solid filled outline around puck | static (no animation) | puck is in the correct position; FSM may advance |
  | PENDING | <HEX_PENDING> | solid filled outline, 60% alpha | brief 200 ms pulse to 100% alpha then settle | puck detected; system is computing comparison |
  | INVALID-WITH-GHOST | <HEX_INVALID> | dashed outline around puck (where it is) PLUS a ghost outline at correct location | the GHOST pulses at 0.5 Hz to draw the eye | puck outside tolerance; ghost shows where to put it |
  | DISCONNECTED | <HEX_DISCONNECTED> | dotted outline around the projected target zone (no puck involved) | slow rotation of dotted outline (1 turn / 5 s) | no marker detected; place a puck on the table |

  ## Outline geometry

  - VALID: solid filled circle, diameter = puck diameter + 8 mm (8 mm halo around puck).
  - PENDING: same as VALID but 60% alpha, then a 200-ms pulse to 100% alpha and back.
  - INVALID-WITH-GHOST: TWO concentric outlines around the puck (where puck IS): a dashed outline at puck-diameter + 8 mm, dash 4 mm on / 4 mm off, line weight 3 px. PLUS a SEPARATE ghost outline at the CORRECT target zone: same dashed style but 30% alpha, line weight 2 px, pulsing 100% / 30% alpha at 0.5 Hz.
  - DISCONNECTED: a single dotted outline at the projected target zone, dot 2 mm diameter spaced 6 mm apart, 50% alpha, slowly rotating.

  ## Tolerance

  - DEFAULT TOLERANCE: a puck centre within 15 mm of the projected target centre = VALID. Outside that = INVALID.
  - Plan 07 may tune this to 10–25 mm based on the actual ArUco-detection jitter measured during the vertical-slice run; record the chosen value in `vision/calibration/TOLERANCE.md` after tuning.
  - Phase 3 may set a per-puck tolerance (e.g. tighter for walls, looser for footprint pucks).

  ## Audio cue (Phase 2 decision)

  - **Phase 2 vertical slice: NO audio.** Audio is a Phase-4 deliverable per CONTEXT.md "Out of scope". The vertical slice tests the visual closed loop end-to-end; adding audio adds a debugging surface we don't need yet.
  - Phase 4 will add: short success tone on VALID transitions, low neutral hum on PENDING, soft "click-back" on INVALID. Spec'd then.

  ## Latency budget

  - Detection (ArUco) → state classification: < 50 ms.
  - State classification → projection update: < 100 ms.
  - Total visible-feedback latency: < 150 ms (matches HITL-02 + Phase 6 final-demo target).
  - Ghost pulse animation: 0.5 Hz = 2 s period, smooth eased-sine alpha modulation, NOT a square wave (looks broken).

  ## TouchDesigner implementation hints

  - Use `Constant TOP` + `Composite TOP` for state-coloured outlines.
  - Use a single `Switch TOP` driven by the FSM state CHOP to flip between the 4 visual states.
  - Use `LFO CHOP` at 0.5 Hz, sine wave, mapped to alpha for the ghost pulse.
  - The "ghost at correct position" output is just a SECOND constant + transform pipeline that draws the outline at the projected target coordinates — not the detected puck coordinates.

  ## Why these choices

  - Augmented Bricklaying's "ghost of correct position" pattern (Mitterberger et al. 2020) is the closest published precedent for letting users self-correct without text. Same here.
  - IPCC AR6 / viridis-derived / cyan-magenta palettes (whichever was chosen in Task 6.1) avoid the red-green axis that fails colourblind viewers.
  - Two-cue redundancy means a colourblind viewer sees state from outline style alone; a viewer with hearing loss is unaffected (no audio); a viewer at a distance still sees the static-vs-pulsing distinction.

  ## See also

  - `docs/research/lit-review/02-augmented-assembly.md` — Mitterberger 2020.
  - `docs/research/lit-review/OVERVIEW.md` "What the literature says fails" item 3 — accessibility critique.
  - `docs/research/lit-review/05-lca-visualization.md` (background; Phase 4 wobble-layer visual language extends this spec).
  - `.planning/phases/02-data-research-physical-model-design/02-07-cv-vertical-slice-PLAN.md` — Plan 07 implements this spec.
  ```

  Replace `<HEX_VALID>`, `<HEX_PENDING>`, `<HEX_INVALID>`, `<HEX_DISCONNECTED>` with the concrete values from Task 6.1's decision (e.g. for `custom-4-state-saturated`: `#00B4B4`, `#888888`, `#D946EF`, `#1E3A8A`).</action>
  <read_first>
    - docs/research/lit-review/02-augmented-assembly.md (Mitterberger 2020 interaction loop)
    - docs/research/lit-review/OVERVIEW.md "What the literature says fails" section
    - docs/research/lit-review/05-lca-visualization.md (background — read for the data-vis colour conventions context)
    - .planning/phases/02-data-research-physical-model-design/02-CONTEXT.md "Specifics" section
    - Task 6.1 decision output
  </read_first>
  <acceptance_criteria>
    - `touchdesigner/ERROR-FEEDBACK-SPEC.md` exists.
    - File contains a "## States" table with exactly 4 rows (VALID, PENDING, INVALID-WITH-GHOST, DISCONNECTED).
    - Every row in the States table contains entries for `Secondary cue 1` AND `Secondary cue 2` — never blank (the redundancy rule is enforced).
    - File contains an "## Outline geometry" section with concrete dimensions in mm and px.
    - File contains a "## Tolerance" section with a default value (15 mm).
    - File contains an "## Audio cue (Phase 2 decision)" section with the explicit "NO audio in Phase 2" decision.
    - File contains a "## Latency budget" section with the < 150 ms total figure.
    - File contains 4 distinct hex colour codes (verify by grep for `#[0-9A-Fa-f]{6}` returning at least 4 unique matches).
    - No row has the same colour as another row (uniqueness check on hex values).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 6.3: Generate touchdesigner/error-feedback-palette.png swatch image</name>
  <action>Create a small Python script that renders a 4-swatch palette as PNG using PIL or matplotlib. Save it to `touchdesigner/error-feedback-palette.png`. Use the 4 hex values from `touchdesigner/ERROR-FEEDBACK-SPEC.md`. The image: 4 horizontal rectangles, each 200 × 100 px, labelled below with state name + hex code. Total image size 800 × 150 px.

  Skeleton (uses Pillow which is a transitive dep of opencv-contrib-python via numpy — if Pillow isn't installed, add `pillow` to vision/pyproject.toml or use matplotlib which is more likely installed):

  ```python
  """Render the locked 4-state palette as a swatch reference image."""
  from PIL import Image, ImageDraw, ImageFont

  STATES = [
      ("VALID",        "<HEX_VALID>"),
      ("PENDING",      "<HEX_PENDING>"),
      ("INVALID-GHOST","<HEX_INVALID>"),
      ("DISCONNECTED", "<HEX_DISCONNECTED>"),
  ]
  W, H = 200, 100
  PAD = 30  # space below for labels
  img = Image.new("RGB", (W * 4, H + PAD), "white")
  d = ImageDraw.Draw(img)
  try:
      font = ImageFont.truetype("arial.ttf", 14)
  except Exception:
      font = ImageFont.load_default()
  for i, (name, hexv) in enumerate(STATES):
      x0 = i * W
      d.rectangle([x0, 0, x0 + W, H], fill=hexv)
      d.text((x0 + 8, H + 4), f"{name}", fill="black", font=font)
      d.text((x0 + 8, H + 18), hexv, fill="black", font=font)
  img.save("touchdesigner/error-feedback-palette.png")
  print("wrote touchdesigner/error-feedback-palette.png")
  ```

  Replace `<HEX_*>` with the concrete chosen values from Task 6.2. Run the script. Verify the PNG exists and visually shows 4 distinct colour swatches.</action>
  <read_first>
    - touchdesigner/ERROR-FEEDBACK-SPEC.md (Task 6.2 — for the 4 hex values)
  </read_first>
  <acceptance_criteria>
    - `touchdesigner/error-feedback-palette.png` exists.
    - Image is at least 800 × 130 px.
    - Image is openable in any image viewer and shows 4 distinct colour rectangles.
  </acceptance_criteria>
</task>

<task type="checkpoint:human-action">
  <name>Task 6.4: Produce touchdesigner/error-feedback-mockup.png (HUMAN — design tool required)</name>
  <what-built>The spec is locked, the palette swatch exists. The mockup that shows what the actual projection LOOKS like in each state is more efficient to produce in a design tool (Figma, Affinity Designer, Adobe XD, or even hand-sketched on paper + photographed) than to script.</what-built>
  <how-to-verify>
    1. Open your design tool of choice. Canvas size: 1280 × 720 px (matches default projector resolution).
    2. Draw 4 panels (each 640 × 360 px), one per state from `touchdesigner/ERROR-FEEDBACK-SPEC.md`:
       - VALID: a solid-filled cyan/teal halo around a placeholder circle (puck) at the projected target.
       - PENDING: same halo at 60% alpha.
       - INVALID-WITH-GHOST: the puck circle in one location with a dashed outline; AND a ghost outline at a DIFFERENT location (showing where the puck SHOULD go).
       - DISCONNECTED: a dotted outline at the target with no puck visible.
    3. Each panel: small text label under it ("VALID — puck in tolerance, FSM advances", etc.).
    4. Export as PNG. Save to `touchdesigner/error-feedback-mockup.png`.
    5. Check that a teammate seeing the mockup for the first time can match each panel to its state from the SPEC.md description without asking.
  </how-to-verify>
  <resume-signal>Type "mockup-saved" when the PNG is committed, OR "delayed: <reason>" if blocked. Plan 07 can proceed without the mockup (the SPEC.md is the implementation source of truth) but the mockup helps the TD owner mentally model the result.</resume-signal>
</task>

</tasks>

<verification>
- `touchdesigner/ERROR-FEEDBACK-SPEC.md` exists and contains 4-state table + outline geometry + tolerance + audio decision + latency budget sections.
- `touchdesigner/error-feedback-palette.png` exists.
- `touchdesigner/error-feedback-mockup.png` exists (after Task 6.4 checkpoint).
- The hex values in the spec match the swatch colours in palette.png.
- Plan 07's `<read_first>` for its implementation tasks references `touchdesigner/ERROR-FEEDBACK-SPEC.md` (verifies the design-implementation handoff).
</verification>
