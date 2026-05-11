# Metrics Engine Gaps

This note tracks what is already usable from `origin/treethreetree` and what still needs normalization before the final metrics engine can read the data safely.

## Imported Now

- `data/methods_db.json` has been updated with Rafik's richer metadata, confidence ranges, and shape-factor notes.
- Raw branch CSVs now live in `data/imports/treethreetree/`.
- Rafik's decision log is available at `.planning/phases/rafik-data-tasks.md`.

## Safe To Reuse Immediately

- Method descriptions, source labels, confidence ranges, and phase descriptions from `data/methods_db.json`
- Masonry raw data as the strongest Catalonia-anchored reference set
- Reclaimed-brick methodology notes as a baseline / wobble overlay source

## Not Engine-Ready Yet

### 1. Mixed phase models

- `masonry.csv` and `3d-printed.csv` use the project's five construction phases.
- `prefab.csv` does not. It is organized by lifecycle stages (`A1-A3`, `A4`, `A5`, `B`, `C`) plus `sub_method`.
- The current engine expects `foundation`, `structure`, `roof`, `openings`, `finishing`.

Needed:
- A clear mapping from lifecycle-stage prefab data into the project's phase-based UI model.
- A team decision on whether prefab should be shown as:
  - one merged method
  - CLT vs modular-concrete sub-modes
  - or a lifecycle-only comparison card outside the phase walkthrough

### 2. Mixed unit bases

- Several rows are not on the same basis:
  - `kg CO2eq / m2 GFA`
  - `kg CO2eq / m2 wall`
  - `kg CO2eq / m3`
  - total `calendar days`
- The current engine multiplies numeric rows by area, which only works for per-m2 values.

Needed:
- A normalization rule for wall-to-GFA conversions, especially in 3D-printed and reclaimed-brick structure rows.
- A separate rule for time values, because many imported `time_days` rows are total phase durations, not `days / m2`.

### 3. Extra columns and missing tokens

- `prefab.csv` has an extra `sub_method` column.
- `reclaimed-brick.csv` has an extra `allocation_rule` column.
- Raw files also use `NA`, which the current engine did not treat as missing until now.

Needed:
- A normalization pass before raw import files are moved into `data/methods/`.

### 4. Catalonia-specific gaps that still remain

- No peer-reviewed Catalan 3D-printing LCA in the imported data
- No Spanish/Catalan primary prefab phase dataset
- No Catalan primary reclaimed-brick cost/logistics dataset
- Prefab transport penalty to Barcelona exists in raw notes, but not yet translated into the project's five phases

### 5. Still missing for the final engine

- `data/SOURCES.md` needs real source-key entries for the imported CSV rows
- `selected_material` logic is still undefined in the current engine
- `selected_program`, `revenue_estimate`, and `profit_estimate` remain out of scope and should stay null unless the project expands
- A final decision is still needed on whether reclaimed brick stays a baseline-only overlay or becomes a fully comparable engine method

## Suggested Next Step

1. Normalize `masonry`, `3d-printed`, and `reclaimed-brick` into engine-safe CSVs under `data/methods/`.
2. Decide the prefab mapping strategy before building `data/methods/prefab.csv`.
3. Only then wire the engine away from dev fallbacks.

