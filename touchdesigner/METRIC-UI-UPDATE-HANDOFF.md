# Metric UI TouchDesigner Update Handoff

Date: 2026-05-18

This document summarizes the TouchDesigner metric UI work completed in the current delivery pass. It is intended as a practical handoff for the team so the latest `.toe`, Python callbacks, assets, and runtime behaviors can be understood and refreshed without reconstructing the full implementation history.

## Scope

This pass focused on the projection-side Metric UI that mirrors the `Metric Ui Simulation` prototype and extends it for installation use inside TouchDesigner.

Delivered areas:

- Bootstrapped TouchDesigner network generation from Python
- Building-part selection and zone hit-testing
- Phase chips and floor/phase scroller mapping
- Guidance glow and onboarding cues
- Method and phase icon pass
- Roof icon correction
- UI-state stability fixes, including BOM-safe DAT refresh
- Method-card animated previews using GIF assets
- Test coverage for selection, scroller mapping, and manifest data

## Main UX/UI Updates

### 1. Bootstrap-driven TD network

`touchdesigner/scripts/metric_ui_bootstrap.py` now acts as the single source of truth for the TouchDesigner scaffold.

It creates or updates:

- core callback DATs
- metrics + UI-state DAT modules
- `render_footprint` Script TOP
- panel Text TOPs
- phase chip block Text TOPs
- method preview Movie File In TOPs

This makes the setup re-runnable and idempotent. Re-running bootstrap updates the existing nodes instead of duplicating them.

### 2. Building-part selection

The main plan panel now has a storage-driven building-zone model.

Implemented capabilities:

- named zone definitions
- zone-level area / wall area / perimeter metadata
- whole-building fallback
- single selection
- additive multi-selection
- coordinate hit-test selection

Main selection helpers:

- `set_selected_building_parts(...)`
- `toggle_selected_building_part(...)`
- `clear_selected_building_parts(...)`
- `select_building_part_at(...)`

Stored values now include:

- `selected_zone_ids`
- `selected_zone_labels`
- `selected_part_label`
- `selected_parts_count`
- `area_m2`
- `selected_wall_area_m2`
- `selected_perimeter_m`

### 3. Phase chips and scroller mapping

The phase row at the top is no longer a single text line. It now behaves as separate chips with active-state styling.

Construction phase scroller mapping:

- `0-20` foundation
- `20-40` structure / walls
- `40-60` roof
- `60-80` openings
- `80-100` finishing

Prefab lifecycle scroller mapping:

- `0-50` CLT track
- `50-100` modular concrete track

Each half is subdivided across the lifecycle stages:

- `A1-A3`
- `A4`
- `A5`
- `B`
- `C`

Floor count mapping is method-aware and respects the current floor constraints for:

- masonry
- 3d printed
- prefab CLT
- prefab modular concrete

Main helpers:

- `floor_scroller_summary(...)`
- `phase_scroller_summary(...)`
- `set_floor_count_from_scroller(...)`
- `set_phase_from_scroller(...)`

### 4. Guidance layer and onboarding feedback

A lightweight guidance system was added to move the user through the flow:

1. choose method
2. set floors
3. choose phase
4. click building part
5. review impact

The UI-state payload now exposes:

- `guidance_target`
- `guidance_message`
- `guidance_highlight_blocks`

The renderer uses that payload to draw:

- breathing glows
- panel halos
- outer-corner beacon lines

This creates a more legible installation flow than static panels alone.

### 5. Symbol language pass

Minimal vector-style symbols were added for:

- phase chips
- method cards

These were then refined to better match the architectural context:

- foundation: footing / base lines
- walls: wall grid
- roof: gable roof silhouette
- openings: window frame
- finishing: finishing gesture
- masonry: brick grid
- 3d printed: print head + layered lines
- prefab: modular stacked units

The roof icon was explicitly corrected after the first pass to remove the upside-down triangle reading.

### 6. Method-card animated previews

Three animated GIF previews were integrated into the `Choose Method` cards:

- masonry: `touchdesigner/assets/method_loops/masonry_mode.gif`
- 3d printed: `touchdesigner/assets/method_loops/3d_printed_mode.gif`
- prefab: `touchdesigner/assets/method_loops/prefab_mode.gif`

The render layer places each preview inside the method card with:

- rounded masking
- dark glass overlay
- method-color tint
- active/inactive treatment

This keeps the previews visually aligned with the existing UI language rather than looking pasted on top.

### 7. Stability and refresh fixes

The bootstrap reader now strips UTF-8 BOM characters when copying repository scripts into TouchDesigner DATs.

This fixed the recurring issue where `ui_state` would fail to compile inside TouchDesigner and the UI would appear stuck on a stale phase.

Relevant fix:

- `_read_repo_text(...).lstrip("\\ufeff")`

## Files Added or Updated

### Core TouchDesigner scripts

- `touchdesigner/scripts/metric_ui_bootstrap.py`
- `touchdesigner/scripts/footprint_viz_v5.py`
- `touchdesigner/scripts/ui_state.py`
- `touchdesigner/scripts/state_chop_v1.py`
- `touchdesigner/scripts/vision2_state_chop.py`

### Added media assets

- `touchdesigner/assets/method_loops/masonry_mode.gif`
- `touchdesigner/assets/method_loops/3d_printed_mode.gif`
- `touchdesigner/assets/method_loops/prefab_mode.gif`

### Added / updated tests

- `tests/test_metric_ui_bootstrap.py`
- `tests/test_touchdesigner_ui_state.py`
- `tests/test_touchdesigner_metrics_engine.py`

### Included TouchDesigner project file

- `vertical-slice.leo-integration.toe`

## TouchDesigner Runtime Notes

After pulling the latest changes, the main refresh flow in TouchDesigner is:

```python
root = op('/project1')
boot = op('/project1/bootstrap_metric_ui').module
boot.bootstrap_metric_ui(owner=root)
root.op('refresh_metrics_ui').module.refresh(owner=root)
root.op('render_footprint').cook(force=True)
```

Useful verification calls:

```python
root.fetch('ui_state', {})
boot.phase_scroller_summary(owner=root)
boot.floor_scroller_summary(owner=root)
```

Method preview nodes created by bootstrap:

- `method_preview_masonry`
- `method_preview_3d_printed`
- `method_preview_prefab`

## Verification Completed

Local verification completed with:

```bash
python -m py_compile touchdesigner/scripts/metric_ui_bootstrap.py touchdesigner/scripts/footprint_viz_v5.py touchdesigner/scripts/ui_state.py
python -m unittest tests.test_metric_ui_bootstrap tests.test_touchdesigner_ui_state tests.test_touchdesigner_metrics_engine
```

## Known Follow-Ups

The following are still good next steps:

- connect physical floor / phase scrollers to the helper setters
- add click-driven selection bridge from panel input to `select_building_part_at(...)`
- expand right-side cards with richer confidence / warning display
- consider FBX or video phase previews beyond method-card loops
- tune preview opacity and active-card emphasis on the projector itself

## Summary

This delivery moves the TouchDesigner UI from a mostly static mirrored layout to a more stateful installation interface:

- it can guide the visitor,
- respond to method / phase / floor / part changes,
- display animated method previews,
- and stay refreshable from a single bootstrap script.

The result is closer to the simulation prototype while being shaped for projection use and future hardware integration.
