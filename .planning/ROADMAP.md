# Roadmap: Hardware III — Human-in-the-Loop Interactive Systems

**Created:** 2026-04-10
**Milestone:** v1 — Working Interactive Prototype (Finals May 22, 2026)

---

## Phase 1 — S1 Proposal & FSM Foundation
**Deadline:** Before April 17 (Session 2)
**Goal:** Submit all S1 deliverables and define the project concept clearly enough to build on.

**Delivers:**
- Project proposal document (module type, connection logic, input method, feedback strategy)
- Project management schedule (Gantt/Kanban covering S1–S7, roles and tasks)
- First FSM diagram on paper (3–5 states, labeled transitions)
- Embodied interaction observation (photo/sketch of non-touchscreen interaction)

**Requirements:** S1-01, S1-02, S1-03, S1-04
**Canonical refs:** Session 1 slides — "What your proposal needs to answer" (p.54), "Homework" (p.57)

---

## Phase 2 — Input Mapping & Module Definition
**Deadline:** Session 2 (April 17) → Session 3 (May 4)
**Goal:** Define the module geometry/connection logic and get the sensor pipeline running in Grasshopper.

**Delivers:**
- Module type and connection logic documented
- Valid vs invalid placement rules defined
- Sensor/webcam connected via Firefly → Grasshopper data stream live
- Mapping function chosen (direct / juicy / stepped) and implemented

**Requirements:** MOD-01 to MOD-04, INP-01 to INP-03
**Canonical refs:** Session 1 slides — "Skeleton of any interactive system" (p.18), "Mappin - the translation function" (p.40)

---

## Phase 3 — FSM Implementation in Grasshopper
**Deadline:** Session 3 (May 4)
**Goal:** Full FSM running in Anemone — all states, transitions, and projection outputs wired up.

**Delivers:**
- Complete FSM diagram (IDLE → READY → CHECKING → CONFIRMED/ERROR → COMPLETE)
- FSM implemented in Grasshopper with Anemone
- Each state triggers different projection output
- Rule format: IF [condition] → THEN IN STATE [name] applied throughout

**Requirements:** FSM-01 to FSM-05
**Canonical refs:** Session 1 slides — "FSM: a map of all behaviours" (p.43), "FSM in a fabrication context" (p.44), "How to draw your FSM" (p.46)

---

## Phase 4 — Human-in-the-Loop Assembly
**Deadline:** Session 4 (May 11)
**Goal:** System validates human placement in real time — cannot proceed without correct action.

**Delivers:**
- Assembly sequence defined (order of modules)
- CHECKING state validates placement before advancing
- Error recovery: wrong placement gets correction guidance, not reset
- Spatial feedback under 150ms

**Requirements:** HITL-01 to HITL-04
**Canonical refs:** Session 1 slides — "Projection as a fabrication guide - Example" (p.34), "The chain: interaction - logic - fabrication" (p.39)

---

## Phase 5 — Projection Mapping Integration
**Deadline:** Session 5 (May 18)
**Goal:** Projector calibrated and showing reactive fabrication guidance on the physical surface.

**Delivers:**
- Projector calibrated to assembly surface
- Projection guides placement (light outlines target position)
- Color/pattern changes per FSM state (green=confirmed, red=error, ambient=idle)
- Completion sequence when all modules placed

**Requirements:** PROJ-01 to PROJ-05
**Canonical refs:** Session 1 slides — "Not a screen. A surface that knows you're there." (p.33), "Projection as a fabrication guide - Example" (p.34)

---

## Phase 6 — Integration, Testing & Final Presentation
**Deadline:** Finals May 22
**Goal:** End-to-end loop runs reliably. Demo-ready. PM schedule finalized.

**Delivers:**
- Full system test: enter space → detect → project guide → place → validate → next step
- Bug fixes and latency tuning (<150ms feedback)
- PM schedule updated and submitted
- Presentation materials ready

**Requirements:** FIN-01, FIN-02, FIN-03
**Canonical refs:** Session 1 slides — "Finals: Group Project" (p.4), course schedule (p.3)

---

## Summary

| Phase | Name | Deadline | Status |
|-------|------|----------|--------|
| 1 | S1 Proposal & FSM Foundation | April 17 | ○ Pending |
| 2 | Input Mapping & Module Definition | May 4 | ○ Pending |
| 3 | FSM Implementation in Grasshopper | May 4 | ○ Pending |
| 4 | Human-in-the-Loop Assembly | May 11 | ○ Pending |
| 5 | Projection Mapping Integration | May 18 | ○ Pending |
| 6 | Integration, Testing & Finals | May 22 | ○ Pending |

---
*Roadmap created: 2026-04-10*
