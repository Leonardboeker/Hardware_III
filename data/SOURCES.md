# data/SOURCES.md

This file is the citation registry for every `source` key used in
`data/methods/*.csv`.

Expected entry format:

```text
source-key - full citation - tier - what this source underwrites
```

Example:

```text
bedec-2026 - ITeC Banco BEDEC 2025/2026 release - Tier 1 - Catalonia baseline for cost and material quantities
```

Notes:
- Every populated CSV row should point to a key that exists here.
- Keep keys lowercase and kebab-case.
- If a number is still unknown, use `source=NA` and `source_tier=missing` in the CSV instead of inventing a placeholder citation.
