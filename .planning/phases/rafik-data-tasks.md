# Rafik - Person 6 Data Tasks
**Role:** Data Research + Narrative Owner
**Deadline:** Finals May 22, 2026
**File to populate:** `data/methods_db.json`

---

## STATUS KEY
- [ ] = open
- [x] = resolved
- [~] = deferred

---

## Block 1 - Schema & Methods Foundation

- [~] **T1** Fix the methods: confirm the 4 construction methods - DEFERRED (team-level decision, already locked in proposal: Masonry, 3D Printed, Prefab/CLT, Reclaimed Brick)
- [x] **T2** Define the data schema: what fields does each method entry need beyond what's there (id, name, color, puck counts)?
- [x] **T3** Decide data format: ranges (min/max) or single values + margin? And how to encode source tier?

---

## Block 2 - CSV Population (research already done, transcribe it)
Source: docs/research_2/ strands. Schema: phase, parameter, value_low, value_high, unit, assumption, source, source_tier

- [x] **T4** Populate data/methods/masonry.csv from strand 01 (Hispalyt EPDs + BEDEC + CYPE - strong Catalan data)
- [x] **T5** Populate data/methods/3d-printed.csv from strand 02 (global sources, flag geographic gap, include 7 wobbles)
- [x] **T6** Populate data/methods/prefab.csv from strand 03 (Austrian/Swedish CLT EPDs + HK modular, flag transport penalty)
- [x] **T7** Populate data/methods/reclaimed-brick.csv from strand 04 (Swiss/Finnish sources, flag as EU proxy, baseline not competitor)

---

## Block 3 - methods_db.json Update

- [x] **T8** Replace wrong methods (Cantilever/Arch/Truss) with real ones + add LCA summary fields per method

---

## Block 4 - Narrative Layer

- [x] **T9** Masonry description: scientific, neutral, factual
- [x] **T10** 3D Printed description (include honest flag: no local data)
- [x] **T11** Prefab/CLT description
- [x] **T12** Reclaimed Brick description (honest baseline, CO2 accounting swing flagged)
- [x] **T13** 5 phase texts: Foundation, Structure, Roof, Openings, Finishing (one line each)
- [x] **T14** Final comparison insight: what should the visitor feel after the comparison?

---

## Decisions Log

### T1 - Methods - DEFERRED 2026-05-09
**Decision:** Not Rafik's call. Already locked in proposal: Masonry, 3D Printed Concrete, Prefab/CLT, Reclaimed Brick.
**Reasoning:** Team-level decision made at proposal stage. Rafik researches data FOR these methods.

### T2 - Data Schema - RESOLVED 2026-05-09
**Decision:** 5 fields per method: `cost_per_m2_range`, `co2_per_m2_range`, `labor_hours_range`, `time_range`, `source_label`. Plus `description` for narrative.
**Reasoning:** Already defined in INTERFACE_CONTRACT.md on master. No need to redesign.

### T3 - Data Format - RESOLVED 2026-05-09
**Decision:** Ranges (min-max string e.g. "280-420 kgCO2e/m2") + source_label string. Already the contract spec.
**Reasoning:** INTERFACE_CONTRACT.md already has placeholder rows in this format. Rafik fills real values into the same shape.
**Deferred:** Reclaimed Brick has no placeholder row yet - Rafik adds it.
