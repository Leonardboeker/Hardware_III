# Team Roles & Responsibilities

## Purpose

This document defines the responsibilities, deliverables, and key questions for each team member in the Hardware III project.

The team should work from the **layered state model** now locked in the repo:
- `Canonical Content FSM`
- `System Wrapper States`
- `Visual Feedback States`

These three layers must not be mixed.

## Shared State Model

### Canonical Content FSM

```text
IDLE -> METHOD -> FOOTPRINT -> HEIGHT -> MATERIALS -> VALIDATED -> PHASE_N -> COMPARISON
```

`PHASE_N` covers:
- Foundation
- Structure / Walls
- Roof
- Openings
- Finishing

### System Wrapper States

- `CALIBRATION_CHECK`
- `ERROR`
- `RESET`
- `MANUAL_OVERRIDE`

### Visual Feedback States

- `DISCONNECTED`
- `PENDING`
- `INVALID`
- `VALID`
- `IDLE_ANIM`
- `SUMMARY`
- `COMPARISON`

## Person 1 - System Architecture + Integration Lead

Owns the overall system structure and makes sure all parts connect cleanly.

### Main responsibilities
- Define the complete layered state model.
- Keep the distinction clear between:
  - Canonical Content FSM
  - System Wrapper States
  - Visual Feedback States
- Create the main system architecture diagram.
- Define the data flow between:
  - Computer Vision
  - TouchDesigner FSM
  - Projection UI
  - Data layer
  - Physical model
  - Sensors / sound
- Define interface contracts between team members.

### Must deliver
- Final canonical FSM diagram.
- Wrapper-state definition.
- Visual feedback state definition.
- Input contract from Computer Vision to TouchDesigner.
- Output contract from FSM to Projection / Visuals.
- Integration map.
- Calibration checklist.
- Demo runbook.
- Fallback strategy.

### Key questions to answer
- What is the current content state?
- Is the system in a wrapper state?
- What visual state should the projector show?
- What input triggers the next state?
- What happens if the system fails?
- How do we run the final demo from start to finish?

## Person 2 - TouchDesigner Logic + FSM Owner

Owns the actual interactive behavior inside TouchDesigner.

### Main responsibilities
- Implement the canonical content FSM in TouchDesigner.
- Keep wrapper states separate from content states.
- Publish visual feedback states separately from content states.
- Receive normalized data from Computer Vision and sensors.
- Convert interpreted inputs into state changes.
- Manage timers, delays, confirmation windows, phase stepping, and reset logic.
- Implement manual override buttons for demo safety.

### Must implement

#### Canonical content FSM
- `IDLE`
- `METHOD`
- `FOOTPRINT`
- `HEIGHT`
- `MATERIALS`
- `VALIDATED`
- `PHASE_N`
- `COMPARISON`

#### System wrapper states
- `CALIBRATION_CHECK`
- `ERROR`
- `RESET`
- `MANUAL_OVERRIDE`

#### Visual feedback states
- `DISCONNECTED`
- `PENDING`
- `INVALID`
- `VALID`
- `IDLE_ANIM`
- `SUMMARY`
- `COMPARISON`

### Must deliver
- Working TouchDesigner FSM prototype based on the current `fsm_full.py` logic.
- Debug panel showing:
  - current content state
  - current wrapper state
  - current visual state
  - detected markers / pucks
  - active piece ID
  - confidence
  - selected method
  - selected material
  - current phase index
  - error code
- Manual controls:
  - reset
  - force next
  - force confirm
  - manual demo mode

### Key questions to answer
- When does the content FSM change state?
- When does the wrapper layer interrupt the content FSM?
- How does the system recover from errors?
- How does the system know the configuration is ready?
- How does the system trigger the visual layer?

## Person 3 - TouchDesigner Visuals + Projection Mapping Owner

Owns everything the user sees on the table.

### Main responsibilities
- Design and build the projected UI.
- Create the visual language for the visual feedback states.
- Align projection to the physical table and markers.
- Display guides, outlines, warnings, data cards, comparison tables, and phase previews.
- Make the system readable without verbal explanation.

### Must design
- Table grid.
- Active placement zones.
- Glowing target outlines.
- Ghost correction overlays.
- Phase bar.
- Phase preview panel.
- Instruction text.
- Summary overlay.
- Comparison table.
- Error visuals.
- Projection masks.

### State-based visual output

#### Content-state driven views
- `IDLE` -> attract mode
- `METHOD` -> method selection target
- `FOOTPRINT` -> next footprint target
- `HEIGHT` -> height controller target
- `MATERIALS` -> material controller target
- `VALIDATED` -> summary layout
- `PHASE_N` -> phase sequence overlays
- `COMPARISON` -> full comparison view

#### Visual feedback states
- `DISCONNECTED` -> lost-tracking view
- `PENDING` -> waiting target outline
- `INVALID` -> red halo + correction ghost
- `VALID` -> green confirmation feedback
- `IDLE_ANIM` -> dark grid / ambient animation
- `SUMMARY` -> validated summary data
- `COMPARISON` -> final comparison layout

### Key questions to answer
- What does each content state look like?
- What does each visual feedback state look like?
- Can the user understand the next action in 3 seconds?
- Is the projection aligned with the physical pieces?
- Are errors visually clear?

## Person 4 - Computer Vision + Camera Owner

Owns the tracking system.

### Main responsibilities
- Set up webcam / Kinect / camera.
- Detect ArUco markers reliably.
- Track projector-space position, ID, and target validity of each piece.
- Detect whether a piece is inside the correct zone.
- Detect whether a piece is stable enough to confirm.
- Reduce false positives caused by projector light.
- Send clean interpreted data to TouchDesigner.

### Must deliver

A normalized data packet such as:

```json
{
  "marker_detected": true,
  "marker_count": 3,
  "piece_id": "FOOTPRINT_03",
  "piece_type": "geometry",
  "x": 0.42,
  "y": 0.63,
  "rotation": 91.4,
  "confidence": 0.93,
  "is_stable": true,
  "is_inside_zone": true,
  "zone_id": "footprint_zone_03"
}
```

### Must define
- Marker ID system.
- Detection zones.
- Confidence threshold.
- Stability threshold.
- Marker loss tolerance.
- Camera calibration method.
- Lighting / projector interference strategy.

### Key questions to answer
- Which piece is on the table?
- Where is it?
- Is it stable?
- Is it inside the correct zone?
- Is the detection reliable enough for the FSM?

## Person 5 - Rhino + Physical Model / Fabrication Owner

Owns the physical construction kit.

### Main responsibilities
- Design the physical pieces.
- Define the modular building geometry.
- Create the phase-based assembly sequence.
- Model footprint pieces, height controller, material controller, and phase assets.
- Prepare 3D print / laser cut / fabrication files.
- Attach ArUco markers to pieces.
- Define tolerances and physical placement logic.
- Provide simplified geometry previews for projection.

### Must deliver
- Physical model pieces.
- Piece ID list.
- Piece type list.
- Canonical phase sequence.
- Valid / invalid placement rules.
- Rhino model.
- Fabrication files.
- Phase preview assets:
  - foundation
  - structure / walls
  - roof
  - openings
  - finishing
  - final comparison preview

### Key questions to answer
- What physical pieces exist?
- What does each piece represent?
- Which pieces are required for each content state?
- What makes a configuration valid or invalid?
- What geometry does the UI need to display?

## Person 6 - Data Research + Narrative Owner

Owns the construction data and the story of the project.

### Main responsibilities
- Research construction industry data.
- Create comparison tables for different construction methods.
- Provide realistic data ranges, not only single values.
- Write short narrative texts for each method and phase.
- Define what the project communicates politically, economically, and environmentally.

### Main research categories

#### 1. Construction methods
- Masonry / brick construction
- 3D printed construction
- Prefabricated timber / CLT
- Reclaimed brick baseline

#### 2. Environmental data
- CO2 emissions
- Embodied carbon
- Material origin
- Transport impact
- Waste generation
- Recyclability / reusability

#### 3. Labor data
- Labor hours
- Skill intensity
- Manual vs automated work
- On-site vs off-site labor
- Assembly complexity

#### 4. Construction time
- Total duration
- Phase-based time
- Speed differences by method

#### 5. Cost data
- Material cost
- Labor cost
- Logistics cost
- Equipment cost
- Cost per m2
- Cost ranges by method

#### 6. Revenue logic
- Sale price per m2
- Rental price per m2
- Revenue estimate
- Profit estimate
- Explicit assumptions

#### 7. Narrative layer
- Masonry text
- 3D print text
- Prefab text
- Phase texts
- Final comparison insight

### Must deliver
- CSV / table of values
- Data source list
- Range-based comparison logic
- Short UI text
- Method descriptions
- Final project narrative

### Key questions to answer
- What are we comparing?
- Where do the numbers come from?
- Are the numbers ranges or fixed values?
- What does each method imply?
- What should the user learn from the comparison?

## Person 7 - ESP32 / Sensor + Sound + QA / Operations Owner

Owns physical sensing, sound feedback, reliability, and demo operation.

### Main responsibilities
- Set up proximity sensor / lean-in trigger.
- Send user presence data to TouchDesigner.
- Add sound cues for key events.
- Organize power, cables, and hardware layout.
- Test the whole system before demo.
- Create setup and shutdown checklist.
- Log errors during testing.
- Prepare fallback operation for demo day.

### Sensor responsibilities
- Detect whether a user approaches the table.
- Support the idle-to-engaged behavior while content FSM remains in `IDLE` until method selection begins.
- Detect absence for timeout / reset.
- Provide optional reset button or emergency button.

### Sound responsibilities
- user enters
- piece accepted
- validation
- error
- phase advance
- comparison

### QA responsibilities
- Test marker detection.
- Test projection alignment.
- Test content-state transitions.
- Test wrapper-state recovery.
- Test reset.
- Test manual fallback.
- Test cables and power.
- Prepare emergency checklist.

### Must deliver
- Working sensor input.
- Sound cue list.
- QA checklist.
- Demo setup checklist.
- Error log.
- Backup plan.

### Key questions to answer
- Does the system start reliably?
- What happens if someone walks away?
- What happens if a marker is not detected?
- Can we recover quickly during the demo?
- Can another person operate the system without explanation?

## Shared System Pipeline

```text
Physical Pieces
    |
    v
Computer Vision
    |
    v
TouchDesigner FSM
    |
    v
TouchDesigner Visuals / Projection
    |
    v
Interactive Construction Exhibit
```
