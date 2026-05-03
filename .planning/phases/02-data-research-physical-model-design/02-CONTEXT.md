# Phase 2: Data Research & Physical Model Design — Context

**Gathered:** 2026-05-03
**Status:** Ready for planning
**Source:** Synthesized from ACTIONS.md + lit-review/OVERVIEW.md + locked decisions in PROJECT.md (no `/gsd-discuss-phase` run — context built from existing artifacts, similar to PRD express path)

<domain>
## Phase Boundary

Phase 2 delivers **the foundational data corpus + the first working closed-loop CV vertical slice** that proves the chosen architecture is viable before Phase 3 scales it to the full FSM with ten pucks.

**In scope:**
- Tier-1 LCA data sourcing for the three target methods (Masonry, 3D-Printed, Prefab) + the reclaimed-brick baseline. Catalonia regional sources prioritised.
- Camera-projector calibration rig (checkerboard + ArUco-board procedure, documented and repeatable).
- One-puck closed-loop CV vertical slice in TouchDesigner: ArUco puck on table → overhead webcam detects → position compared against projected target zone → projector shows green (valid) or red ghost (correct position) → TD state advances.
- 3D-print 3 test ArUco pucks (final 10 in Phase 3) and design 3 method-selector models for the RFID pedestal in Rhino.
- Lock the error-feedback visual language (color, ghost projection, optional audio cue).
- Apply the three slide-deck reference corrections (reacTable, Augmented Bricklaying, Augmented Carpentry) before next presentation.

**Out of scope (Phase 3+ owns these):**
- Scaling closed-loop CV to ten footprint pucks + height + material controllers (Phase 3).
- Full FSM in TouchDesigner with all eight states wired (Phase 3).
- RFID pedestal + ESP firmware integration (Phase 4).
- Methodology-wobble overlay as a TD component (Phase 4 — Phase 2 only delivers the *data ranges* this layer will draw from).
- Sound layer / proximity sensor / projection-mapping calibration in exhibition lighting (Phases 4-5).
- AI-generated phase animations (paused per locked decision #4 until Phase 2's tier-1 numbers are signed off).

</domain>

<decisions>
## Implementation Decisions

### Locked decisions inherited from project (PROJECT.md, dated 2026-05-03)

These five positions are taken — backed by the literature review at `docs/research/lit-review/`. Not subject to renegotiation in this phase.

1. **Closed-loop computer vision from day one.** The Phase 2 vertical slice MUST be closed-loop. No "press a button to advance" baseline. Manual hotkey override is built in Phase 6 as emergency demo insurance only.
2. **TouchDesigner is the runtime.** Replaces Anemone (FSM) and Firefly (vision). All Phase 2 software work happens in TouchDesigner + OpenCV/Python (the latter either standalone piping to TD via OSC, or inside a TD Script CHOP — implementation choice deferred to the planner).
3. **Reclaimed brick is a baseline toggle.** Phase 2 sources reclaimed-brick LCA values as the floor; visualisation is Phase 5 responsibility.
4. **Methodology-wobble must be expressible.** Phase 2 stores LCA values as **ranges with assumption notes**, not single figures, so Phase 4's wobble overlay has data to draw from. CSV column convention: `value_low, value_high, assumption, source, source_tier`.
5. **AI-generated phase animations paused.** Phase 2 must NOT spend any time on phase-animation work.

### Data sourcing tiering (NEW for Phase 2)

Every LCA data row MUST carry a `source_tier` annotation:
- **Tier 1**: Peer-reviewed journal article OR validated EPD (Environmental Product Declaration) registered with INIES, EPDItaly, or EPD International. CYPE, BEDEC (ITeC), and Spain-published EPDs count as Tier 1 for Catalonia regional baseline.
- **Tier 2**: Government / institutional report (EU Joint Research Centre, ITeC publications outside BEDEC, Re:Crete and Halle 118 case studies for reclaimed brick).
- **Tier 3**: Vendor claim (Apis Cor, ICON, COBOD, TECLA WASP, modular prefab manufacturers). Must be flagged as `tier=3` and disclosed in any presentation.

**Rule:** Tier 3 numbers may appear in the dataset but never as the *sole* number for a method. Every Tier 3 datapoint must have a Tier 1 or Tier 2 sibling for triangulation.

### Closed-loop CV vertical slice — minimum acceptance

The "one-puck vertical slice" success criterion (ROADMAP Phase 2.4) means demonstrating end-to-end:
1. ArUco puck (pre-3D-printed test piece, ~Ø50mm with marker on top face) placed within camera-visible area.
2. Overhead webcam captures frame in TouchDesigner (via Video Device In TOP or Python+OpenCV piping via OSC — planner picks).
3. ArUco detection runs (cv2.aruco.detectMarkers or equivalent TD Script CHOP).
4. Detected puck centre point is transformed from camera-pixel space to projector-output space using the homography produced by the calibration rig.
5. Position compared against a projected target zone (rectangle or circle drawn by TD in projector output).
6. **Within-tolerance:** projector shows green confirmation around the puck. TD FSM advances to next state. **Out-of-tolerance:** projector shows red ghost at the correct position. FSM stays in current state.
7. End-to-end latency under 150 ms (measured detection-to-projection-update — same threshold as Phase 6 final demo).

This is a *vertical slice* — small in scope, complete in depth. Single puck, single state transition, single target zone. Phase 3 scales it.

### Calibration rig — minimum acceptance

A documented, repeatable procedure that any team member can run in <30 min:
1. Camera intrinsics calibrated using a printed checkerboard (cv2.calibrateCamera).
2. Projector-to-camera homography calibrated using a printed ArUco board (project known marker positions, detect them with the camera, solve for homography matrix).
3. Both calibration outputs (intrinsics matrix, distortion coefficients, homography) saved to `vision/calibration/` as YAML/JSON, version-controlled.
4. A `RECALIBRATE.md` runbook in `vision/calibration/` describing the procedure step by step.

### Data store convention

LCA datasets stored as CSV under `data/`:
- `data/methods/masonry.csv`, `3d-printed.csv`, `prefab.csv`, `reclaimed-brick.csv`
- Schema: `phase,parameter,value_low,value_high,unit,assumption,source,source_tier`
- Where `phase` is one of: foundation, structure, roof, openings, finishing
- Where `parameter` is one of: co2_kg_per_m2, labor_hours_per_m2, time_days, cost_eur_per_m2, material_origin

### Claude's Discretion (left to the planner)

These are implementation choices the planner can make based on team skills:
- **Vision pipeline location:** Python+OpenCV standalone (piping to TD via OSC) vs TD Script CHOP with OpenCV. Both work; choice depends on whoever owns `vision/`.
- **ArUco dictionary:** DICT_4X4_50 vs DICT_5X5_100 vs DICT_6X6_250 — picks affect marker physical size needed for reliable detection at table-distance.
- **Calibration target sizes:** the printed checkerboard and ArUco board dimensions, given the actual camera + projector throw distance the team has access to.
- **CSV vs JSON for data:** CSV is the recommended default but planner may justify JSON if there's structural nesting that doesn't map well.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project-level decisions (these supersede any older content)
- `.planning/PROJECT.md` — concept, FSM, locked decisions (2026-05-03 update)
- `.planning/STATE.md` — current phase status
- `.planning/ROADMAP.md` — Phase 2 Success Criteria (just realigned, this is the source of truth for "what done looks like")
- `.planning/REQUIREMENTS.md` — REQ definitions for MOD-01..04 and INP-01..03
- `CONTRIBUTING.md` — locked decisions section, branching rules, TouchDesigner .toe coordination

### Lit review (the research backing for Phase 2 decisions)
- `docs/research/lit-review/OVERVIEW.md` — synthesis briefing (read first)
- `docs/research/lit-review/ACTIONS.md` — week-by-week action plan, source of Phase 2 task list
- `docs/research/lit-review/01-tui-tabletops.md` — TUI lineage; ArUco library citation (Garrido-Jurado et al. 2014); reacTable provenance
- `docs/research/lit-review/02-augmented-assembly.md` — Augmented Bricklaying interaction loop (the pattern to replicate); error-feedback visual language reference
- `docs/research/lit-review/03-projection-guided-construction.md` — calibration techniques; Parascho's assembly-FSM framing; TouchDesigner runtime references
- `docs/research/lit-review/04-reuse-and-reclaimed-materials.md` — Re:Crete and Halle 118 case studies (reclaimed-brick LCA sources)
- `docs/research/lit-review/05-lca-visualization.md` — *will inform Phase 4 not Phase 2*, but useful background
- `docs/research/lit-review/06-comparative-lca-and-museum-interactives.md` — Catalonia data sources (CYPE, BEDEC, ITeC); LCA methodology caveats (Pomponi et al., De Wolf et al., Hertwich)

### Subsystem READMEs (define folder conventions Phase 2 work lands in)
- `vision/README.md` — vision pipeline conventions (camera intrinsics in `calibration/`, OSC out)
- `data/README.md` — CSV conventions, mandatory `source` annotation
- `cad/README.md` — 3D-print version log + STL naming
- `touchdesigner/README.md` — `.toe` coordination rules

</canonical_refs>

<specifics>
## Specific Ideas

### Direct guidance derived from ACTIONS.md Week 1 tasks (these become candidate plans)

1. **Camera-projector calibration rig.** Days 1-2. Highest-leverage engineering task. Owner = Vision. Per strand 03 — calibration drift is the demo-day failure mode of this whole literature.
2. **One puck → one target → one transition.** Minimum closed-loop demo proving the architecture works end-to-end. Owner = Vision + TouchDesigner. References Augmented Bricklaying interaction loop (strand 02).
3. **Error-feedback visual language.** Decide *now* what wrong-placement looks like. Augmented Bricklaying's pattern is the right reference. Owner = TouchDesigner + Curation.
4. **LCA data sourcing — Catalonia tier-1.** CYPE, BEDEC (ITeC), publicly available EPDs. CSV with mandatory `source_tier` column. Vendor claims (Apis Cor, ICON, TECLA) flagged tier 3. Owner = Data.
5. **3D-print 3 test ArUco pucks.** Lock dimensions and marker size from Week 1 detection-distance tests. Owner = CAD.
6. **Slide-deck reference corrections** (tonight, before any next presentation): "Swiss museum DJ table" → reacTable; "Brick Vault" → Augmented Bricklaying; "Discrete Wood" → Augmented Carpentry.

### Specific Augmented Bricklaying patterns to replicate (strand 02)

- Closed-loop confirmation pattern: detect → compare → confirm/reject → advance state.
- Error-state ghost projection: when wrong position detected, project the *correct* position as a transparent ghost so the user can self-correct without text instructions.
- Iterative tolerance tuning: start with generous tolerance for the vertical slice, tighten as Phase 3 scales.

### Specific Re:Crete + Halle 118 numbers (strand 04, indicative — to be re-verified by Data owner)

- Re:Crete pedestrian bridge: ~1/3 the CO₂ of equivalent new RC; on par with glulam.
- Halle 118 (baubüro in situ): ~60% GHG reduction vs new construction.
- These are the **anchor numbers** for the reclaimed-brick baseline. Data owner must confirm methodology and source-tier them before they go in `data/methods/reclaimed-brick.csv`.

</specifics>

<deferred>
## Deferred Ideas

- **AI-generated phase animations** — locked decision #4: paused until Phase 2's tier-1 numbers are signed off. Phase 4 may revisit.
- **Sound layer** — Phase 4 owns this; Phase 2 must not start.
- **Methodology-wobble overlay as a TD component** — Phase 4 builds; Phase 2 only stores the underlying data ranges.
- **Scaling to all 10 footprint pucks + height + material controllers** — Phase 3.
- **RFID pedestal + ESP firmware** — Phase 4 (the firmware/ folder exists; no Phase 2 work in it).
- **Re-calibration in exhibition lighting** — Phase 5; Phase 2 calibrates in studio conditions only.

</deferred>

---

*Phase: 02-data-research-physical-model-design*
*Context gathered: 2026-05-03 — synthesized from ACTIONS.md, lit-review/OVERVIEW.md, and PROJECT.md locked decisions (no /gsd-discuss-phase pass required given existing artifact density)*
