# Values — Strand 06: Feasibility, Origin, Transport, Jobs, Carbon Budget

Five tables, one per sub-strand. Where a value could not be verified at primary source within this session's time budget it is marked `UNKNOWN` with `source = NA` per the iron rules. Methodology-wobble is annotated where relevant.

Locked decisions inherited from prior strands: the four installation methods are
**M1 Masonry** (fired clay block + cement mortar),
**M2-C 3D-printed concrete** (printable OPC mix),
**M2-E 3D-printed earth** (raw earth + stabiliser),
**M3-C Modular prefab — concrete (MiC)**,
**M3-T Modular prefab — CLT**,
**M4 Reclaimed brick** (re-laid hand-cleaned brick).

---

## Table 6 — Feasibility constraints

| method | constraint | value | source | reference_doc |
|---|---|---|---|---|
| M1 Masonry | Max storeys (load-bearing unreinforced, typical Catalan practice) | 4 storeys (5 with reinforced detailing) | CTE DB-SE-F + EN 1996-1-1 | DBSE-F (Spanish); EN 1996-1-1 |
| M1 Masonry | Min wall thickness, load-bearing | 115 mm absolute; 240 mm typical for >2 storey | EN 1996-1-1 §8.1; DB-SE-F | EN 1996-1-1 |
| M1 Masonry | Max slenderness ratio λ = h_ef / t_ef | 27 (unreinforced, vertical loads) | EN 1996-1-1 Annex F; DB-SE-F | EN 1996-1-1 |
| M1 Masonry | Max unsupported wall height between floors | derived: 2.7–3.1 m for 115 mm wall, 6.3–7.3 m for 240 mm (λ=27) | derived from EN 1996-1-1 | EN 1996-1-1 |
| M1 Masonry | Applicable building types | low-rise residential, school, small commercial; not high-rise | DB-SE-F | DBSE-F |
| M2-C 3D-printed concrete | Built single-storey load-bearing precedent | yes (multiple ICON, COBOD-printed houses) | ICC-ES ESR-4652 | ESR-4652 |
| M2-C 3D-printed concrete | Built multi-storey precedent | 2 storeys, 9.5 m, 640 m² (Apis Cor / Dubai Municipality, 2019) | Dezeen / Apis Cor | dezeen.com/2019/12/22 |
| M2-C 3D-printed concrete | Code status, EU/Spain (May 2026) | Treated case-by-case; NO Eurocode addendum for 3DPC; ICC 1150 (US) at public-comment stage | ICC 1150 draft 2024-11-26 | ICC-1150-DRAFT |
| M2-C 3D-printed concrete | Max single-print volume (BOD2) | 12 m W × 27 m L × 9 m H | COBOD BOD2 spec | cobod.com/solution/bod2 |
| M2-C 3D-printed concrete | Structural-vs-decorative classification, typical EU permitting | non-structural unless explicit alternate-means approval; structural-shell with reinforced lintels and slabs | ICC-ES ESR-4652 (analogue) | ESR-4652 |
| M2-E 3D-printed earth | Max storeys claimed | 1 storey (TECLA: 4.2 m peak, 2 modules) | WASP / Mario Cucinella Architects | 3dwasp.com/en/3d-printed-house-tecla |
| M2-E 3D-printed earth | Eurocode coverage | NONE (no formal earth-construction Eurocode); national-annex variants (FR, DE, IT) cover rammed earth and adobe but NOT printed earth | EN 1996-1-1 (covers fired clay only) | — |
| M2-E 3D-printed earth | Permitting status, Spain | experimental / prototype; TOVA permitted as research structure at Valldaura, not as residential dwelling | IAAC TOVA project page | iaac.net/projects/tova |
| M3-C Modular concrete (MiC) | Max storeys (built precedent) | 17 storeys (InnoCell, Hong Kong, 2020) | WSP / HKSTP | wsp.com (HKSTP) |
| M3-C Modular concrete (MiC) | Max storeys (design capacity, declared) | 40 storeys, "wall connection technology" (Chun Wo, HK) | Chun Wo Development Holdings | chunwo.com/en/inno-projects-offsite |
| M3-C Modular concrete (MiC) | Max road-transport module dimensions, Spain (no oversize permit) | 2.55 m W × 4.0 m H × 16.5 m L; 40 t gross | Spanish Reg. Gen. Vehículos (RD 970/2020 + 2024 update) | fernandezaedo.com summary |
| M3-C Modular concrete (MiC) | Max road-transport module dimensions, Spain (oversize "Genérica" permit) | 3.0 m W × 4.5 m H × 20.55 m L; 45 t gross | Spanish DGT Genérica permit | tigertruck.eu / Nooteboom |
| M3-T Modular CLT | Max storeys (built precedent, pure timber) | 18 storeys, 85.4 m (Mjøstårnet, Norway, 2019) | Moelven / Abrahamsen 2018 | moelven.com (PDF) |
| M3-T Modular CLT | Max storeys (built precedent, hybrid CLT + concrete core) | 24 storeys, 84 m (HoHo Wien, Austria, 2019) | HASSLACHER / WCTE | hasslacher.com/hoho-vienna-en |
| M3-T Modular CLT | Catalan code limit (May 2026) | de-facto governed by CTE DB-SI fire requirements; no fixed storey ceiling but tall-timber requires fire-engineered alternate-means approval | CTE DB-SE / DB-SI | codigotecnico.org |
| M3-T Modular CLT | Eurocode coverage | EN 1995-1-1 (Eurocode 5), EN 1995-1-2 (fire) | CEN | EN 1995-1-1 |
| M4 Reclaimed brick | Max storeys (typical re-laid practice, EU) | 2–3 storeys load-bearing; non-structural facade unrestricted | inferred from Salmio & Huuhka 2026 + practice survey | doi.org/10.5334/bc.651 |
| M4 Reclaimed brick | Allowable working stress vs new masonry | 50 % of equivalent new unit (US masonry-reclamation guidance, conservatively transferable) | Brick Industry Association Tech Note 15 | gobrick.com/15-salvaged-brick |
| M4 Reclaimed brick | Primary feasibility constraint | stock availability, not strength | Salmio & Huuhka 2026 | doi.org/10.5334/bc.651 |
| M4 Reclaimed brick | BEDEC catalogue entry (Catalan industry standard reference) | NONE for `totxo recuperat` (locked decision from prior strand) | inherited from Strand 04 | — |

**Wobble note (Sub-6).** "Max storeys" is not a single number in any Eurocode — it emerges from the interaction of mortar grade, wall thickness, slenderness, and seismic action. Catalonia is in a low-to-moderate seismic zone. The values above represent typical practice envelopes, not formal prescriptive limits. The installation should display them as bands, not points.

---

## Table 7 — Material origin (country / region)

| material | typical_origin_country | specific_facility_or_region | distance_to_barcelona_km | source |
|---|---|---|---|---|
| Fired clay brick (Catalan baseline) | Spain | Piera Ecocerámica (Hostalets de Pierola, Barcelona prov.) | ~50 km | suppliers.catalonia.com/detail/ceramica-pierola-sl/853 |
| Fired clay brick (Spanish) | Spain | Hispalyt member network (~85 % of Spanish sectoral production) | 50–500 km depending on plant | tejasverea.com/en/hispalyt-en/ |
| Cement / OPC clinker | Spain | Cementos Molins, Sant Vicenç dels Horts (Baix Llobregat) | ~15 km | molins.es/en/about-us |
| Cement / OPC clinker (alt.) | Spain | Cemex Alcanar (Tarragona) | ~200 km | cemnet.com/global-cement-report/country/spain |
| 3D-printed concrete mix | Spain (cement) + EU (admixtures) | Spanish OPC + admixtures from Sika/BASF EU plants | 50–300 km cement; 1 000–1 500 km specialty admixtures | inferred from EU specialty supply network |
| Earth (3DP) — Catalan baseline | Spain (Catalonia) | Valldaura Labs / TOVA = 50 m radius around print site | <0.1 km | iaac.net/projects/tova |
| Earth (3DP) — typical realistic | Spain (Catalonia) | site-quarried subsoil + nearby quarry | <5 km | inferred from cob/rammed-earth practice |
| CLT — Austrian | Austria | Stora Enso Bad St. Leonhard (Carinthia); Stora Enso Ybbs (Lower Austria); Hasslacher (Carinthia) | ~1 850 km road; ~2 200 km via rail+road | storaenso.com/en/about-stora-enso/stora-enso-locations |
| CLT — Swedish | Sweden | Stora Enso Gruvön; Setra | ~2 800 km road; ~2 200 km rail+sea via Tarragona | storaenso.com locations |
| CLT — Finnish | Finland | Metsä Wood Punkaharju | ~3 200 km road | metsawood.com |
| Modular concrete (MiC) | Spain (limited) / imports | Spanish modular market is small; most concrete-MiC stock is bespoke per project; import dependency from Hong Kong / Poland / Germany | 50–2 500 km (case-dependent) | UNKNOWN — `source = NA` for typical Catalan supplier |
| Modular CLT (assembled) | Austria / Germany | Hasslacher, Binderholz, KLH Massivholz | ~1 600–1 900 km road | hasslacher.com; binderholz.com |
| Reclaimed brick (Catalonia) | Spain (Catalonia) | informal urban-mining flows; no centralised supplier; BEDEC has no entry | <50 km when available; supply gap = primary constraint | Salmio & Huuhka 2026; locked-decision Strand 04 |
| Steel rebar | Spain / Poland / Morocco / Bosnia | ArcelorMittal Warsaw (PL), Sonasid (MA), Zenica (BA); Sagunto (Spain) is FLAT products, NOT rebar | ~600–2 500 km depending on mill | flateurope.arcelormittal.com/ourmills/711/sagunto |
| Mortar (cement) | Spain | Cementos Molins / Cemex Alcanar | 15–200 km | molins.es; cemnet.com |
| Lintels (precast concrete) | Spain | local Catalan precasters | 50–150 km | UNKNOWN specific facility — `source = NA` |

**Note.** The brief listed "ArcelorMittal Sagunto, etc." as a Spanish rebar source. Verification at the ArcelorMittal Sagunto plant page (flateurope.arcelormittal.com/ourmills/711/sagunto) shows Sagunto is a flat-products mill, not a rebar mill. Spanish rebar consumed in Catalonia comes principally from Polish (ArcelorMittal Warsaw), Moroccan (Sonasid), or Bosnian (Zenica) mills. This is a relevant correction to the input brief.

---

## Table 8 — Transport distance to Barcelona

| material | typical_distance_km | low_high_range | mode | source |
|---|---|---|---|---|
| Fired clay brick (Catalan) | ~50 km (Piera ↔ BCN) | 30–150 km | road | suppliers.catalonia.com/detail/ceramica-pierola-sl/853 |
| Fired clay brick (Hispalyt EPD A4 baseline) | UNKNOWN this session | 50–150 km claimed in brief | road | source = NA (PDF binary; brief stated 87 km but not re-verifiable here) |
| OPC cement (Cementos Molins) | ~15 km | 10–30 km | road | molins.es |
| OPC cement (Cemex Alcanar) | ~200 km | 150–250 km | road | cemnet.com |
| 3D-printed concrete mix (Spanish OPC + EU admixtures) | ~150 km cement + 1 200 km admixtures (weighted ≪ cement) | 50–300 km | road | inferred |
| Earth, 3DP (TOVA precedent) | <0.05 km | 0.005–0.5 km | hand / wheelbarrow | iaac.net/projects/tova |
| Earth, 3DP (realistic urban Catalan project) | ~5 km | 1–20 km | road, light truck | inferred |
| CLT (Austrian, Bad St. Leonhard) | ~1 850 km | 1 700–2 000 km | road; rail-truck possible to Tarragona | storaenso.com; distantias.com |
| CLT (Swedish, Gruvön) | ~2 800 km | 2 500–3 100 km | sea-rail-road combination | storaenso.com |
| CLT (Finnish, Punkaharju) | ~3 200 km | 2 900–3 500 km | sea-rail-road | metsawood.com |
| Modular concrete unit (Spanish) | ~150 km | 50–500 km | road (Genérica oversize permit ≥3.0 m wide) | RD 970/2020 |
| Modular concrete unit (imported Polish) | ~2 200 km | 2 000–2 500 km | road or rail-truck | inferred |
| Reclaimed brick (Catalan urban-mining best case) | <50 km | 0.5–50 km | road, light truck | Salmio & Huuhka 2026 (≤480 km T1 / ≤315 km T2 thresholds) |
| Reclaimed brick (carbon-erased threshold) | 480 km T1 / 315 km T2 | hard upper bound | road | doi.org/10.5334/bc.651 |
| Steel rebar (Polish ArcelorMittal Warsaw) | ~2 400 km | 2 200–2 600 km | road / road-rail | flateurope.arcelormittal.com |
| Steel rebar (Bosnian Zenica) | ~2 100 km | 1 900–2 300 km | road | flateurope.arcelormittal.com |

**Wobble note (Sub-8).** The road-distance figures are point-to-point Google-Maps-grade estimates rounded to 50 km. They reflect a single representative truck route; real shipments use multimodal optimisation and the LCA-A4 figure should bracket ±20 %. The 480 km / 315 km Salmio-Huuhka thresholds are paper-derived (Finnish climate-mix electricity baseline); applied to Spanish electricity mix the threshold could shift upward (Spanish grid is less coal-intensive). The installation's wobble layer should display the brick-transport thresholds as a bracketed band, not a hard line.

---

## Table 9 — Jobs / employment impact

| method | fte_per_100m2_low | fte_per_100m2_high | skilled_pct | semi_pct | unskilled_pct | onsite_factory_split | source |
|---|---|---|---|---|---|---|---|
| M1 Masonry | 0.30 | 0.50 | ~30 % | ~40 % | ~30 % | 100 % onsite | derived from Spanish productivity €112 400/FTE/yr (CaixaBank) + Estatefy 2024; UNKNOWN at peer-reviewed precision — `source = NA` for primary FTE/m² figure |
| M2-C 3D-printed concrete | 0.10 | 0.20 | ~50 % (technician-printer-operator + engineer-supervisor) | ~30 % | ~20 % | ~70 % onsite (printing) + ~30 % offsite (mix prep, BIM, programming) | Hossain et al. 2020 (50–80 % labour-cost reduction); Apis Cor / Dezeen 2019 (15 vs ~30 workers, 50 % reduction) |
| M2-E 3D-printed earth | 0.10 | 0.25 | ~50 % | ~30 % | ~20 % | ~80 % onsite (material is local) + ~20 % offsite (mix tuning) | UNKNOWN at peer-reviewed precision — `source = NA`; range derived by analogy from M2-C |
| M3-C Modular concrete (MiC) | 0.20 | 0.35 | ~40 % | ~40 % | ~20 % | 20–25 % onsite / 75–80 % factory | McKinsey 2019; WEF 2025 (30 % fewer on-site labour hours; ~80 % activity offsite) |
| M3-T Modular CLT | 0.20 | 0.35 | ~50 % (CNC operators, factory carpenters) | ~30 % | ~20 % | 20–30 % onsite / 70–80 % factory | McKinsey 2019; HoHo / Mjøstårnet case practice |
| M4 Reclaimed brick | 0.50 | 0.90 | ~25 % (skilled mason re-laying) | ~35 % | ~40 % (deconstruction labour) | 100 % onsite (deconstruction site + new site) | Salmio & Huuhka 2026 (T1 = 1.4 h per worker per re-usable yield; deconstruction-side labour-intensive) |

**Wobble note (Sub-9).** FTE-per-100m² is poorly studied at peer-review precision in Spain. The numbers above are best-available bands derived from cross-source triangulation (McKinsey global; WEF Europe-wide; ILO sectoral; Spanish productivity benchmarks; case-study FTE counts). Treat them as ±50 % wobble. The skill-mix percentages are even more uncertain (no Spanish peer-reviewed disaggregation found) and should be treated as ±15 absolute percentage points.

**Source-bias direction explicit (per iron-rule 4):**
- McKinsey 2019: industry-favourable, _LOWBALL_ on labour displacement.
- WEF 2025: industry-aligned, _LOWBALL_.
- Hossain et al. 2020 (peer-reviewed Sustainability paper): _BIASED HIGH_ on displacement (counts only on-site labour reduction, undercounts factory + machine-tending uplift).
- ILO 2018 / 2025: worker-protection multilateral; quantitative method (Frey-Osborne style) is contested but neutral on Sub-9 quantitatively.
- Salmio & Huuhka 2026: peer-reviewed; bias is environmental-LCA framing, not labour-political.

---

## Table 10 — Remaining 1.5 °C carbon budget

| metric | value | unit | as_of_date | source |
|---|---|---|---|---|
| Remaining 1.5 °C budget (50 % chance) | virtually exhausted ("breached within 4 years at current rate") | Gt CO₂ | start of 2025 | Global Carbon Budget 2025 FAQs |
| Remaining 1.5 °C budget (50 % chance, headline residual) | ~170 | Gt CO₂ | start of 2025 (computed from prior 220 Gt minus 2024 emissions of ~38 Gt + LUC) | Climate Change Tracker / GCB 2025 |
| Remaining 1.7 °C budget (50 % chance) | 525 | Gt CO₂ | start of 2025 | Global Carbon Budget 2025 FAQs |
| Remaining 2.0 °C budget (50 % chance) | 1 055 | Gt CO₂ | start of 2025 | Global Carbon Budget 2025 FAQs |
| Years remaining at 2025 emission rate, 1.7 °C | ~12 | yr | 2025 projection | Global Carbon Budget 2025 |
| Years remaining at 2025 emission rate, 2.0 °C | ~25 | yr | 2025 projection | Global Carbon Budget 2025 |
| Total annual fossil-fuel CO₂ emissions | 38.1 | Gt CO₂/yr | 2025 projected | Global Carbon Budget 2025 |
| Total annual land-use-change CO₂ emissions | 4.1 | Gt CO₂/yr | 2025 projected | Global Carbon Budget 2025 |
| Year-on-year change 2024 → 2025 | +1.1 | % | 2025 | Global Carbon Budget 2025 |
| Buildings + construction sector — share of global energy | 32 | % | 2023 data, 2024/25 reporting | UNEP GSR 2024/25 |
| Buildings + construction sector — share of global CO₂ (energy + process) | 34 (UNEP) / 37 (IEA legacy) | % | 2023 data | UNEP GSR 2024/25; IEA Buildings tracker |
| Buildings sector — operational emissions | ~10 | Gt CO₂/yr | 2023 | UNEP GSR 2024/25 |
| Construction (embodied: cement, steel, aluminium) | ~2.5 | Gt CO₂/yr | 2022 | IEA / UNEP GSR |
| Construction (embodied: brick + glass, additional) | ~1.2 | Gt CO₂/yr | 2022 | IEA / UNEP GSR |
| New-construction-only emissions | ~2.5 (≈ 7 % global) | Gt CO₂/yr | 2022 | IEA chart / UNEP GSR |
| Required reduction by 2030, sector | 28 | % | vs 2023 baseline | UNEP GSR 2024/25 |
| Embodied-carbon reduction required by 2030 (Architecture 2030) | 65 | % | vs current | architecture2030.org |
| Embodied carbon — structure + sub-structure + enclosure (annual GHG share) | 11 | % global / 28 % of buildings sector | 2023 | architecture2030.org |
| Decoupling year (sector-emissions flat while floor-area grew) | 2023 | year | UNEP first-time finding | UNEP GSR 2024/25 |

**Wobble note (Sub-10).** The 1.5 °C budget figure depends on (1) probability threshold (50 vs 67 %), (2) baseline temperature window (1850-1900 vs 1986-2005), and (3) assumed non-CO₂-forcer trajectory. The "virtually exhausted" headline is for the 50 % probability threshold; for 67 % the budget is already negative — i.e. exhausted as of late 2024. The installation's live counter should display the source date (Global Carbon Budget 2025-11) and the probability threshold next to the number.
