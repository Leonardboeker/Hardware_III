# Interface Contract / Shared Data Language

## 1. Purpose

This document defines the shared data language between the subsystems of the Hardware III project.

It is not the FSM diagram.

The distinction is:
- System Architecture / Interface Contract = who sends what data to whom
- FSM Diagram = which state changes into which state under which condition

This contract defines the common language between:
- Computer Vision
- TouchDesigner FSM
- TouchDesigner Visuals / Projection
- Data / Metrics Layer
- Sensor / ESP32 Layer
- Physical Model / Fabrication Layer

The goal is that every team member can build their part independently, while still connecting cleanly to the full system.

## 2. System Architecture Data Flow

```text
Physical Pieces
    ->
Computer Vision
    ->
TouchDesigner FSM
    ->
TouchDesigner Visuals / Projection
    ->
Interactive Table UI

Optional branches:

Sensor / ESP32
    ->
TouchDesigner FSM

Data / Metrics Layer
    ->
TouchDesigner FSM / Visuals

Rhino / Fabrication
    ->
Piece Definitions / Zone Definitions
    ->
Computer Vision / TouchDesigner FSM / Visuals
```

### Architecture note

The physical model does not talk directly to the visuals.
It must first be interpreted as structured data by Computer Vision and by the piece definitions supplied from Rhino / Fabrication.

The FSM should not depend on raw camera images.
It should depend only on clean interpreted fields such as:
- `piece_id`
- `confidence`
- `is_stable`
- `is_inside_zone`

## 3. CV -> FSM Input Contract

This is the data packet that Computer Vision must send to the FSM.

### Required fields
- `timestamp`
- `marker_detected`
- `marker_count`
- `piece_id`
- `piece_type`
- `x`
- `y`
- `rotation`
- `confidence`
- `is_stable`
- `is_inside_zone`
- `zone_id`

### Optional fields
- `user_present`
- `proximity_value`
- `selected_material`
- `selected_program`
- `overlap_detected`
- `marker_loss_ms`

### JSON example

```json
{
  "timestamp": 1777858800123,
  "marker_detected": true,
  "marker_count": 2,
  "piece_id": "WALL_A_01",
  "piece_type": "geometry",
  "x": 0.42,
  "y": 0.63,
  "rotation": 91.4,
  "confidence": 0.93,
  "is_stable": true,
  "is_inside_zone": true,
  "zone_id": "build_zone_01"
}
```

### Field definitions

| Field | Type | Description | Used by FSM for |
|---|---|---|---|
| `timestamp` | integer | Unix timestamp in milliseconds for packet timing | timeout checks, packet freshness |
| `marker_detected` | bool | True when at least one valid marker is detected | enter active states, detect signal presence |
| `marker_count` | integer | Number of currently detected markers | overlap checks, multi-piece logic |
| `piece_id` | string | Unique identifier of the active or reported piece | piece-specific rules, sequencing, validation |
| `piece_type` | string | Piece category such as `geometry`, `material_token`, `program_token`, `control_token` | routing behavior by piece class |
| `x` | float | Normalized X coordinate on table surface | zone checks, movement detection |
| `y` | float | Normalized Y coordinate on table surface | zone checks, movement detection |
| `rotation` | float | Piece rotation in degrees | orientation validation |
| `confidence` | float | Detection confidence from 0.0 to 1.0 | trust threshold, error handling |
| `is_stable` | bool | True when piece position is stable for required time window | valid transition gating |
| `is_inside_zone` | bool | True when piece lies inside its allowed zone | placement validation, error detection |
| `zone_id` | string | Identifier of the detected or intended zone | matching piece to legal zone |
| `user_present` | bool | Optional presence flag derived from CV or merged sensing | onboarding, absence handling |
| `proximity_value` | float | Optional normalized proximity value from 0.0 to 1.0 | engage threshold, interface intensity |
| `selected_material` | string or null | Material token interpreted by CV if visible | material selection transitions |
| `selected_program` | string or null | Program token interpreted by CV if visible | scenario selection, metrics routing |
| `overlap_detected` | bool | True when markers or pieces conflict spatially | immediate error state |
| `marker_loss_ms` | integer | Duration since marker was last valid | grace period before error |

### Contract rules

- Coordinates must be normalized to the calibrated table space before being sent to the FSM.
- `confidence` should be stable enough for logic use; the FSM is not responsible for denoising raw camera jitter.
- `piece_id` values must match the Rhino / Fabrication piece definition list exactly.
- If multiple markers are tracked simultaneously, the packet format may be extended to an array, but the minimum prototype must still expose the currently active piece in the fields above.

## 4. FSM -> Visuals / Projection Output Contract

This is the data packet that the FSM sends to the visual and projection system.

### Required fields
- `current_state`
- `previous_state`
- `instruction`
- `active_piece_id`
- `state_color`
- `valid_zone_geometry`
- `projected_guides`
- `warning_message`
- `metrics_visible`
- `comparison_mode`

### Optional fields
- `cost_estimate`
- `co2_estimate`
- `labor_hours`
- `construction_time`
- `revenue_estimate`
- `profit_estimate`
- `confidence_display`
- `sound_cue`
- `log_event`

### JSON example

```json
{
  "current_state": "CONFIGURING",
  "previous_state": "WAITING_FOR_PIECES",
  "instruction": "Place the next structural piece",
  "active_piece_id": "WALL_A_01",
  "state_color": "safety_yellow",
  "valid_zone_geometry": "build_zone_01",
  "projected_guides": ["active_outline", "next_zone", "footprint_preview"],
  "warning_message": null,
  "metrics_visible": false,
  "comparison_mode": false
}
```

### Field definitions

| Field | Type | Description | Used by Visuals for |
|---|---|---|---|
| `current_state` | string | Authoritative runtime state | select visual mode and composition |
| `previous_state` | string | State before current one | transitions, debug overlay, animation continuity |
| `instruction` | string | Main user instruction for current moment | on-table text, side label, guidance messaging |
| `active_piece_id` | string or null | Piece currently expected, corrected, or highlighted | targeted overlays and previews |
| `state_color` | string | Named palette token such as `safety_yellow`, `amber`, `red_oxide`, `green_confirm` | state color system |
| `valid_zone_geometry` | string or object | Zone identifier or geometry payload for legal placement | outlines, masks, valid footprint guides |
| `projected_guides` | array | List of active guide layers to display | guide switching and compositing |
| `warning_message` | string or null | Error or recovery message | warning overlays and correction prompts |
| `metrics_visible` | bool | Whether metrics should be shown now | hide or reveal data cards |
| `comparison_mode` | bool or string | Whether compare view is active | split layout, comparison table activation |
| `cost_estimate` | number or string | Cost output or range | result cards, comparison graphics |
| `co2_estimate` | number or string | CO2 output or range | environmental overlays |
| `labor_hours` | number or string | Labor hours output or range | labor comparison panels |
| `construction_time` | number or string | Time output or range | schedule bars, phase timing UI |
| `revenue_estimate` | number or string | Revenue output or range | economic summary |
| `profit_estimate` | number or string | Profit output or range | business outcome summary |
| `confidence_display` | float | Confidence shown for operator debugging | debug panel and health overlays |
| `sound_cue` | string | Sound event token such as `error_buzz`, `confirm_ping` | audio trigger routing |
| `log_event` | string | Event summary for debug or logging | operator log and diagnostics |

### Contract rules

- Visuals must render what the FSM sends; they must not invent new states.
- `instruction` should be short enough to read on the table within 3 seconds.
- `state_color` must follow the project palette consistently so users learn the logic fast.
- `valid_zone_geometry` may begin as a zone ID in the prototype and later expand into polygon or transform data.

## 5. FSM Transition Conditions

The FSM does not need raw camera data.
It only needs clean interpreted values from the interface contract.

Examples:
- IF `marker_detected == true` AND `is_stable == true` THEN ENTER `CONFIGURING`
- IF `confidence < 0.75` for more than `500 ms` THEN ENTER `ERROR`
- IF `is_inside_zone == false` THEN ENTER `ERROR`
- IF `selected_material != null` THEN ENTER `VALIDATING`
- IF `current_state == RESULT` AND marker position changes THEN ENTER `CONFIGURING`

### How the fields are used

- `marker_detected` tells the FSM whether the system has a usable object event.
- `is_stable` tells the FSM whether the placement is trustworthy enough to accept.
- `confidence` tells the FSM whether the detection can be trusted.
- `is_inside_zone` tells the FSM whether the piece is legally positioned.
- `piece_type` tells the FSM how to interpret the object:
  - geometry piece
  - material token
  - program token
  - control token
- `marker_loss_ms` tells the FSM whether to wait briefly or fail into `ERROR`.
- `selected_material` and `selected_program` tell the FSM when enough scenario data exists to validate and analyse.

### Practical rule

Computer Vision interprets.
The FSM decides.
Visuals display.

## 6. Data / Metrics Layer Contract

This is the contract for the Data Research + Narrative Owner and for the metrics lookup logic used by TouchDesigner.

### Input expected by data layer
- `area_m2`
- `shape_factor`
- `selected_material`
- `selected_program`
- `construction_method`
- `number_of_floors`

### Output returned
- `cost_estimate`
- `co2_estimate`
- `labor_hours`
- `construction_time`
- `revenue_estimate`
- `profit_estimate`
- `source_label`
- `confidence_range`

### Example metrics table

| construction_method | cost_per_m2_range | co2_per_m2_range | labor_hours_range | time_range | source_label |
|---|---|---|---|---|---|
| masonry | 950-1350 EUR/m2 | 280-420 kgCO2e/m2 | 22-34 h/m2 | 14-20 weeks | literature_mix_v1 |
| prefab_timber | 1100-1600 EUR/m2 | 140-260 kgCO2e/m2 | 12-20 h/m2 | 8-12 weeks | literature_mix_v1 |
| concrete_3dp | 1000-1500 EUR/m2 | 220-390 kgCO2e/m2 | 8-16 h/m2 | 6-10 weeks | literature_mix_v1 |

### Contract rules

- The data layer must provide ranges, not only fixed values.
- Every output must be traceable to a `source_label`.
- If data is missing, the layer must return a null or error token instead of fabricating a number.
- `profit_estimate` must be based on explicit assumptions, not hidden guesses.

## 7. Sensor / ESP32 Input Contract

This is the contract for the ESP32 or other sensor system.

### Fields
- `user_present`
- `proximity_value`
- `reset_signal`
- `sensor_online`

### JSON example

```json
{
  "user_present": true,
  "proximity_value": 0.78,
  "reset_signal": false,
  "sensor_online": true
}
```

### Field definitions

| Field | Type | Description | Used by FSM for |
|---|---|---|---|
| `user_present` | bool | True when a user is near or engaged with the table | `IDLE -> ONBOARDING`, absence logic |
| `proximity_value` | float | Normalized distance or intensity value from 0.0 to 1.0 | engage threshold, lean-in effects |
| `reset_signal` | bool | Explicit reset trigger from operator or hardware control | any state -> `RESET` |
| `sensor_online` | bool | Health flag for the sensor subsystem | health monitoring, fallback mode |

### Trigger logic

- `IDLE -> ONBOARDING` when `user_present == true`
- `any state -> RESET` when `reset_signal == true`
- absence timeout -> `RESET` or `IDLE` when `user_present == false` for long enough

### Contract rules

- Sensor data should support the FSM, not replace Computer Vision.
- If `sensor_online == false`, the system should fall back to CV-based presence when possible.
- `reset_signal` must always have higher priority than normal interaction.

## 8. Rhino / Fabrication Contract

This is the contract for the Rhino + Physical Model / Fabrication Owner.

### Required outputs from Rhino / Fabrication
- `piece_id` list
- `piece_type` list
- physical dimensions
- marker placement location
- legal zones
- valid adjacency rules
- phase sequence
- simplified geometry previews
- phase preview assets

### Example piece definition

```text
piece_id: WALL_A_01
piece_type: geometry
phase: WALLS
allowed_zone: build_zone_01
valid_after: FOUNDATION_01
valid_before: ROOF_01
```

### Contract rules

- Every physical piece must have one stable `piece_id`.
- Marker placement must be documented so Computer Vision can read pieces consistently.
- Legal zones must match the calibrated table coordinates used by TouchDesigner.
- Valid adjacency rules must be explicit enough for the FSM to test legality.
- Simplified geometry previews must be lightweight enough for projection graphics and phase preview panels.

## 9. Naming Conventions

### Piece naming
- Geometry pieces: `WALL_A_01`, `FLOOR_01`, `ROOF_01`
- Material tokens: `TOKEN_CLT`, `TOKEN_CONCRETE`, `TOKEN_BRICK`
- Program tokens: `TOKEN_RESIDENTIAL`, `TOKEN_OFFICE`
- Control tokens: `TOKEN_CONFIRM`, `TOKEN_COMPARE`, `TOKEN_RESET`

### State naming

Rules:
- uppercase
- one or two words max

Examples:
- `IDLE`
- `CONFIGURING`
- `VALIDATING`
- `RESULT`
- `ERROR`
- `RESET`

### Zone naming
- `build_zone_01`
- `material_zone`
- `program_zone`
- `confirm_zone`

### Contract rule

Names must stay stable across:
- fabrication files
- CV output
- FSM rules
- visuals
- metrics lookup

If a name changes in one subsystem, it must be updated in the interface contract first.

## 10. Responsibility Matrix

| Subsystem | Owner | Sends | Receives | Must Not Do |
|---|---|---|---|---|
| Physical Pieces | Person 5 | piece IDs, dimensions, phase rules, marker placement, zone logic | feedback from architecture and CV constraints | must not change piece IDs without updating the interface contract |
| Computer Vision | Person 4 | normalized marker packet, confidence, stability, zone match, overlap flags | piece definitions, zone definitions, calibration rules | must not design UI |
| TouchDesigner FSM | Person 2 | current state, instructions, guide commands, warnings, metrics visibility | normalized CV packet, sensor input, data outputs | must not depend on raw camera noise |
| TouchDesigner Visuals | Person 3 | projected guides, state visuals, comparison displays | FSM output contract, geometry previews | must not invent state logic |
| Data Research | Person 6 | metrics tables, narrative text, source labels, ranges | geometry and scenario inputs from FSM | must not provide unsourced fixed numbers without ranges |
| ESP32 + Sound + QA | Person 7 | presence flags, reset signal, sound cues, setup checks, logs | current state, operator needs, hardware status | must not bypass the FSM with hidden behavior |
| System Architecture | Person 1 | interface contracts, integration map, calibration checklist, runbook | updates from all subsystems | must not leave subsystem boundaries undefined |

## 11. Minimum Prototype Contract

This is the minimum working version required for the next class.

### Required
- One ArUco marker detected
- `piece_id`, `x`, `y`, `confidence`, `is_stable`, `is_inside_zone` available
- FSM has at least 3 states:
  - `IDLE`
  - `CONFIGURING`
  - `ERROR`
- Projection changes visibly per state
- Manual reset exists

### Minimum success condition

The prototype is valid if:
- one marker can be placed into a valid zone
- the FSM can enter `CONFIGURING`
- invalid placement or low confidence can enter `ERROR`
- reset returns the system to `IDLE`

## 12. Notes for Implementation in TouchDesigner

Recommended implementation:
- Use `Table DATs` for state definitions and piece definitions.
- Use `Python DAT` or `Execute DAT` for FSM logic.
- Use `CHOPs` for timers and debounced values.
- Use `TOPs` for visual projection layers.
- Keep a debug panel showing the current data packet and current FSM state.

### Recommended debugging view
- current FSM state
- previous FSM state
- latest CV packet
- active piece ID
- confidence
- stability flag
- zone ID
- selected material
- current warning or error code

### Practical implementation note

For the prototype, keep the interface contract simple and explicit.
It is better to send a small clean packet that always works than a large ambiguous packet that no one trusts.
