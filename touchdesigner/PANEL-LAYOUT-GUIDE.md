# Panel Layout Guide (1280×720)

UI layout from `reference/Panel_Ui.pdf`, scaled from 1920×1080 → 1280×720
(scale factor 2/3) for the TD Non-Commercial resolution limit.

## Panel coordinates

| Panel ID | x, y, w, h | What goes in it |
|----------|------------|-----------------|
| `panel_top_phase_navigation` | 271, 15, 600, 67 | Phase selector (foundation → finishing) |
| `panel_left_info` | 17, 15, 213, 467 | Current phase info, impact, material, logistics |
| `panel_left_assembly_sequence` | 17, 493, 307, 173 | Assembly sequence preview + thumbnails |
| `panel_main_plan_simulation` | 245, 108, 652, 373 | **Footprint geometry — auto-rendered** |
| `panel_method_selection` | 337, 493, 560, 173 | **Method color block — auto-rendered** |
| `panel_right_comparison` | 910, 15, 353, 292 | Phase-based comparison table |
| `panel_right_cost_chart` | 910, 321, 353, 160 | Cost breakdown chart |
| `panel_right_phase_preview` | 910, 493, 353, 173 | Phase preview + checklist |
| `bar_bottom_status` | 0, 687, 1280, 33 | Reset, help, audio, heartbeat dot |

## Build phases

### Phase 1 — Frame (DONE)

`render_footprint` Script TOP now draws:
- Background + edge frames for all 9 panels
- Footprint geometry inside `panel_main_plan_simulation`
- Method color block inside `panel_method_selection`
- Heartbeat dot inside `bar_bottom_status`

No code change needed in TD — just re-paste [`scripts/footprint_viz_v5.py`](scripts/footprint_viz_v5.py)
into the existing `render_footprint` Script TOP.

### Phase 2 — Text overlays (NEXT)

Add one Text TOP per text-bearing panel, then composite over `render_footprint`.

Naming convention: `text_<panel_id>` — e.g. `text_method_selection`, `text_left_info`.

| Text TOP | Position (x, y, w, h) | Content (expression mode) |
|---|---|---|
| `text_top_phase` | 271, 15, 600, 67 | active phase name (e.g. "STRUCTURE") |
| `text_left_info` | 17, 15, 213, 467 | phase info text block |
| `text_method_selection` | 337+170, 493, 390, 173 | method name (right of color block) |
| `text_right_comparison` | 910, 15, 353, 292 | comparison table rows |
| `text_right_cost` | 910, 321, 353, 160 | total cost + breakdown |
| `text_right_phase_preview` | 910, 493, 353, 173 | checklist |
| `text_bottom_status` | 30, 687, 1250, 33 | help text + heartbeat label |

For each Text TOP:
- Resolution = panel size from the table above
- Font Size: see suggested sizes below
- Color = white (1,1,1,1) or grey (0.85, 0.85, 0.85, 1.0)
- Align: per panel design

Suggested font sizes for 1280×720:
- Panel labels / headings: 18 pt
- Body text: 13 pt
- Big numbers (method name, totals): 28 pt

### Phase 3 — Compose

Replace the current `compose_final` Over TOP with a **Layout TOP** chain
or a series of stacked Over TOPs that place each Text TOP at its
target panel position. Order:

```
render_footprint  (bottom layer — panel frames + footprint + method color)
  + text_top_phase
  + text_left_info
  + text_method_selection
  + text_right_comparison
  + text_right_cost
  + text_right_phase_preview
  + text_bottom_status
  = compose_final → projector_out
```

Each Over TOP needs Translate ty/tx set to position the text panel correctly.

> Tip: instead of N stacked Over TOPs, use one **Composite TOP** with N inputs —
> set each input's "Translate" in the Composite parameters. Cleaner network.

## Quick test of Phase 1

After re-pasting `footprint_viz_v5.py`:

1. Inline-preview of `render_footprint` should show **9 dark rectangles** with borders
2. Change `rfid_in` Channel 0 Value → the block inside `panel_method_selection`
   changes color (terracotta / cyan / yellow / grey)
3. Run vision pipeline → puck circles appear inside `panel_main_plan_simulation`,
   not stretched over the whole canvas
4. The heartbeat dot in the bottom-left of the status bar is green when
   vision is running, red when offline

If something looks wrong: take a screenshot of the `render_footprint` preview
and we adjust.
