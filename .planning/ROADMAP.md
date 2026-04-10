# Roadmap: Hardware III — Comparative Construction Assembly Installation

**Created:** 2026-04-10
**Milestone:** v1 — Working Interactive Prototype (Finals May 22, 2026)

---

## Overview

Six-phase project to build an interactive table installation where users assemble 2–4 physical scale models (each a different construction method) guided by projection. Data (CO₂, labor hours) appears piece by piece; a final comparison view is projected after all models complete.

## Phases

- [ ] **Phase 1: Proposal & FSM Foundation** - Submit S1 deliverables, lock concept, draw FSM on paper
- [ ] **Phase 2: Data Research & Physical Model Design** - Source construction data, design and fabricate physical model parts
- [ ] **Phase 3: FSM Implementation & Assembly Logic** - Full FSM in Anemone, piece detection, placement validation pipeline
- [ ] **Phase 4: Human-in-the-Loop Assembly & Sound** - Complete guided assembly loop, sound layer, ESP32 integration
- [ ] **Phase 5: Projection Mapping & Comparison View** - Projector calibrated, all visual layers, comparison statistics view
- [ ] **Phase 6: Integration, Testing & Finals** - Reliable end-to-end demo, physical models fabricated, PM schedule finalized

## Phase Details

### Phase 1: Proposal & FSM Foundation
**Goal**: Submit all S1 deliverables before Session 2. Concept fully defined: guided comparative assembly + projection + data + sound.
**Depends on**: Nothing (first phase)
**Deadline**: April 17, 2026
**Requirements**: S1-01, S1-02, S1-03, S1-04
**Success Criteria** (what must be TRUE):
  1. Project proposal submitted (1 page / 3 slides): module type, connection logic, input method, feedback method
  2. Project management schedule submitted with Gantt covering S1–S7, team roles, deliverables per session
  3. FSM diagram drawn on paper: IDLE → GUIDING → CHECKING → CONFIRMED → NEXT_PIECE → MODEL_COMPLETE → NEXT_MODEL → COMPARISON
  4. Embodied interaction observation submitted: photo or sketch of non-touchscreen daily life interaction
  5. Decision made: which 2–4 construction methods to compare + which building/object type
**Plans**: TBD

---

### Phase 2: Data Research & Physical Model Design
**Goal**: Source the data (CO₂, labor, time) for each construction method. Design and fabricate physical model parts.
**Depends on**: Phase 1
**Deadline**: May 4, 2026
**Requirements**: MOD-01, MOD-02, MOD-03, MOD-04, INP-01, INP-02, INP-03
**Success Criteria** (what must be TRUE):
  1. Data set compiled per construction method: CO₂ kg/m², labor hours, construction time, material origin
  2. Physical model parts designed in Rhino (laser cut or 3D printed per method)
  3. Marker/color system for piece recognition defined
  4. Sensor pipeline tested: webcam → Firefly → Grasshopper position data live
**Plans**: TBD

---

### Phase 3: FSM Implementation & Assembly Logic
**Goal**: Full FSM running in Anemone. Placement detection → state transitions → data display pipeline working end-to-end.
**Depends on**: Phase 2
**Deadline**: May 4, 2026
**Requirements**: FSM-01, FSM-02, FSM-03, FSM-04, FSM-05, INP-01, INP-02, INP-03
**Success Criteria** (what must be TRUE):
  1. Complete FSM in Grasshopper (Anemone): all 8 states wired and transitioning
  2. Piece detection: camera detects placement, validates position against target zone
  3. Per-piece data trigger: confirmed placement → CO₂ + labor hours displayed in projection
  4. Error state: wrong placement → ghost projection shows correct position
  5. Rule format applied: IF [piece in zone X] → THEN IN STATE CONFIRMED
**Plans**: TBD

---

### Phase 4: Human-in-the-Loop Assembly & Sound
**Goal**: Full guided assembly loop works for at least 2 construction methods. Sound layer integrated.
**Depends on**: Phase 3
**Deadline**: May 11, 2026
**Requirements**: HITL-01, HITL-02, HITL-03, HITL-04
**Success Criteria** (what must be TRUE):
  1. Assembly sequence defined per model (piece order, placement zones)
  2. CHECKING state validates within 300ms, ERROR recovery without full reset
  3. Sound per construction method: ambient audio per step, method-specific soundscape
  4. ESP32 proximity sensor wired: leaning in → triggers data zoom/detail layer
  5. Model complete → summary → transition to next model working
**Plans**: TBD

---

### Phase 5: Projection Mapping & Comparison View
**Goal**: Projector calibrated, all visual layers working. Comparison statistics view complete.
**Depends on**: Phase 4
**Deadline**: May 18, 2026
**Requirements**: PROJ-01, PROJ-02, PROJ-03, PROJ-04, PROJ-05
**Success Criteria** (what must be TRUE):
  1. Projector calibrated to table surface (homography mapping in GH/TouchDesigner)
  2. Visual layers per state: guide outlines, data overlays, method explanations
  3. Comparison view: all models complete → full-table statistics graphic (CO₂, hours, time, cost)
  4. Projection quality: crisp piece outlines, readable data at ambient light levels
**Plans**: TBD

---

### Phase 6: Integration, Testing & Finals
**Goal**: Reliable end-to-end demo. Physical models fabricated. PM schedule finalized.
**Depends on**: Phase 5
**Deadline**: May 22, 2026
**Requirements**: FIN-01, FIN-02, FIN-03
**Success Criteria** (what must be TRUE):
  1. Complete system test: user enters → places piece → data shows → builds all models → comparison view
  2. Latency under 150ms for detection → projection response
  3. All physical model parts fabricated and tested
  4. PM schedule updated and submitted for finals
  5. Working demo can be run without intervention
**Plans**: TBD

---

## Summary

| Phase | Name | Deadline | Status |
|-------|------|----------|--------|
| 1 | Proposal & FSM Foundation | April 17 | ○ Pending |
| 2 | Data Research & Physical Model Design | May 4 | ○ Pending |
| 3 | FSM Implementation & Assembly Logic | May 4 | ○ Pending |
| 4 | Human-in-the-Loop Assembly & Sound | May 11 | ○ Pending |
| 5 | Projection Mapping & Comparison View | May 18 | ○ Pending |
| 6 | Integration, Testing & Finals | May 22 | ○ Pending |

---
*Roadmap updated: 2026-04-10 — reformatted for GSD tooling compatibility*
