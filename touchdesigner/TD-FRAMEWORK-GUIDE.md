# TouchDesigner Framework Setup Guide

Build this network in `vertical-slice.toe`.
Recommended TD build: `2025.32050`.

This guide reflects the current shared direction:
- 9-panel projection layout
- `render_footprint` as the single final Script TOP
- normalized `metrics_engine`
- `ui_state` as the panel-text bridge

## Fastest Path

If you want the network scaffold created automatically inside TouchDesigner:

1. Add a Text DAT named `bootstrap_metric_ui`
2. Paste [touchdesigner/scripts/metric_ui_bootstrap.py](/o:/Hardware_III/touchdesigner/scripts/metric_ui_bootstrap.py)
3. Turn `Module` ON
4. Run:

```python
op("bootstrap_metric_ui").module.bootstrap_metric_ui()
```

Optional demo seed:

```python
op("bootstrap_metric_ui").module.seed_demo_state()
```

That creates the main nodes, text panels, callback DATs, and the `refresh_metrics_ui`
helper DAT. The rest of this guide describes the same network manually.

## Core Nodes

| Node name | Type | Role |
|-----------|------|------|
| `vision_in` | OSC In CHOP | live CV / OSC data |
| `rfid_in` | Constant CHOP now, Serial DAT later | method selection |
| `compute_state` | Script CHOP | aggregates area, heartbeat, method id |
| `render_footprint` | Script TOP | draws the 9-panel layout and auto-blits panel text |
| `metrics_engine` | Text DAT, Module ON | computes `metrics_output` |
| `ui_state` | Text DAT, Module ON | converts `metrics_output` into panel text strings |
| `lca_data` | Script DAT | exposes `methods_db.json` rows inside TD |
| `text_<panel_id>` | Text TOP | optional text overlay per panel |
| `projector_out` | Window COMP | sends the final frame to the projector |

## Architecture

```text
vision_in ----.
              +--> compute_state -------------------------------.
rfid_in -----'                                               |
                                                              |
metrics_engine (DAT module) ---> owner storage: metrics_output |
ui_state      (DAT module) ---> owner storage: text_*         |
                                                              v
text_<panel_id> TOPs -------------------------------> render_footprint -> projector_out
```

`render_footprint` is the final image. No `compose_final` and no Over TOP are needed.

## Step 0 - Clean Up Old Nodes

Delete old one-off nodes if they are still present:
- `compose_final`
- `stats_text`
- old `text1`, `over1`, `over2`, `transform1`
- unused `script1`, `script2`, `script3`

Keep the actual inputs if they already exist and rename them into the names below.

## Step 1 - `vision_in` (OSC In CHOP)

Rename your OSC input node to `vision_in`.

Recommended settings:
- `Protocol`: `UDP`
- `Port`: `7000`
- `Active`: `On`

## Step 2 - `rfid_in`

For now use a Constant CHOP:
1. Add `CHOP -> Constant`
2. Rename it to `rfid_in`
3. Create channel `method_id`
4. Set its value to `0`

Later, when the ESP32 reader is ready, replace this with a Serial DAT and paste
`touchdesigner/scripts/serial_rfid_v1.py` into the callbacks.

## Step 3 - `compute_state` (Script CHOP)

1. Add `CHOP -> Script`
2. Rename to `compute_state`
3. Paste [touchdesigner/scripts/state_chop_v1.py](/o:/Hardware_III/touchdesigner/scripts/state_chop_v1.py)
4. Set `Cook Type` to `Every Frame`

This outputs:
- `puck_count`
- `area_px2`
- `area_m2`
- `method_id`
- `hb_alive`

If the richer OSC payload is available later, you can swap in
[touchdesigner/scripts/vision2_state_chop.py](/o:/Hardware_III/touchdesigner/scripts/vision2_state_chop.py)
instead.

## Step 4 - `lca_data` (Script DAT)

1. Add `DAT -> Script`
2. Rename to `lca_data`
3. Paste [touchdesigner/scripts/lca_data_reader.py](/o:/Hardware_III/touchdesigner/scripts/lca_data_reader.py)
4. Pulse cook / keep it available in the network

This gives the TD network a live table view of `data/methods_db.json`.

## Step 5 - `metrics_engine` (Text DAT, Module ON)

1. Add `DAT -> Text`
2. Rename to `metrics_engine`
3. Paste [touchdesigner/scripts/metrics_engine.py](/o:/Hardware_III/touchdesigner/scripts/metrics_engine.py)
4. Turn `Module` ON

This module reads owner storage like `current_method`, `area_m2`,
`number_of_floors`, and `current_phase_name`, then stores `metrics_output`.

## Step 6 - `ui_state` (Text DAT, Module ON)

1. Add `DAT -> Text`
2. Rename to `ui_state`
3. Paste [touchdesigner/scripts/ui_state.py](/o:/Hardware_III/touchdesigner/scripts/ui_state.py)
4. Turn `Module` ON

After metrics recompute, call:

```python
op("metrics_engine").module.compute_and_store_touchdesigner()
op("ui_state").module.compute_and_store_touchdesigner_ui()
```

That writes panel-facing storage keys such as:
- `text_top_phase_navigation`
- `text_left_info`
- `text_left_assembly_sequence`
- `text_method_selection`
- `text_right_comparison`
- `text_right_cost_chart`
- `text_right_phase_preview`
- `text_bar_bottom_status`

## Step 7 - `render_footprint` (Script TOP)

1. Add `TOP -> Script`
2. Rename to `render_footprint`
3. Paste [touchdesigner/scripts/footprint_viz_v5.py](/o:/Hardware_III/touchdesigner/scripts/footprint_viz_v5.py)
4. Set resolution to `1280 x 720`
5. Set `Cook Type` to `Every Frame`

This script:
- draws all 9 panels
- draws the footprint polygon in the center panel
- draws the method color block
- draws heartbeat status
- auto-composites any `Text TOP` named `text_<panel_id>`

## Step 8 - Add Text TOPs For Panels

Create Text TOPs only for the panels you want populated immediately.
At minimum, create:
- `text_top_phase_navigation`
- `text_left_info`
- `text_left_assembly_sequence`
- `text_method_selection`
- `text_right_comparison`
- `text_right_cost_chart`
- `text_right_phase_preview`
- `text_bar_bottom_status`

Set each Text TOP's text expression to:

```python
parent().fetch(me.name, "")
```

Because each TOP is named `text_<panel_id>`, this expression makes the TOP read
its matching storage value directly.

Panel sizes and coordinates are listed in
[touchdesigner/PANEL-LAYOUT-GUIDE.md](/o:/Hardware_III/touchdesigner/PANEL-LAYOUT-GUIDE.md).

## Step 9 - `projector_out` (Window COMP)

Rename your display window to `projector_out` and wire:

```text
render_footprint -> projector_out
```

Recommended settings:
- resolution `1280 x 720`
- correct monitor index for the projector

## First Local Test

Before the full control flow is wired, seed a few owner storage values manually:

```python
parent().store("current_method", "masonry")
parent().store("area_m2", 42.0)
parent().store("number_of_floors", 3)
parent().store("current_phase_name", "structure")
```

Then run:

```python
op("metrics_engine").module.compute_and_store_touchdesigner()
op("ui_state").module.compute_and_store_touchdesigner_ui()
```

Expected result:
- panel texts appear in the correct 9-panel slots
- bottom bar shows area / method / status
- method panel shows the selected method
- right-side cards show totals and active-stage values

## When RFID Hardware Arrives

Replace the Constant CHOP with a Serial DAT:
1. Delete the Constant CHOP `rfid_in`
2. Add `DAT -> Serial`
3. Rename it to `rfid_in`
4. Set the correct COM port and `115200` baud
5. Paste [touchdesigner/scripts/serial_rfid_v1.py](/o:/Hardware_III/touchdesigner/scripts/serial_rfid_v1.py)

No `compute_state` script change should be needed.
