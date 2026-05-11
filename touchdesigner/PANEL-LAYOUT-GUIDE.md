# Panel Layout Guide (1280×720)

UI from `reference/Panel_Ui.pdf`, scaled from 1920×1080 → 1280×720
(TD Non-Commercial limit). One Script TOP does **everything** — panels,
footprint geometry, method color, AND auto-places text from named Text TOPs.

## Network topology — much simpler now

```
vision_in ─┐
rfid_in   ─┼─► compute_state ─┐
                              │
                              ▼
                       render_footprint  ─►  projector_out
                       (Script TOP, also reads
                        all text_<panel_id> TOPs)
                              ▲
                              │
              text_method_selection (Text TOP)
              text_top_phase_navigation (Text TOP)
              text_right_comparison (Text TOP)
              ... (one per panel you want text in)
```

**No more `compose_final`. No more Over TOP. No more Translate math.**

## Panel coordinates (1280×720)

| Panel ID | x, y, w, h | Text TOP name | Suggested font size |
|----------|------------|---------------|---------------------|
| `top_phase_navigation` | 271, 15, 600, 67 | `text_top_phase_navigation` | 28 |
| `left_info` | 17, 15, 213, 467 | `text_left_info` | 13 |
| `left_assembly_sequence` | 17, 493, 307, 173 | `text_left_assembly_sequence` | 13 |
| `main_plan_simulation` | 245, 108, 652, 373 | — (footprint auto-rendered) | — |
| `method_selection` | 337, 493, 560, 173 | `text_method_selection` | 42 |
| `right_comparison` | 910, 15, 353, 292 | `text_right_comparison` | 14 |
| `right_cost_chart` | 910, 321, 353, 160 | `text_right_cost_chart` | 16 |
| `right_phase_preview` | 910, 493, 353, 173 | `text_right_phase_preview` | 14 |
| `bar_bottom_status` | 0, 687, 1280, 33 | `text_bar_bottom_status` | 14 |

## How to add text to any panel

This is the **only workflow** you need. Repeat per panel.

1. **Add → TOP → Text**
2. **Rename** to `text_<panel_id>` exactly (e.g. `text_method_selection`)
3. **Common Tab** → **Resolution** = panel's `w` × `h` from the table above
4. **Text Tab** → click `=` next to **Text** for expression mode, or type a literal string
5. **Font Tab** → set Size from the table, **Horizontal Align**: Center, **Vertical Align**: Center
6. **Color Tab** → text color (white = `1, 1, 1, 1`)
7. **DON'T wire it to anything** — the Script TOP picks it up automatically by name

That's it. The Script TOP reads the Text TOP's pixels every frame and composites them into the right panel position.

## Ready-to-paste Text expressions

For text panels with data binding (Expression mode):

**`text_method_selection`** — current construction method name:
```python
['NO METHOD', 'MASONRY', '3D PRINTED', 'PREFAB'][max(0, min(int(op('compute_state')['method_id'][0]), 3))]
```

**`text_bar_bottom_status`** — live status line:
```python
'VISION ' + ['OFFLINE','LIVE'][int(op('compute_state')['hb_alive'][0])] + '   |   Pucks: ' + str(int(op('compute_state')['puck_count'][0])) + '   |   Area: ' + str(int(op('compute_state')['area_px2'][0])) + ' px²'
```

**`text_top_phase_navigation`** — static phase name for now:
```python
'FOUNDATION'
```

**`text_left_info`** — placeholder per phase (multi-line):
```python
'PHASE INFO\\n\\nImpact: TBD\\nMaterial: TBD\\nLogistics: TBD'
```

**`text_right_comparison`** — placeholder for comparison table:
```python
'COMPARISON\\n\\nMasonry: ...\\n3D Printed: ...\\nPrefab: ...'
```

**`text_right_cost_chart`** — total cost placeholder:
```python
'TOTAL COST\\n\\n€ —— / m²'
```

**`text_right_phase_preview`** — checklist placeholder:
```python
'PHASE CHECKLIST\\n\\n☐ Place pucks\\n☐ Validate\\n☐ Continue'
```

## Cleanup: delete the old composite chain

The old approach used `compose_final` (Over TOP) + a single `text_method_selection`
positioned with manual Translate. Both can go:

1. Click on `compose_final` → **Delete**
2. (Don't delete `text_method_selection` — we want to keep that Text TOP, just
   rename if needed and let the Script TOP pick it up automatically)
3. Wire **`render_footprint` Out → `projector_out` In** directly

## Verifying it works

Inline-preview `render_footprint` (key `1` over the node). You should see:
- All 9 panels with borders
- Whatever text is in `text_method_selection` showing inside the method selection
  panel — automatically, no translates set anywhere
- Heartbeat dot bottom-left
- Method color block on left side of method panel

Change `rfid_in` value → method block color + method name update live.

## Why this is better than Over TOPs

- **One source of truth** — panel positions live in the Python script
- **Pixel-precise** — no normalized `-0.5..+0.5` math
- **Scales** — add a 10th panel? Add one entry to `PANELS` dict, done
- **Less network clutter** — no compose chain
- **Auto-discovery** — if you don't create `text_left_info`, that panel just
  shows empty frame, no errors
