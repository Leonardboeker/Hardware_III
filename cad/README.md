# cad/

Print-ready 3D files for the physical components.

## Inventory

- 3 method-selector models (masonry, 3DP, prefab) — go on the RFID pedestal
- 10 ArUco footprint pucks (circular, ~Ø50mm — confirm)
- 1 height marker (physically distinct shape)
- 1 material controller (physically distinct shape)
- RFID pedestal housing
- Camera mount (if needed)

## Conventions

- Track the **source** file (`.3dm`, `.f3d`, `.step`) AND the export (`.stl`).
- Name pattern: `<part>-v<n>.stl`, e.g., `puck-aruco-v2.stl`. Bump the version when the print result changes.
- Print settings (layer height, infill, supports) → put them in a sibling `.md` next to the STL or in this README's print log below.

## Print log

| Part | Version | Printed by | Date | Notes |
|---|---|---|---|---|
| _e.g. puck-aruco-v1_ | _v1_ | _name_ | _YYYY-MM-DD_ | _result_ |
