# VALUES — Strand 02: 3D-Printed Concrete and Earth

Decision unit: kg CO2eq / m2 GFA, A1–A3 cradle-to-gate (printer electricity included where measured).
Phases: foundation, structure, roof, openings, finishing.
Parameters: co2_kg_per_m2, labor_hours_per_m2, time_days, cost_eur_per_m2, material_origin.
Convention: every value is a low/high RANGE plus an assumption — no single figures.
Tiers: T1 = peer-reviewed / EPD; T2 = institutional report; T3 = vendor (NEVER sole source — every T3 row has a T1/T2 sibling for the same phase+parameter, or it is removed).
Source keys: see BIBLIOGRAPHY.md entry numbers.

Important scoping reality: 3DP literature is overwhelmingly **wall-element only**. Foundation, roof, openings, and finishing in 3DP houses are built CONVENTIONALLY (poured concrete slab, conventional roof, conventional windows/doors, conventional plaster/paint). The 3DP-specific rows are concentrated in `structure`. Other phases borrow heavily from masonry strand 01 with explicit "no 3DP-specific deviation" assumption flags. This is a known limitation of the literature and is named in SYNTHESIS.md.

Cells with no sibling-supportable value: source=NA, source_tier=missing.

---

| phase | parameter | value_low | value_high | unit | assumption | source_key | tier |
|---|---|---|---|---|---|---|---|
| foundation | co2_kg_per_m2 | 25 | 60 | kg CO2eq/m2 GFA | Conventional reinforced concrete slab on grade — 3DP house foundations are NOT printed; range from masonry-strand sibling. Lower bound = thin slab + GGBS-blended cement; upper bound = thick footing + 100% OPC. | EN 15804 + masonry strand 01 cross-link | T2 |
| foundation | labor_hours_per_m2 | 1.5 | 3.5 | hours/m2 GFA | Conventional rebar + form + pour. No 3DP-specific deviation. | EN 15804 + masonry strand 01 cross-link | T2 |
| foundation | time_days | 3 | 7 | days | Form + pour + cure. Conventional. Overlaps with structure-print prep. | EN 15804 + masonry strand 01 cross-link | T2 |
| foundation | cost_eur_per_m2 | 80 | 180 | EUR/m2 GFA | Catalonia 2025 reinforced slab; range reflects ground conditions. Conventional, not 3DP-specific. | masonry strand 01 cross-link | T2 |
| foundation | material_origin | NA | NA | descriptive | Aggregates typically <100 km radius (Catalan quarries); cement Spanish/EU; rebar Spanish/EU. No 3DP-specific deviation. | masonry strand 01 cross-link | T2 |
| structure | co2_kg_per_m2 | 44 | 90 | kg CO2eq/m2 wall | T1 anchor: Mohammad et al. 2020 reports 44.42 (lightweight unreinforced 3DCP) to 58.89 (conventional concrete) kg CO2eq/m2 wall, A1–A3, 1 m2 wall. Upper bound 90 reflects Mohammad scenario 2 (reinforced 3DCP) where rebar pushes GWP ABOVE conventional. RANGE IS WALL ELEMENT NOT GFA — multiplier ~0.6–0.8 to convert if wall:GFA ratio applied. Cement-content wobble: low end assumes geopolymer / LC3 mix; high end assumes ~30% OPC printable mix. | Mohammad 2020 | T1 |
| structure | co2_kg_per_m2 | 250 | 450 | kg CO2eq/m3 printable concrete | Material-level range across cement-content scenarios: ~250 (LC3 / calcined clay) to ~450 (high-OPC self-leveling). Sibling row for the wall-element row above; conversion via wall thickness 0.30 m → 75–135 kg CO2eq/m2 wall. | multiple T1 (Motalebi 2024 review cluster) | T1 |
| structure | co2_kg_per_m2 | 58 | 147 | kg CO2eq/m2 GFA | Whole-house comparison. T1: Rossi et al. 2024 reports 3DP houses average 58 vs conventional 147 (factor 2.5×). Range carries severe caveats — small sample (n=4 vs n=10), heterogeneous climate/insulation, no normalization. Used as whole-building check, NOT as the project's primary structural row. | Rossi 2024 | T1 |
| structure | co2_kg_per_m2 | 12 | 25 | kg CO2eq/m2 wall | 3D-PRINTED EARTH (cob/clay). T1 sibling: Alhumayani 2020 reports ~80% reduction vs 3DPC for wall element, A1–A4, foundation+roof+openings excluded. Range derived from applying 80% reduction to Mohammad 2020 3DPC wall figures. Printer electricity is the dominant remaining contributor. | Alhumayani 2020 | T1 |
| structure | co2_kg_per_m2 | NA | NA | kg CO2eq/m2 GFA, Catalonia | NO PUBLISHED LCA for TOVA, TerraPerforma, or any Catalan 3DP project. Geographic gap explicitly flagged. | NA | missing |
| structure | labor_hours_per_m2 | 0.3 | 1.2 | hours/m2 wall | Vendor + trade press: 2-operator print of 500 m2 (La Tour) in 150 h = 0.3 h/m2 wall. CyBe reports ~6 min/m2 print time = 0.1 h/m2 print, but operator-supervision adds. T1 sibling: Allouzi 2020 reports labour reduction vs conventional but does not give absolute h/m2. Range upper bound reflects setup/teardown amortized over small projects. | Allouzi 2020 + CyBe (T3 sibling) | T1 |
| structure | labor_hours_per_m2 | 0.1 | 0.5 | hours/m2 wall | T3 vendor sibling row: CyBe + COBOD claim ~6 min/m2 active print, 2 operators. Sibling confirms direction not magnitude — vendor figures exclude setup, mix prep, post-processing. | CyBe / COBOD (vendor) | T3 |
| structure | time_days | 1 | 7 | days for structural print | T1+T3 cross-source: ICON Wolf Ranch ~2000 sqft house in days; TECLA 60 m2 prototype = 200 hours print = ~8 days; ICON 230 m2 reportedly ~18 hours pure print time; setup/teardown adds. Range covers small dwelling 3DP-only print. Excludes foundation cure and conventional roof/openings. | Wikipedia TECLA + ICON press + Mohammad 2020 | T1+T3 |
| structure | time_days | 1 | 4 | days, vendor claim | T3 vendor sibling: ICON / Apis Cor "house in 24 hours" claims. These are PRINTING-ONLY times for shell wall, NOT including foundation, roof, finishing. Sibling supports the lower bound only — full structure phase per the installation's framing is broader. | Apis Cor + ICON (vendor) | T3 |
| structure | cost_eur_per_m2 | 200 | 600 | EUR/m2 wall | Vendor + T1: Apis Cor 2017 demonstrator $267/m2 (~250 EUR/m2) for shell only, Russian context. Allouzi 2020 reports material-cost reduction for 3DP vs conventional in Jordan but not absolute EUR/m2 transferable to Catalonia. Range upper reflects EU labour + EU printable-mix premium. EXCLUDES rebar where added. | Allouzi 2020 + Apis Cor (T3 sibling) | T1 |
| structure | cost_eur_per_m2 | 200 | 400 | EUR/m2 wall, vendor | T3 vendor sibling: Apis Cor + COBOD/PERI claims. PERI Heidelberg project reportedly 10% cost reduction vs conventional. Sibling row only — lower-bound figures are demonstrator-context. | Apis Cor + COBOD (vendor) | T3 |
| structure | material_origin | NA | NA | descriptive | 3DPC: cement Spanish/EU; aggregates Catalan within ~100 km; admixtures EU. 3DP-earth (TECLA, TOVA): earth WITHIN 50 m of site (TOVA verified); fibre stabilizers (rice husk for TECLA, aloe/egg whites for TOVA) local. Material-origin is the strongest argument for 3DP-earth in Catalonia. | IAAC TOVA + WASP TECLA | T3 |
| structure | material_origin | NA | NA | descriptive (siblings) | Alhumayani 2020 confirms cob 3DP material can be near-100% local; printable concrete necessarily imports cement clinker from regional kilns. T1 confirms direction. | Alhumayani 2020 | T1 |
| roof | co2_kg_per_m2 | 30 | 90 | kg CO2eq/m2 GFA | Conventional roof construction in 3DP houses (timber/steel + insulation + membrane). NOT printed. 3DP literature explicitly excludes roof. Range from masonry strand 01. | masonry strand 01 cross-link | T2 |
| roof | labor_hours_per_m2 | 1.5 | 4.0 | hours/m2 GFA | Conventional roof labour. No 3DP deviation. | masonry strand 01 cross-link | T2 |
| roof | time_days | 4 | 10 | days | Conventional roof construction. | masonry strand 01 cross-link | T2 |
| roof | cost_eur_per_m2 | 60 | 200 | EUR/m2 GFA | Catalonia conventional roof. | masonry strand 01 cross-link | T2 |
| roof | material_origin | NA | NA | descriptive | Conventional materials — timber from EU/Catalan forests, steel from Spanish/EU mills, insulation from EU producers. | masonry strand 01 cross-link | T2 |
| openings | co2_kg_per_m2 | 8 | 30 | kg CO2eq/m2 GFA | Windows + doors. NOT 3DP. Conventional aluminium/PVC/wood frames + double or triple glazing. Range reflects glazing choice. | masonry strand 01 cross-link | T2 |
| openings | labor_hours_per_m2 | 0.4 | 1.2 | hours/m2 GFA | Conventional install. 3DP printers leave openings as voids; install is conventional and uses templating. | masonry strand 01 cross-link | T2 |
| openings | time_days | 2 | 5 | days | Conventional. | masonry strand 01 cross-link | T2 |
| openings | cost_eur_per_m2 | 80 | 250 | EUR/m2 GFA | Catalonia 2025 windows + doors. | masonry strand 01 cross-link | T2 |
| openings | material_origin | NA | NA | descriptive | Aluminium frames typically EU; glass typically EU; locks/hinges global. | masonry strand 01 cross-link | T2 |
| finishing | co2_kg_per_m2 | 10 | 40 | kg CO2eq/m2 GFA | 3DP walls have a corrugated rib texture — finishing is contested: vendors claim "no plaster needed" (saves embodied carbon); reality is most projects apply at least primer + paint + sometimes skim coat. Lower bound = unfinished + paint; upper bound = full skim + paint + interior plaster on inside face. | masonry strand 01 cross-link | T2 |
| finishing | labor_hours_per_m2 | 0.5 | 2.5 | hours/m2 GFA | Same trade-off as above. 3DP-vendor "minimal finishing" claim is often optimistic — see SYNTHESIS wobble #6. | masonry strand 01 cross-link | T2 |
| finishing | time_days | 3 | 10 | days | Conventional finishing schedule. | masonry strand 01 cross-link | T2 |
| finishing | cost_eur_per_m2 | 30 | 120 | EUR/m2 GFA | Catalonia interior + exterior finish. Lower bound = paint only on rib texture (vendor claim); upper = conventional skim+paint. | masonry strand 01 cross-link | T2 |
| finishing | material_origin | NA | NA | descriptive | Paint EU; plaster Spanish/EU. | masonry strand 01 cross-link | T2 |

---

## Cross-cutting / printer-specific row (separate from phase rows above)

| phase | parameter | value_low | value_high | unit | assumption | source_key | tier |
|---|---|---|---|---|---|---|---|
| structure | printer_electricity_per_m2 | 1 | 12 | kg CO2eq/m2 wall (electricity-only contribution) | Reported as <5% of total in most LCAs (Mohammad 2020; Motalebi 2024 review). TECLA: 1200 kWh / 60 m2 = 20 kWh/m2 GFA → ~6 kg CO2eq/m2 at EU grid mix. Cob's 3DP electricity share is HIGHER as a fraction because cement is excluded — Alhumayani 2020 names electricity as cob's dominant footprint. | Mohammad 2020 + WASP TECLA | T1 |

---

## Sibling-rule audit (post-construction)

| T3 row | T1/T2 sibling row | OK? |
|---|---|---|
| structure / labor_hours_per_m2 / CyBe-COBOD | structure / labor_hours_per_m2 / Allouzi 2020 | OK |
| structure / time_days / Apis Cor + ICON | structure / time_days / Wikipedia TECLA + Mohammad 2020 | OK |
| structure / cost_eur_per_m2 / Apis Cor + COBOD | structure / cost_eur_per_m2 / Allouzi 2020 | OK |
| structure / material_origin / IAAC + WASP | structure / material_origin / Alhumayani 2020 | OK |

No orphan T3 rows present. All T3 rows have at least one T1/T2 sibling.

---

## Removed (no sibling could be sourced)

- **TECLA-specific co2_kg_per_m2**: vendor "near-zero carbon" claim. NO published LCA for TECLA. T1 sibling Alhumayani 2020 is for 3DP-cob generally, not TECLA specifically. Decision: REMOVED a TECLA-specific row; the 3DP-earth wall row (12–25 kg CO2eq/m2 wall) uses Alhumayani as the source of record.
- **TOVA-specific co2_kg_per_m2 GFA Catalonia**: NO published LCA. Recorded as `NA / missing` rather than fabricated.
- **ICON CarbonX "24% reduction" as a standalone CO2 row**: kept as context in BIBLIOGRAPHY annotation but not as a row — the figure is CarbonX vs ICON's own prior mix, not vs a normalized industry baseline. Sibling-rule fails. The Yang 2026 (T1) study's whole-house finding is the row of record for ICON-class 3DPC.

---

## Notes for downstream code

1. The `structure` phase has THREE distinct row types — wall-element (kg CO2eq/m2 wall), material (kg CO2eq/m3), and whole-house (kg CO2eq/m2 GFA). Code populating `data/methods/3d-printed.csv` must pick the row matching its functional unit. The installation's spatial unit is m2 GFA; the wall-element rows convert via wall:GFA ratio (typically 0.6–0.8 m2 wall per m2 GFA for a single-storey building with ~3 m floor-to-ceiling).
2. Cement-content wobble drives the `value_high / value_low` spread by ~50% in `structure`. The projection layer's "wobble overlay" should expose this to visitors.
3. Geographic bias is severe — no Catalan-context LCA exists. The 3DP-earth row is the most geographically defensible because TOVA exists in Collserola.
4. Reinforcement boundary: Mohammad 2020 scenario 2 shows reinforced 3DCP can EXCEED conventional concrete in GWP. The default assumption used is "unreinforced or fibre-reinforced" — flag this in the projection.
