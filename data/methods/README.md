# data/methods/

Drop the per-method metrics CSV files here.

Expected filenames:
- `masonry.csv`
- `3d-printed.csv`
- `prefab.csv`
- `reclaimed-brick.csv`

Required header for every file:

```text
phase,parameter,value_low,value_high,unit,assumption,source,source_tier
```

The metrics engine starter at
[metrics_engine.py](/o:/Hardware_III/touchdesigner/scripts/metrics_engine.py)
reads this folder directly.
