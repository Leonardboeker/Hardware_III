# data/

LCA datasets and any structured data the runtime reads.

## What goes here

- Per-method, per-phase datasets: CO2, labor hours, cost, time, material quantity
- Regional logistics data (Catalonia focus)
- Real-world equivalents lookup (e.g. "X tons of wood = Y trees")

## Schema

CSV remains the preferred format because it diffs cleanly and can be read by the
standalone metrics pipeline without extra dependencies.

Raw imported files live under:

```text
data/imports/treethreetree/
```

Normalized engine-safe files live under:

```text
data/methods/
```

The normalized pipeline uses this unified header:

```text
method,data_model,display_mode,phase,lifecycle_stage,sub_method,metric,value_low,value_high,unit,basis,source_key,confidence_min,confidence_max,selected_material,notes,metadata
```

Field rules:
- `phase`: one of `foundation`, `structure`, `roof`, `openings`, `finishing`
- `parameter`: one of `co2_kg_per_m2`, `labor_hours_per_m2`, `time_days`, `cost_eur_per_m2`, `material_origin`
- `value_low`, `value_high`: numeric range for measurable values, or the same string twice for labels such as `material_origin`
- `unit`: e.g. `kg CO2eq/m2`, `hours/m2`, `days`, `EUR/m2`, or `label`
- `assumption`: one short note explaining the boundary or modeling assumption
- `source`: citation key that resolves in `data/SOURCES.md`
- `source_tier`: `1`, `2`, `3`, or `missing`

The planned runtime files are:

```text
methods/
  masonry.csv
  3d-printed.csv
  prefab.csv
  reclaimed-brick.csv
logistics/
  catalonia-transport.csv
equivalents.csv
```

## Source tiers

- `1`: peer-reviewed paper, EPD, or validated regional database
- `2`: institutional or case-study source
- `3`: vendor claim, allowed only when triangulated against Tier 1 or 2
- `missing`: explicit placeholder when the team does not yet have a defensible number

## Missing-data convention

Missing values should be explicit, not silent.

If a row is not ready yet, still include it with `null` in normalized data or
the raw import placeholders in `data/imports/treethreetree/`.

Raw-import placeholders may still use:

```text
value_low=UNKNOWN
value_high=UNKNOWN
source=NA
source_tier=missing
```

This lets the metrics engine return partial results and "data gap" warnings
instead of faking precision.

## CSV comments

The metrics engine ignores lines beginning with `#`.
This is useful for method-level notes such as the reclaimed-brick baseline note.

## Standalone pipeline

The current normalization and engine code is intentionally separate from
TouchDesigner:

```text
metrics/pipeline.py
data/normalization_rules.json
```

## Sourcing rule

Every populated value needs a source. Unsourced numbers should be treated as
temporary development placeholders only and removed before the final demo.
