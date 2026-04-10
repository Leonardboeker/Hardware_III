# Roadmap: Hardware III — Comparative Construction Assembly Installation

**Created:** 2026-04-10
**Milestone:** v1 — Working Interactive Prototype (Finals May 22, 2026)

---

## Phase 1 — Proposal, Concept Lock & FSM Sketch
**Deadline:** Before April 17 (Session 2)
**Goal:** Submit all S1 deliverables. Concept fully defined: guided comparative assembly + projection + data + sound.

**Delivers:**
- Project proposal (1 page / 3 slides):
  - Module type: building/object parts per construction method
  - Connection logic: guided placement, camera validates position
  - Input: overhead webcam + ESP32 proximity
  - Feedback: projection shows placement guide → CO₂ + labor data on confirmation + sound
- Project management schedule: Gantt covering S1–S7, team roles, deliverables per session
- FSM diagram on paper: IDLE → GUIDING → CHECKING → CONFIRMED → NEXT_PIECE → MODEL_COMPLETE → NEXT_MODEL → COMPARISON
- Embodied interaction observation (non-touchscreen daily life example)
- Decision: which 2–4 construction methods to compare + which building/object type

**Requirements:** S1-01, S1-02, S1-03, S1-04

---

## Phase 2 — Data Research & Physical Model Design
**Deadline:** Session 2 → Session 3 (April 17 – May 4)
**Goal:** Source the data (CO₂, labor, time) for each construction method. Design and fabricate physical model parts.

**Delivers:**
- Data set per construction method: CO₂ kg/m², labor hours, construction time, material origin
- Physical model parts designed in Rhino (laser cut or 3D printed per method)
- Marker/color system for piece recognition defined
- Sensor pipeline tested: webcam → Firefly → Grasshopper position data live

**Requirements:** MOD-01 to MOD-04, INP-01 to INP-03

---

## Phase 3 — FSM Implementation & Assembly Logic
**Deadline:** Session 3 (May 4)
**Goal:** Full FSM running in Anemone. Placement detection → state transitions → data display pipeline working end-to-end.

**Delivers:**
- Complete FSM in Grasshopper (Anemone): all 8 states wired
- Piece detection: camera detects placement, validates position against target zone
- Per-piece data trigger: confirmed placement → CO₂ + labor hours displayed
- Error state: wrong placement → ghost projection shows correct position
- Rule format applied: IF [piece in zone X] → THEN IN STATE CONFIRMED

**Requirements:** FSM-01 to FSM-05, INP-01 to INP-03

---

## Phase 4 — Human-in-the-Loop Assembly & Sound
**Deadline:** Session 4 (May 11)
**Goal:** Full guided assembly loop works for at least 2 construction methods. Sound layer integrated.

**Delivers:**
- Assembly sequence defined per model (piece order, placement zones)
- CHECKING state validates within 300ms, ERROR recovery without full reset
- Sound per construction method: ambient audio per step, method-specific soundscape
- ESP32 proximity sensor wired: leaning in → triggers data zoom/detail layer
- Model complete → summary → transition to next model working

**Requirements:** HITL-01 to HITL-04, sound layer

---

## Phase 5 — Projection Mapping & Comparison View
**Deadline:** Session 5 (May 18)
**Goal:** Projector calibrated, all visual layers working. Comparison statistics view complete.

**Delivers:**
- Projector calibrated to table surface (homography mapping in GH/TouchDesigner)
- Visual layers per state: guide outlines, data overlays, method explanations
- Comparison view: all models complete → full-table statistics graphic (CO₂, hours, time, cost)
- Projection quality: crisp piece outlines, readable data at ambient light levels

**Requirements:** PROJ-01 to PROJ-05

---

## Phase 6 — Integration, Testing & Final Presentation
**Deadline:** Finals May 22
**Goal:** Reliable end-to-end demo. Physical models fabricated. PM schedule finalized.

**Delivers:**
- Complete system test: user enters → places piece → data shows → builds all models → comparison
- Latency under 150ms for detection → projection response
- All physical model parts fabricated and tested
- PM schedule updated and submitted for finals
- Presentation flow documented

**Requirements:** FIN-01, FIN-02, FIN-03

---

## Summary

| Phase | Name | Deadline | Status |
|-------|------|----------|--------|
| 1 | Proposal, Concept Lock & FSM Sketch | April 17 | ○ Pending |
| 2 | Data Research & Physical Model Design | May 4 | ○ Pending |
| 3 | FSM Implementation & Assembly Logic | May 4 | ○ Pending |
| 4 | Human-in-the-Loop Assembly & Sound | May 11 | ○ Pending |
| 5 | Projection Mapping & Comparison View | May 18 | ○ Pending |
| 6 | Integration, Testing & Finals | May 22 | ○ Pending |

---
*Roadmap updated: 2026-04-10 — concept finalized*
