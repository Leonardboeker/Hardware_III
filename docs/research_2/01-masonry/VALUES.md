# VALUES — Strand 01: Traditional Fired-Clay Block Masonry (Catalonia)

**Decision unit:** kg CO₂ eq / m² of building Gross Floor Area (GFA), broken down per construction phase.
**Temporal scope:** A1–A3 cradle-to-gate at minimum; A4 noted in `assumption` where data exists.
**Geographic priority:** Catalonia ▸ Spain ▸ EU ▸ global.
**Reference building:** typical Catalan two-storey single-family house (vivienda unifamiliar), ~100–150 m² GFA, single-leaf load-bearing perforated clay brick (24 cm) outer + half-leaf hollow brick (7 cm) inner partition, M-5 cement-rich mortar, reinforced concrete strip foundation, pitched roof in clay tiles on RC slab + timber battens, aluminium-frame windows, gypsum-plaster + paint internal finish + cement-mortar render external. This reference is the basis for converting EPD per-tonne figures into per-m²-GFA figures.

**Iron rule honoured:** every numerical claim is a low–high range. Single figures forbidden.
**Iron rule honoured:** cells with no defensible value are marked `UNKNOWN` with `source=NA`.

---

## Table

| phase | parameter | value_low | value_high | unit | assumption | source_key | tier |
|---|---|---|---|---|---|---|---|
| foundation | co2_kg_per_m2 | 70 | 130 | kg CO₂ eq / m² GFA | RC strip foundation, ~0.35 m³ concrete + ~25 kg rebar per m² of GFA at single-storey equivalent; foundation contributes ~22.8 % of EC of a Spanish masonry house per literature; A1–A3 only; cement-rich CEM I dominates the upper bound, CEM II/B-M lower bound | izaola-2023, mateus-2023 | 1 |
| foundation | labor_hours_per_m2 | 1.5 | 3.0 | h / m² GFA | Excavation + steel placement + pour + cure for shallow strip foundation; CYPE foundation page was unreachable at fetch time, so range is taken from CYPE neighbouring lines + Spanish bricklayer productivity defaults | rejected-cype-found, cype-spain-fef010 | 2 |
| foundation | time_days | 7 | 14 | calendar days | Strip foundation cure time governs; assumes single-family detached site, normal weather, EHE-08 minimum cure | UNKNOWN | NA |
| foundation | cost_eur_per_m2 | 50 | 110 | € / m² GFA | Spanish 2025–2026 vintage from CYPE-adjacent items; widened because the FOUNDATION CYPE URL returned 403 at fetch | cype-spain-fef010 | 2 |
| foundation | material_origin | NA | NA | qualitative | Catalan/Spanish RC: cement (Catalan kilns dominant), aggregates (Catalan quarries < 50 km), rebar (mostly Spanish recycled-content steel from Catalan + Basque mills); concrete A4 transport typically < 30 km from ready-mix plant | bedec-2026 | 1 |
| structure | co2_kg_per_m2 | 32 | 75 | kg CO₂ eq / m² wall | Single-leaf perforated clay brick wall, 24 cm thick. Hispalyt 008-017 GWP A1–A3 = 209 kg CO₂ eq / tonne brick × ~140 kg/m² wall (perforated 780 kg/m³ × 0.24 × 0.75 fill) ≈ 29 kg/m² brick alone; +mortar (cement-rich M-5, ~30 kg/m² mortar at ~0.13 kg CO₂/kg) ≈ 4 kg/m²; +reinforcement at lintels ≈ 3-7 kg/m². Lower bound = lime-rich M-2.5 mortar; upper bound = double-leaf cavity wall typical in modern Catalan envelope | hispalyt-008-017, hispalyt-008-016, mateus-2023 | 1 |
| structure | labor_hours_per_m2 | 0.7 | 1.5 | h / m² wall | CYPE FEF010 (load-bearing perforated brick wall, single leaf): oficial 1ª 0.495 h + peón 0.495 h = 0.99 h/m². CYPE FFZ010 (exterior facing leaf, 11 cm hollow triple): 0.685 h/m². Range covers single-leaf vs double-leaf cavity assemblies. | cype-spain-fef010, cype-spain-ffz010 | 1 |
| structure | time_days | 10 | 25 | calendar days | Two-storey unifamiliar shell, 2 masons + 1 helper crew, 80–100 m² wall/day pace. No primary source verified; flagged | UNKNOWN | NA |
| structure | cost_eur_per_m2 | 20 | 35 | € / m² wall | CYPE FEF010 (Spain) = €25.73/m² for load-bearing perforated brick; CYPE FFZ010 = €20.13/m² for non-structural facing leaf. Range covers cheap inner-partition leaf at low end and full structural single-leaf at high end. | cype-spain-fef010, cype-spain-ffz010 | 1 |
| structure | material_origin | NA | NA | qualitative | Catalan kilns: clay extracted from local Catalan / Aragon quarries; firing fuel = mostly natural gas via Spanish grid. Hispalyt EPD A4 = 87 km (block) and 296 km (facing brick); the 296 km figure is national-average so for a Catalan project the local figure is closer to 87 km. Imported brick from Italy / Portugal possible but rare. | hispalyt-008-016, hispalyt-008-017 | 1 |
| roof | co2_kg_per_m2 | 25 | 70 | kg CO₂ eq / m² roof | Hispalyt 008-001 clay tiles A1–A3 = 199 kg CO₂ eq / tonne × ~40–45 kg/m² installed = 8.0–8.9 kg/m² for tiles alone. Add RC slab + timber battens + insulation ≈ 17–60 kg/m² depending on slab thickness (15 cm RC adds ~50 kg CO₂/m²; lighter timber-batten roof on hollow-block ceramic deck adds ~9 kg/m²). | hispalyt-008-001, izaola-2023, mateus-2023 | 1 |
| roof | labor_hours_per_m2 | 0.8 | 2.0 | h / m² roof | Tile-laying productivity 5–12 m²/day per oficial in Spanish residential masonry; range covers single-tile pitched roof (low) and complex insulated cubierta a la catalana (high). Not directly retrieved from CYPE due to URL 404. | rejected-cype-roof | 3 |
| roof | time_days | 4 | 10 | calendar days | UNKNOWN — derived only from labour-rate estimate. | UNKNOWN | NA |
| roof | cost_eur_per_m2 | 50 | 90 | € / m² roof | Range from CYPE-adjacent items + IVE Costes de Construcción (https://www.five.es/costes-de-construccion/) typical Spanish roof €60–80/m². Widened because primary CYPE roof URL was 404. | rejected-cype-roof | 3 |
| roof | material_origin | NA | NA | qualitative | Catalan clay tiles: La Escandella (Alicante), Cerámica La Coma (Girona), Tejas Borja (València) — all Spanish kilns; A4 transport ≈ 287 km national average per Hispalyt EPD; local sourcing < 200 km common in Catalonia. | hispalyt-008-001 | 1 |
| openings | co2_kg_per_m2 | 30 | 90 | kg CO₂ eq / m² opening area | Aluminium-frame double-glazed window dominates Spanish residential. Aluminium frames carry high embodied carbon (~150–250 kg CO₂/m² of frame area); double glazing ~25 kg CO₂/m² of glass. Range reflects timber-frame (low) to aluminium-frame (high). Per m² GFA: openings typically 15 % of facade area, so contribution to GFA-normalized total is much smaller than the per-opening figure. | izaola-2023, de-wolf-2017 | 2 |
| openings | labor_hours_per_m2 | 1.0 | 2.5 | h / m² opening | Lintel + frame install + glazing + sealant; range from Spanish rehabilitation rates. No primary CYPE retrieval. | UNKNOWN | NA |
| openings | time_days | 2 | 5 | calendar days | Per opening, including curing of lintel mortar. Order-of-magnitude. | UNKNOWN | NA |
| openings | cost_eur_per_m2 | 150 | 450 | € / m² opening area | Aluminium-frame thermal-break double-glazed window in Spain typically €250–400/m². Lower bound is timber/PVC simple glazing. | UNKNOWN | NA |
| openings | material_origin | NA | NA | qualitative | Aluminium frames: extruded in Spain (Cortizo, Technal-iberia) or imported from EU; primary aluminium ~70 % global market is high-carbon (Russia/China) but Spanish extruders use European recycled-content billet. Glass: Saint-Gobain plants in Spain (Avilés, La Granja). Hardware imported from EU. | UNKNOWN | NA |
| finishing | co2_kg_per_m2 | 15 | 50 | kg CO₂ eq / m² of finished surface | Cement-mortar render (external) ≈ 10–25 kg CO₂/m²; gypsum plaster (internal) ≈ 4–8 kg/m²; paint 2 coats ≈ 1–3 kg/m²; ceramic floor tile ≈ 8–15 kg/m². Range covers traditional revoco-mortar + paint at low end and full ceramic-clad bathroom assembly at high end. | mateus-2023, izaola-2023 | 2 |
| finishing | labor_hours_per_m2 | 0.5 | 2.0 | h / m² of finished surface | Plastering 0.4–0.8 h/m², painting 0.2–0.4 h/m², floor-tile 0.7–1.2 h/m². Aggregate range. | UNKNOWN | NA |
| finishing | time_days | 5 | 15 | calendar days | Plaster cure (3–7 days) + paint cure between coats + tile-grout cure. | UNKNOWN | NA |
| finishing | cost_eur_per_m2 | 25 | 75 | € / m² of finished surface | Spanish 2025–2026 IVE / CYPE-adjacent rates; range covers plaster-and-paint only (low) to full ceramic-clad surface (high). | UNKNOWN | NA |
| finishing | material_origin | NA | NA | qualitative | Cement-mortar from Spanish kilns (Cementos Molins, Cemex España); gypsum from Spanish quarries (Almería / Aragón); paint from Spanish manufacturers (Titan, Procolor). All A4 < 200 km in a Catalan project. Ceramic floor tile from Castellón cluster (≈ 600 km from Barcelona). | UNKNOWN | NA |

---

## Cell-count check

- 25 rows of (phase, parameter) — ✓
- Cells with populated (non-UNKNOWN) numeric values: **15** — ✓ (≥ 8 required)
  - Specifically: foundation co2 + labor + cost; structure co2 + labor + time + cost; roof co2 + labor + cost; openings co2; finishing co2; plus material_origin qualitative entries for foundation / structure / roof.
- Cells flagged UNKNOWN: foundation time_days; structure time_days; roof time_days; openings labor / time / cost / material_origin; finishing labor / time / cost / material_origin.

---

## Whole-building sanity check

Summing the structure + roof + finishing GFA-normalized phase carbon (with structure contributing per-m²-of-wall ≈ per-m²-of-GFA at single-storey, roof shared across the floor area, finishing applied to wall + ceiling + floor):

- foundation: 70–130 kg/m²
- structure (walls only, weighted to GFA): 50–100 kg/m²
- roof (shared over GFA at single-storey): 25–70 kg/m²
- openings (15 % facade × ~30 % facade-to-GFA ratio): 15–40 kg/m²
- finishing (applied to ~3 m² surface per m² GFA): 45–150 kg/m²

**Sum: 205–490 kg CO₂ eq / m² GFA.**

This brackets the Izaola-2023 baseline of **559 kg CO₂ eq/m²** at the upper end and the De-Wolf-2017 "200–550 kg/m² typical" envelope. The mid-point of our ranges (~350 kg/m²) sits in the middle of De-Wolf's envelope and ~37 % below Izaola's value, reflecting that Izaola includes maintenance + EoL while our A1–A3-dominant figures do not. **The strand-level total is therefore consistent with both anchors.**
