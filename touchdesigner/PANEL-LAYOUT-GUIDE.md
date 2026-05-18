# Panel Layout Guide (1280 x 720)

The panel geometry matches the `metric-ui-simulation` layout scaled from
`1920 x 1080` to `1280 x 720`.

`render_footprint` draws all frames and auto-places any Text TOP named
`text_<panel_id>` into the matching slot.

## Panel Table

| Panel ID | Bounds `(x, y, w, h)` | Text TOP name |
|----------|------------------------|---------------|
| `top_phase_navigation` | `271, 15, 600, 67` | `text_top_phase_navigation` |
| `left_info` | `17, 15, 213, 467` | `text_left_info` |
| `left_assembly_sequence` | `17, 493, 307, 173` | `text_left_assembly_sequence` |
| `main_plan_simulation` | `245, 108, 652, 373` | none |
| `method_selection` | `337, 493, 560, 173` | `text_method_selection` |
| `right_comparison` | `910, 15, 353, 292` | `text_right_comparison` |
| `right_cost_chart` | `910, 321, 353, 160` | `text_right_cost_chart` |
| `right_phase_preview` | `910, 493, 353, 173` | `text_right_phase_preview` |
| `bar_bottom_status` | `0, 687, 1280, 33` | `text_bar_bottom_status` |

## Important Notes

- There is no separate physical `prefab_lifecycle_card` panel in TouchDesigner.
  That content shares the `right_comparison` slot, just like the browser sim.
- `render_footprint` is the final compositor. You do not need `compose_final`.
- Text TOPs can stay unconnected. The Script TOP discovers them by name.

## Recommended Text TOP Expression

For every `text_<panel_id>` TOP, use:

```python
parent().fetch(me.name, "")
```

That makes each TOP read the storage value written by `ui_state.py`.

## Minimum Starter Set

If you want the fastest first pass, create these first:
- `text_top_phase_navigation`
- `text_method_selection`
- `text_right_comparison`
- `text_right_phase_preview`
- `text_bar_bottom_status`
