# Requirements: Hardware III — Human-in-the-Loop Interactive Systems

**Defined:** 2026-04-10
**Core Value:** Working interactive prototype where projection guides modular assembly in real time

## v1 Requirements (Semester delivery — May 22)

### Session 1 Deliverables (due April 17)

- [ ] **S1-01**: Project proposal submitted (1 page or 3 slides): module type, connection logic, intended human input, intended feedback method
- [ ] **S1-02**: Project management schedule submitted: Gantt/Kanban/Sprint log with tasks, roles, dates, deliverables covering S1–S7
- [ ] **S1-03**: Embodied interaction observation: photo or sketch of one non-touchscreen interaction in daily life
- [ ] **S1-04**: First FSM drawn on paper: 3–5 states with labeled transitions

### Module & Connection Logic (Session 2 — April 17)

- [ ] **MOD-01**: Module type defined (physical geometry, material)
- [ ] **MOD-02**: Connection logic defined (snap-fit, slot, gravity, adhesive, rope, etc.)
- [ ] **MOD-03**: Connection valid vs invalid states defined (what makes a placement correct)
- [ ] **MOD-04**: Input method finalized (hand distance, body position, or physical object placement)

### FSM & System Logic (Session 3 — May 4)

- [ ] **FSM-01**: FSM diagram complete (states: IDLE, READY, CHECKING, CONFIRMED, ERROR, COMPLETE minimum)
- [ ] **FSM-02**: All states have defined projection outputs (what light does in each state)
- [ ] **FSM-03**: All transitions labeled with trigger (sensor event, timer, gesture)
- [ ] **FSM-04**: FSM implemented in Grasshopper using Anemone
- [ ] **FSM-05**: Rule format applied: IF [condition] → THEN IN STATE [name]

### Sensor & Input Pipeline (Session 3–4)

- [ ] **INP-01**: Sensor/webcam connected and streaming data into Grasshopper via Firefly
- [ ] **INP-02**: Human input mapped to fabrication parameter (mapping function defined: direct/juicy/stepped)
- [ ] **INP-03**: Input triggers correct FSM state transitions in real time

### Human-in-the-Loop Assembly (Session 4 — May 11)

- [ ] **HITL-01**: System cannot advance past CHECKING state without valid human placement
- [ ] **HITL-02**: System provides spatial feedback within 150ms of placement
- [ ] **HITL-03**: Error recovery: wrong placement → system guides correction without reset
- [ ] **HITL-04**: Assembly sequence defined (which module comes next, in what order)

### Projection Mapping (Session 5–6 — May 11–18)

- [ ] **PROJ-01**: Projector calibrated to physical assembly surface
- [ ] **PROJ-02**: Projection shows next placement target (light outlines where module should go)
- [ ] **PROJ-03**: Projection changes color/pattern based on FSM state (green = confirmed, red = error)
- [ ] **PROJ-04**: System updates projection in real time as human places modules
- [ ] **PROJ-05**: Completion state: all modules placed → full assembly celebration sequence

### Final Prototype (May 22)

- [ ] **FIN-01**: End-to-end loop works: human enters space → system detects → placement guide projects → human places → system validates → next step appears
- [ ] **FIN-02**: Project management schedule updated each session and submitted for finals
- [ ] **FIN-03**: Working demo can be run without intervention

## v2 Requirements (Future / Not in scope for this semester)

- **V2-01**: Multiple simultaneous users
- **V2-02**: Sound feedback in addition to projection
- **V2-03**: Robotic arm integration (Parascho direction)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Touchscreens / tablets | Explicitly excluded by course — kills spatial awareness |
| Static projection | Must be reactive — no pre-recorded content |
| Full automation (no human) | Human judgment must be in the loop by course requirement |
| Mobile app interface | No conventional apps per course brief |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| S1-01 to S1-04 | Phase 1 | Pending |
| MOD-01 to MOD-04 | Phase 2 | Pending |
| FSM-01 to FSM-05 | Phase 3 | Pending |
| INP-01 to INP-03 | Phase 3 | Pending |
| HITL-01 to HITL-04 | Phase 4 | Pending |
| PROJ-01 to PROJ-05 | Phase 5 | Pending |
| FIN-01 to FIN-03 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 28 total
- Mapped to phases: 28
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-10*
