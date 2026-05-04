# Team Roles & Responsibilities

## Purpose

This document defines the responsibilities, deliverables, and key questions for each team member in the Hardware III project.

It is intended to keep ownership clear across:
- system architecture
- FSM logic
- projection visuals
- computer vision
- physical fabrication
- data research
- sensor, sound, QA, and operations

## Person 1 - System Architecture + Integration Lead

Owns the overall system structure and makes sure all parts connect cleanly.

### Main responsibilities
- Define the complete FSM logic.
- Define all system states, transitions, conditions, and fallback modes.
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
- Final FSM diagram.
- Input contract from Computer Vision to TouchDesigner.
- Output contract from FSM to Projection / Visuals.
- Integration map.
- Calibration checklist.
- Demo runbook.
- Fallback strategy.

### Key questions to answer
- What state is the system in?
- What input triggers the next state?
- What does each person need to send to the next person?
- What happens if the system fails?
- How do we run the final demo from start to finish?

## Person 2 - TouchDesigner Logic + FSM Owner

Owns the actual interactive behavior inside TouchDesigner.

### Main responsibilities
- Implement the FSM in TouchDesigner.
- Build the state transition logic.
- Receive normalized data from Computer Vision and sensors.
- Convert inputs into state changes.
- Manage timers, delays, confirmation windows, and reset logic.
- Implement manual override buttons for demo safety.

### Must implement
- `IDLE`
- `CONFIGURING`
- `MATERIAL_SELECT`
- `VALIDATING`
- `ANALYSING`
- `RESULT`
- `COMPARE`
- `ERROR`
- `RESET`

### Must deliver
- Working TouchDesigner FSM prototype.
- Debug panel showing:
  - current state
  - detected markers
  - active piece ID
  - confidence
  - selected material
  - error code
- Manual controls:
  - reset
  - force next
  - force confirm
  - manual demo mode

### Key questions to answer
- When does the system change state?
- How does the system recover from errors?
- How does the system know the configuration is ready?
- How does the system trigger the visual layer?

## Person 3 - TouchDesigner Visuals + Projection Mapping Owner

Owns everything the user sees on the table.

### Main responsibilities
- Design and build the projected UI.
- Create the visual language for each FSM state.
- Build projection mapping setup.
- Align graphics to the physical table and model.
- Display guides, outlines, warnings, data cards, comparison tables, and phase previews.
- Make the system readable without verbal explanation.

### Must design
- Table grid.
- Active placement zones.
- Glowing footprint outlines.
- Phase bar.
- Phase preview panel.
- Instruction text.
- Data overlays.
- Comparison table.
- Error visuals.
- Result screen.
- Projection masks.

### State-based visual output
- `IDLE` -> dark grid, ambient animation.
- `CONFIGURING` -> active yellow/white guides.
- `VALIDATING` -> amber "checking" overlay.
- `ANALYSING` -> scanline / calculation animation.
- `RESULT` -> cost, CO2, labor, time, profit display.
- `COMPARE` -> side-by-side method comparison.
- `ERROR` -> red outline and correction ghost.
- `COMPLETE` -> final summary.

### Key questions to answer
- What does each state look like?
- Can the user understand the next action in 3 seconds?
- Is the projection aligned with the physical pieces?
- Are errors visually clear?

## Person 4 - Computer Vision + Camera Owner

Owns the tracking system.

### Main responsibilities
- Set up webcam / Kinect / camera.
- Detect ArUco markers reliably.
- Track position, rotation, ID, and confidence of each physical piece.
- Detect if a piece is inside the correct zone.
- Detect if a piece is stable.
- Reduce false positives caused by projector light.
- Send clean data to TouchDesigner.

### Must deliver

A normalized data packet such as:

```json
{
  "marker_detected": true,
  "marker_count": 3,
  "piece_id": "WALL_A_01",
  "piece_type": "geometry",
  "x": 0.42,
  "y": 0.63,
  "rotation": 91.4,
  "confidence": 0.93,
  "is_stable": true,
  "is_inside_zone": true,
  "zone_id": "build_zone"
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
- Model foundation, walls, roof, openings, finishing, and final state.
- Prepare 3D print / laser cut / fabrication files.
- Attach ArUco markers to pieces.
- Define tolerances and physical placement logic.
- Provide 3D models or renders for the phase preview panel.

### Must deliver
- Physical model pieces.
- Piece ID list.
- Piece type list.
- Assembly sequence.
- Valid / invalid placement rules.
- Rhino model.
- Fabrication files.
- Phase preview assets:
  - foundation
  - structure / walls
  - roof
  - openings
  - finishing
  - final

### Key questions to answer
- What physical pieces exist?
- What does each piece represent?
- Which pieces are required for each phase?
- What makes a configuration valid or invalid?
- What geometry does the UI need to display?

## Person 6 - Data Research + Narrative Owner

Owns the construction data and the story of the project.

### Main responsibilities
- Research construction industry data.
- Create comparison tables for different construction methods.
- Provide realistic data ranges, not only single values.
- Write short narrative texts for each material / method.
- Define what the project is trying to communicate politically, economically, and environmentally.

### Main research categories

#### 1. Construction methods

Research and compare:
- Masonry / brick construction.
- 3D printed construction.
- Prefabricated timber / CLT.
- Optional: low-carbon concrete, recycled aggregate, bio-based insulation.

#### 2. Environmental data

Research:
- CO2 emissions per material.
- Embodied carbon.
- Material origin.
- Transport impact.
- Waste generation.
- Recyclability / reusability.

#### 3. Labor data

Research:
- Labor hours per construction method.
- Skill intensity.
- Manual vs automated work.
- On-site vs off-site labor.
- Assembly complexity.

#### 4. Construction time

Research:
- Typical construction duration.
- Phase-based time:
  - foundation
  - walls
  - roof
  - openings
  - finishing
- Speed differences between masonry, prefab, and 3D printing.

#### 5. Cost data

Research:
- Material cost.
- Labor cost.
- Logistics cost.
- Equipment cost.
- Approximate cost per m2.
- Cost range by construction method.

#### 6. Real estate / revenue logic

Research:
- Sale price per m2.
- Rental price per m2.
- Office vs residential revenue.
- Estimated project revenue.
- Estimated profit:
  - revenue - construction cost
- Basic assumptions must be clearly stated.

#### 7. Narrative layer

Write short texts for:
- Masonry
- 3D printed
- Prefab timber
- Each construction phase
- Final comparison insight

Example:

`Masonry is locally sourced and repairable, but labor-intensive and slower to assemble.`

### Must deliver
- CSV / table of values.
- Data source list.
- Range-based comparison logic.
- Short UI text.
- Method descriptions.
- Final project narrative.

### Key questions to answer
- What are we comparing?
- Where do the numbers come from?
- Are the numbers ranges or fixed values?
- What does each construction method imply?
- What should the user learn from the comparison?

## Person 7 - ESP32 / Sensor + Sound + QA / Operations Owner

Owns physical sensing, sound feedback, reliability, and demo operation.

### Main responsibilities
- Set up proximity sensor / lean-in trigger.
- Send user presence data to TouchDesigner.
- Add sound cues for key states.
- Organize power, cables, and hardware layout.
- Test the whole system before demo.
- Create setup and shutdown checklist.
- Log errors during testing.
- Prepare fallback operation for demo day.

### Sensor responsibilities
- Detect if a user approaches the table.
- Trigger transition from `IDLE` to `ONBOARDING`.
- Detect absence for timeout / reset.
- Optional reset button or emergency button.

### Sound responsibilities

Create sound cues for:
- user enters
- piece accepted
- validation
- error
- confirmation
- complete

### QA responsibilities
- Test marker detection.
- Test projection alignment.
- Test state transitions.
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
Data Calculation
    |
    v
TouchDesigner Visuals / Projection
    |
    v
Interactive Construction Exhibit
```
