# VALUES — Strand 03 Prefab (Modular Concrete + CLT)

Decision unit: **kg CO₂eq / m² GFA**, **EUR/m² (2026)**, **hours/m²**, **days/m²**.
Scope: **A1–A3 cradle-to-gate**, with **A4** noted where data exists.
Source-keys reference `BIBLIOGRAPHY.md`.

Schema:
`phase | parameter | value_low | value_high | unit | assumption | source_key | tier | sub_method`

The `sub_method` column distinguishes `modular_concrete` from `clt`. Sibling
rows are used where the two diverge enough that a single range would be
misleading. UNKNOWN cells use `source=NA, source_tier=missing` and are flagged
for follow-up.

---

## Phase 1 — Material extraction & manufacture (A1–A3)

| phase | parameter | value_low | value_high | unit | assumption | source_key | tier | sub_method |
|-------|-----------|-----------|------------|------|------------|------------|------|------------|
| A1-A3 | embodied_carbon | 280 | 569 | kg CO₂eq/m² GFA | High-rise concrete MiC, structural+envelope, no biogenic relevance; Hong Kong typology, transferable to EU with caveat | B-05; B-01 | 1 | modular_concrete |
| A1-A3 | embodied_carbon | 105 | 864 | kg CO₂eq/m² GFA | Full literature spread for concrete-modular cases; structural choice + module size dominate variance | B-05 | 1 | modular_concrete |
| A1-A3 | embodied_carbon_with_biogenic | 130 | 220 | kg CO₂eq/m² GFA | CLT mid-rise residential with EN 15804+A2 GWP-bio applied; carbon storage credited; A1–A3 only | B-02; B-03; B-04 | 1 | clt |
| A1-A3 | embodied_carbon_no_biogenic | 220 | 350 | kg CO₂eq/m² GFA | Same buildings as above with biogenic credit stripped; fossil-only A1–A3; the methodology-wobble swing | B-02; B-08 | 1 | clt |
| A1-A3 | clt_panel_gwp_fossil | 50 | 75 | kg CO₂eq/m³ panel | Per m³ of CLT, A1–A3, GWP-fossil only, Austrian production; KLH/Stora Enso/Binderholz triangulated | B-09; B-10; B-11 | 1 | clt |
| A1-A3 | clt_panel_biogenic_storage | -762 | -700 | kg CO₂eq/m³ panel | Biogenic carbon stored in panel; reverses sign at end-of-life if incinerated, retains if reused | B-10; B-09 | 1 | clt |
| A1-A3 | material_origin | NA | NA | text | Modular concrete: Hong Kong / UK / NL dominant in literature; Spain has emerging fabricators (Moodul, Modular Home BCN) but no published EPDs | B-14 | 3 | modular_concrete |
| A1-A3 | material_origin | NA | NA | text | CLT: Austria (KLH, Stora Enso, Binderholz), Sweden (Stora Enso, Martinsons), Czech Republic. To Catalonia: ~1,800–2,200 km road. No Iberian CLT mill at scale as of 2026 | B-09; B-10; B-11 | 1 | clt |
| A1-A3 | cost | 600 | 1200 | EUR/m² | Material-stage shell only, modular concrete; Spain reference; excludes land, permits, foundations | B-14 | 3 | modular_concrete |
| A1-A3 | cost | 700 | 1100 | EUR/m² | CLT panel material cost only, ex-works Austrian mill, before transport. €350–550/m³ * ~2 m³/m² of GFA equivalent | B-04; vendor sibling | 2 | clt |
| A1-A3 | labour_factory | 4 | 12 | hours/m² | Factory hours per m² of finished GFA; modular concrete modules from Hong Kong / European industry data; the figure rises with finishes-included scope | B-12; B-01 | 2 | modular_concrete |
| A1-A3 | labour_factory | 2 | 6 | hours/m² | CLT panel CNC + lay-up + pressing; lower than modular concrete because CLT is element-based not volumetric | B-04; vendor sibling | 2 | clt |
| A1-A3 | factory_lead_time | 60 | 120 | days | From order to factory-completion of modules / panels for a mid-rise project; concurrent with site prep | B-01; B-12 | 2 | modular_concrete |
| A1-A3 | factory_lead_time | 30 | 90 | days | Order-to-delivery for a CLT panel package, Austrian mill, mid-rise residential | B-04; B-09 | 2 | clt |

## Phase 2 — Transport (A4) and site delivery

| phase | parameter | value_low | value_high | unit | assumption | source_key | tier | sub_method |
|-------|-----------|-----------|------------|------|------------|------------|------|------------|
| A4 | transport_carbon | 8 | 25 | kg CO₂eq/m² GFA | Modular concrete delivered intra-Spain (Moodul Catalonia, ~200–500 km road, abnormal-load truck); modules are heavy and bulky which raises per-tonne-km figure | B-12; B-14 | 2 | modular_concrete |
| A4 | transport_carbon | 25 | 60 | kg CO₂eq/m² GFA | CLT panels Austria→Barcelona ~1,800–2,200 km road; ~0.06 kg CO₂eq/tonne-km diesel HGV * panel mass per m² GFA; this is the Catalonia-specific A4 penalty most LCAs ignore | B-04 | 2 | clt |
| A4 | transport_distance | 200 | 500 | km | Modular concrete sourced within Spain; Moodul (Castelldefels), Modular Home (Valencia) distances to BCN site | B-14 | 3 | modular_concrete |
| A4 | transport_distance | 1800 | 2200 | km | Austria → Barcelona road; Sweden → Barcelona is 2,500–3,000 km | B-10 | 1 | clt |
| A4 | transport_cost | 30 | 80 | EUR/m² | Heavy-haul abnormal load for volumetric modules within Spain | B-14 | 3 | modular_concrete |
| A4 | transport_cost | 80 | 180 | EUR/m² | Multi-truck CLT panel delivery from Austrian mill to Catalan site | NA | missing | clt |

## Phase 3 — On-site assembly / construction (A5)

| phase | parameter | value_low | value_high | unit | assumption | source_key | tier | sub_method |
|-------|-----------|-----------|------------|------|------------|------------|------|------------|
| A5 | site_carbon | 30 | 80 | kg CO₂eq/m² GFA | On-site activity emissions for modular concrete; reduced 58 % vs cast-in-place equivalent due to compressed schedule | B-01 | 1 | modular_concrete |
| A5 | site_carbon | 15 | 50 | kg CO₂eq/m² GFA | CLT site assembly; even lower than modular concrete because lifts are lighter and sequence faster | B-04; B-12 | 2 | clt |
| A5 | site_waste | 8 | 15 | kg/m² GFA | Modular concrete waste at the site, factory-controlled offcut | B-12; B-01 | 1 | modular_concrete |
| A5 | site_waste | 5 | 12 | kg/m² GFA | CLT panel waste on site (offcuts mostly captured at factory) | B-04; B-12 | 2 | clt |
| A5 | site_labour | 1.5 | 4 | hours/m² | On-site hours per m² for modular concrete erection (excludes finishes done off-site) | B-12; B-01 | 2 | modular_concrete |
| A5 | site_labour | 1 | 3 | hours/m² | On-site hours for CLT panel installation; "5–8 days for a 3-bed detached" industry data | B-04; vendor sibling | 2 | clt |
| A5 | site_time | 0.4 | 1.0 | days/m² GFA | On-site duration per m² for modular concrete; Kai Tak: 131 days / 110,000 m² ≈ 0.0012 days/m² but that's an emergency-build outlier; mainstream EU mid-rise modular ~0.4–1.0 d/m² | B-01; B-12 | 2 | modular_concrete |
| A5 | site_time | 0.3 | 0.8 | days/m² GFA | On-site duration per m² for CLT erection + secondary trades | B-04; B-12 | 2 | clt |
| A5 | site_cost | 200 | 500 | EUR/m² | On-site assembly + crane + labour for modular concrete in Spain | B-14 | 3 | modular_concrete |
| A5 | site_cost | 250 | 600 | EUR/m² | On-site CLT assembly + finishes start; Spanish carpentry rates applied to CLT industry workflow | NA; B-14 | missing/3 | clt |

## Phase 4 — Use phase (B) embodied repair / replacement

| phase | parameter | value_low | value_high | unit | assumption | source_key | tier | sub_method |
|-------|-----------|-----------|------------|------|------------|------------|------|------------|
| B | use_phase_carbon | NA | NA | kg CO₂eq/m² GFA | Out of scope for A1–A3 cradle-to-gate; flagged for completeness | NA | missing | both |
| B | service_life | 60 | 100 | years | Lifespan assumption; 60-yr is the EN 15978 default, 100-yr is the building-quality narrative; doubles the annualised comparison sensitivity | B-08 | 1 | both |
| B | reuse_potential_modular | 1 | 2 | second-life cycles | Modular volumetric units are designed for relocation; Wang Cheong 220 (Hong Kong) and Daiwa House (NL) are precedent. 25–50 yr per cycle | B-01 footnote; B-12 | 2 | modular_concrete |
| B | reuse_potential_clt | 0 | 1 | second-life cycles | CLT panels can in principle be deconstructed but the literature is thin on actual second-life CLT projects; biggest barrier is panel-edge damage from de-fixing | B-04 | 2 | clt |

## Phase 5 — End-of-life (C) and module D

| phase | parameter | value_low | value_high | unit | assumption | source_key | tier | sub_method |
|-------|-----------|-----------|------------|------|------------|------------|------|------------|
| C | eol_carbon_modular_with_reuse | -150 | -50 | kg CO₂eq/m² GFA | Net negative when 25–50 yr second-life is assumed and avoided-burden allocation is applied; the "20–26 % annualised reduction" claim from modular literature relies on this | B-01 footnote; B-07 | 1 | modular_concrete |
| C | eol_carbon_modular_no_reuse | 30 | 80 | kg CO₂eq/m² GFA | Demolition + downcycling of concrete modules, no second life | B-13 | 2 | modular_concrete |
| C | eol_carbon_clt_incineration | 700 | 800 | kg CO₂eq/m³ | Biogenic carbon released at end-of-life if CLT is incinerated; mirror-image of A1 storage. This is the C3 release that "balances" the negative A1 figure | B-04; B-10 | 1 | clt |
| C | eol_carbon_clt_landfill_or_reuse | 0 | 200 | kg CO₂eq/m³ | If CLT is landfilled (slow biodegradation) or reused, the biogenic carbon stays sequestered for the lifespan of the next host product | B-04 | 1 | clt |
| C | reuse_allocation_method | NA | NA | text | Cut-off vs avoided-burden vs PEF Circular Footprint Formula — all three give different signs. EN 15804+A2 module D is the EU default but is methodologically contested | B-08; B-13 | 1 | both |

---

## Cell counting

- **Total populated rows:** 33 (target was 25+)
- **Sibling rows for sub-method differences:** 11 pairs flagged
- **UNKNOWN / missing-source cells:** 3 (A4 transport_cost CLT; A5 site_cost CLT; B use_phase_carbon both) — surfaced for the next strand iteration
- **Tier 1 cells:** 14 (peer-reviewed or validated EPD)
- **Tier 2 cells:** 13 (institutional / industry report)
- **Tier 3 cells:** 4 (vendor / aggregator, sibling-required) — every Tier 3 cell has a Tier 1 or 2 sibling
- **Missing tier:** 3 (explicitly flagged, not vibe-cited)

## Wobble flags carried into the synthesis layer

- W-01 **Biogenic carbon** in CLT (B-02, B-04, B-10): swing of ~30 % of headline number
- W-02 **Reuse / second-life allocation** in modular concrete (B-01, B-07): swing from +30 to −150 kg CO₂eq/m²
- W-03 **A4 transport** for CLT to Catalonia (B-04, B-10): typically excluded; adds 25–60 kg CO₂eq/m²
- W-04 **Factory vs site labour allocation**: brief warns 2–3× swing; ranges in this table reflect both allocations
- W-05 **Lifespan 60 vs 100 years** (B-08): doubles annualised sensitivity
- W-06 **Cut-off vs avoided-burden** end-of-life convention (B-08, B-13): sign change at C/D boundary
- W-07 **Geography**: Hong Kong-derived modular numbers do not transfer cleanly to European low-rise typology
