# VALUES — Reclaimed Brick Masonry (Strand 04)

Decision unit: **kg CO₂eq / m² of GFA per phase, A1–A3 cradle-to-gate; EUR/m²; labour-hours/m²; days; material-origin string.**

This strand carries an extra `allocation_rule` column. For `structure / co2_kg_per_m2` three sibling rows are reported under cut-off, avoided-burden, and system-expansion to surface the methodology wobble that is the load-bearing finding of this strand.

Source keys map to entries in `BIBLIOGRAPHY.md`. Tier per entry.

```
phase | parameter | value_low | value_high | unit | allocation_rule | assumption | source_key | tier
```

---

## Foundation

| phase | parameter | value_low | value_high | unit | allocation_rule | assumption | source_key | tier |
|---|---|---|---|---|---|---|---|---|
| foundation | co2_kg_per_m2 | NA | NA | kg CO2eq/m2 GFA | NA | Reclaimed brick is rarely used for foundations (load + moisture). Foundation typically remains conventional RC; carbon attributable to brick reuse here is zero. Defer to masonry strand foundation row. | NA | missing |
| foundation | labor_hours_per_m2 | NA | NA | h/m2 | — | Same as above. | NA | missing |
| foundation | time_days | NA | NA | days | — | Same as above. | NA | missing |
| foundation | cost_eur_per_m2 | NA | NA | EUR/m2 | — | Same as above. | NA | missing |
| foundation | material_origin | "conventional RC strip / pad foundation" | "conventional RC strip / pad foundation" | — | NA | Reclaimed brick literature does not address foundations; treated as out-of-scope for this strand. | Devènes 2022 (analogous scoping) | 1 |

## Structure (load-bearing reclaimed-brick masonry)

| phase | parameter | value_low | value_high | unit | allocation_rule | assumption | source_key | tier |
|---|---|---|---|---|---|---|---|---|
| structure | co2_kg_per_m2 | 8 | 25 | kg CO2eq/m2 GFA | cut-off | Brick wall ~ 350 kg/m² for a 20 cm load-bearing wall. Reclaimed-brick A1–A3 = 20.4 kg CO₂eq/t (RBC EPD). Cut-off allocates production burden to first life → second-life upstream burden = 0; only processing (138 kWh/t cleaning + transport ≤ 50 km) counts. New-mortar contribution ≈ 5–10 kg CO₂eq/m². Range reflects yield 70–85 % and transport 0–50 km. | RBC_EPD_2024 + Salmio_Huuhka_2026 | 1 |
| structure | co2_kg_per_m2 | 18 | 45 | kg CO2eq/m2 GFA | avoided-burden | Same wall, avoided-burden methodology: second life is credited the avoided new-brick production (~250–350 kg CO₂eq/t × ~70 % credit share) but bears partial deconstruction burden. RBC EPD reports A–C total = −3.18 kg CO₂eq/t under avoided burden (i.e. net negative at full lifecycle); A1–A3-equivalent here is positive but lower-bound than cut-off when the credit share is < 100 %. Range reflects 50/50 vs degressive split between donor and receiver lifetimes. | RBC_EPD_2024 + DeWolf_2020 | 1 |
| structure | co2_kg_per_m2 | 35 | 70 | kg CO2eq/m2 GFA | system-expansion (PAS-2050 distributed / 50-50) | Splits production burden equally between the two service lives: ~125–175 kg CO₂eq/t allocated to the second life. With 350 kg/m² wall mass that is ~44–61 kg CO₂eq/m² + mortar + transport. This row exists to show why headline numbers swing ~3–5× across rules — the methodology wobble the installation must own. | DeWolf_2020 + Salmio_Huuhka_2026 | 1 |
| structure | labor_hours_per_m2 | 2.5 | 6.5 | h/m2 | — | Reclaimed-brick laying: cleaning + sorting ≈ 4 labour-h per tonne (Salmio & Huuhka 2026). 350 kg/m² wall = 1.4 h cleaning. Plus laying 1.5–4 h/m² for hand-fitted variable-dimension reused brick (vs ~0.8–1.2 h/m² for new uniform brick, BEDEC 2026 baseline) — i.e. **2–4× the labour of new brick**, consistent with brief. | Salmio_Huuhka_2026 + BEDEC_2026 (proxy) | 1 (LCA) / 2 (BEDEC laying-rate proxy) |
| structure | time_days | 14 | 35 | days | — | For a ~ 100 m² GFA single-storey reference building, structural reclaimed-brick walls take 2–5 weeks. Stock-matching design step (Brütting 2020) adds upfront design days not counted in laying. | Brütting_2020 + IAAC_Mat_Mining | 1 |
| structure | cost_eur_per_m2 | 95 | 220 | EUR/m2 | — | Reclaimed-brick price proxies: UK / DE wholesale £0.50–€1.50 per brick × ~50 bricks/m² = €25–75 material; labour at €25–35/h × 3–6 h = €75–210; mortar + sundries €15–25. Catalonia data is ABSENT — this range is EU proxy. Lower than new-brick rendered facade in some cases due to "free" upstream brick, higher when stock-matching design fees included. | Restado_2026 + Concular_2026 (cost proxy) | 2 |
| structure | material_origin | "demolition site within ≤ 50 km — local urban mining" | "demolition site ≤ 480 km — long-distance reclaim" | km radius | — | Salmio & Huuhka (2026) sensitivity: T1 (hand-held) remains net-beneficial up to 480 km; T2 (excavator) up to 315 km. Re:Crete used regional Fribourg/Lausanne sourcing (~< 30 km). K.118 sourced Basel-Zürich (~100–150 km). Catalonia: no operational hub; sourcing would currently be ad-hoc demolition-site negotiation. | Salmio_Huuhka_2026 + Devènes_2022 + insitu_K118 | 1 / 2 |

## Roof

| phase | parameter | value_low | value_high | unit | allocation_rule | assumption | source_key | tier |
|---|---|---|---|---|---|---|---|---|
| roof | co2_kg_per_m2 | NA | NA | kg CO2eq/m2 GFA | NA | Reclaimed brick is not a roof material. K.118 used reused steel for roof structure; reclaimed clay roof tiles are a separate sub-category not assessed in this strand. | NA | missing |
| roof | labor_hours_per_m2 | NA | NA | h/m2 | — | Same; defer to roof-tile / steel-trussed strand. | NA | missing |
| roof | time_days | NA | NA | days | — | Same. | NA | missing |
| roof | cost_eur_per_m2 | NA | NA | EUR/m2 | — | Same. | NA | missing |
| roof | material_origin | NA | NA | — | — | Same. | NA | missing |

## Openings

| phase | parameter | value_low | value_high | unit | allocation_rule | assumption | source_key | tier |
|---|---|---|---|---|---|---|---|---|
| openings | co2_kg_per_m2 | NA | NA | kg CO2eq/m2 GFA | NA | Reclaimed-brick wall openings (lintels, jambs) are formed in brick + mortar without separate components. K.118 reused steel windows from a Zürich office building — that is the openings parameter for that case but is not brick. Brick lintels: small carbon, dominated by new-mortar, reported jointly under structure row. | NA | missing |
| openings | labor_hours_per_m2 | 0.5 | 1.5 | h/m2 | — | Indicative only: reclaimed-brick lintel formation adds ~ 0.5–1.5 h per m² of opening to the structure-phase laying rate. Not normalised to GFA — needs cross-strand reconciliation. | engineering judgement on Salmio_Huuhka_2026 + BEDEC | 3 |
| openings | time_days | NA | NA | days | — | — | NA | missing |
| openings | cost_eur_per_m2 | NA | NA | EUR/m2 | — | — | NA | missing |
| openings | material_origin | "reclaimed timber lintels (if available) or new RC lintels" | "reclaimed steel lintels from urban mining" | — | — | K.118 demonstrated reused-steel lintels from Basel-sourced steel skeleton building. No primary data on Catalan reclaimed lintel supply. | insitu_K118 | 2 |

## Finishing

| phase | parameter | value_low | value_high | unit | allocation_rule | assumption | source_key | tier |
|---|---|---|---|---|---|---|---|---|
| finishing | co2_kg_per_m2 | 0 | 5 | kg CO2eq/m2 GFA | cut-off | Exposed reclaimed-brick walls require minimal finishing (no render or paint typically applied — the surface is the architectural feature). Carbon attributable to finishing ≈ 0–5 kg CO₂eq/m² (sealant, optional repointing mortar). | RBC_EPD_2024 (system boundary) + IAAC_Mat_Mining (architectural convention) | 1 / 2 |
| finishing | labor_hours_per_m2 | 0.2 | 1.0 | h/m2 | — | Repointing + cleaning of exposed face ~0.2–1.0 h/m². No render/skim layer needed. | Salmio_Huuhka_2026 (cleaning step) | 1 |
| finishing | time_days | 1 | 4 | days | — | Repointing + final cleaning for a ~100 m² wall area. | engineering judgement on Salmio_Huuhka_2026 | 2 |
| finishing | cost_eur_per_m2 | 5 | 20 | EUR/m2 | — | Repointing labour + sealant. Catalan baseline: BEDEC 2026 lists rendered-facade finishing at €15–35/m²; reclaimed-brick exposed face is at the lower end because no render is needed. | BEDEC_2026 (proxy) | 2 |
| finishing | material_origin | "lime-based pointing mortar (locally batched)" | "hydraulic-lime mortar (local quarry within 100 km)" | — | — | Lime mortar preferred for compatibility with old reclaimed bricks; cement mortar is technically possible but reduces future-reclaim potential (third-life loss). | Salmio_Huuhka_2026 + Devos_2024 | 1 |

---

## Populated-cell count

- 5 phases × 5 parameters = 25 cells.
- **Structure: 7 populated rows** (3 sibling allocation rows for `co2_kg_per_m2` + 4 single rows for the other parameters) — meets the brief's call-out for 2–3 sibling rows.
- **Foundation: 1 populated** (material origin disclosure).
- **Roof: 0 populated** (5× missing) — by design; reclaimed brick is not a roof material.
- **Openings: 2 populated** (one Tier-3 engineering-judgement and one Tier-2 origin) — flagged for cross-strand reconciliation.
- **Finishing: 5 populated.**
- **Total populated: 15** (≥ 6 required by brief). Of these, **9 are Tier 1**, **4 are Tier 2**, and **2 are Tier 3 (engineering judgement)** clearly marked.

## Allocation-rule swing summary (load-bearing finding)

For the same physical wall (350 kg/m² of reclaimed brick + new lime mortar, 50 km transport):

| Allocation rule | Reported A1–A3 GWP per m² wall | Source |
|---|---|---|
| Cut-off (brief recommendation) | **8–25 kg CO₂eq/m²** | RBC EPD 2024; Salmio & Huuhka 2026 |
| Avoided burden (RBC EPD A–C total) | **18–45 kg CO₂eq/m²** (A1–A3 equivalent) | RBC EPD 2024 |
| System-expansion / 50-50 split | **35–70 kg CO₂eq/m²** | De Wolf et al. 2020 (K.118 case); EU PEF method family |

**The lowest and highest values differ by ~5×.** This is not a contradiction — it is the finding. The installation's methodology-wobble overlay must surface the rule choice or the headline number is dishonest.

## Cross-method comparison context (for the BASELINE FLOOR role)

For wall comparison only (not whole-building):
- Reclaimed brick vs new fired brick (cut-off): **−86 % to −95 % GWP** (Salmio & Huuhka 2026; Devos 2024).
- Reclaimed brick vs new RC: −63 % to −74 % at the structural-element scale (Devènes 2022 — direct evidence for cut concrete blocks; analogous behaviour expected for brick).
- Whole-building reuse (K.118): **−60 % GHG** at building scale, ≈ 70 % component reuse.

These are the relative reductions the installation will plot the other three methods AGAINST when reclaimed brick is the floor.

## Geographic-transfer caveat

All Tier 1 reclaimed-brick LCA evidence is **Finnish (Salmio & Huuhka), UK (RBC EPD), Belgian/Dutch (Devos), Swiss (Re:Crete, K.118)**. None is Catalan. The installation must either:
1. Use the EU proxy values with explicit "non-Catalan" disclosure on the methodology overlay, or
2. Commission a Catalan inventory study before any final exhibition copy claims a region-specific number.
