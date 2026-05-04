# research_2 — Deep-Research Dispatch (2026-05-04)

Five parallel deep-research strands dispatched after Phase 2 plans landed and the **finger-tracking pivot** was locked. Each strand produces three artifacts in its own subdirectory:

- `BIBLIOGRAPHY.md` — annotated, primary-source-verified, tier-graded
- `VALUES.md` — extracted numerical ranges (low/high) with assumption + source + tier per cell
- `SYNTHESIS.md` — narrative + methodology wobbles + named biases + brief-revisit conclusion

## Strands

| # | Strand | Scope |
|---|--------|-------|
| 01 | Masonry | Catalan fired-clay block masonry, A1–A3 cradle-to-gate, all 5 phases × 5 parameters |
| 02 | 3D-printed | Concrete (ICON, Apis Cor, COBOD) + earth (TECLA, WASP), with cement-content + geometry wobbles |
| 03 | Prefab | Modular concrete (MiC) + mass-timber CLT, with biogenic-carbon + reuse-allocation wobbles |
| 04 | Reclaimed brick | Re:Crete + Halle 118 anchored; cut-off vs avoided-burden allocation surfaced |
| 05 | Animations + gesture | Hand-tracking interaction precedents (load-bearing post-pivot), AI animation tools, methodology-wobble visualization |

## Decision unit (applies to strands 01–04)

- **Spatial:** kg CO₂eq / m² of GFA, broken down per phase
- **Temporal:** A1–A3 cradle-to-gate; 2026 EUR for cost; hours/m² for labour
- **Methodological:** every value as a range (low, high) + named assumption text — no single figures
- **Geographic priority:** Catalonia ▸ Spain ▸ EU ▸ global (widest only when no regional source exists)

## Tiering (locked, do not renegotiate)

- **Tier 1:** peer-reviewed journal OR validated EPD (INIES / EPDItaly / EPD International) OR CYPE / BEDEC / ITeC for Catalan baseline
- **Tier 2:** government / institutional report (EU JRC, ITeC outside BEDEC, EPFL SXL Re:Crete, baubüro in situ Halle 118)
- **Tier 3:** vendor claim (Apis Cor, ICON, COBOD, TECLA WASP, modular brochures) — never as sole source for any cell; must have a Tier 1/2 sibling

## Iron rules (deep-research)

1. Every claim has a citation. No unsupported assertions.
2. No vibe-citing — every reference verified at primary source (DOI / publisher / institutional URL).
3. Gray zone = FAIL. If a citation cannot be confirmed, it does not appear.
4. Disclose contradictions — if sources disagree, report both with evidence-quality comparison.
5. Name biases as first-class findings — never "biases may exist", always the specific mechanism.

## Downstream consumers

- `data/methods/*.csv` populated by Plan 02-02 will read from each strand's `VALUES.md`.
- `data/SOURCES.md` will be merged from each strand's `BIBLIOGRAPHY.md`.
- Phase 4's methodology-wobble overlay reads the assumption text from `VALUES.md` rows — this is why ranges + named system boundaries are non-negotiable.
