---
phase: 2
plan: 04
title: Design 3 method-selector models in Rhino (Masonry / 3DP / Prefab)
owner: _TBD_
wave: 1
depends_on: []
files_modified:
  - cad/method-selector-masonry-v1.3dm
  - cad/method-selector-masonry-v1.stl
  - cad/method-selector-3dp-v1.3dm
  - cad/method-selector-3dp-v1.stl
  - cad/method-selector-prefab-v1.3dm
  - cad/method-selector-prefab-v1.stl
  - cad/METHOD-SELECTORS-SPEC.md
  - cad/README.md
autonomous: false
requirements:
  - MOD-01
  - MOD-04
estimated_effort_hours: 4
---

<objective>
Design 3 distinct method-selector models in Rhino — one for Masonry, one for 3D-Printed, one for Modular Prefab — that visually represent each construction method's geometric language. These are the physical tokens the user places on the RFID pedestal in the FSM's METHOD state to choose a construction method (per PROJECT.md FSM section). Phase 4 wires the RFID + ESP32 firmware that READS them; this plan only DESIGNS the models so they exist in time for Phase 4 fabrication and so Phase 2's vertical slice can use them as visual reference. Each model must (a) fit on the RFID pedestal footprint (assume ~80 × 80 × 80 mm bounding box until pedestal housing is locked in Phase 4 — leave room for revision), (b) be visually distinguishable at a glance (different forms/silhouettes; the user shouldn't need to read a label), and (c) be 3D-printable on a standard FDM printer in <2 hours each. STL exports are produced now so the team can pre-print or reprint between Phase 2 and Phase 4 as needed. Reclaimed-brick is NOT a method selector — per locked decision #3 it's a baseline TOGGLE, not a fourth competitor; it gets a different physical token (visually distinct, possibly a separate dock or a side puck) which is OUT OF SCOPE for this plan.
</objective>

<must_haves>
- 3 Rhino source files (`.3dm`) and 3 STL exports — one per method (masonry, 3dp, prefab).
- Each STL fits within an 80 × 80 × 80 mm bounding box (leaves design room for the eventual RFID pedestal slot in Phase 4).
- The 3 models are visually distinguishable in a single glance — described in `cad/METHOD-SELECTORS-SPEC.md` with a one-sentence visual rationale per model linking the form to the construction method's geometric language.
- `cad/METHOD-SELECTORS-SPEC.md` documents (a) bounding-box, (b) print settings, (c) the form-rationale per model, (d) where the RFID tag will eventually go (cavity / underside slot / etc.) — so Phase 4 firmware integration knows where to embed the tag.
- Print time per model is < 120 minutes at standard FDM settings (sliced and verified — but actual printing is deferred; Phase 2 only requires the design + STL, NOT printing 3 models. Phase 4 prints them.)
- Models do NOT carry labels — visual form alone communicates the method (per OVERVIEW.md TL;DR item 1: "tokens carry identity and pose; projection carries meaning").
- `cad/README.md` inventory section (top of file) is updated to confirm the 3 method-selector models are designed (mark them as "designed, awaiting print" rather than just listed as TBD).
</must_haves>

<tasks>

<task type="auto">
  <name>Task 4.1: Write cad/METHOD-SELECTORS-SPEC.md (form-language brief + RFID-cavity locations)</name>
  <action>Create `cad/METHOD-SELECTORS-SPEC.md` with the form brief BEFORE designing in Rhino. This is the design contract the Rhino models must satisfy. Use this exact content:

  ```markdown
  # Method-selector models — design specification

  Three physical tokens placed by the user on the RFID pedestal during the FSM's METHOD state. Visual form alone communicates the construction method — no labels, no text. Per locked decision (CONTRIBUTING.md #1) and OVERVIEW.md TL;DR item 1 ("tokens carry identity and pose; projection carries meaning"), labelling these tokens would throw away the project's primary design lever.

  ## Constraints

  | Parameter | Value |
  |---|---|
  | Bounding box (max) | 80 × 80 × 80 mm |
  | Bounding box (min) | 40 × 40 × 40 mm — needs visual presence at table-distance viewing |
  | Material | PLA (standard FDM) |
  | Wall thickness (printed) | ≥ 1.2 mm to handle RFID tag cavity |
  | Visual contrast | each model must be distinguishable in 1 second from any viewing angle |
  | RFID tag cavity | one cavity per model: ~30 × 30 × 3 mm slot, on the UNDERSIDE, accessible after print without re-printing (e.g. press-fit, or screwed access panel) |
  | Print orientation | flat-bottom (cavity face down on build plate) so cavity is unsupported and clean |

  ## Form rationale per method

  ### Masonry (model 1)
  - Form: a small stack of brick-like rectangular prisms, slightly offset from each other (visual reference: a stretcher-bond brick stack, ~3 courses high).
  - Why: bricks are *the* iconic masonry unit; a layered stack reads "site-built, course by course".
  - Reference: Augmented Bricklaying (Mitterberger et al. 2020) — visual language of stacked discrete units.
  - Approximate dimensions: 70 × 30 × 50 mm (W × D × H), each "brick" ~22 × 30 × 14 mm, 3 courses.

  ### 3D-Printed (model 2)
  - Form: a hollow extruded toroidal/spiral wall with visible printed-bead striations on the external surface — TECLA / ICON visual language.
  - Why: 3DP construction's signature visual is the layered concrete bead; making the model SHOW its layer lines (rather than smoothing them) reads "additive process".
  - Reference: TECLA project (Cucinella + WASP, 2021); Striatus Bridge (ZHA + BRG, 2021).
  - Approximate dimensions: Ø60 mm × 70 mm tall, hollow, 3 mm wall thickness with 2-mm-tall horizontal grooves every 4 mm — modelled as actual geometry, NOT relying on slicer print artefacts.

  ### Prefab (model 3)
  - Form: a stack of 2 or 3 cuboid modules at slightly different scales, suggesting volumetric building modules / containers / CLT panels assembled.
  - Why: prefab's visual identity is "factory-made discrete volumes plugged together" — clean orthogonal forms, sharp edges, visible joint lines.
  - Reference: K.118 Halle 118 (baubüro in situ 2021); generic CLT panel assemblies; modular MiC volumes.
  - Approximate dimensions: 70 × 50 × 60 mm overall; modelled as 2 stacked modules of ~70×50×30 each, with a clearly visible 1-mm gap or chamfer between them to read "assembled, not monolithic".

  ## RFID tag cavity (all three)

  - Slot: 30 × 30 × 3 mm rectangular pocket on the underside of each model, centred under the model's centre-of-mass.
  - Access: open-bottom (the pocket is hollow on the underside; the printed tag cavity is closed on top and on all 4 sides).
  - Phase 4 will print, embed an MFRC522-compatible Mifare Classic tag in the pocket, and seal with a dot of hot glue or a 3D-printed press-fit cover.

  ## Print settings (all three)

  | Setting | Value |
  |---|---|
  | Layer height | 0.2 mm |
  | Infill | 20% (light — these are not load-bearing) |
  | Wall count | 3 |
  | Material | PLA, distinct colour per method (e.g. red/orange = masonry; light grey = 3DP; dark grey = prefab) — colour is secondary cue; form is primary |
  | Print orientation | flat bottom on build plate; RFID cavity faces down; supports only as needed |
  | Estimated print time | < 120 min per model |

  ## Phase 4 hand-off

  When Phase 4 wires RFID, the firmware owner needs:
  - Each model assigned a Mifare card UID (recorded in `firmware/RFID-UIDS.md` — Phase 4 task).
  - The cavity opens cleanly post-print (verified during Plan 04 print test).
  - Phase 4 may reprint these models with revised cavity dimensions if v1 does not seat cleanly.
  ```

  Don't deviate from these dimensions in Task 4.2 unless you find a Rhino modelling constraint that forces a change — in which case update this file FIRST, then model.</action>
  <read_first>
    - cad/README.md
    - .planning/PROJECT.md "FSM States" + "Toolkit" sections
    - .planning/phases/02-data-research-physical-model-design/02-CONTEXT.md
    - docs/research/lit-review/OVERVIEW.md TL;DR item 1
    - docs/research/lit-review/02-augmented-assembly.md (Mitterberger 2020 / Augmented Bricklaying visual language)
  </read_first>
  <acceptance_criteria>
    - `cad/METHOD-SELECTORS-SPEC.md` exists.
    - File contains 3 distinct sections under "## Form rationale per method", named "Masonry", "3D-Printed", "Prefab".
    - Each section names approximate dimensions and a literature reference.
    - File contains "## RFID tag cavity (all three)" section with concrete cavity dimensions (30 × 30 × 3 mm).
    - File contains "## Print settings" with layer height, infill, and per-model colour assignments.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 4.2: Model masonry method-selector in Rhino</name>
  <action>Open Rhino. Create `cad/method-selector-masonry-v1.3dm`. Model the masonry token per `cad/METHOD-SELECTORS-SPEC.md` "Masonry (model 1)":

  - Build 3 stacked brick prisms, each 22 × 30 × 14 mm, with stretcher-bond offset (each course shifted ~10 mm from the one below).
  - Total bounding box: ~70 × 30 × 50 mm (W × D × H).
  - On the UNDERSIDE of the bottom-course centre: subtract a 30 × 30 × 3 mm rectangular pocket centred under the model's centre-of-mass for the RFID tag.
  - 1 mm chamfer on all visible top edges (visual polish + reduces print fragility).

  Save as `cad/method-selector-masonry-v1.3dm`. Export STL as `cad/method-selector-masonry-v1.stl`:
  - Binary STL
  - Tolerance: 0.1 mm
  - Units: millimetres

  Open in slicer, slice with PLA + 0.2 mm + 20% infill + 3 walls, flat-bottom orientation. Confirm: print time < 120 min, no support needed under the RFID cavity (cavity faces DOWN on print bed, so the cavity opening is the FIRST layer — no support material inside).

  Save the screenshot from Rhino top + perspective + front views to `cad/preview/method-selector-masonry-v1.png` — useful for the spec doc and for Phase 4 reference.</action>
  <read_first>
    - cad/METHOD-SELECTORS-SPEC.md (Task 4.1)
    - cad/README.md (naming + version conventions)
  </read_first>
  <acceptance_criteria>
    - `cad/method-selector-masonry-v1.3dm` exists and is non-empty.
    - `cad/method-selector-masonry-v1.stl` exists and is non-empty.
    - STL bounding box (verified via slicer or any STL viewer): all three dimensions ≤ 80 mm and ≥ 40 mm.
    - Slice estimate < 120 min at standard PLA settings.
    - Preview render in `cad/preview/method-selector-masonry-v1.png` exists.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 4.3: Model 3D-printed method-selector in Rhino</name>
  <action>Open Rhino. Create `cad/method-selector-3dp-v1.3dm`. Model the 3DP token per `cad/METHOD-SELECTORS-SPEC.md` "3D-Printed (model 2)":

  - Build a hollow cylinder/torus of Ø60 mm × 70 mm tall, 3 mm wall thickness.
  - Add explicit horizontal grooves: 2 mm tall × 1 mm deep, every 4 mm of height, modelled as actual geometry (subtract a thin ring at every 4-mm interval). Approximately 17 grooves total.
  - On the UNDERSIDE: subtract a 30 × 30 × 3 mm rectangular pocket for the RFID tag (centred).
  - Bottom face flat (will sit on RFID pedestal); top face open (hollow cylinder geometry).

  Save as `cad/method-selector-3dp-v1.3dm`. Export STL: `cad/method-selector-3dp-v1.stl`. Slice estimate < 120 min.

  Save Rhino preview to `cad/preview/method-selector-3dp-v1.png`.</action>
  <read_first>
    - cad/METHOD-SELECTORS-SPEC.md (Task 4.1)
    - Task 4.2 output (for naming/formatting consistency)
  </read_first>
  <acceptance_criteria>
    - `cad/method-selector-3dp-v1.3dm` exists and is non-empty.
    - `cad/method-selector-3dp-v1.stl` exists and is non-empty.
    - STL bounding box dimensions: Ø ≤ 80 mm, height ≤ 80 mm, ≥ 40 mm in all dimensions.
    - The model has visible horizontal grooves modelled as geometry (verify in any STL viewer — should see ridges, not a smooth cylinder).
    - Slice estimate < 120 min.
    - Preview render in `cad/preview/method-selector-3dp-v1.png` exists.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 4.4: Model prefab method-selector in Rhino</name>
  <action>Open Rhino. Create `cad/method-selector-prefab-v1.3dm`. Model the prefab token per `cad/METHOD-SELECTORS-SPEC.md` "Prefab (model 3)":

  - Build 2 stacked rectangular modules, each 70 × 50 × 30 mm, with a 1 mm chamfer or 1 mm gap visible between them (modelled as real geometry — subtract a 1 × 70 × 1 mm strip at the seam).
  - Total bounding box: ~70 × 50 × 60 mm.
  - On the UNDERSIDE of the bottom module: subtract a 30 × 30 × 3 mm rectangular pocket for the RFID tag (centred).
  - 1 mm chamfer on all top + outside edges (visual polish + emphasises the discrete-volume reading).

  Save as `cad/method-selector-prefab-v1.3dm`. Export STL: `cad/method-selector-prefab-v1.stl`. Slice estimate < 120 min.

  Save Rhino preview to `cad/preview/method-selector-prefab-v1.png`.</action>
  <read_first>
    - cad/METHOD-SELECTORS-SPEC.md (Task 4.1)
    - Tasks 4.2 + 4.3 outputs (consistency)
  </read_first>
  <acceptance_criteria>
    - `cad/method-selector-prefab-v1.3dm` exists and is non-empty.
    - `cad/method-selector-prefab-v1.stl` exists and is non-empty.
    - STL bounding box: all dimensions ≤ 80 mm and ≥ 40 mm.
    - The model has a visible seam line between the two stacked modules (verify in any STL viewer).
    - Slice estimate < 120 min.
    - Preview render in `cad/preview/method-selector-prefab-v1.png` exists.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 4.5: Update cad/README.md inventory + print log entries (designed, awaiting print)</name>
  <coordination_required>
    **`cad/README.md` is also modified by Plan 02-03 (ArUco pucks fabrication) in the same Wave 1.** Whoever edits this file second MUST `git pull` first AND merge their inventory + print-log changes into the existing table without clobbering the other plan's rows. Recommended: the cad/ folder primary owner applies BOTH plan 02-03's and plan 02-04's batches in a single sequential pass to avoid the merge conflict entirely. Coordinate via group chat before touching this file.
  </coordination_required>
  <action>Edit `cad/README.md`. In the "## Inventory" section, update the line "3 method-selector models (masonry, 3DP, prefab) — go on the RFID pedestal" — replace with:

  ```
  3 method-selector models (masonry, 3DP, prefab) — designed in Phase 2 (see cad/METHOD-SELECTORS-SPEC.md). Awaiting print + RFID embed in Phase 4.
  ```

  Then in the "## Print log" table at the bottom, add 3 ROWS (these are "designed but not printed yet" rows — they document existence of the design, not a physical print):

  ```
  | method-selector-masonry-v1 | v1 | designed by _TBD_ | 2026-05-03 | STL ready, awaiting Phase 4 print |
  | method-selector-3dp-v1 | v1 | designed by _TBD_ | 2026-05-03 | STL ready, awaiting Phase 4 print |
  | method-selector-prefab-v1 | v1 | designed by _TBD_ | 2026-05-03 | STL ready, awaiting Phase 4 print |
  ```

  Do not delete or modify any existing rows. Do not change the "Conventions" section. **Before saving:** confirm Plan 02-03's print-log additions (3 puck-aruco-v1 rows) are either already present (apply on top) or coordinated to be applied in the same edit pass.</action>
  <read_first>
    - cad/README.md (current contents)
    - Task 4.1, 4.2, 4.3, 4.4 outputs
  </read_first>
  <acceptance_criteria>
    - `cad/README.md` "Inventory" section mentions `cad/METHOD-SELECTORS-SPEC.md`.
    - `cad/README.md` "Print log" table contains 3 new rows with names matching `method-selector-masonry-v1`, `method-selector-3dp-v1`, `method-selector-prefab-v1`.
    - The "Notes" column for each new row contains the string "Phase 4" (clearly marking these as Phase-4 prints, not Phase-2).
    - If Plan 02-03 has already added its 3 puck-aruco-v1 rows, those rows are still present (no clobbering).
  </acceptance_criteria>
</task>

</tasks>

<verification>
- 3 .3dm files exist in `cad/` for the three methods.
- 3 .stl files exist in `cad/` for the three methods.
- 3 preview PNGs exist in `cad/preview/`.
- `cad/METHOD-SELECTORS-SPEC.md` exists and references all three models.
- `cad/README.md` print log has 3 new rows for the method-selectors.
- For each STL, the bounding-box-fits check: open in any STL viewer, all dimensions ≥ 40 mm and ≤ 80 mm.
- For each STL, slicing in PrusaSlicer/Cura/BambuStudio at 0.2 mm + 20% infill + PLA returns a print estimate < 120 min.
</verification>
