# UI State Integration

This note explains how to connect the normalized metrics engine to
TouchDesigner panel text without forcing the render layer to parse nested
Python dictionaries.

## Purpose

`touchdesigner/scripts/ui_state.py` converts `metrics_output` into:

- a compact `ui_state` payload
- panel-ready strings
- storage keys such as `text_right_phase_preview`

That gives us a clean split:

- `metrics_engine.py` owns calculations
- `ui_state.py` owns panel text and panel-facing labels
- projection scripts only render

## Recommended TouchDesigner setup

Inside the same Base COMP or owner that stores runtime state:

1. Add a Text DAT named `metrics_engine`
2. Paste `touchdesigner/scripts/metrics_engine.py`
3. Enable Module ON
4. Add a Text DAT named `ui_state`
5. Paste `touchdesigner/scripts/ui_state.py`
6. Enable Module ON

## Runtime flow

When scenario values change:

```python
op('metrics_engine').module.compute_and_store_touchdesigner()
op('ui_state').module.compute_and_store_touchdesigner_ui()
```

The second call reads `metrics_output` from owner storage and writes:

- `ui_state`
- `ui_panel_texts`
- `text_top_phase_navigation`
- `text_left_info`
- `text_left_assembly_sequence`
- `text_method_selection`
- `text_right_comparison`
- `text_right_cost_chart`
- `text_right_phase_preview`
- `text_bar_bottom_status`
- `text_stats_text`

## Text TOP expressions

If the Text TOPs live in the same owner component, use expressions like:

```python
parent().fetch('text_top_phase_navigation', '')
```

```python
parent().fetch('text_right_phase_preview', '')
```

```python
parent().fetch('text_bar_bottom_status', '')
```

For the older lightweight scaffold, `stats_text` can read:

```python
parent().fetch('text_stats_text', '')
```

## What the UI layer exposes

The stored `ui_state` payload includes:

- `method_label`
- `status_label`
- `path_label`
- `data_model_label`
- `display_mode_label`
- `active_stage_key`
- `active_stage_label`
- `sub_method_label`
- `warning_labels`
- `sequence_summary`
- `available_sub_methods`
- `stage_selection`
- `stage_summaries`
- `totals`
- `panel_texts`

## Current scope

This is the first bridge layer only.

It already supports:

- phase path vs lifecycle path labeling
- active stage summary text
- totals text
- prefab sub-method label display
- warning text summary
- compatibility with Leo's 9-panel naming
- compatibility with the current `stats_text` bottom-strip scaffold

It does not yet add:

- interactive prefab toggles inside TD
- floor-stepper controls
- richer chart graphics
- zone-by-zone simulation behavior

Those come after this data-binding layer is stable.
