# data/

LCA datasets and any structured data the runtime reads.

## What goes here

- Per-method, per-phase datasets: CO₂/ton, labor hours, cost, time, material qty
- Regional logistics data (Catalonia focus)
- Real-world equivalents lookup (e.g., "X tons of wood = Y trees")

## Format

CSV preferred — diffs cleanly, opens anywhere. JSON only if there's nested structure.

Suggested files:
```
methods/
├── masonry.csv
├── 3d-printed.csv
└── prefab.csv
phases/
└── phase-templates.csv      # the ~5 phases per method
logistics/
└── catalonia-transport.csv
equivalents.csv              # wood→trees, concrete→cars, etc.
```

## Sourcing rule

Every row needs a source. Add a `source` column with a citation key that matches a file in `docs/research/`. Numbers without sources get pulled before the final demo.
