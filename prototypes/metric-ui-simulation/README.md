# Metric UI Simulation

Local browser prototype for testing the metric-engine contract without touching TouchDesigner files.

## Setup

```bash
npm install
npm run dev
```

Expected local URL:

`http://localhost:5173`

## What It Simulates

- A fixed `1920 x 1080` projection canvas
- Absolute-positioned panel layout matching the current projection plan
- Method switching for `Masonry`, `3D Printed`, and `Prefab`
- Method-dependent floor selection with a local stepper control
- Phase navigation for phase-based methods
- Lifecycle-only behavior for prefab
- Interactive center-plan zone selection with single-select and `Shift + click` multi-select
- Geometry-driven mock metric updates
- Debug overlay toggle with the `D` key

## Layout Model

The prototype uses a browser wrapper that scales the internal `1920 x 1080` canvas to fit the window while preserving the original coordinate system.

Key panels include:

- `panel_left_info`
- `panel_top_phase_navigation`
- `panel_main_plan_simulation`
- `panel_right_comparison`
- `panel_prefab_lifecycle_card`
- `panel_right_cost_chart`
- `panel_left_assembly_sequence`
- `panel_method_selection`
- `panel_right_phase_preview`
- `bar_bottom_status`

The intended interaction order is:

1. Choose method
2. Set floors
3. Choose phase or lifecycle mode
4. Click building part

## Data Model Behavior

### Phase-Based

Used for:

- `Masonry`
- `3D Printed`

These keep the construction phase model:

- `foundation`
- `structure`
- `roof`
- `openings`
- `finishing`

Phase clicks update the visible metric bundle.

Each phase-based method also carries its own floor range assumptions:

- `Masonry`: 1-5 floors, default 2
- `3D Printed`: 1-2 floors, default 1

These are prototype assumptions for UI testing, not validated engineering limits.

### Lifecycle-Based

Used for:

- `Prefab`

Prefab intentionally stays lifecycle-based and does **not** get remapped into construction phases.

The right comparison panel is replaced by the prefab lifecycle card and uses:

- `A1-A3`
- `A4`
- `A5`
- `B`
- `C`

The lifecycle card includes:

- `Lifecycle-only dataset` badge
- CLT / Modular Concrete toggle
- active geometry basis display

Prefab floor limits depend on the selected prefab type:

- `CLT / Timber Prefab`: 1-8 floors, default 3
- `Modular Concrete Prefab`: 1-12 floors, default 4

These limits are also prototype assumptions and should later be replaced by
validated structural, regulatory, or fabrication constraints.

## Center Plan Zone Selection

The center simulation panel includes clickable zones:

- `zone_core`
- `zone_north_wing`
- `zone_south_wing`
- `zone_east_wing`
- `zone_west_wing`
- `zone_courtyard`
- `zone_facade_band`

Interaction:

- Single click selects one zone
- `Shift + click` toggles multi-selection
- Clicking empty plan area resets to whole-building mode

Metric scaling responds to:

- `total selected area`
- `wall surface`
- `boundary length`

With floor-aware geometry enabled, the simulation distinguishes:

- `Footprint Area`
- `Total Selected Area = footprint area x floor count`
- `Wall Surface = base wall surface x floor count`
- `Building Height = floor count x floor height`

## Metric Logic

The simulation uses mock local coefficients only.

Main files:

- [src/mockMetricData.ts](./src/mockMetricData.ts)
- [src/calculateMockMetrics.ts](./src/calculateMockMetrics.ts)

The mock calculator enforces:

- `kgCO2eq_per_m2_gfa` -> multiply by total selected area
- `kgCO2eq_per_m2_wall` -> multiply by wall surface
- `calendar_days` / `total_days` -> do **not** multiply by area
- `days_per_m2` -> multiply by total selected area

This keeps the simulation focused on UI layout, interaction logic, metric contract, prefab lifecycle behavior, and zone-based scaling.

The browser stepper stands in for a future physical floor-count input such as
RFID, a rotary selector, or another fabricated interaction device.

## TouchDesigner Safety

This prototype does **not** modify any TouchDesigner files.

Everything is isolated under:

`prototypes/metric-ui-simulation/`
