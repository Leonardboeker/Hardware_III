# Interface Contract / Shared Data Language

## 1. Purpose

This document defines the shared data language between the subsystems of the Hardware III project.

It is **not** the FSM diagram.

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

## 2. State Model Layers

The project uses three different state layers.
They must not be mixed.

### Canonical Content FSM

This is the main visitor-facing interaction sequence and the current **canonical FSM**:

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

`PHASE_N` is the TouchDesigner implementation state for the five locked building phases:
- Foundation
- Structure / Walls
- Roof
- Openings
- Finishing

### System Wrapper States

These are system-level modes that sit around the canonical content FSM:
- `CALIBRATION_CHECK`
- `ERROR`
- `RESET`
- `MANUAL_OVERRIDE`

They are not the main content sequence.
They exist for setup, recovery, and operator safety.

### Visual Feedback States

These are projection output states, not the canonical content FSM:
- `DISCONNECTED`
- `PENDING`
- `INVALID`
- `VALID`
- `IDLE_ANIM`
- `SUMMARY`
- `COMPARISON`

They answer:
- Is the system alive?
- Is the piece in the right zone?
- Is the current step confirmed?
- Should the projector show the summary or the full comparison?

## 3. System Architecture Data Flow

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

## 4. Current Working TouchDesigner Contract

This is the **current live implementation contract** used by the working TouchDesigner prototype.

### Vision -> TouchDesigner storage

From [osc_handler.py](/o:/Hardware_III/touchdesigner/scripts/osc_handler.py):

```python
pucks[id] = {
    "projector_xy": (px, py),
    "in_target": bool,
    "last_frame": int,
    "lost": False
}

vision_alive: bool
last_heartbeat_frame: int
manual_advance: bool
```

### Current live messages

| OSC address | Args | Meaning |
|---|---|---|
| `/puck/detected` | `id, frame, proj_x, proj_y, in_target` | One puck is visible and mapped into projector space |
| `/puck/lost` | `id` | A previously visible puck is now lost |
| `/vision/heartbeat` | `frame` | Vision pipeline is alive |

### Why this matters

The current working FSM in [fsm_full.py](/o:/Hardware_III/touchdesigner/scripts/fsm_full.py) already depends on this structure.
Any future interface expansion must stay compatible with it or explicitly replace it.

## 5. CV -> FSM Input Contract

This is the **full normalized contract** Computer Vision should eventually provide to the FSM as the project scales beyond the current vertical slice.

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
| `timestamp` | integer | Unix timestamp in milliseconds | timeout checks, packet freshness |
| `marker_detected` | bool | True when at least one valid marker is detected | state gating |
| `marker_count` | integer | Number of currently visible markers | overlap or completeness logic |
| `piece_id` | string | Unique piece identifier | sequencing, lookup, validation |
| `piece_type` | string | Category such as `geometry`, `method_token`, `material_token`, `control_token` | content-state routing |
| `x` | float | Normalized X coordinate in table space | movement checks |
| `y` | float | Normalized Y coordinate in table space | movement checks |
| `rotation` | float | Piece rotation in degrees | orientation validation |
| `confidence` | float | Detection confidence from `0.0-1.0` | trust threshold |
| `is_stable` | bool | True when placement is stable over time | transition confirmation |
| `is_inside_zone` | bool | True when piece lies inside legal zone | valid vs invalid placement |
| `zone_id` | string | Zone identifier | matching to expected target |
| `user_present` | bool | Optional presence flag | idle engagement, timeout handling |
| `proximity_value` | float | Optional normalized sensor value | lean-in behavior, engagement threshold |
| `selected_material` | string or null | Optional material selection value | `MATERIALS -> VALIDATED` logic |
| `selected_program` | string or null | Optional program selection value | metrics lookup |
| `overlap_detected` | bool | True when pieces conflict spatially | wrapper `ERROR` mode |
| `marker_loss_ms` | integer | Time since marker was last valid | dropout tolerance |

### Mapping to the current working implementation

| Normalized field | Current live TD storage |
|---|---|
| `piece_id` | `pucks[id]` key |
| `x`, `y` | currently `projector_xy` in projected space |
| `is_inside_zone` | `in_target` |
| `marker_detected` | puck exists and is not lost |
| `marker_loss_ms` | currently approximated through `lost` and heartbeat timing |
| `vision_alive` | separate storage flag, not part of the normalized packet yet |

## 6. FSM -> Visuals / Projection Output Contract

This is what the FSM should send to the projection layer.

### Required fields
- `current_content_state`
- `system_wrapper_state`
- `visual_feedback_state`
- `instruction`
- `active_piece_id`
- `state_color`
- `valid_zone_geometry`
- `projected_guides`
- `warning_message`
- `metrics_visible`
- `comparison_mode`

### Optional fields
- `current_phase_index`
- `current_phase_name`
- `cost_estimate`
- `co2_estimate`
- `labor_hours`
- `construction_time`
- `material_origin`
- `revenue_estimate`
- `profit_estimate`
- `phase_breakdown`
- `data_status`
- `confidence_display`
- `sound_cue`
- `log_event`

### JSON example

```json
{
  "current_content_state": "FOOTPRINT",
  "system_wrapper_state": null,
  "visual_feedback_state": "INVALID",
  "instruction": "Place the next footprint puck",
  "active_piece_id": "FOOTPRINT_03",
  "state_color": "red_oxide",
  "valid_zone_geometry": "footprint_zone_03",
  "projected_guides": ["target_outline", "ghost_target", "current_halo"],
  "warning_message": "Piece is outside the allowed zone",
  "metrics_visible": false,
  "comparison_mode": false
}
```

### Field definitions

| Field | Type | Description | Used by Visuals for |
|---|---|---|---|
| `current_content_state` | string | Current canonical content FSM state | choose the main interaction view |
| `system_wrapper_state` | string or null | Current wrapper mode such as `ERROR` or `RESET` | override normal flow when needed |
| `visual_feedback_state` | string | Projection feedback mode such as `PENDING`, `INVALID`, `VALID` | choose feedback graphics |
| `instruction` | string | Main instruction for the user | table text and side labels |
| `active_piece_id` | string or null | Piece currently expected or corrected | target-specific overlays |
| `state_color` | string | Named palette token | stable color language |
| `valid_zone_geometry` | string or object | Expected legal zone | outlines and masks |
| `projected_guides` | array | Active guide layers | overlay switching |
| `warning_message` | string or null | Error or correction message | warning visuals |
| `metrics_visible` | bool | Whether metrics should be rendered now | summary and comparison gating |
| `comparison_mode` | bool | Whether comparison view is active | split layouts |
| `current_phase_index` | integer | Phase index within `PHASE_N` | phase bar and phase preview |
| `current_phase_name` | string | Phase name such as `FOUNDATION` | phase labels |
| `cost_estimate` | number or string | Cost output or range | result cards |
| `co2_estimate` | number or string | CO2 output or range | environmental overlays |
| `labor_hours` | number or string | Labor output or range | labor display |
| `construction_time` | number or string | Time output or range | timing bars |
| `material_origin` | string or object | Origin summary or per-phase origin labels | supply-chain overlays |
| `revenue_estimate` | number or string | Revenue output | business summary |
| `profit_estimate` | number or string | Profit output | business summary |
| `phase_breakdown` | object | Per-phase metric payload for detailed overlays | phase cards and debug panels |
| `data_status` | string | Whether the metrics result is `ok`, `partial`, or `fallback` | trust and warning UI |
| `confidence_display` | float | Debug confidence | operator panel |
| `sound_cue` | string | Audio event token | sound routing |
| `log_event` | string | Log line or state event | diagnostics |

## 7. FSM Transition Conditions

The FSM does not need raw camera images.
It needs interpreted values.

### Canonical content FSM examples
- IF `method_selector.in_target == true` for `CONFIRM_HOLD_FRAMES` THEN ENTER `METHOD`
- IF all required footprint pucks are confirmed in order THEN ENTER `HEIGHT`
- IF height marker is confirmed THEN ENTER `MATERIALS`
- IF material marker is confirmed THEN ENTER `VALIDATED`
- IF `advance_to_phase_n == true` THEN ENTER `PHASE_N`
- IF all methods are completed THEN ENTER `COMPARISON`

### Wrapper state examples
- IF `vision_alive == false` long enough THEN set `visual_feedback_state = DISCONNECTED`
- IF `reset_signal == true` THEN ENTER wrapper `RESET`
- IF `overlap_detected == true` THEN ENTER wrapper `ERROR`

### Visual feedback examples
- IF puck exists but `in_target == false` THEN `visual_feedback_state = INVALID`
- IF puck exists and `in_target == true` but hold not complete THEN `visual_feedback_state = VALID`
- IF no puck exists yet in current step THEN `visual_feedback_state = PENDING`
- IF content state is `VALIDATED` THEN `visual_feedback_state = SUMMARY`

## 8. Data / Metrics Layer Contract

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
- `material_origin`
- `revenue_estimate`
- `profit_estimate`
- `source_label`
- `confidence_range`
- `phase_breakdown`
- `data_status`

### Example metrics table

| construction_method | cost_per_m2_range | co2_per_m2_range | labor_hours_range | time_range | source_label |
|---|---|---|---|---|---|
| masonry | 950-1350 EUR/m2 | 280-420 kgCO2e/m2 | 22-34 h/m2 | 14-20 weeks | literature_mix_v1 |
| prefab_timber | 1100-1600 EUR/m2 | 140-260 kgCO2e/m2 | 12-20 h/m2 | 8-12 weeks | literature_mix_v1 |
| concrete_3dp | 1000-1500 EUR/m2 | 220-390 kgCO2e/m2 | 8-16 h/m2 | 6-10 weeks | literature_mix_v1 |

### Rules
- Use ranges, not single unsupported numbers.
- Every value must carry a source label.
- Missing data must return null or error, not fake precision.

### Current implementation direction

The starter implementation for this layer now lives in:
- [metrics_engine.py](/o:/Hardware_III/touchdesigner/scripts/metrics_engine.py)

It already supports:
- CSV loading from `data/methods/*.csv`
- provisional fallback values while CSV files are still missing
- TouchDesigner `fetch/store` integration
- per-phase breakdowns plus total summary outputs

## 9. Sensor / ESP32 Input Contract

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

### What they do
- `user_present` can wake idle visuals or future onboarding behavior while content FSM remains in `IDLE`
- `reset_signal` must override everything and clear the session
- `sensor_online` is a health flag, not a content-state trigger

## 10. Rhino / Fabrication Contract

The fabrication layer must provide:
- piece ID list
- piece type list
- marker placement map
- legal zones
- valid adjacency rules
- phase sequence
- simplified geometry previews
- phase preview assets

### Example

```text
piece_id: FOOTPRINT_03
piece_type: geometry
content_state: FOOTPRINT
allowed_zone: footprint_zone_03
valid_after: FOOTPRINT_02
valid_before: HEIGHT_01
```

## 11. Naming Conventions

### Content states
- `IDLE`
- `METHOD`
- `FOOTPRINT`
- `HEIGHT`
- `MATERIALS`
- `VALIDATED`
- `PHASE_N`
- `COMPARISON`

### Wrapper states
- `CALIBRATION_CHECK`
- `ERROR`
- `RESET`
- `MANUAL_OVERRIDE`

### Visual feedback states
- `DISCONNECTED`
- `PENDING`
- `INVALID`
- `VALID`
- `IDLE_ANIM`
- `SUMMARY`
- `COMPARISON`

### Piece naming
- `FOOTPRINT_01`
- `HEIGHT_01`
- `MATERIAL_01`
- `TOKEN_METHOD_MASONRY`
- `TOKEN_METHOD_3D_PRINTED`
- `TOKEN_METHOD_PREFAB`

## 12. Responsibility Matrix

| Subsystem | Owner | Sends | Receives | Must Not Do |
|---|---|---|---|---|
| Physical Pieces | Person 5 | piece IDs, dimensions, phase rules, marker placement, zone logic | architecture + CV constraints | must not change piece IDs without updating the contract |
| Computer Vision | Person 4 | normalized marker packet, projector-space coordinates, in-target flags, heartbeat | piece definitions, zone definitions, calibration rules | must not design UI |
| TouchDesigner FSM | Person 2 | content state, wrapper state, visual state, guide commands, metric triggers | normalized CV data, sensor input, data outputs | must not depend directly on raw camera noise |
| TouchDesigner Visuals | Person 3 | projection overlays, phase graphics, summaries, comparison layouts | FSM output contract, geometry previews | must not invent state logic |
| Data Research | Person 6 | metrics tables, source labels, ranges, narrative text | validated scenario inputs | must not provide unsourced fixed values |
| ESP32 + Sound + QA | Person 7 | presence flags, reset signal, sound cues, QA logs | FSM state outputs, operator needs | must not bypass the FSM |
| System Architecture | Person 1 | contracts, integration map, runbook, calibration checklist | subsystem updates | must not leave state layers ambiguous |

## 13. Minimum Prototype Contract

The minimum working version for the next class is:
- one ArUco marker detected
- `piece_id`, `x`, `y`, `confidence`, `is_stable`, `is_inside_zone` available or mapped from the current live contract
- canonical content FSM at least proving `IDLE -> METHOD` or `IDLE -> FOOTPRINT` behavior
- visible projection change per visual feedback state
- manual reset or manual advance exists

## 14. Notes For Implementation In TouchDesigner

- Use `Table DATs` for piece definitions, phase names, and state lookup.
- Use `Python DAT` or `Script CHOP` for FSM logic.
- Use `CHOPs` for timers, heartbeat checks, and debounced confirmation windows.
- Use `TOPs` for guide projection, ghost overlays, and summary / comparison layouts.
- Keep a debug panel showing:
  - `current_content_state`
  - `system_wrapper_state`
  - `visual_feedback_state`
  - latest puck storage
  - `vision_alive`
  - `current_method`
  - `current_phase`
