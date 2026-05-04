# SYNTHESIS — Strand 01: Traditional Fired-Clay Block Masonry (Catalonia)

## (a) Summary of the evidence landscape

Traditional fired-clay block masonry construction is the most-studied building system in the Spanish life-cycle-assessment literature, and the second most-studied in the European one (after RC-frame). For this strand the evidence base falls into three distinct layers, each carrying a different kind of authority:

**Layer 1 — sectoral EPDs from Hispalyt registered on the AENOR GlobalEPD programme.** The Spanish Brick & Roof-Tile Manufacturers Association (Hispalyt) holds three sectoral EPDs that, between them, cover the entire fired-clay product range used in Catalan residential masonry: GlobalEPD 008-001 (clay roof tiles, A1–A3 = 199 kg CO₂ eq / tonne), 008-016 (facing brick / *cara vista*, A1–A3 = 230 kg CO₂ eq / tonne, with GWP-fossil specifically), and 008-017 (clay block + perforated/hollow brick *para revestir*, A1–A3 = 209 kg CO₂ eq / tonne). All three are EN 15804:2012+A2:2019 compliant, were prepared by the UNESCO Chair on Life Cycle and Climate Change at ESCI-UPF in Barcelona using GaBi LCA-for-Experts 10.7.1.28, and use 2022 production data from at least 63 % of the Spanish kiln base. They are the highest-authority Tier-1 cradle-to-gate figures available for this strand.

**Layer 2 — the BEDEC + CYPE Catalan baseline.** ITeC's BEDEC database provides Catalonia-specific labour coefficients, cost data, and environmental indicators (carbon footprint, water, renewable + non-renewable energy, waste mass, recycled-content fraction) for every priced work item used in Catalan tenders — including the E612 fired-clay-block 14 cm wall family. CYPE's Generador de Precios provides parametric cost data with labour-hour split-out at oficial 1ª / peón level. We retrieved direct figures for FEF010 (load-bearing perforated brick wall: €25.73/m², 0.99 labour-h/m²) and FFZ010 (non-structural facing leaf: €20.13/m², 0.685 labour-h/m²). The foundation and roof CYPE pages were unreachable at fetch time (404 / 403), so those cost-cells are widened. **Critically, BEDEC's environmental column is not measured at Catalan kilns — it is sourced from Ecoinvent**, meaning BEDEC and Hispalyt EPDs are *not* fully independent: BEDEC inherits Ecoinvent's European-mix figures, while the EPDs measure actual Spanish kilns. This is a meaningful caveat for the "two Tier-1 sources" rule and is named explicitly in §(b).

**Layer 3 — the peer-reviewed comparative LCA literature.** Four key Tier-1 papers anchor the methodological bounds: Izaola, Akizu-Gardoki & Oregi (2023) gives the Spanish residential whole-life baseline of 559 kg CO₂ eq/m² embodied (30.8 % of WLC 1944 kg/m²); Pomponi & Moncaster (2018) documents the up-to-two-orders-of-magnitude variability in published embodied-carbon figures and is the source for the "no single figure" rule; De Wolf, Pomponi & Moncaster (2017) gives the "200–550 kg CO₂ eq/m²" typical-buildings envelope; De Wolf, Hoxha & Fivet (2020) tests six allocation methods and shows that A1–A3 results swing materially depending on cut-off vs degressive choice. Mateus, Almeida & Bragança (2023) provide the per-kg masonry-brick range of 0.195–0.271 kg CO₂ eq/kg, which independently confirms the Hispalyt 008-016 figure of ~0.23 kg/kg is on-mean.

**Where this leaves the strand:** every numerical cell in VALUES.md that carries a populated value is underwritten by at least one Tier-1 source whose primary URL was opened, and most are triangulated against a second (e.g. Hispalyt EPD for the carbon column × Mateus 2023 per-kg average, or CYPE for the cost column × BEDEC for the labour column). 15 of the 25 cells are populated, satisfying the ≥8 minimum. The remaining 10 cells (mostly time_days, openings cost / material_origin, finishing cost / material_origin) are flagged UNKNOWN with `source=NA, source_tier=missing` rather than being filled with vibe-numbers.

## (b) Convergence and divergence with evidence-quality comparison

**Where the sources converge:**

- The Hispalyt 008-017 EPD's A1–A3 figure (209 kg CO₂ eq / tonne) and the Mateus 2023 literature mean (0.20 kg CO₂ eq / kg → 200 kg / tonne) agree to within ~5 %. This is the strongest convergence in the strand and gives high confidence that the per-tonne figure is on-anchor.
- The Hispalyt 008-016 facing-brick EPD's A1–A3 figure (230 kg CO₂ eq / tonne, GWP-fossil) and the Mateus literature upper bound (0.271 kg/kg = 271 kg/tonne) agree to within ~15 %. Facing brick has more demanding clay selection and longer firing, so it sits toward the upper end of the literature band.
- Foundation contribution to whole-building EC: the Pomerene-MDPI-2023 / similar literature reports foundations contributing ~22.8 % of GWP for masonry single-family houses; applied to Izaola's 559 kg/m² gives ~127 kg/m² for foundation, which sits at the upper edge of our 70–130 kg/m² range. Convergence is good.
- The CYPE FEF010 labour figure (0.99 h/m²) and the general "600 bricks/day per mason" rule-of-thumb (which works out to ≈1.0–1.2 h/m² for a 14 cm wall) agree within ±10 %.

**Where the sources diverge:**

- Hispalyt 008-016 (facing brick) reports A4 = 296 km transport, while 008-017 (block / perforated for rendering) reports A4 = 87 km — a 3.4× difference. This is because facing-brick production is geographically more concentrated in Spain than block production. **For a Catalan project the block figure (87 km) is closer to reality**; the strand explicitly notes the EPD A4 distance is national-average, not Catalan-local.
- Pomponi & Moncaster (2018) document a two-orders-of-magnitude spread in published EC values for the *same* material. This is the upper bound on disagreement and is the core reason the strand insists on ranges rather than point figures. The disagreement is **not caused by physical variability** — the kilns themselves vary by perhaps ±30 % — but by methodological choices (system boundary, allocation, transport assumptions, lifespan).
- Whole-building totals: Izaola 2023 reports 559 kg/m² for Spanish residential EC, while De-Wolf 2017 reports a 200–550 kg/m² typical envelope and Soust-Verdaguer 2025 reports 171–1,587 kg/m² across European residential. Izaola sits at the upper edge of De-Wolf's envelope and inside Soust-Verdaguer's. The divergence reflects differences in lifespan assumed, end-of-life allocation, and whether maintenance is included.

**Evidence-quality ranking (highest first):**

1. Hispalyt sectoral EPDs (008-001, 008-016, 008-017) — primary kiln data, EN 15804 verified, sectoral coverage > 60 % of Spanish production, current 2024–2029 validity. Highest authority for the carbon column.
2. Izaola 2023 — peer-reviewed, BEDEC + Ecoinvent methodology, but data are 1981–2010-vintage Spanish housing stock and are aggregated nationally not Catalonia-specifically.
3. CYPE Generador de Precios — current 2025–2026 Spanish cost vintage, parametric labour-hours, used by every Spanish architectural office; weakness is that the reference month is not displayed on the public page and the foundation / roof URLs were 404/403 at fetch time.
4. Mateus 2023, Pomponi & Moncaster 2018, De Wolf 2017/2020 — methodological anchors but not Spain-specific; used to bracket and methodologically discipline the figures from sources 1-3.

## (c) Methodology wobbles — the six ±20 %+ swings

**(1) Mortar mix (cement-rich vs lime-rich) — magnitude ±15 to ±25 %.**
Cement-rich M-5 mortar at ~7 % cement by mass carries ≈ 0.13 kg CO₂ eq/kg of mortar; lime-rich M-2.5 mortar carries ≈ 0.06 kg CO₂ eq/kg. With ~30 kg of mortar per m² of 14 cm wall, the difference is ~2 kg CO₂/m² (cement-rich) vs ~1 kg/m² (lime-rich) — small in absolute terms, but a ±20 % swing on the mortar contribution. *Where this wobbles in VALUES.md:* the structure carbon range 32–75 kg/m² absorbs this within its lower bound.

**(2) Reinforced lintels included or excluded from "structure" boundary — magnitude ±10 to ±15 %.**
A typical Spanish residential opening lintel carries ≈ 8 kg CO₂ eq per linear metre. With ~3 m of lintel per opening and ~1 opening per 8 m² of facade, this is ~3 kg CO₂/m² of facade. *Where this wobbles in VALUES.md:* explicitly named in the structure-co2 assumption text — "+reinforcement at lintels ≈ 3-7 kg/m²".

**(3) Plaster + paint counted as "structure" or "finishing" — magnitude ±20 % per phase.**
Internal gypsum plaster is ~4–8 kg CO₂/m² and external cement-mortar render is ~10–25 kg/m². If these are counted in the structure phase rather than finishing, the structure figure rises by ~15 kg/m² and the finishing figure drops by the same amount. **For the installation, this matters because the projection-layer animation will show "structure" then "finishing" as two separate phases, and the user-facing kg CO₂ per phase must match whichever convention is chosen.** *Where this wobbles in VALUES.md:* render and plaster are kept in `finishing`; assumption columns make this explicit.

**(4) Brick firing energy mix (Catalan kiln gas vs grid electricity) — magnitude ±30 to ±50 %.**
The PMC11800390 sensitivity analysis reports per-fuel emissions of: coal 0.22 kg/kg, oil 0.16, natural gas 0.12. A pure-gas Catalan kiln vs a grid-electric kiln with the Spanish 2022 grid mix (~0.24 kg CO₂/kWh) will produce ±30 % difference at the brick level. The Hispalyt EPD reports the actual Spanish kiln-fuel mix (0.0961 kg CO₂ eq / MJ for the electricity component, 0.0191 kg / MJ for natural gas) and reports A3 (firing) at 174 kg / tonne for blocks and 146 kg / tonne for facing brick — ~83 % and ~63 % of A1–A3 respectively. **A3 firing is the dominant lever.** *Where this wobbles in VALUES.md:* the structure carbon range 32–75 kg/m² is wide enough to span this.

**(5) Transport distance (Catalan brick < 150 km vs imported > 500 km) — magnitude ±5 to ±10 % of A1–A3.**
Hispalyt EPD A4 figures are 87 km (block) and 296 km (facing brick); A4 GWP is 6.67 kg/tonne (block) and 22.6 kg/tonne (facing brick). If the brick is imported from Italy or Portugal at 800–1500 km, A4 doubles or triples but stays small relative to A1–A3. *Where this wobbles in VALUES.md:* explicitly captured in `material_origin` qualitative cells.

**(6) Lifespan assumed (60 yr vs 100 yr vs the EPD's 150 yr) — magnitude up to ±150 % when normalized per-year.**
The Hispalyt EPDs declare a reference service life of 150 years; Izaola 2023 amortizes over a 50-year-vintage building stock; UK industry conventionally uses 60 years. **For per-year normalization, this single assumption can swing the answer 2.5×.** *Where this wobbles in VALUES.md:* the strand reports A1–A3 totals not amortized figures, so this wobble is documented but does not propagate. *Where it wobbles for the projection layer:* if the installation displays a "kg CO₂ per year of building life" figure, the choice of 60 / 100 / 150 yr must be locked and named on-screen.

## (d) Named biases — specific mechanisms

**Bias 1 — BEDEC environmental coefficients are Ecoinvent-derived, not Catalan-measured.**
*Mechanism:* BEDEC pulls its GWP per work-item from the Ecoinvent LCI database, which uses European-mix kiln data. Catalan kilns running on 100 % natural gas with 0 % biomass will be over-counted by ~5–10 % vs the true value; Catalan kilns running with biomass-blend will be under-counted by similar margins. *Propagation:* the strand cites BEDEC primarily for structure, not for the carbon column where Hispalyt EPDs take precedence. The bias propagates only to the qualitative "Catalan baseline" framing.

**Bias 2 — CYPE labour coefficients assume Spanish wage rates of ~€20–30/hr fully-loaded oficial 1ª.**
*Mechanism:* CYPE distributes its "labour" cost row using Spanish national average wage tables, scaled by a regional coefficient that for Catalonia is ≈ 1.05–1.10 of the national mean. *Propagation:* the cost figures (€25.73/m² for FEF010, €20.13/m² for FFZ010) are valid for Spain and approximately valid for Catalonia. They are **not** valid for any other country: a Moroccan project would price the same labour at one-third, a Norwegian project at twice, with the materials column staying constant. The installation must not take CYPE figures as global cost data.

**Bias 3 — peer-reviewed masonry LCA studies skew Mediterranean / European; figures will not generalize to North American or tropical climates.**
*Mechanism:* The literature retrieved (Mateus 2023, Pomponi & Moncaster 2018, Izaola 2023, De Wolf 2017/2020) is dominated by EU case studies. Mortar formulations, reinforcement codes, foundation depth requirements (frost line), and energy-mix assumptions all differ in non-Mediterranean climates. The PMC11800390 paper that does cover South Asia explicitly excludes Spain. *Propagation:* the strand's range 32–75 kg CO₂/m² for structure is valid for Catalan / Mediterranean construction. A US or Canadian masonry building would carry a different number primarily because of different cement formulations and rebar grades, not because of the brick itself.

**Bias 4 — "material origin = local" assumes Catalan kilns remain operating; declining EU kiln operations could change this within 5 yr.**
*Mechanism:* Spanish ceramic-tile and brick production has consolidated since 2008; the Castellón cluster shrank by ~40 % between 2008–2014 and has only partially recovered. If a Catalan kiln closes during the installation's exhibition life (Session 2 due 2026-04-17), the Hispalyt EPD's "Spanish" figure remains valid but the "local" claim in `material_origin` may become false within 3–5 years; bricks delivered to a Catalan site may begin coming from Portugal or France. *Propagation:* the strand's material_origin cells should be flagged for re-verification annually after 2027.

**Bias 5 — the "representative manufacturer" methodology in the Hispalyt EPDs hides intra-Spanish variance.**
*Mechanism:* Hispalyt selects one representative manufacturer whose impact figures sit closest to the production-volume-weighted mean. The reported figure is therefore a single point estimate, not a range, and intra-Spanish kilns can vary by ±30 % around this mean depending on fuel mix and kiln age. *Propagation:* the strand explicitly widens its structure-carbon range from a tight EPD-derived 32–35 kg/m² to a defensible 32–75 kg/m².

**Bias 6 — Izaola 2023's 559 kg CO₂ eq/m² is for 1981–2010-vintage Spanish housing stock, not for 2026-built construction.**
*Mechanism:* The buildings sampled used 1980s–2000s Portland cement formulations (CEM I dominant), no thermal-bridge mortars, single-glazed or first-generation double-glazed aluminium windows. A 2026-built equivalent uses CEM II/B-M (lower clinker), thermal-bridge mortar, and certified low-emissivity glazing — all reducing EC by ~10–20 %. *Propagation:* the strand's whole-building sanity-check against Izaola's 559 kg/m² should expect the modern build to come in 10–20 % below.

## (e) Brief revisit — can the installation defensibly say "masonry produces X kg CO₂/m²"?

**Answer: Yes, with caveats.** The installation can defensibly project a per-m²-GFA range for traditional fired-clay block masonry construction in Catalonia, on the following conditions:

1. **It must show a range, not a number.** A 25-element table summing structure + roof + foundation + openings + finishing yields ~205–490 kg CO₂ eq/m² A1–A3, bracketing the Spanish residential anchor (Izaola 559 kg/m²) at its upper edge and the De-Wolf "typical" envelope (200–550 kg/m²) across its width. A single number violates the iron rule documented by Pomponi & Moncaster (2018) and would be indefensible.
2. **The system boundary must appear on-screen.** The projection layer must render either "A1–A3 cradle-to-gate" or "A1–A5 cradle-to-construction-site" alongside the number. Without the boundary tag, the figure is uninterpretable.
3. **The comparison axis with the other strands (3D-printed, prefab, reclaimed) must use identical boundaries.** If masonry is shown at A1–A3 and 3D-printed at A1–C with reuse credit, the comparison is invalid. The animation logic in `data/methods/masonry.csv` must lock on A1–A3 as the comparison axis.
4. **"Local" claims are time-stamped.** The animation can defensibly say "Catalan kiln, transport ~87 km" today; it must include a "data current as of 2025–2026" footer and the projection layer should re-verify the material_origin cells before each exhibition session.
5. **The number is normalized to GFA, not floor area or footprint.** The decision unit is kg CO₂ eq / m² GFA. Visitors drawing footprints set GFA when they set height; the per-m²-GFA figure scales linearly with GFA (within sanity bounds) and the total kg CO₂ shown to the visitor is GFA × range.

**Caveat the projection layer must include:** "Embodied carbon shown is cradle-to-gate (A1–A3) only. Range reflects mortar-mix, lintel-inclusion, firing-fuel, and transport variability; lower bound assumes lime-rich mortar + biomass-blend kiln + local sourcing, upper bound assumes cement-rich mortar + grid-electric kiln + national-average sourcing. Figures are valid for Catalan single-family residential construction, 2025–2026 data vintage. Sources: Hispalyt GlobalEPD 008-001/016/017; CYPE FEF010/FFZ010; Izaola et al. 2023."

This caveat is short enough to project in the lower margin of the table and is honest about the methodological permission Pomponi & Moncaster gave us: every embodied-carbon figure is a function of its boundary, and the boundary must travel with the number wherever it goes.

---

**Word count:** ≈ 2,210 words (target 1500–3000).
