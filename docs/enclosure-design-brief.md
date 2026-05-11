# ESP32 + RC522 Enclosure Design Brief

## Goal

Design a housing/enclosure for the ESP32 microcontroller and RC522 RFID reader
so they sit neatly instead of as naked hardware on the installation table.

## Hardware dimensions

- ESP32: ~51 × 25 × 7 mm
- RC522 RFID reader: ~60 × 40 × 5 mm

## Planned workflow

### Step 1 — Geometry (Rhino + Grasshopper)

Write a parametric GHPython script that builds the enclosure:
- Fully parametric — wall thickness, slot dimensions, tolerances adjustable
- Export STL for 3D printing
- I (Rafik) run it inside Rhino (already installed at IAAC)

### Step 2 — Render (Blender headless)

Write a Blender Python script that:
- Imports the STL or recreates the geometry
- Applies nice materials (matte plastic, subtle logo)
- Sets up product-shot lighting + camera
- Renders to PNG with no UI needed

Run from terminal: `blender --background --python render_enclosure.py`
Install Blender if needed: `winget install BlenderFoundation.Blender`

## Open questions (answer before starting)

1. 3D print for real OR just render for presentation — or both?
2. Aesthetic direction: match the installation (dark/architectural) or neutral/technical?
3. RFID reader access: top-open slot for tag tapping, or fully enclosed with a slit?

## When ready

Ask Claude to write:
- `cad/enclosure/enclosure.gh` — Grasshopper script
- `cad/enclosure/render_enclosure.py` — Blender render script
