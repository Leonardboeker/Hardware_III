# TouchDesigner Bootstrap

This is the quickest way to stand up the scaled `metric-ui-simulation` layout
inside TouchDesigner at `1280 x 720`.

## What It Creates

`touchdesigner/scripts/metric_ui_bootstrap.py` creates or updates:

- `vision_in`
- `rfid_in`
- `compute_state`
- `compute_state_callbacks`
- `lca_data`
- `lca_data_callbacks`
- `metrics_engine`
- `ui_state`
- `refresh_metrics_ui`
- `render_footprint`
- `render_footprint_callbacks`
- `projector_out`
- every `text_<panel_id>` TOP needed by the 9-panel layout

It also writes the current repo versions of:

- [metrics_engine.py](/o:/Hardware_III/touchdesigner/scripts/metrics_engine.py)
- [ui_state.py](/o:/Hardware_III/touchdesigner/scripts/ui_state.py)
- [state_chop_v1.py](/o:/Hardware_III/touchdesigner/scripts/state_chop_v1.py)
- [footprint_viz_v5.py](/o:/Hardware_III/touchdesigner/scripts/footprint_viz_v5.py)
- [lca_data_reader.py](/o:/Hardware_III/touchdesigner/scripts/lca_data_reader.py)

## Run It

Inside TouchDesigner:

1. Add a Text DAT named `bootstrap_metric_ui`
2. Paste [touchdesigner/scripts/metric_ui_bootstrap.py](/o:/Hardware_III/touchdesigner/scripts/metric_ui_bootstrap.py)
3. Turn `Module` ON
4. In the Textport run:

```python
op("bootstrap_metric_ui").module.bootstrap_metric_ui()
```

## Optional Demo Preview

To immediately populate the interface with a masonry example:

```python
op("bootstrap_metric_ui").module.seed_demo_state()
```

This stores sample TD owner state and then calls:

```python
op("refresh_metrics_ui").module.refresh()
```

## Important Notes

- The bootstrap targets the component that contains the DAT.
- The layout is already scaled to `1280 x 720`.
- `render_footprint` remains the final renderer.
- `text_<panel_id>` TOPs use:

```python
parent().fetch(me.name, "")
```

- If a Script CHOP / Script TOP callback does not bind automatically in your TD
  build, point it manually to the matching callback DAT:
  - `compute_state -> compute_state_callbacks`
  - `render_footprint -> render_footprint_callbacks`
  - `lca_data -> lca_data_callbacks`

## After Bootstrap

The usual refresh call is:

```python
op("refresh_metrics_ui").module.refresh()
```

You can run that after changing owner storage like `current_method`,
`area_m2`, `number_of_floors`, or `current_phase_name`.
