# rhino-gh/

Rhino models and Grasshopper definitions — the parametric geometry side of the project.

## What lives here

- `.3dm` Rhino files (geometry of the three method models, the table mock-up, anything we 3D print)
- `.gh` / `.ghx` Grasshopper definitions (parametric building generation per method)
- Any GHPython / C# scripts referenced by the GH definitions

## Conventions

- Name files by what they contain, not by date: `prefab-module-generator.gh`, not `final_v3_REAL.gh`.
- `.gh` is binary, `.ghx` is XML. `.ghx` diffs better — prefer it for source-of-truth versions, export `.gh` for performance if needed.
- Document the inputs each definition expects in a comment cluster at the top-left of the canvas.
- Heavy reference geometry → `media/` or external storage, not here.
