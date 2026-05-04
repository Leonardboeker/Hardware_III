---
phase: 2
plan: 02
title: LCA data sourcing — Catalonia tier-1 + reclaimed brick baseline
owner: _TBD_
wave: 1
depends_on: []
files_modified:
  - data/methods/masonry.csv
  - data/methods/3d-printed.csv
  - data/methods/prefab.csv
  - data/methods/reclaimed-brick.csv
  - data/SOURCES.md
  - data/README.md
autonomous: false
requirements:
  - INP-02
estimated_effort_hours: 10
---

<objective>
Populate `data/methods/*.csv` with cradle-to-gate (A1–A3) embodied-carbon, labour-hours, time, cost, and material-origin values for the four comparator methods (masonry, 3D-printed concrete/earth, modular prefab, and reclaimed brick as the baseline). Every row carries an explicit `source` and `source_tier` annotation per the locked tiering rule (CONTEXT.md > Decisions > Data sourcing tiering). Numbers are stored as RANGES (`value_low`, `value_high`) plus `assumption` text so Phase 4's methodology-wobble overlay has the underlying data to draw from. This plan addresses INP-02 (input mapped to fabrication parameter — here, the LCA parameter that the projection layer will surface) by establishing the data corpus the runtime will read. Catalonia tier-1 sources (CYPE, BEDEC/ITeC, EPDs) are prioritised; vendor claims (Apis Cor, ICON, TECLA, COBOD, modular vendor brochures) MAY appear but only as Tier 3 with a Tier 1 or Tier 2 sibling row for triangulation. Reclaimed brick uses Re:Crete and Halle 118 as anchor cases.
</objective>

<must_haves>
- Four CSV files exist in `data/methods/`: `masonry.csv`, `3d-printed.csv`, `prefab.csv`, `reclaimed-brick.csv`.
- Each CSV uses the schema `phase,parameter,value_low,value_high,unit,assumption,source,source_tier` (header row matches exactly).
- Each CSV has rows covering ALL FIVE phases (foundation, structure, roof, openings, finishing) and ALL FIVE parameters (co2_kg_per_m2, labor_hours_per_m2, time_days, cost_eur_per_m2, material_origin) — i.e. up to 25 rows per method, with `value_low=value_high="UNKNOWN"` and `source_tier="missing"` allowed for cells where no defensible source was found in the time budget. Missing cells are explicit, not implicit.
- No row has a populated `value_low/value_high` without a populated `source` and `source_tier`.
- `data/SOURCES.md` exists and contains the full citation for every distinct `source` key used in any CSV (e.g. `bedec-2026`, `kupfer-2021-recrete`, `wang-2024-modular`, `cype-2026`, `findings-2024-3dp`, `liu-2021-clt`, `pomponi-2017-wobble`, etc.) with author/year/venue/DOI or URL.
- For every `source_tier=3` row in any CSV, the SAME `phase,parameter` pair has at least ONE OTHER row with `source_tier` 1 or 2 in the same CSV (the "triangulation rule" from CONTEXT.md — Tier 3 may appear but never alone). If no Tier 1/2 sibling can be sourced in the time budget, the Tier 3 row is REMOVED rather than left orphaned.
- The reclaimed-brick CSV anchors at minimum the two cases the lit review highlighted: Re:Crete pedestrian bridge (~1/3 the CO₂ of new RC; Küpfer et al. 2021) and Halle 118 (~60% GHG reduction; baubüro in situ 2021). Both as `source_tier=2`.
- `data/README.md` is updated so the schema, tiering rule, and triangulation rule are documented in-file (not only in CONTEXT.md). Link back to `data/SOURCES.md` and to `docs/research/lit-review/06-comparative-lca-and-museum-interactives.md`.
</must_haves>

<tasks>

<task type="auto">
  <name>Task 2.1: Update data/README.md with locked schema, tiering, triangulation rules</name>
  <action>Edit `data/README.md`. Replace its current "Format" and "Sourcing rule" sections with the following content (verbatim — these are the locked decisions from CONTEXT.md):

  ```markdown
  ## Schema (LOCKED 2026-05-03)

  All `data/methods/*.csv` files use this exact header:

  ```
  phase,parameter,value_low,value_high,unit,assumption,source,source_tier
  ```

  - `phase`: one of `foundation`, `structure`, `roof`, `openings`, `finishing`.
  - `parameter`: one of `co2_kg_per_m2`, `labor_hours_per_m2`, `time_days`, `cost_eur_per_m2`, `material_origin`.
  - `value_low`, `value_high`: numeric range. For string-valued parameters (`material_origin`), use the same string in both columns (e.g. `local`, `local`).
  - `unit`: SI or human-readable, e.g. `kg CO2eq/m2`, `hours/m2`, `days`, `EUR/m2`.
  - `assumption`: one-sentence note on system boundary, lifespan, biogenic carbon, functional unit, or grid mix that produced the range. NEVER blank when value is populated.
  - `source`: short citation key (e.g. `bedec-2026`, `kupfer-2021-recrete`). Must resolve in `data/SOURCES.md`.
  - `source_tier`: integer 1, 2, or 3 — see "Source tiering" below. Use the literal string `missing` when value cells are `UNKNOWN`.

  ## Source tiering (LOCKED 2026-05-03)

  - **Tier 1**: peer-reviewed journal article OR validated EPD registered with INIES, EPDItaly, or EPD International. CYPE, BEDEC (ITeC), and Spain-published EPDs count as Tier 1 for the Catalonia regional baseline.
  - **Tier 2**: government / institutional report (EU JRC, ITeC publications outside BEDEC, Re:Crete and Halle 118 case studies for reclaimed brick).
  - **Tier 3**: vendor claim (Apis Cor, ICON, COBOD, TECLA WASP, modular prefab manufacturers).

  ## Triangulation rule (LOCKED 2026-05-03)

  Tier 3 numbers may appear in any CSV but **never as the sole number for a method × phase × parameter cell**. Every Tier 3 datapoint must have at least one Tier 1 or Tier 2 sibling row in the same CSV for the same `phase,parameter` pair. Orphaned Tier 3 rows are removed.

  ## Missing data convention

  When no defensible source is found in the time budget, the row is still present with `value_low=value_high=UNKNOWN`, `source=NA`, `source_tier=missing`. Missing data is explicit, not implicit. Phase 4's methodology-wobble overlay reads these rows and shows them as "data gap" indicators rather than rendering blank chart space.

  ## See also

  - `data/SOURCES.md` — full citations for every `source` key used in any CSV.
  - `docs/research/lit-review/06-comparative-lca-and-museum-interactives.md` — the LCA backing literature.
  - `docs/research/lit-review/04-reuse-and-reclaimed-materials.md` — the reclaimed-brick baseline backing.
  - `.planning/phases/02-data-research-physical-model-design/02-CONTEXT.md` — the locked decisions this schema implements.
  ```

  Keep the existing "What goes here" section at the top. Do not delete anything from the README that is not in the "Format" / "Sourcing rule" sections.</action>
  <read_first>
    - data/README.md (current contents)
    - .planning/phases/02-data-research-physical-model-design/02-CONTEXT.md (decisions section, especially "Data sourcing tiering" and "Data store convention")
    - docs/research/lit-review/06-comparative-lca-and-museum-interactives.md "Methodological caveats" section
  </read_first>
  <acceptance_criteria>
    - `grep -c "phase,parameter,value_low,value_high,unit,assumption,source,source_tier" data/README.md` returns at least 1.
    - `grep -c "Tier 1" data/README.md` returns at least 1; same for "Tier 2" and "Tier 3".
    - `grep -c "Triangulation rule" data/README.md` returns at least 1.
    - `grep -c "UNKNOWN" data/README.md` returns at least 1 (missing-data convention is documented).
    - `grep -c "source_tier" data/README.md` returns at least 3.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 2.2: Build data/SOURCES.md citation registry</name>
  <action>Create `data/SOURCES.md` with one entry per distinct citation that will be used as a `source` key in any CSV in Task 2.3. At minimum include the keys listed below; add others as the data sourcing turns up new sources. For each entry, give: (a) the short key (one line, lowercase-kebab); (b) full author/year/title/venue; (c) DOI or URL; (d) tier (1/2/3); (e) one-sentence note on what kinds of figures it underwrites (e.g. "Catalan baseline for masonry; cite by ITeC item code on the projector").

  Required entries (start here, add as needed):

  ```
  - bedec-2026 — ITeC Banco BEDEC, 2025–2026 release. https://en.itec.cat/services/bedec/ — Tier 1. Catalan baseline for masonry, concrete, prefab modules. Cite by ITeC item code.
  - cype-2026 — CYPE Ingenieros generadores de precios construction database (Spain). http://www.generadordeprecios.info/ — Tier 1. Catalan baseline for cost (EUR/m2) and material quantities.
  - kupfer-2021-recrete — Küpfer, C., Bastien-Masse, M., Devènes, J., Fivet, C. (2021). Re:Crete Footbridge. EPFL SXL & Smart Living Lab, Fribourg. — Tier 2. Reclaimed concrete: ~1/3 CO2 of equivalent new RC; on par with glulam.
  - baubuero-2021-halle118 — baubüro in situ (2021). K.118 Kopfbau Halle 118, Winterthur. https://insitu.ch — Tier 2. Reclaimed components: ~60% GHG reduction at building scale; 500 t primary materials saved.
  - wang-2024-modular — Wang, X. et al. (2024). Comparative analysis of embodied carbon in modular and conventional construction methods in Hong Kong. Scientific Reports 14. https://www.nature.com/articles/s41598-024-73906-7 — Tier 1. Modular: ~6% lower than site-built initially; 20–26% lower with 25–50 yr second-life reuse.
  - sciencedirect-2026-3dp — On the sustainability of digital construction: Whole building life cycle carbon emissions according to three construction techniques. https://www.sciencedirect.com/science/article/abs/pii/S2352710226004845 — Tier 1. 3DPC: 10% lower than CMU, 5% lower than STF over 100 yr.
  - findings-2024-3dp — Comparison of Embodied Carbon of 3D-printed vs. Conventionally Built Houses. https://findingspress.org/article/89707 — Tier 1 (peer-reviewed but contested). 3DPC: 58 vs 147 kg CO2eq/m2 (~factor 2.5) — flag as upper-bound benefit only; cross-check mix design.
  - alhumayani-2020-cob — Alhumayani, H. et al. (2020). Environmental assessment of large-scale 3D printing in construction: A comparative study between cob and concrete. Journal of Cleaner Production. — Tier 1. 3DP cob walls: ~80% GWP reduction vs printed concrete (wall element only).
  - mohammad-2023-3dp-review — Mohammad, M. et al. (2023). A systematic review of life cycle assessments of 3D concrete printing. Cleaner Materials. — Tier 1. Meta-review establishing 3DCP claim sensitivity to cement content + reinforcement boundary.
  - liu-2021-clt — Liu, Y. et al. (2021). Comparative LCA of cross laminated timber building and concrete building with special focus on biogenic carbon. Energy & Buildings. — Tier 1. CLT: 46.5% lower GHG in production+construction (with biogenic).
  - hemmati-2024-mass-timber — Hemmati, M. et al. (2024). Comparison of Embodied Carbon Footprint of a Mass Timber Building. USDA Forest Products Lab / Buildings. — Tier 1. Mass timber: 198 kg CO2eq/m2 vs steel 243.
  - pomponi-2017-wobble — Pomponi, F., Moncaster, A. (2017). Scrutinising embodied carbon in buildings. Journal of Cleaner Production. https://www.sciencedirect.com/science/article/abs/pii/S136403211730998X — Tier 1. Methodological caveats; the methodology-wobble layer cites this for the caveat copy in Phase 4.
  - dewolf-2020-reuse-allocation — De Wolf, C., Hoxha, E., Fivet, C. (2020). Comparison of environmental assessment methods when reusing building components. Sustainable Cities and Society 61, 102322. — Tier 1. Reuse allocation rules; cite when displaying reclaimed-brick range to defend against "you cherry-picked the allocation".
  - tecla-2021-vendor — TECLA (Mario Cucinella Architects + WASP, 2021). 3D-printed earth house, Massa Lombarda. https://www.3dwasp.com/en/3d-printed-house-tecla/ — Tier 3 (vendor). 60 m2 shell, 200 hr print, ~6 kW draw. NEVER used as sole source for any cell.
  - apiscor-vendor — Apis Cor 3D printer vendor claims. https://www.apis-cor.com/ — Tier 3 (vendor). Use only for material_origin or print-rate context, never as sole CO2 source.
  - icon-vendor — ICON 3D printer vendor claims. https://www.iconbuild.com/ — Tier 3 (vendor). Same rule as Apis Cor.
  - cobod-vendor — COBOD 3D printer vendor claims. https://cobod.com/ — Tier 3 (vendor). Same rule.
  ```

  Add a header section explaining the file purpose, the tier definitions (one-line each, point at data/README.md for the full version), and the file format ("each entry: short-key — full citation — tier — what it underwrites").</action>
  <read_first>
    - docs/research/lit-review/06-comparative-lca-and-museum-interactives.md (the entire "Headline numbers the team can use" table)
    - docs/research/lit-review/04-reuse-and-reclaimed-materials.md (Re:Crete, Halle 118 entries)
    - docs/research/lit-review/OVERVIEW.md "Full reference list" section
    - .planning/phases/02-data-research-physical-model-design/02-CONTEXT.md "Data sourcing tiering"
  </read_first>
  <acceptance_criteria>
    - `data/SOURCES.md` exists.
    - `grep -c "Tier 1" data/SOURCES.md` returns at least 8 (we expect ≥8 Tier-1 sources).
    - `grep -c "Tier 2" data/SOURCES.md` returns at least 2 (Re:Crete + Halle 118 minimum).
    - `grep -c "Tier 3" data/SOURCES.md` returns at least 3 (TECLA + at least 2 of Apis Cor / ICON / COBOD).
    - The keys `bedec-2026`, `kupfer-2021-recrete`, `baubuero-2021-halle118`, `wang-2024-modular`, `pomponi-2017-wobble` are all present (these are the load-bearing keys for downstream CSVs).
    - Every entry has a URL or DOI on its line.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 2.3: Populate data/methods/masonry.csv with tier-annotated ranges</name>
  <action>Create `data/methods/masonry.csv`. Header row must be exactly `phase,parameter,value_low,value_high,unit,assumption,source,source_tier`. Then ONE row per (phase, parameter) combination — 5 phases × 5 parameters = 25 rows total. Where defensible numbers exist, populate; where they don't, use `UNKNOWN,UNKNOWN,...,NA,missing`.

  Populate at minimum these rows with real values from `data/SOURCES.md`:

  - `structure,co2_kg_per_m2`: range 150–250 kg CO2eq/m2 (Catalonia masonry baseline). Assumption: "fired clay block masonry, A1–A3 cradle-to-gate, BEDEC line items for fired clay 14 cm wall + interior plaster + mortar; reinforcement of lintels included; finishes excluded". Source: `bedec-2026`. Tier: 1.
  - `structure,co2_kg_per_m2` (sibling row for triangulation): range 165–210. Assumption: "CMU baseline used in 2026 ScienceDirect 3DPC comparison, Climate Zone 4A, 100-yr service life". Source: `sciencedirect-2026-3dp`. Tier: 1.
  - `structure,labor_hours_per_m2`: range 4–8 hours/m2. Assumption: "skilled mason + labourer, single-leaf wall, no openings, BEDEC time coefficient". Source: `bedec-2026`. Tier: 1.
  - `structure,cost_eur_per_m2`: range 80–140 EUR/m2. Assumption: "Catalonia 2026 generador de precios, fired clay block + mortar + labour, finishes excluded". Source: `cype-2026`. Tier: 1.
  - `structure,time_days`: range 0.05–0.10 days/m2. Assumption: "derived from labor_hours/8". Source: `cype-2026`. Tier: 1.
  - `structure,material_origin`: low=`local`, high=`local`. Assumption: "Catalan brick manufacturers within ~150 km of Barcelona; transport <0.5 kg CO2/m2". Source: `bedec-2026`. Tier: 1.

  - `foundation,co2_kg_per_m2`: range 30–60. Assumption: "RC strip footing, common to all comparators, A1–A3". Source: `bedec-2026`. Tier: 1.
  - `roof,co2_kg_per_m2`: UNKNOWN range, assumption "varies by typology — to be sourced once typology locked in Phase 3". Source: `NA`. Tier: `missing`.
  - `openings,co2_kg_per_m2`: range 8–15. Assumption: "double-glazed PVC window, 1.5 m2 average per opening, 1 opening per 10 m2 wall". Source: `bedec-2026`. Tier: 1.
  - `finishing,co2_kg_per_m2`: range 12–25. Assumption: "interior gypsum plaster + paint + exterior render". Source: `bedec-2026`. Tier: 1.

  Fill the remaining (phase, parameter) cells with `UNKNOWN` rows using the convention in 2.1. Total: exactly 25 data rows + 1 header row.

  IMPORTANT: where you cite `bedec-2026`, leave a one-line `assumption` text that names the BEDEC item-code family (e.g. "BEDEC E612... fired clay block 14 cm"). Exact item codes are nice-to-have not load-bearing — if you can't find them in 30 min of searching, use the family name.</action>
  <read_first>
    - data/README.md (after Task 2.1 update)
    - data/SOURCES.md (after Task 2.2 — to know which keys are valid)
    - docs/research/lit-review/06-comparative-lca-and-museum-interactives.md "Headline numbers" table
  </read_first>
  <acceptance_criteria>
    - `data/methods/masonry.csv` exists.
    - First line is exactly `phase,parameter,value_low,value_high,unit,assumption,source,source_tier`.
    - File has exactly 26 lines (1 header + 25 data rows = 5 phases × 5 parameters).
    - Every row whose `value_low` is NOT `UNKNOWN` has a non-empty `assumption` AND a `source` that resolves in `data/SOURCES.md` AND a numeric (1, 2, 3) `source_tier`.
    - Every row whose `value_low` IS `UNKNOWN` has `source=NA` AND `source_tier=missing`.
    - At least 8 of the 25 rows have populated (non-UNKNOWN) values.
    - No row has `source_tier=3` (masonry CSV uses tier 1 sources only — vendor claims don't apply to masonry).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 2.4: Populate data/methods/3d-printed.csv with triangulated tier-annotated ranges</name>
  <action>Create `data/methods/3d-printed.csv` with the same schema as masonry. 5 phases × 5 parameters = 25 rows + 1 header.

  Critical: 3DP is the method where vendor (Tier 3) claims are most likely to leak into the data. Apply the triangulation rule strictly — every Tier 3 row must have a Tier 1 or Tier 2 sibling row for the same (phase, parameter) pair, OR the Tier 3 row is removed.

  Populate at minimum:

  - `structure,co2_kg_per_m2`: range 60–150. Assumption: "3DPC wall, A1–A3 cradle-to-gate, includes printable concrete mix (high-OPC) + steel mesh reinforcement; geometry not optimised; 100-yr service life". Source: `sciencedirect-2026-3dp`. Tier: 1.
  - `structure,co2_kg_per_m2` (sibling, optimistic): range 50–80. Assumption: "Findings 2024 headline 58 kg CO2eq/m2 — geometry-optimised low-cement printable mix; treat as upper-bound benefit". Source: `findings-2024-3dp`. Tier: 1.
  - `structure,co2_kg_per_m2` (sibling, cob/earth): range 30–60. Assumption: "3DP cob/earth wall, ~80% reduction vs printed concrete on wall element only — does NOT include foundation/roof/openings". Source: `alhumayani-2020-cob`. Tier: 1.
  - `structure,co2_kg_per_m2` (Tier 3 vendor sibling — only valid because Tier 1 siblings exist): range 30–50. Assumption: "TECLA earth printer marketing material; 200 hr print time, ~6 kW draw, local-soil mix; NOT peer-reviewed; included for projection-overlay debate value only". Source: `tecla-2021-vendor`. Tier: 3.
  - `structure,labor_hours_per_m2`: range 0.5–2 hours/m2. Assumption: "1 operator monitoring printer + 1 finishing labourer, includes setup time; printer cycle dominates not labour". Source: `mohammad-2023-3dp-review`. Tier: 1.
  - `structure,time_days`: range 0.02–0.10 days/m2. Assumption: "200 hr print for TECLA 60 m2 shell = ~3.3 hr/m2 = ~0.14 days at 24-hr printing; comparable for ICON Vulcan". Source: `tecla-2021-vendor`. Tier: 3.
  - `structure,time_days` (Tier 1 sibling for triangulation): range 0.03–0.15 days/m2. Assumption: "derived from Mohammad 2023 meta-review of 3DCP printing rates 0.5–2 m3/hr at typical wall thicknesses". Source: `mohammad-2023-3dp-review`. Tier: 1.
  - `structure,cost_eur_per_m2`: UNKNOWN range. Assumption: "vendor cost claims (50% cheaper) do not survive scrutiny per lit-review; no Catalan defensible figure available". Source: `NA`. Tier: `missing`.
  - `structure,material_origin`: low=`local`, high=`global`. Assumption: "earth printers (TECLA) use local soil; concrete printers (ICON, Apis Cor) use industrial mix often sourced regionally; printer hardware itself is imported". Source: `tecla-2021-vendor`. Tier: 3.
  - `structure,material_origin` (Tier 1 sibling): low=`regional`, high=`regional`. Assumption: "concrete printable mix typically sourced within ~200 km of print site per industry practice". Source: `mohammad-2023-3dp-review`. Tier: 1.

  - `foundation,co2_kg_per_m2`: range 30–60 (same as masonry; foundation is method-agnostic for these comparators). Source: `bedec-2026`. Tier: 1.
  - `roof,co2_kg_per_m2`: UNKNOWN. Assumption: "TECLA-style closed-shell roofs vs hybrid timber roofs not yet sourced; 3DPC roof is rare and unstable in literature". Source: `NA`. Tier: `missing`.
  - `openings,co2_kg_per_m2`: range 8–15 (same as masonry). Source: `bedec-2026`. Tier: 1.
  - `finishing,co2_kg_per_m2`: UNKNOWN. Assumption: "3DP wall surface texture is sometimes left exposed (no finishing) and sometimes plastered like masonry — depends on architectural choice". Source: `NA`. Tier: `missing`.

  Fill remaining cells with UNKNOWN rows. Validate the triangulation rule: every Tier 3 row has a Tier 1/2 sibling for the same (phase, parameter). If you cannot find a sibling for a Tier 3 row, remove the Tier 3 row.</action>
  <read_first>
    - data/README.md
    - data/SOURCES.md
    - docs/research/lit-review/06-comparative-lca-and-museum-interactives.md (entire Part A)
    - docs/research/lit-review/OVERVIEW.md TL;DR item 3 ("the numbers are unstable")
  </read_first>
  <acceptance_criteria>
    - `data/methods/3d-printed.csv` exists.
    - First line is exactly `phase,parameter,value_low,value_high,unit,assumption,source,source_tier`.
    - File has at minimum 26 lines (1 header + 25 data rows; sibling rows for same phase/parameter pair add additional rows — total may be larger).
    - At least 3 rows have `source_tier=1`.
    - Every row with `source_tier=3` has at least one OTHER row in the same file with the same `(phase,parameter)` and `source_tier` 1 or 2 (verify by sort/uniq on the first two columns).
    - `grep -c "tecla-2021-vendor" data/methods/3d-printed.csv` returns at most 3 (vendor sources are sparse).
    - `grep -c "UNKNOWN" data/methods/3d-printed.csv` returns at least 5 (we expect significant data gaps for 3DP).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 2.5: Populate data/methods/prefab.csv with modular construction ranges</name>
  <action>Create `data/methods/prefab.csv`. Modular prefab covers concrete volumetric (MiC) AND mass-timber CLT panel construction, since both qualify under "prefab" in this installation's framing. Use Wang 2024 (Sci Reports) for modular concrete, Liu 2021 + Hemmati 2024 for CLT.

  Populate at minimum:

  - `structure,co2_kg_per_m2`: range 130–200. Assumption: "concrete volumetric modular (MiC), high-rise residential, Hong Kong study; ~6% lower than site-built initial; biogenic carbon excluded". Source: `wang-2024-modular`. Tier: 1.
  - `structure,co2_kg_per_m2` (sibling — CLT alternative): range 150–200. Assumption: "mass timber / CLT building (Hemmati 2024 cites 198 kg CO2eq/m2 mean); biogenic carbon INCLUDED — strip biogenic and value rises ~30%". Source: `hemmati-2024-mass-timber`. Tier: 1.
  - `structure,co2_kg_per_m2` (sibling — CLT with reuse scenario): range 100–160. Assumption: "modular with 25–50 yr second-life reuse: 20–26% lower annual emissions per Wang 2024 — REUSE is the lever, not prefabrication itself". Source: `wang-2024-modular`. Tier: 1.
  - `structure,labor_hours_per_m2`: range 1–3. Assumption: "factory + onsite assembly combined; factory hours allocated per m2 of finished module". Source: `wang-2024-modular`. Tier: 1.
  - `structure,time_days`: range 0.01–0.05 days/m2 onsite (factory time excluded). Assumption: "onsite installation rate of pre-built modules; factory production parallel and not on critical path". Source: `wang-2024-modular`. Tier: 1.
  - `structure,cost_eur_per_m2`: UNKNOWN. Assumption: "modular cost data is patchy and not Catalonia-specific; vendor brochures only". Source: `NA`. Tier: `missing`.
  - `structure,material_origin`: low=`regional`, high=`global`. Assumption: "Catalan modular suppliers exist; CLT often imported from Austria/Germany/Sweden". Source: `wang-2024-modular`. Tier: 1.

  - `foundation,co2_kg_per_m2`: range 30–60 (same as other methods). Source: `bedec-2026`. Tier: 1.
  - `roof,co2_kg_per_m2`: range 20–50. Assumption: "factory-assembled roof module included in volumetric MiC; CLT roof panels lower bound, concrete-deck modular roof upper bound". Source: `liu-2021-clt`. Tier: 1.
  - `openings,co2_kg_per_m2`: range 8–15 (same as masonry — openings are method-agnostic). Source: `bedec-2026`. Tier: 1.
  - `finishing,co2_kg_per_m2`: range 10–20. Assumption: "factory-applied interior finish; lower than site-applied finish for same m2 due to reduced waste". Source: `liu-2021-clt`. Tier: 1.

  Fill remaining cells with UNKNOWN rows.</action>
  <read_first>
    - data/README.md
    - data/SOURCES.md
    - docs/research/lit-review/06-comparative-lca-and-museum-interactives.md (Wang 2024, Liu 2021, Hemmati 2024 entries)
    - docs/research/lit-review/OVERVIEW.md "Cross-cutting themes" item 5 ("Reuse and lifespan dominate")
  </read_first>
  <acceptance_criteria>
    - `data/methods/prefab.csv` exists.
    - First line is exactly `phase,parameter,value_low,value_high,unit,assumption,source,source_tier`.
    - File has at minimum 26 lines.
    - At least 6 rows have `source_tier=1`.
    - No row has `source_tier=3` (no defensible vendor-only data goes here without a sibling).
    - At least one row's `assumption` mentions either "biogenic" OR "reuse" OR "lifespan" — these are the load-bearing methodology levers per the lit review.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 2.6: Populate data/methods/reclaimed-brick.csv as the baseline floor</name>
  <action>Create `data/methods/reclaimed-brick.csv`. Per locked decision #3, reclaimed brick is the BASELINE the other methods are measured against — not a fourth competitor. The Phase 5 comparison view (and Phase 4's wobble layer) read this file to draw the "floor" line.

  Populate at minimum:

  - `structure,co2_kg_per_m2`: range 30–80. Assumption: "reclaimed brick re-laid with new mortar; A1–A3 production burden allocated to the FIRST life (cut-off allocation per De Wolf 2020); transport from urban-mining yard <50 km; mortar A1–A3 included; reuse of brick avoids the ~70% of cradle-to-gate emissions associated with firing". Source: `kupfer-2021-recrete`. Tier: 2.
  - `structure,co2_kg_per_m2` (sibling — alt allocation): range 50–110. Assumption: "same reuse scenario but with avoided-burden allocation (split between first and second life); methodology choice swings result by ~50%". Source: `dewolf-2020-reuse-allocation`. Tier: 1.
  - `structure,co2_kg_per_m2` (sibling — Halle 118 building-scale anchor): range 60–100. Assumption: "Halle 118 reported ~60% GHG reduction at building scale; back-calculated to per-m2 GFA assuming new-build baseline ~200 kg CO2eq/m2". Source: `baubuero-2021-halle118`. Tier: 2.
  - `structure,labor_hours_per_m2`: range 8–16 hours/m2. Assumption: "reclaimed brick requires hand-cleaning of old mortar before re-laying; 2x to 4x labour of new brick masonry per insitu.ch and Brütting 2019 stock-matching framework". Source: `baubuero-2021-halle118`. Tier: 2.
  - `structure,time_days`: range 0.10–0.20 days/m2. Assumption: "derived from labour_hours/8; 2-4x slower than new masonry due to cleaning and stock-matching". Source: `baubuero-2021-halle118`. Tier: 2.
  - `structure,cost_eur_per_m2`: UNKNOWN. Assumption: "Catalan reclaimed-brick cost depends on stock availability and demolition-source distance; no defensible regional figure located. Concular/Restado data is German market.". Source: `NA`. Tier: `missing`.
  - `structure,material_origin`: low=`local`, high=`local`. Assumption: "by definition the value of reuse comes from local urban mining; transport >100 km erases most carbon advantage per De Wolf 2020". Source: `dewolf-2020-reuse-allocation`. Tier: 1.

  - `foundation,co2_kg_per_m2`: range 30–60. Same as other methods (foundations are typically NOT reclaimed at this scale; same RC footing). Source: `bedec-2026`. Tier: 1.
  - `roof,co2_kg_per_m2`: UNKNOWN. Assumption: "reclaimed-brick vault roofs exist but rare; pair with Re:Crete arch precedent in Phase 5 visualization layer". Source: `NA`. Tier: `missing`.
  - `openings,co2_kg_per_m2`: range 8–15 (same as masonry — openings are method-agnostic). Source: `bedec-2026`. Tier: 1.
  - `finishing,co2_kg_per_m2`: range 5–15. Assumption: "reclaimed brick often left exposed (no plaster) for aesthetic + provenance display reasons; lower than masonry finishing". Source: `baubuero-2021-halle118`. Tier: 2.

  Fill remaining cells with UNKNOWN rows.

  IMPORTANT: leave a comment row at the top of the file (after the header) like this — this CSV has a load-bearing role in the comparison view:

  ```
  # phase,parameter,value_low,value_high,unit,assumption,source,source_tier
  # NOTE: this CSV is the BASELINE FLOOR. Phase 5 comparison view plots all other methods relative to these values per locked decision #3 (CONTRIBUTING.md).
  ```

  CSV parsers must skip these lines — use a leading `#` and ensure parsing code is comment-aware. (Standard Python csv module skips them via `csv.reader` with a custom filter; document this expectation in `data/README.md` Task 2.1 if needed.)</action>
  <read_first>
    - data/README.md
    - data/SOURCES.md
    - docs/research/lit-review/04-reuse-and-reclaimed-materials.md (Re:Crete, Halle 118, De Wolf entries; "The 4th method question" section)
    - docs/research/lit-review/OVERVIEW.md "The fourth method question" section
    - .planning/phases/02-data-research-physical-model-design/02-CONTEXT.md "Specific Re:Crete + Halle 118 numbers"
  </read_first>
  <acceptance_criteria>
    - `data/methods/reclaimed-brick.csv` exists.
    - File contains a comment row referencing locked decision #3.
    - First non-comment line is exactly `phase,parameter,value_low,value_high,unit,assumption,source,source_tier`.
    - File has at minimum 26 data rows.
    - The `kupfer-2021-recrete` and `baubuero-2021-halle118` source keys appear at least once each (the two anchor cases per CONTEXT.md "Specifics").
    - At least 4 rows have `source_tier=2` and at least 2 rows have `source_tier=1`.
    - No row has `source_tier=3` (vendor data is meaningless for reclaimed material).
  </acceptance_criteria>
</task>

</tasks>

<verification>
- All four `data/methods/*.csv` files exist.
- For each file: `head -1` returns exactly `phase,parameter,value_low,value_high,unit,assumption,source,source_tier`.
- For each file: row count is at least 26 (1 header + 25 phase × parameter combinations).
- `data/SOURCES.md` exists and contains all distinct `source` keys used in any CSV.
- Triangulation rule check: every row in every CSV with `source_tier=3` has at least one OTHER row in the SAME csv with the same `(phase,parameter)` first-two-fields and `source_tier` in {1, 2}. (Verify by Python script: read each csv, group by (phase, parameter), within each group if any tier=3 then must exist tier in {1,2}.)
- `data/README.md` documents the schema, tiering, and triangulation rule (verify with grep for the strings "phase,parameter,value_low", "Tier 1", "Tier 2", "Tier 3", "Triangulation").
- `data/methods/reclaimed-brick.csv` references both Re:Crete (`kupfer-2021-recrete`) and Halle 118 (`baubuero-2021-halle118`).
</verification>
