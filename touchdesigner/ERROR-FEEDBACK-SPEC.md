# Error Feedback Visual Language Spec

**Status:** LOCKED (Phase 2, Plan 02-06)
**Owner:** TD Logic (FSM) + TD Visuals (Projection)
**Referenced by:** Plan 02-07, fsm_vertical_slice.py, fsm_full.py

---

## Visual State Codes

| Code | Name | When | Projection Output |
|------|------|------|-------------------|
| 0 | DISCONNECTED | No vision heartbeat ≥ 1s, or no puck detected ≥ 1s | Dotted white outline of target zone, pulsing at 1 Hz |
| 1 | PENDING | Puck detected but outside target zone, not enough to show ghost | Solid white outline of target zone |
| 2 | INVALID | Puck detected, outside zone, clear wrong-placement | **Ghost** at correct position (cyan, 40% opacity) + **red halo** at current puck position |
| 3 | VALID | Puck inside target zone, confirming (or confirmed) | **Green halo** at puck position, expanding ring animation |
| 4 | IDLE_ANIM | FSM in IDLE state | Slow breathing pulse across all target zones, white |
| 5 | SUMMARY | All pieces confirmed for one model | Full data overlay: CO₂ range, labor hours, construction time. White text on dark background |
| 6 | COMPARISON | All 3 models complete | Full-table comparison: all methods side-by-side, reclaimed-brick baseline as floor line |

---

## Ghost Projection (INVALID state)

The ghost pattern follows the **Augmented Bricklaying** convention (Mitterberger et al. 2020):
- Ghost shape: exact footprint of the expected puck position, same size as puck
- Ghost color: **cyan (#00FFFF)**, opacity 40%
- Current puck: **red halo** (#FF3333), 3px stroke
- Both rendered simultaneously so user sees where it is vs where it should be

**Recovery without reset:** as soon as puck enters the correct zone → visual switches to VALID without any button press.

---

## Tolerance Zones

Target zones are defined in projector-pixel space by the Python vision pipeline.
Radius is set in `vision/calibration/TOLERANCE.md`.

Visual feedback:
- Outside tolerance radius → INVALID (if puck detected) or PENDING (if no puck)
- Inside tolerance radius → VALID confirmation sequence begins
- Dwell time before confirmation: `CONFIRM_HOLD_FRAMES = 5` frames (~167ms at 30fps)

---

## Projection Colors

| Element | Color | Hex |
|---------|-------|-----|
| Target zone outline | White | #FFFFFF |
| Valid / confirmed | Green | #00FF88 |
| Invalid / wrong position | Red | #FF3333 |
| Ghost (correct position) | Cyan | #00FFFF |
| Disconnected pulse | White dimmed | #AAAAAA |
| Data text | White | #FFFFFF |
| Reclaimed baseline | Orange accent | #FF8C00 |

---

## Implementation Notes (for TD Visuals person)

1. The `visual_state` channel output from `fsm_vertical_slice.py` / `fsm_full.py` (Script CHOP) drives a **Switch TOP** that selects which overlay to project.
2. Each state is a separate TOP branch — composited onto the base projection via an **Over TOP**.
3. Ghost position: read `pucks[TARGET_ID]['projector_xy']` and the known `target_xy` from storage. Draw both in the Ghost TOP branch.
4. VALID animation: use a **Ramp TOP** + **Feedback TOP** for the expanding ring — trigger reset on each new VALID event via the `lca_trigger` channel pulse.
5. DISCONNECTED dotted outline: use a **Line MAT** or **SOP to TOP** with a dashed pattern; animate opacity with a slow **LFO CHOP** at 1 Hz.
