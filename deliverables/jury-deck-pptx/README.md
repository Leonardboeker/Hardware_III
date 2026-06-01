# Hardware III · Jury deck · PowerPoint version

PowerPoint mirror of the HTML deck at `../jury-deck/`. Same 19 slides, same content, same brand colors. Built from a single Python script.

## Open it

`HARDWARE_III_jury.pptx` (86 MB — most of it is the embedded demo video on slide 02).

PowerPoint 2019+ on Windows or Mac, or Keynote, or LibreOffice Impress.

## Fonts

The script names **Funnel Display**, **Funnel Sans**, and **JetBrains Mono**. If they are not installed on the presenting machine, PowerPoint substitutes the system default (usually Calibri / Consolas). Install the three fonts from Google Fonts for fidelity matching the HTML deck:

- https://fonts.google.com/specimen/Funnel+Display
- https://fonts.google.com/specimen/Funnel+Sans
- https://fonts.google.com/specimen/JetBrains+Mono

## Regenerate after edits

Edit `build_pptx.py`, then from repo root:

```powershell
python deliverables\jury-deck-pptx\build_pptx.py
```

Output overwrites `HARDWARE_III_jury.pptx`.

Dependencies: `python-pptx` 1.0+ (`pip install python-pptx`).

## Slide map

| # | Section | PPTX function |
|---|---------|---------------|
| 00 | Title | `slide_00_title` |
| 01 | Context · problem | `slide_01_context_problem` |
| 02 | Context · proposition (video poster + embedded clip) | `slide_02_context_proposition` |
| 03 | Experience | `slide_03_experience` |
| 04 | Interaction · phase + lifecycle tracks | `slide_04_interaction` |
| 05 | Logic architecture | `slide_05_logic` |
| 06 | Architecture | `slide_06_architecture` |
| 07 | Computer vision | `slide_07_vision` |
| 08 | Hand gesture sketch | `slide_08_gestures` |
| 09 | TouchDesigner runtime | `slide_09_touchdesigner` |
| 10 | Physical layer | `slide_10_physical` |
| 11 | Height slider 02.1 | `slide_11_slider` |
| 12 | Data layer | `slide_12_data` |
| 13 | Metrics engine | `slide_13_metrics` |
| 14 | Layout · empty | `slide_14_layout_empty` |
| 15 | Layout · roles | `slide_15_layout_roles` |
| 16 | Layout · annotated | `slide_16_layout_annotated` |
| 17 | Fabrication | `slide_17_fabrication` |
| 18 | Bibliography · Tier 1 sources + databases + standards | `slide_18_bibliography` |
| 19 | End | `slide_19_end` |

## Notes

- The demo video on slide 02 is embedded via `add_movie`. Opening the file outside PowerPoint may not preview the video poster; click slide 02 in PowerPoint slideshow mode to play.
- Diagram arrows use OOXML `tailEnd` triangles. Some converters (Google Slides import, Keynote import) may render arrows differently.
- Tables are native PPTX tables (slides 12 and 17), editable inline.

## Source of truth

The HTML deck at `../jury-deck/index.html` remains the canonical version. PPTX is a snapshot for jury / archive distribution. If content changes, edit both.
