---
phase: 2
plan: 08
title: REQUIREMENTS.md tech-stack realignment (drop stale Anemone/Firefly references)
owner: _TBD_
wave: 3
depends_on: [5, 7]
files_modified:
  - .planning/REQUIREMENTS.md
  - .planning/STATE.md
autonomous: true
requirements:
  - INP-01
estimated_effort_hours: 1
---

<objective>
Update `.planning/REQUIREMENTS.md` to remove the stale references to Grasshopper/Anemone/Firefly that the older requirements language baked in (e.g. INP-01 "via Firefly", FSM-04 "in Grasshopper using Anemone"). Per the planning context's tech-stack realignment note, the locked stack is TouchDesigner + OpenCV + ArUco + Rhino/GH (geometry only). This plan does the documentation drift cleanup so future readers don't go hunting for Firefly when they pick up Phase 3 or beyond. It depends on Plan 05 (calibration rig) and Plan 07 (vertical slice) so we update REQUIREMENTS.md only AFTER the new stack has been demonstrated to work — i.e. we update with confidence rather than speculation. Addresses INP-01 (sensor pipeline streaming to runtime) by replacing "via Firefly" language with "via OpenCV → OSC → TouchDesigner" so the requirement language matches what was actually built. Also updates STATE.md to mark Phase 2 progress as the wave completes.
</objective>

<must_haves>
- `.planning/REQUIREMENTS.md` no longer contains the strings "Firefly", "Anemone" — those references have been replaced with the new-stack equivalents.
- The semantic intent of every realigned requirement is preserved (e.g. INP-01's intent is "sensor pipeline streaming to runtime" — we keep that intent and just change the named tool).
- An explicit `## Tech-stack realignment 2026-05-03` change-log section is added at the bottom of REQUIREMENTS.md noting what was changed and why, with a back-reference to PROJECT.md's locked decisions.
- `.planning/STATE.md` "Progress" table is updated to reflect Phase 2 completion (assuming Plans 01-07 are all checked off; if not, leave it as Active).
</must_haves>

<tasks>

<task type="auto">
  <name>Task 8.1: Edit REQUIREMENTS.md — replace stale tool references</name>
  <action>Edit `.planning/REQUIREMENTS.md`. Apply these EXACT find-replaces in this order (use the Edit tool, not Write — preserve everything else):

  1. Replace `**FSM-04**: FSM implemented in Grasshopper using Anemone`
     With:    `**FSM-04**: FSM implemented in TouchDesigner (replaces Anemone in original spec — see PROJECT.md Locked decision #2)`

  2. Replace `**INP-01**: Sensor/webcam connected and streaming data into Grasshopper via Firefly`
     With:    `**INP-01**: Sensor/webcam connected and streaming data into TouchDesigner runtime via OpenCV + OSC bridge (replaces Firefly path in original spec — see PROJECT.md Locked decision #2). Implemented Phase 2 — vision/src/run_vertical_slice.py.`

  Then APPEND a new section at the end of the file:

  ```markdown

  ## Tech-stack realignment 2026-05-03

  This requirements doc was originally written 2026-04-10 with a Grasshopper + Anemone (FSM) + Firefly (vision) stack. Per Locked decision #2 in PROJECT.md (dated 2026-05-03, backed by `docs/research/lit-review/03-projection-guided-construction.md`), the stack is now TouchDesigner runtime + OpenCV/ArUco vision pipeline + Rhino/Grasshopper for geometry generation only.

  Requirements affected:
  - **FSM-04** — re-named tool: Anemone → TouchDesigner.
  - **INP-01** — re-named tool path: Firefly → OpenCV+OSC bridge.

  Semantic intent of every requirement is unchanged. The new tools are now used.

  Phase 2 (this phase) ships the proof that the new stack works end-to-end via the one-puck closed-loop CV vertical slice (`.planning/phases/02-data-research-physical-model-design/02-07-cv-vertical-slice-PLAN.md`). Phase 3 scales this slice to the full FSM with all 10 footprint pucks + height + material in TouchDesigner.

  See also: `CONTRIBUTING.md` "Locked project decisions" section.
  ```

  Do NOT modify any other requirement IDs (S1-*, MOD-*, FSM-01/02/03/05, HITL-*, PROJ-*, FIN-*) — they are tool-agnostic and don't need realignment.</action>
  <read_first>
    - .planning/REQUIREMENTS.md (full current file)
    - .planning/PROJECT.md "Locked decisions" section
    - CONTRIBUTING.md "Locked project decisions" section
  </read_first>
  <acceptance_criteria>
    - `grep -c "Firefly" .planning/REQUIREMENTS.md` returns 0 (no remaining occurrences in the active requirement language).
    - `grep -c "Anemone" .planning/REQUIREMENTS.md` returns at most 1 (the historical reference inside the realignment changelog mentioning "originally written ... Anemone (FSM)" is acceptable; the working requirement text contains zero).
    - `grep -c "TouchDesigner" .planning/REQUIREMENTS.md` returns at least 3 (the two replaced lines + the realignment changelog).
    - `grep -c "## Tech-stack realignment 2026-05-03" .planning/REQUIREMENTS.md` returns 1.
    - The total line count increased by ~12-15 (new section added; 2 lines edited but length similar).
    - All other requirement IDs (MOD-01, MOD-02, MOD-03, MOD-04, FSM-01, FSM-02, FSM-03, FSM-05, INP-02, INP-03, HITL-01, HITL-02, HITL-03, HITL-04, PROJ-01..05, FIN-01..03, S1-01..04, V2-01..03) are still present in the file (verify by grep — count should match the original count exactly).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 8.2: Update STATE.md to reflect Phase 2 progress</name>
  <action>Edit `.planning/STATE.md`. Apply these targeted updates:

  1. Find the line `**Status:** Pending — to be planned via `/gsd-plan-phase 2`` under "## Current Phase".
     Replace with: `**Status:** In progress — plans created, see `.planning/phases/02-data-research-physical-model-design/02-*-PLAN.md`. Phase 2 closes when all 8 plans pass their verification.`

  2. In the Progress table, change the Phase 2 row from `○ Active — planning` to `○ Active — executing`.

  3. Replace the "Immediate Next Action" line `Run /gsd-plan-phase 2 to create a detailed plan for Phase 2 (data sourcing + physical model design + first closed-loop CV vertical slice).`
     With: `Run /gsd-execute-phase 2 to execute the 8 plans in `.planning/phases/02-data-research-physical-model-design/`. Wave 1 plans (01-06) run in parallel; Wave 2 (07) depends on 03+05+06; Wave 3 (08) depends on 05+07.`

  4. Add a "## Phase 2 plans" section just before the "## Notes" section:

     ```markdown
     ## Phase 2 plans

     Wave 1 (parallel): 01-slide-deck-corrections, 02-lca-data-sourcing, 03-aruco-pucks-fabrication, 04-method-selector-models, 05-camera-projector-calibration-rig, 06-error-feedback-visual-language.
     Wave 2: 07-cv-vertical-slice (depends on 03 + 05 + 06).
     Wave 3: 08-requirements-realignment (this plan; depends on 05 + 07).

     **Gating deliverable**: 07-cv-vertical-slice. Phase 3 cannot start until this works (per ROADMAP Phase 2 success criterion #4).
     ```

  Do not change anything else in STATE.md.</action>
  <read_first>
    - .planning/STATE.md (full current contents)
    - .planning/ROADMAP.md (for Phase 2 success criteria reference)
  </read_first>
  <acceptance_criteria>
    - `grep -c "○ Active — executing" .planning/STATE.md` returns 1.
    - `grep -c "## Phase 2 plans" .planning/STATE.md` returns 1.
    - `grep -c "/gsd-execute-phase 2" .planning/STATE.md` returns at least 1.
    - The original "## Locked decisions (2026-05-03)" section is still present (no accidental deletions — verify by grepping for "Closed-loop CV from day one").
  </acceptance_criteria>
</task>

</tasks>

<verification>
- `.planning/REQUIREMENTS.md` no longer contains "Firefly" anywhere; "Anemone" appears only in the historical changelog line, not in active requirement text.
- `.planning/REQUIREMENTS.md` ends with a "## Tech-stack realignment 2026-05-03" section.
- `.planning/STATE.md` reflects Phase 2 as "Active — executing" and lists the 8 plans by wave.
- All other content in both files is preserved.
</verification>
