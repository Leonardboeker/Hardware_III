# Hardware III · Jury deck

Reveal.js deck for the IAAC final critique, 2026-05-22.

## Open it

```bash
cd deliverables/jury-deck
python -m http.server 8765
# open http://localhost:8765
```

Or just open `index.html` directly in a modern browser (Chrome / Firefox / Safari) — fonts come from Google Fonts and Reveal comes from jsDelivr, so an internet connection is needed.

Keyboard: `→ ←` navigate. `F` fullscreen. `S` speaker view. `Esc` overview.

## Export to PDF

Append `?print-pdf` to the URL, then File → Print → Save as PDF. Set paper to landscape, margins to zero, "Background graphics" on.

```
http://localhost:8765/?print-pdf
```

## Media

Slide 02 (Context · The proposition) embeds a live detection demo from `assets/media/demo_detection.mp4`. The video autoplays muted on loop. To replace it, drop a new MP4 at that path with the same filename, or update the `<source src=...>` in `index.html`.

## Slide map

| # | Section | Notes |
|---|---------|-------|
| 00 | Title | Brand mark, team, dates |
| 01 | Context · problem | "Construction decisions carry hidden consequences" |
| 02 | Context · proposition | Live demo video (assets/media/demo_detection.mp4) |
| 03 | Experience | Output per phase: CO₂, energy, labour, time, cost |
| 04 | Interaction | 8-step FSM + 5 phase chips |
| 05 | Logic architecture | Content FSM + wrapper + visual codes |
| 06 | Architecture | Input / runtime / output block diagram |
| 07 | Computer vision | 5-step pipeline + OSC channels |
| 08 | Hand gesture sketch (NEW) | vision2 gestures table |
| 09 | TouchDesigner runtime | 7-node network |
| 10 | Physical layer | Method models, footprint pucks, config inputs |
| 11 | Height slider · Phase 02.1 (NEW) | DollaTek slider pipeline |
| 12 | Data layer | Three-method sources table |
| 13 | Metrics engine (NEW) | Data → ui_state → panels |
| 14 | Layout · empty grid | 9-panel projection |
| 15 | Layout · role legend | Input / output / state |
| 16 | Layout · named panels | Annotated grid |
| 17 | Fabrication (NEW) | Components and references |
| 18 | Bibliography (NEW) | Tier 1 academic sources, databases, standards |
| 19 | End | Repository + demo entry point |

## What was added vs the original PDF

- Hand gesture sketch (vision2) slide.
- Height slider Phase 02.1 slide.
- Metrics engine + 9-panel UI flow slide.
- Fabrication status table.
- Reclaimed brick removed from the data-layer table (dropped from v1).
- ArUco dial ID 10 replaced by the DollaTek slider where height is described.

## Design system

See `DESIGN.md` and `PRODUCT.md` at the repo root. Tokens are in `assets/css/theme.css`.

- Typography: Funnel Display + Funnel Sans + JetBrains Mono.
- Color: tinted off-white paper, near-black ink, three OKLCH method colours pulled from `touchdesigner/scripts/footprint_viz_v5.py`.
- Layout: 12-column grid, asymmetric, left-aligned, no centered title stacks.
- Motion: page-load stagger only, exponential ease-out, respects `prefers-reduced-motion`.

## Editing

Each slide is one `<section>` with a `.slide` grid inside. Numbers in `.slide-kicker` and `.slide-foot` are hand-maintained — if you reorder slides, update those by hand. Diagrams are inline SVG, theme-aware via `currentColor`.
