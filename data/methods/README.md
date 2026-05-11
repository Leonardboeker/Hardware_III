# data/methods/

This folder now stores the normalized, engine-safe metrics datasets.

Expected filenames:
- `masonry.csv`
- `3d-printed.csv`
- `prefab.csv`
- `reclaimed-brick.csv`

Unified normalized header:

```text
method,data_model,display_mode,phase,lifecycle_stage,sub_method,metric,value_low,value_high,unit,basis,source_key,confidence_min,confidence_max,selected_material,notes,metadata
```

Model notes:
- `masonry` and `3d-printed` are `phase_based`
- `prefab` is `lifecycle_based`
- `reclaimed-brick` is `overlay`

Do not edit raw imported CSVs here.
Those stay under:

```text
data/imports/treethreetree/
```

The standalone normalization and engine pipeline lives in:

```text
metrics/pipeline.py
```
