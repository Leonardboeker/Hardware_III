# Roadmap: Hardware III — Comparative Construction Assembly Installation

**Created:** 2026-04-10
**Milestone:** v1 — Working Interactive Prototype (Finals May 22, 2026)

---

## Overview

Six-phase project to build an interactive table installation where users assemble 2–4 physical scale models (each a different construction method) guided by projection. Data (CO₂, labor hours) appears piece by piece; a final comparison view is projected after all models complete.

### Canonical layered model

The roadmap now assumes a layered TouchDesigner state model:
- **Canonical content FSM**: `IDLE -> METHOD -> FOOTPRINT -> HEIGHT -> MATERIALS -> VALIDATED -> PHASE_N -> COMPARISON`
- **System wrapper states**: `CALIBRATION_CHECK`, `ERROR`, `RESET`, `MANUAL_OVERRIDE`
- **Visual feedback states**: `DISCONNECTED`, `PENDING`, `INVALID`, `VALID`, `IDLE_ANIM`, `SUMMARY`, `COMPARISON`

All phase goals and success criteria should be interpreted through this separation.

## Phases

- [x] **Phase 1: Proposal & FSM Foundation** — Submitted April 17, 2026 (`Group_3_Hardware_III_Proposal.pdf`)
- [ ] **Phase 2: Data Research & Physical Model Design** — Source tier-1 LCA data (Catalonia: CYPE/BEDEC/ITeC/EPDs), fabricate ArUco pucks + method-selector models, calibrate camera-projector rig, ship a one-puck closed-loop CV vertical slice
- [ ] **Phase 3: FSM Implementation & Assembly Logic** — Full FSM in **TouchDesigner** (replaces Anemone), closed-loop CV at every transition, error-feedback visual language locked
- [ ] **Phase 4: Human-in-the-Loop Assembly & Sound** — Scale loop to all 10 footprint pucks + height + material controllers, RFID pedestal + ESP integration, methodology-wobble layer as first-class TD component
- [ ] **Phase 5: Projection Mapping & Comparison View** — Re-calibrate in exhibition lighting, comparison view + reclaimed-brick baseline overlay, paired equivalents (absolute + equivalent + assumption)
- [ ] **Phase 6: Integration, Testing & Finals** — Manual-override hotkey as demo insurance, three back-to-back rehearsals, slide-deck reference corrections (reacTable, Augmented Bricklaying, Augmented Carpentry)

## Phase Details

### Phase 1: Proposal & FSM Foundation ✅ COMPLETE
**Goal**: Submit all S1 deliverables before Session 2. Concept fully defined: guided comparative assembly + projection + data + sound.
**Depends on**: Nothing (first phase)
**Deadline**: April 17, 2026 — **submitted on time**
**Status**: ✅ Complete (`Group_3_Hardware_III_Proposal.pdf` on master)
**Requirements**: S1-01, S1-02, S1-03, S1-04
**Success Criteria** (all met):
  1. ✅ Proposal submitted: 3 slides, 1-page PDF
  2. ✅ Gantt + Project management schedule submitted
  3. ✅ FSM diagram submitted (evolved during Session 2 to: IDLE → METHOD → FOOTPRINT → HEIGHT → MATERIALS → VALIDATED → 5 PHASES → COMPARISON)
  4. ✅ Embodied interaction observation submitted
  5. ✅ Methods locked: Masonry, 3D Printed, Prefab + Reclaimed brick as baseline toggle (locked 2026-05-03 post-lit-review)
**Plans**: `phases/01-proposal-fsm-foundation/PLAN.md`

---

### Phase 2: Data Research & Physical Model Design
**Goal**: Lock the tier-1 LCA data per method, fabricate the first physical components (ArUco pucks + method-selector models), and ship a working **one-puck closed-loop CV vertical slice** that validates the full pipeline before scaling to ten pucks in Phase 3.
**Depends on**: Phase 1 ✅
**Deadline**: May 4, 2026
**Requirements**: MOD-01, MOD-02, MOD-03, MOD-04, INP-01, INP-02, INP-03
**Success Criteria** (what must be TRUE):
  1. **LCA dataset compiled per method**, every value carrying a `source` annotation tier (peer-reviewed > EPD > vendor). Catalonia tier-1 sources prioritised: CYPE, BEDEC (ITeC), and EPDs. Vendor claims (Apis Cor, ICON, TECLA) flagged as such. Numbers stored as **ranges with assumption notes**, not single figures, so the methodology-wobble layer in Phase 4 has data to draw from.
  2. **Reclaimed brick baseline** values sourced (Re:Crete, Halle 118 case studies as starting points) — embodied carbon of reuse will become the floor every other method is plotted against.
  3. **Camera-projector calibration rig** built and documented: checkerboard for camera intrinsics + ArUco board for projector-camera homography. Procedure repeatable in <30 min by any team member.
  4. **One-puck closed-loop vertical slice** runs end-to-end: ArUco puck on table → overhead webcam detects in TouchDesigner → position compared against projected target zone → projector shows green (valid) or red ghost (correct position) → TD state advances. This is the proof that closed-loop is achievable; Phase 3 scales to ten pucks.
  5. **Physical components fabricated**: at least 3 test ArUco pucks 3D-printed (final 10 in Phase 3), and the 3 method-selector models for the RFID pedestal designed in Rhino.
  6. **Error-feedback visual language locked**: what wrong-placement looks like (color, ghost projection, optional audio cue). Documented in `docs/research/lit-review/ACTIONS.md` reference-frame; concrete spec lives in `phases/02-.../`.
  7. Three reference corrections applied to the slide deck before any next presentation: "Swiss museum DJ table" → reacTable; "Brick Vault" → Augmented Bricklaying; "Discrete Wood" → Augmented Carpentry.
**Plans**: TBD (run `/gsd-plan-phase 2`)

---

### Phase 02.1: Height Slider Integration - DollaTek 10K slide potentiometer on ESP32-RFID GPIO34, drives HEIGHT FSM state via Serial. Replaces ArUco-Dial ID-10. (INSERTED)

**Goal:** [Urgent work - to be planned]
**Requirements**: TBD
**Depends on:** Phase 2
**Plans:** 0 plans

Plans:
- [ ] TBD (run /gsd:plan-phase 02.1 to break down)

### Phase 3: FSM Implementation & Assembly Logic
**Goal**: Scale the Phase 2 vertical slice into the **full FSM running in TouchDesigner** (replaces the originally-planned Grasshopper/Anemone). Every transition is gated by closed-loop CV — no button-advance baseline.
**Depends on**: Phase 2
**Deadline**: May 4, 2026
**Requirements**: FSM-01, FSM-02, FSM-03, FSM-04, FSM-05, INP-01, INP-02, INP-03
**Success Criteria** (what must be TRUE):
  1. Complete FSM in **TouchDesigner**: all 8 states wired and transitioning (IDLE → METHOD → FOOTPRINT → HEIGHT → MATERIALS → VALIDATED → 5 PHASES → COMPARISON), with each transition gated by camera confirmation against an expected projected target.
  2. All 10 footprint ArUco pucks tracked simultaneously. Polygon + area calculation surfaces footprint in m² to the FSM.
  3. Height marker and material controller (distinct ArUco IDs) integrated.
  4. Per-state data trigger: confirmed transition → corresponding LCA data layer projected. Numbers are **ranges, not single figures**, with source tier visible.
  5. Error state: wrong placement → ghost projection shows correct position (the locked Augmented Bricklaying pattern). Recovery without full reset.
  6. Rule format applied throughout: IF [puck-set matches expected target within tolerance] → THEN [transition].
  7. Anchored to Parascho's assembly-as-state-machine framing (cite ETH Diss. 25839 in any phase write-up).
**Plans**: TBD

---

### Phase 4: Human-in-the-Loop Assembly & Sound
**Goal**: Full guided closed-loop assembly works for all three methods. **Methodology-wobble layer** added as a first-class projection component. RFID + sound integrated.
**Depends on**: Phase 3
**Deadline**: May 11, 2026
**Requirements**: HITL-01, HITL-02, HITL-03, HITL-04
**Success Criteria** (what must be TRUE):
  1. Assembly sequence defined per method (5 phases × 3 methods = 15 phase configurations).
  2. Visual validation feedback resolves within 300 ms, with `INVALID` / `VALID` projection feedback and recovery without full reset while the content FSM stays in the active step.
  3. **Methodology-wobble layer** (toggleable) shows assumption set, swing range, and source tier behind each LCA number. This is the project's pedagogical contribution per lit-review strands 04, 05, 06 — built as a first-class TD component, not a footnote.
  4. **Real-world equivalents always paired with the absolute number AND assumption** (Reijnierse 2025 — strand 05). No standalone "X trees" framings.
  5. RFID pedestal + ESP integration via OSC over WiFi to TouchDesigner.
  6. ESP32 proximity sensor wired: leaning in → triggers data zoom/detail layer.
  7. Sound per method: ambient audio per phase, method-specific soundscape, AI-generated phase animations remain paused until LCA numbers are signed off.
  8. Model complete → summary → transition to next model working end-to-end.
**Plans**: TBD

---

### Phase 5: Projection Mapping & Comparison View
**Goal**: Re-calibrate in **exhibition lighting** (not studio), reclaimed-brick baseline overlay added, full comparison view shipped.
**Depends on**: Phase 4
**Deadline**: May 18, 2026
**Requirements**: PROJ-01, PROJ-02, PROJ-03, PROJ-04, PROJ-05
**Success Criteria** (what must be TRUE):
  1. **Re-calibration in actual exhibition lighting** — the most important Phase 5 task. Strand 03 of the lit review explicitly warns calibration drift under stage lights is the classic demo-day failure mode of this whole literature. Document any deltas vs studio calibration.
  2. **Hand-occlusion stress test passed**: system recovers when markers are momentarily occluded by user's hand. Failure-recovery on marker loss spec'd.
  3. Visual layers per state: guide outlines, data overlays, method explanations — all using TouchDesigner (initial roadmap mentioned GH alternative; that path is closed).
  4. **Comparison view**: all models complete → full-table statistics graphic (CO₂ ranges, hours, time, cost), with the **reclaimed-brick baseline plotted as the floor every other method is measured against** (locked decision #2).
  5. Projection quality: crisp puck outlines, readable data at ambient light levels.
**Plans**: TBD

---

### Phase 6: Integration, Testing & Finals
**Goal**: Reliable end-to-end demo with explicit safeguards against the closed-loop CV failure modes the lit review warned about.
**Depends on**: Phase 5
**Deadline**: May 22, 2026
**Requirements**: FIN-01, FIN-02, FIN-03
**Success Criteria** (what must be TRUE):
  1. Complete system test: user configures → camera tracks → all transitions fire correctly → builds all 3 methods + reclaimed baseline → comparison view → reset for next visitor.
  2. Latency under 150 ms for detection → projection response.
  3. **Manual-override hotkey** built and documented — hidden, only used by the demoer if CV silently fails on stage. Runtime stays closed-loop; this is emergency human-in-the-loop insurance per ACTIONS.md task #14. ~1 hour to build.
  4. All physical components fabricated and stress-tested (10 final pucks + height + material + 3 method-selector models + RFID pedestal housing).
  5. **Three back-to-back rehearsals** completed and timed. Every failure mode logged.
  6. **Final deck refresh**: cite Parascho ETH Diss. 25839, Mitterberger et al. 2020 (Augmented Bricklaying), Jordà et al. 2007 (reacTable), Garrido-Jurado et al. 2014 (ArUco), Pomponi et al. (LCA caveats). The five anchors that position the project academically.
  7. **AI disclosure** included in any submitted academic text — this lit review and parts of the planning were AI-assisted.
  8. PM schedule updated and submitted for finals.
  9. Working demo can be run without intervention (manual override only as fallback).
**Plans**: TBD

---

## Summary

| Phase | Name | Deadline | Status |
|-------|------|----------|--------|
| 1 | Proposal & FSM Foundation | April 17 | ✅ Complete |
| 2 | Data Research & Physical Model Design | May 4 | ○ Active — planning |
| 3 | FSM Implementation & Assembly Logic (TouchDesigner) | May 4 | ○ Pending |
| 4 | Human-in-the-Loop Assembly & Sound + Methodology-wobble layer | May 11 | ○ Pending |
| 5 | Projection Mapping & Comparison View + reclaimed-brick baseline | May 18 | ○ Pending |
| 6 | Integration, Testing & Finals + manual-override hotkey | May 22 | ○ Pending |

---
*Roadmap updated: 2026-05-03 — Phase 1 closed, Phases 2-6 success criteria realigned to lit-review-backed locked decisions (TouchDesigner stack, closed-loop CV, reclaimed-brick baseline, methodology-wobble layer, paused AI animations).*
