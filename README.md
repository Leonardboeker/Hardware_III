# Hardware III - Guided Comparative Assembly

**Course:** Hardware III - Human-in-the-Loop Interactive Systems  
**Institute:** IAAC, MRAC + MAAI 2025/2026  
**Runtime:** TouchDesigner  
**Project mode:** Interactive construction decision exhibit

## Mission

We compare construction methods by letting people physically configure a small building scenario on a table and immediately see the environmental, labor, time, and economic consequences through projection.

## Core Interaction

The visitor selects a construction method, configures the footprint, sets the height, selects the material logic, validates the scenario, moves through five construction phases, and finally reaches a comparison view.

## Canonical State Model

The repo uses a **layered state model**.
These layers should not be collapsed into one list.

### Canonical Content FSM

This is the main visitor-facing interaction flow and the **canonical FSM** for the project:

```text
IDLE
  ->
METHOD
  ->
FOOTPRINT
  ->
HEIGHT
  ->
MATERIALS
  ->
VALIDATED
  ->
PHASE_N
  ->
COMPARISON
```

`PHASE_N` is the implementation state used in TouchDesigner for the five locked construction phases:
- Foundation
- Structure / Walls
- Roof
- Openings
- Finishing

This canonical content FSM is the one currently reflected in:
- [PROJECT.md](/o:/Hardware_III/.planning/PROJECT.md)
- [ROADMAP.md](/o:/Hardware_III/.planning/ROADMAP.md)
- [fsm_full.py](/o:/Hardware_III/touchdesigner/scripts/fsm_full.py)

### System Wrapper States

These are **system-level modes**, not the main content FSM:
- `CALIBRATION_CHECK`
- `ERROR`
- `RESET`
- `MANUAL_OVERRIDE`

They handle setup, recovery, and operator control around the content FSM.

### Visual Feedback States

These are **projection feedback codes**, not the canonical content FSM:
- `DISCONNECTED`
- `PENDING`
- `INVALID`
- `VALID`
- `IDLE_ANIM`
- `SUMMARY`
- `COMPARISON`

These are defined by the current TouchDesigner visual layer and error feedback logic in:
- [ERROR-FEEDBACK-SPEC.md](/o:/Hardware_III/touchdesigner/ERROR-FEEDBACK-SPEC.md)
- [fsm_full.py](/o:/Hardware_III/touchdesigner/scripts/fsm_full.py)

## Current Runtime Direction

TouchDesigner is the main runtime for:
- FSM logic
- computer vision intake
- projection mapping
- visual state output
- data triggering

Rhino + Grasshopper remain part of the project for:
- geometry authoring
- fabrication preparation
- offline design support

## Tech Stack

| Tool | Role |
|------|------|
| TouchDesigner | Primary runtime: FSM, projection, integration |
| OpenCV + ArUco | Marker detection and vision pipeline |
| Rhino + Grasshopper | Geometry, fabrication logic, offline authoring |
| ESP32 / RFID / proximity sensor | Presence, method selection, hardware triggers |
| Overhead webcam | ArUco tracking |
| Projector | Table projection and visual feedback |

## Source Of Truth

When there is a mismatch between older documents, use this order:

1. [fsm_full.py](/o:/Hardware_III/touchdesigner/scripts/fsm_full.py)
2. [PROJECT.md](/o:/Hardware_III/.planning/PROJECT.md)
3. [ROADMAP.md](/o:/Hardware_III/.planning/ROADMAP.md)
4. [INTERFACE_CONTRACT.md](/o:/Hardware_III/INTERFACE_CONTRACT.md)
5. [FSM_TOUCHDESIGNER_SPEC.md](/o:/Hardware_III/.planning/FSM_TOUCHDESIGNER_SPEC.md)

Older Phase 1 documents may still contain historical FSM sketches such as `GUIDING`, `CHECKING`, `NEXT_PIECE`, or older Grasshopper / Anemone assumptions.
Those should be treated as proposal history, not as the current runtime definition.
