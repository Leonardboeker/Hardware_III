# cad/rhino/

Rhino + Grasshopper files — used **only for offline geometry authoring** of the
physical parts (puck shape, method-selector models, table mock-up, fabrication
support geometry).

The interactive runtime (FSM, vision, projection) lives in TouchDesigner +
Python, not in Grasshopper. See [`INTERFACE_CONTRACT.md`](../../INTERFACE_CONTRACT.md)
for the system-level data flow.

## What lives here

- `.3dm` Rhino source files
- `.gh` / `.ghx` Grasshopper definitions (parametric geometry only)
- GHPython / C# scripts referenced by those definitions

STL exports go in `cad/` (one level up) so they sit next to the other print files.

## Conventions

- Name files by content, not by date: `puck-aruco.gh`, not `final_v3_REAL.gh`
- Prefer `.ghx` (XML, diffable) over `.gh` (binary) for source-of-truth definitions
- Document expected inputs in a comment cluster top-left of the canvas
- Heavy reference geometry → `media/` or external storage, not here
