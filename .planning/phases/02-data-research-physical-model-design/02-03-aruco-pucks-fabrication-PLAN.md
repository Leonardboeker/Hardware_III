---
phase: 2
plan: 03
title: ArUco puck design + 3D-print 3 test pieces
owner: _TBD_
wave: 1
depends_on: []
files_modified:
  - cad/puck-aruco-v1.3dm
  - cad/puck-aruco-v1.stl
  - cad/markers/aruco_dict_4x4_50_id00.png
  - cad/markers/aruco_dict_4x4_50_id01.png
  - cad/markers/aruco_dict_4x4_50_id02.png
  - cad/PUCK-SPEC.md
  - cad/README.md
autonomous: false
requirements:
  - MOD-01
  - MOD-02
  - MOD-03
  - MOD-04
estimated_effort_hours: 5
---

<objective>
Design and 3D-print 3 test ArUco footprint pucks (final 10 in Phase 3 — these 3 are detection-distance test pieces). Lock the puck physical dimensions, the ArUco dictionary, the marker physical size, and the marker-on-top-face attachment method so Plan 05 (calibration rig) and Plan 07 (one-puck closed-loop CV vertical slice) can build against a known geometry. This plan addresses MOD-01 (module type defined: physical geometry, material), MOD-02 (connection logic — here, "no connection between pucks; they sit free on the table surface and connectivity is computed in software from polygon-fit"), MOD-03 (valid vs invalid placement defined: a placement is valid when the puck centre is within tolerance T of a projected target zone — concrete tolerance value set in Plan 07 vertical-slice tuning), and MOD-04 (input method finalized: physical object placement, specifically a puck with a printed ArUco marker on its top face). Output: 3 printed pucks + a `PUCK-SPEC.md` that locks the parameters so the rest of Phase 2 work doesn't have to guess.
</objective>

<must_haves>
- `cad/PUCK-SPEC.md` exists and locks: puck diameter, puck height, ArUco dictionary, ArUco marker physical edge length (mm), marker-on-puck attachment method (printed-paper-glued vs printed-directly-on-top vs etched), marker IDs assigned to each of the 3 test pucks.
- `cad/puck-aruco-v1.3dm` (Rhino source) and `cad/puck-aruco-v1.stl` (export) exist and match the locked PUCK-SPEC.md dimensions.
- 3 printable marker images exist in `cad/markers/` — one per test puck — generated with the locked ArUco dictionary and IDs.
- `cad/README.md`'s print log table has 3 rows added: one per printed puck, with `Date`, `Printed by`, `Notes` filled in.
- 3 physical pucks have been printed and are physically present in the lab — verified by a checkpoint photo / a CAD-owner sign-off.
- The locked ArUco dictionary matches what Plan 05 (calibration) and Plan 07 (vertical slice) will use — i.e. this plan is the source of truth for the ArUco dictionary choice.
</must_haves>

<tasks>

<task type="checkpoint:decision">
  <name>Task 3.1: Decide ArUco dictionary + marker size + puck dimensions (CAD owner + Vision owner)</name>
  <decision>Three coupled parameters must be locked together because they constrain each other: (a) ArUco dictionary; (b) marker physical edge length in mm; (c) puck top-face diameter (must be ≥ marker edge + ~5 mm border).</decision>
  <context>
    From CONTEXT.md "Claude's Discretion":
    - DICT_4X4_50: smallest markers, fastest detection, only 50 IDs available — fine for 10 pucks + dial + height + a few spares.
    - DICT_5X5_100: more bits, more robust to partial occlusion, smaller library hits required.
    - DICT_6X6_250: most robust, largest minimum physical size needed for reliable detection at table-distance.

    From `cad/README.md`: puck Ø~50 mm is suggested but explicitly "confirm".

    From `docs/research/lit-review/01-tui-tabletops.md`: `cv2.aruco` with `DICT_4X4_50` or `DICT_5X5_50` is the documented default for tabletop work.

    Constraint to respect: at the actual camera-to-table distance the team has access to (overhead webcam mounted ~70–120 cm above the table — verify with whoever owns the rig), the marker physical edge must be large enough that ArUco detects reliably at the test resolution. As a starting heuristic, marker edge in pixels at the camera should be ≥ 30 px for DICT_4X4_50, ≥ 40 px for DICT_5X5_100, ≥ 50 px for DICT_6X6_250. The CAD owner + Vision owner should physically test this with a paper printout BEFORE committing to a 3D print.

    Ten footprint pucks need 10 distinct IDs; height marker = ID 10; material controller = ID 11; method-selector pieces in Plan 04 may use IDs 12–14 OR may use RFID instead. Reserve IDs 0–14 across the project.
  </context>
  <options>
    <option id="dict-4x4-50">
      <name>DICT_4X4_50 + 30 mm marker + Ø45 mm puck</name>
      <pros>Small puck, light, fast detection, library has 50 IDs (we need ≤15).</pros>
      <cons>Less robust to partial occlusion (e.g. user's finger on puck edge); fewer error-correction bits.</cons>
    </option>
    <option id="dict-5x5-100">
      <name>DICT_5X5_100 + 40 mm marker + Ø55 mm puck</name>
      <pros>Better robustness to partial occlusion; larger ID space (100); strong default per lit review.</pros>
      <cons>Slightly larger puck; marker generation/print needs higher-res printer.</cons>
    </option>
    <option id="dict-6x6-250">
      <name>DICT_6X6_250 + 50 mm marker + Ø65 mm puck</name>
      <pros>Maximum robustness — handles edge cases like partial occlusion and lighting variation best.</pros>
      <cons>Largest puck; more table real estate consumed; arguably overkill for this use.</cons>
    </option>
  </options>
  <resume-signal>Reply with one of: "dict-4x4-50", "dict-5x5-100", "dict-6x6-250", or "custom: <dict>+<marker_mm>+<puck_diameter_mm>" with rationale. The chosen value is then written into Task 3.2's PUCK-SPEC.md.</resume-signal>
</task>

<task type="auto">
  <name>Task 3.2: Write cad/PUCK-SPEC.md locking the parameters</name>
  <action>Create `cad/PUCK-SPEC.md` with the values chosen in Task 3.1. Use this exact structure (fill in concrete numbers from Task 3.1's decision):

  ```markdown
  # ArUco puck specification (LOCKED 2026-05-03)

  This spec is the source of truth for puck geometry, ArUco dictionary, and marker IDs across the project. Plan 05 (calibration rig) and Plan 07 (one-puck closed-loop CV vertical slice) read this file. Phase 3 scales the test count from 3 to the full 10 footprint pucks + height + material — those use the SAME spec values below.

  ## Puck physical geometry

  | Parameter | Value | Notes |
  |---|---|---|
  | Top-face diameter | <X> mm | flat disc on top to host marker |
  | Total height | <Y> mm | enough mass to sit stably; aim for ~15–20 mm |
  | Bottom rim chamfer | 1 mm × 45° | reduces edge wear |
  | Print material | PLA | standard FDM filament; matte white preferred for high marker contrast |
  | Print colour | matte white | dark/black markers on white substrate maximise ArUco contrast |
  | Infill | 30% | enough mass; faster print |
  | Layer height | 0.2 mm | speed over surface quality (top face is covered by marker anyway) |
  | Top-face surface | smooth, level | no support marks on the top face — orient print so top is the print start |

  ## ArUco marker

  | Parameter | Value |
  |---|---|
  | Dictionary | <DICT_4X4_50 / DICT_5X5_100 / DICT_6X6_250> |
  | Marker edge length | <Z> mm (square) |
  | White border | ≥ 1 marker-cell width on all sides (ArUco convention; do not crop) |
  | Print method | <printed on adhesive label, glued to puck top / printed directly with marker as decal> |

  ## Marker ID assignments

  | ID | Used for | Where |
  |---|---|---|
  | 0 | Test puck #1 | Plan 03 |
  | 1 | Test puck #2 | Plan 03 |
  | 2 | Test puck #3 | Plan 03 |
  | 3–9 | Footprint pucks 4–10 | Phase 3 |
  | 10 | Height dial | Phase 3 |
  | 11 | Material dial | Phase 3 |
  | 12–14 | Method-selector models (if not using RFID) | Plan 04 / Phase 3 |

  ## Detection distance budget

  - Camera mounted ~<H> cm above table.
  - At that height, marker edge resolves to ≥ <P> px in the camera frame.
  - Heuristic floor for reliable detection at this dictionary: ≥ 30 px (DICT_4X4_50), ≥ 40 px (DICT_5X5_100), ≥ 50 px (DICT_6X6_250).

  ## How to regenerate marker images

  ```python
  import cv2
  d = cv2.aruco.getPredefinedDictionary(cv2.aruco.<DICT>)
  for i in range(3):
      img = cv2.aruco.generateImageMarker(d, i, 200)  # 200 px square
      cv2.imwrite(f'cad/markers/aruco_<dict>_id{i:02d}.png', img)
  ```

  Print at <Z> mm × <Z> mm, ≥300 DPI, on matte adhesive paper. Flat-mount on puck top, no rotation reference required (ArUco infers orientation from the marker pattern itself).

  ## Why these choices

  Cross-reference: see Task 3.1 decision rationale in `.planning/phases/02-data-research-physical-model-design/02-03-aruco-pucks-fabrication-PLAN.md`.
  ```

  Replace every `<X>`, `<Y>`, etc. with the concrete value from Task 3.1.</action>
  <read_first>
    - cad/README.md
    - .planning/phases/02-data-research-physical-model-design/02-CONTEXT.md "Claude's Discretion"
    - docs/research/lit-review/01-tui-tabletops.md (ArUco default-dictionary guidance)
    - Task 3.1 decision output
  </read_first>
  <acceptance_criteria>
    - `cad/PUCK-SPEC.md` exists.
    - File contains every concrete parameter from Task 3.1 (no `<X>` placeholders remain).
    - File contains an "## ArUco marker" section with the chosen Dictionary value spelled out as `DICT_4X4_50` or `DICT_5X5_100` or `DICT_6X6_250`.
    - File contains an "## Marker ID assignments" table with IDs 0, 1, 2 explicitly assigned to "Test puck #1", "Test puck #2", "Test puck #3".
    - File contains the regeneration Python snippet under "## How to regenerate marker images".
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 3.3: Generate the 3 marker images (Python script + PNG outputs)</name>
  <action>Create `vision/src/generate_markers.py` (or use an ad-hoc script — it doesn't need to live in `vision/src` permanently if Plan 07 doesn't reuse it, but a committed script is simpler than a one-off REPL session). Script:

  ```python
  """Generate ArUco marker PNGs at 1024 px square per cad/PUCK-SPEC.md."""
  import os
  import cv2

  # MUST MATCH cad/PUCK-SPEC.md "Dictionary" value.
  DICTIONARY_NAME = "<DICT_FROM_PUCK_SPEC>"  # e.g. cv2.aruco.DICT_4X4_50
  OUT_DIR = "cad/markers"
  PIXELS = 1024  # high-res so print at any physical size remains crisp

  os.makedirs(OUT_DIR, exist_ok=True)
  d = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, DICTIONARY_NAME))
  for i in range(3):
      img = cv2.aruco.generateImageMarker(d, i, PIXELS)
      out_path = os.path.join(OUT_DIR, f"aruco_{DICTIONARY_NAME.lower()}_id{i:02d}.png")
      cv2.imwrite(out_path, img)
      print(f"wrote {out_path}")
  ```

  Run the script. Verify the 3 PNG files appear in `cad/markers/`. Each file should be a square black-on-white ArUco marker.

  IMPORTANT: replace `<DICT_FROM_PUCK_SPEC>` with the literal string from PUCK-SPEC.md (e.g. `"DICT_4X4_50"`). The filename pattern in the script names files by lowercased dict name + zero-padded ID — these names must match `files_modified` in the frontmatter (adjust frontmatter if the chosen dict produces different filenames; the names listed assume DICT_4X4_50).</action>
  <read_first>
    - cad/PUCK-SPEC.md (Task 3.2 output)
    - vision/README.md (for the suggested vision/src/ layout convention)
  </read_first>
  <acceptance_criteria>
    - `vision/src/generate_markers.py` exists.
    - Three PNG files exist in `cad/markers/` matching the pattern `aruco_<dict>_id00.png`, `id01.png`, `id02.png`.
    - Each PNG is at minimum 512×512 pixels (preferably 1024×1024 — high-res so print remains crisp at any size).
    - Each PNG is a valid black-on-white image (Python: PIL Image opens without error and `.size[0] == .size[1]`).
    - The script is re-runnable: deleting the PNGs and re-running the script produces identical files.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 3.4: Design puck geometry in Rhino + export STL</name>
  <action>Open Rhino. Create `cad/puck-aruco-v1.3dm` with a single puck primitive matching `cad/PUCK-SPEC.md`:

  - Cylinder, top-face diameter as specced (e.g. Ø45 mm), height as specced (e.g. 18 mm).
  - 1 mm × 45° chamfer on the bottom rim.
  - Top face flat and perpendicular to the cylinder axis (this is where the marker mounts — must be coplanar with the table surface plane when puck is placed).

  Save the source `.3dm` file to `cad/puck-aruco-v1.3dm`. Export as STL to `cad/puck-aruco-v1.stl` with these export settings:
  - Binary STL (smaller file)
  - Tolerance: 0.05 mm
  - Units: millimetres

  Open the exported STL in your slicer (Cura, PrusaSlicer, Bambu Studio — whichever the team's printer uses). Slice with these settings (matching PUCK-SPEC.md):
  - Layer height: 0.2 mm
  - Infill: 30%
  - Material: PLA, matte white preferred
  - Print orientation: TOP FACE DOWN on the build plate (this puts supports on the bottom rim, leaves the top face — where the marker goes — perfectly smooth)
  - Brim: 5 mm (good adhesion)
  - Supports: only as needed for the chamfer

  Confirm slice estimate: each puck should be < 30 minutes to print. If estimate exceeds 60 minutes per puck, re-check infill / layer height settings — overkill defeats "test pieces, not final 10".

  Save slicer project file alongside the STL if your slicer produces one (`puck-aruco-v1.gcode` or `.3mf`) — optional but useful for reproducibility.</action>
  <read_first>
    - cad/PUCK-SPEC.md (Task 3.2 output)
    - cad/README.md (naming + version conventions)
  </read_first>
  <acceptance_criteria>
    - `cad/puck-aruco-v1.3dm` exists and is non-empty.
    - `cad/puck-aruco-v1.stl` exists and is non-empty.
    - The STL, when opened in any STL viewer, shows ONE cylinder of approximately the dimensions in PUCK-SPEC.md (manual visual check).
    - File sizes: `.3dm` typically 50–500 KB; `.stl` typically 5–50 KB. Anything wildly outside this range suggests a misexport.
    - A slicer estimate < 60 minutes per puck (confirm in slicer UI; not committable but verifiable by the print-owner).
  </acceptance_criteria>
</task>

<task type="checkpoint:human-action">
  <name>Task 3.5: Print 3 pucks + apply markers + log to cad/README.md (HUMAN — printer + lab access required)</name>
  <what-built>The STL is ready in `cad/puck-aruco-v1.stl` and the 3 marker PNGs are in `cad/markers/`. The actual printing and physical marker-attachment require a 3D printer and a colour printer; Claude cannot do these.</what-built>
  <coordination_required>
    **`cad/README.md` is also modified by Plan 02-04 (method-selector models) in the same Wave 1.** Whoever edits this file second MUST `git pull` first AND merge their print-log rows into the existing table without clobbering the other plan's rows. Recommended: the cad/ folder primary owner applies BOTH plan 02-03's and plan 02-04's batches in a single sequential pass to avoid the merge conflict entirely. Coordinate via group chat before touching this file.
  </coordination_required>
  <how-to-verify>
    1. Slice `cad/puck-aruco-v1.stl` per the settings in Task 3.4 (layer 0.2 mm, 30% infill, PLA matte white, top-face-down orientation).
    2. Print 3 copies. Total wall-clock time: ~90 minutes (3 × ~30 min) on a typical FDM printer.
    3. Print each marker PNG from `cad/markers/` at the EXACT physical size in `cad/PUCK-SPEC.md` (e.g. 30 × 30 mm) on matte adhesive paper, ≥300 DPI. A standard inkjet/laser printer with photo paper or label sheets works. CRUCIAL: keep the white border around the marker — do NOT crop to the black region.
    4. Cut each marker out (square, with the white border intact).
    5. Stick one marker per puck on the top face, centred. Marker IDs 0, 1, 2 — one per puck. Mark the puck side or bottom with the ID in pen so the team can tell them apart at a glance.
    6. Open `cad/README.md` and add 3 rows to the "Print log" table (NOTE: coordinate with Plan 02-04 owner first — see <coordination_required> above):

       ```
       | puck-aruco-v1 (id 0) | v1 | <YOUR_NAME> | 2026-05-03 | matte white PLA, marker glued, ready for Plan 05/07 |
       | puck-aruco-v1 (id 1) | v1 | <YOUR_NAME> | 2026-05-03 | as above |
       | puck-aruco-v1 (id 2) | v1 | <YOUR_NAME> | 2026-05-03 | as above |
       ```

    7. Take ONE photo of all 3 pucks side-by-side on the table (with markers visible). Save to `cad/photos/pucks-v1-2026-05-03.jpg` so future readers can see what "v1 puck" actually looks like.
  </how-to-verify>
  <resume-signal>Type "3-pucks-printed" with the path to the photo, OR "delayed: <reason>" if the printer is unavailable. If delayed, Plan 07 (vertical slice) is BLOCKED until at least 1 puck exists physically.</resume-signal>
</task>

</tasks>

<verification>
- `cad/PUCK-SPEC.md` exists and contains literal values for diameter, height, dictionary, marker edge.
- `cad/puck-aruco-v1.3dm` and `cad/puck-aruco-v1.stl` exist.
- 3 marker PNGs exist in `cad/markers/` for IDs 0, 1, 2 in the chosen dictionary.
- `cad/README.md` print log has 3 rows added with date 2026-05-03 (or later).
- `cad/photos/pucks-v1-*.jpg` exists (photo evidence of physical pucks).
- The dictionary string in PUCK-SPEC.md matches the string used in `vision/src/generate_markers.py` (consistency check before Plan 05/07 read either).
</verification>
