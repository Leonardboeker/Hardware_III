## Metric UI Progress

Updated: 2026-05-11

This note tracks the current state of the TouchDesigner metric UI integration, the files that were touched, and the remaining roadmap to reach a final demo-ready build.

## Completed So Far

- Bootstrapped a reusable `bootstrap_metric_ui.py` helper for creating and updating the shared TouchDesigner network.
- Added resilient Text TOP configuration so TD parameter name differences do not break layout updates.
- Added compact panel/block text generation in `ui_state.py` for the current 9-panel Leo layout.
- Connected method-driven accent colors in `footprint_viz_v5.py`.
- Verified debug method switching for:
  - `1 = masonry`
  - `2 = 3d_printed`
  - `3 = prefab`
- Added floor constraint helpers in `metric_ui_bootstrap.py`:
  - `floor_constraint_summary()`
  - `set_floor_count()`
  - `step_floor_count()`
  - `set_prefab_sub_method()`
  - `set_current_phase()`
- Added floor constraint logic:
  - Masonry: `1-5`
  - 3D Printed: `1-2`
  - Prefab CLT: `1-8`
  - Prefab Modular Concrete: `1-12`
- Added a visible floor-control text block set for:
  - minus button
  - current floor value
  - plus button
- Synced `compute_state` callbacks with owner storage so method/material/phase updates refresh the UI more reliably.
- Kept TouchDesigner refresh helpers in place so testing can be done from Textport without rebuilding the whole network.

## Files Touched

- `touchdesigner/scripts/metric_ui_bootstrap.py`
- `touchdesigner/scripts/ui_state.py`
- `touchdesigner/scripts/footprint_viz_v5.py`
- `touchdesigner/scripts/state_chop_v1.py`
- `touchdesigner/scripts/vision2_state_chop.py`

## Current Working State

- Method switching is working and updates the UI accent colors.
- Metrics refresh and text panel refresh are working together.
- Floor count can be changed through helper functions and is clamped by method rules.
- Prefab subtype constraints exist in code.
- Phase can be changed through helper functions.

## Known Gaps Right Now

- Floor controls are not yet clickable in the TD UI.
- Phase chips are still display-only and not interactive.
- Center plan selection is not yet connected to real building-part selection.
- Prefab lifecycle mode is not yet presented as a fully separate interaction mode.
- Some typography and spacing still need final polish panel-by-panel.
- Real hardware flow still needs a final pass after UI interaction is complete.

## TouchDesigner Test Helpers

Use these from Textport after reloading the DATs:

```python
root = op("/project1")
op("/project1/bootstrap_metric_ui").module.debug_set_method(1, owner=root)
op("/project1/bootstrap_metric_ui").module.set_floor_count(3, owner=root)
op("/project1/bootstrap_metric_ui").module.set_current_phase("roof", owner=root)
```

Prefab CLT / modular concrete:

```python
root = op("/project1")
op("/project1/bootstrap_metric_ui").module.debug_set_method(3, owner=root)
op("/project1/bootstrap_metric_ui").module.set_prefab_sub_method("clt", owner=root)
op("/project1/bootstrap_metric_ui").module.set_prefab_sub_method("modular_concrete", owner=root)
```

## Remaining Roadmap

### 1. UI Stabilization

- Finalize panel typography, line breaks, and spacing.
- Make the floor control row visually clean and aligned.
- Polish status bar, method notes, total project impact, and current state cards.
- Keep a consistent accent language across all methods.

### 2. Real Floor Interaction

- Make `- / value / +` clickable inside TouchDesigner.
- Trigger `step_floor_count(-1)` and `step_floor_count(+1)` from UI interaction.
- Show method-aware clamp feedback in the UI.
- Refresh totals and state immediately after each click.

### 3. Phase Navigation Interaction

- Turn phase chips into clickable navigation.
- Highlight the active phase cleanly.
- Disable phase chips in prefab mode and show lifecycle messaging instead.

### 4. Building Part Selection

- Implement center-plan selectable zones.
- Support single-select and multi-select.
- Show selected part count and selected area correctly.
- Recompute part impact based on the current selected zone set.

### 5. Prefab Lifecycle Mode

- Add explicit CLT / Modular Concrete UI toggle.
- Replace phase-style comparison with lifecycle-stage presentation:
  - `A1-A3`
  - `A4`
  - `A5`
  - `B`
  - `C`
- Update right-side cards so prefab reads as a distinct mode, not a phase clone.

### 6. Hardware Integration Pass

- Reconnect stable RFID method switching.
- Confirm vision heartbeat / offline behavior.
- Decide whether floor count will be driven by UI, vision markers, or both.
- Stabilize the real demo input path so helper commands are no longer required.

### 7. Save / Compare Flow

- Add scenario save support.
- Add side-by-side comparison between methods or saved runs.
- Prepare a clean demo mode with minimal debug noise.

### 8. Final QA and Demo Prep

- Build a reload/reset checklist.
- Test every method and floor range.
- Test offline and failure fallback states.
- Prepare a short and long demo script for review day.

## Recommended Next Step

The next highest-value task is to finish the floor control as a real clickable UI interaction before moving on to phase chips or center-plan selection.
