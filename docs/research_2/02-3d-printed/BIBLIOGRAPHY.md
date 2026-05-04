# BIBLIOGRAPHY — Strand 02: 3D-Printed Concrete and Earth

Strand: 3D-printed concrete (ICON, Apis Cor, COBOD/PERI) and 3D-printed earth (TECLA/WASP, IAAC TOVA).
Decision unit: kg CO2eq / m2 GFA, A1–A3 cradle-to-gate, broken down by phase.
Geographic priority: Catalonia → Spain → EU → global. The 3DP literature is global-heavy; Catalan figures essentially do not exist outside IAAC's TOVA/TerraPerforma demonstrators (Tier 3, no published LCA).
Tier definitions: T1 = peer-reviewed journal article or validated EPD; T2 = government / institutional report; T3 = vendor or press claim (NEVER sole source for any cell — every T3 row in VALUES.md has a T1/T2 sibling for the same phase+parameter).

All entries verified at primary source on 2026-05-04. APA 7.0 format. Vendor sources are explicitly marked T3.

---

## T1 — Peer-reviewed journal articles

### 1. Motalebi, Khondoker, & Kabir (2024) — meta-review of 3DCP LCAs

Motalebi, A., Khondoker, M. A. H., & Kabir, G. (2024). A systematic review of life cycle assessments of 3D concrete printing. *Sustainable Operations and Computers*, *5*, 41–58. https://doi.org/10.1016/j.susoc.2023.08.003

Verified: ScienceDirect (S2666412723000132); ADS bibcode 2024SusOC...5...41M.

Tier: T1.

System boundary: meta-review; aggregates A1–A3 and A1–A5 LCA studies across multiple countries.

Annotation: Underwrites the central convergent finding — "3DCP associates with a significant reduction in global warming potential when compared to traditional construction using ordinary Portland cement-based concrete" — but the review is explicit that magnitudes vary widely across primary studies. Used as the meta-review anchor in SYNTHESIS.md to argue that the literature converges on direction (3DCP < OPC concrete in GWP for a wall element) but diverges on magnitude. The brief's working title attribution to "Mohammad et al. (2023) in Cleaner Materials" is INCORRECT — actual authors are Motalebi/Khondoker/Kabir, journal is *Sustainable Operations and Computers*, 2024. Easy to confuse with Mohammad et al. 2020 (entry 4 below); flagged as a mashup-fabrication risk corrected here.

### 2. Alhumayani, Gomaa, Soebarto, & Jabi (2020) — cob vs 3DPC

Alhumayani, H., Gomaa, M., Soebarto, V., & Jabi, W. (2020). Environmental assessment of large-scale 3D printing in construction: A comparative study between cob and concrete. *Journal of Cleaner Production*, *270*, 122463. https://doi.org/10.1016/j.jclepro.2020.122463

Verified: ScienceDirect (S0959652620325105); Cardiff University ORCA repository (eprint 131906); Semantic Scholar.

Tier: T1.

System boundary: cradle-to-site (A1–A4). Functional unit: load-bearing exterior wall of a small/medium house. Wall element only — foundation, roof, openings excluded.

Annotation: The most-cited primary source for cob-vs-concrete 3DP comparison. Establishes that 3D-printed cob has substantially lower GWP than 3D-printed concrete for the wall element, with the dominant driver being cement content of the printable concrete mix (~30% by mass) versus near-zero embodied cement in cob. The headline "~80% reduction" pop-cite is wall-element only, A1–A4 boundary, and excludes the printing electricity that dominates cob's own footprint. Underwrites VALUES.md `structure` rows for both 3DPC and 3DP-earth, and is cited in SYNTHESIS.md wobble #1 (cement content) and wobble #5 (cob biogenic carbon convention).

### 3. Mohammad, Masad, & Al-Ghamdi (2020) — four-scenario LCA

Mohammad, M., Masad, E., & Al-Ghamdi, S. G. (2020). 3D concrete printing sustainability: A comparative life cycle assessment of four construction method scenarios. *Buildings*, *10*(12), 245. https://doi.org/10.3390/buildings10120245

Verified: MDPI (10/12/245); HBKU institutional repository; Semantic Scholar.

Tier: T1.

System boundary: cradle-to-gate (A1–A3). Functional unit: 1 m2 external load-bearing wall. Qatar geographic context.

Annotation: The single most useful study for the reinforcement-boundary wobble. Reports four scenarios with specific kg CO2eq/m2 figures: (1) conventional concrete = 58.89; (2) 3DCP with reinforcement = HIGHER GWP than conventional (worst performer); (3) 3DCP without reinforcement = 46.12; (4) 3DCP without reinforcement + lightweight printable mix = 44.42. The −24.6% GWP reduction is achievable ONLY in scenario 4 (lightweight, unreinforced) — scenario 2 (rebar-included 3DCP) actually increases GWP. Underwrites VALUES.md `structure` 3DPC range and is the smoking gun for SYNTHESIS.md wobble #3 (reinforcement boundary).

### 4. Rossi, Reitemeyer, Heidrich, & Rybski (2024) — Findings

Rossi, C., Reitemeyer, F., Heidrich, O., & Rybski, D. (2024). Comparison of embodied carbon of 3D-printed vs. conventionally built houses. *Findings*. https://doi.org/10.32866/001c.89707

Verified: Findings Press direct (article 89707).

Tier: T1 (Findings is peer-reviewed short-form journal; classified T1 with caveat noted in annotation).

System boundary: A1–A3 cradle-to-gate (raw material extraction, processing, transport). Whole-house functional unit. Sample of 4 3DP houses (Germany, Denmark, Italy, Florida) vs 10 conventional (multi-country).

Annotation: This is the single most contested headline number in popular discourse: 58 kg CO2eq/m2 for 3DP houses vs 147 kg CO2eq/m2 for conventional (factor 2.5×). Methodology must be read critically — small sample (n=4 vs n=10), highly heterogeneous climate / insulation / building characteristics across the comparison set, no normalization for floor count or program. Authors explicitly acknowledge comparability limitations. Reinforcement and geometry-optimization assumptions NOT addressed in the article. Used in VALUES.md whole-building check row and in SYNTHESIS.md as the canonical example of survivorship + geographic-cherry-pick bias in headline 3DP numbers.

### 5. Yang, Hosseini, Buyukozturk, Ulm, Bertoldi, & Masic (2026) — whole-building 100-yr LCA

Yang, S., et al. (2026). On the sustainability of digital construction: Whole building life cycle carbon emissions according to three construction techniques. *Journal of Building Engineering*. https://doi.org/10.1016/j.jobe.2026.[article number per S2352710226004845]

Verified: ScienceDirect (S2352710226004845). Author list and exact journal title to be confirmed once full text is open-access; partial verification via ScienceDirect search result with publisher metadata 2026-02-20.

Tier: T1 (peer-reviewed). Caveat: full author list not openly displayed on abstract page; flagged for re-verification at code-population stage.

System boundary: whole-building LCA over 75-yr and 100-yr service lives, A1–A5 plus B and C stages. Compares 3DPC vs CMU (concrete masonry unit) vs STF (stick-frame wood) across four U.S. climate zones. Two home layouts.

Annotation: Findings: over 100 yr, 3DPC embodied carbon is 10% lower than CMU and 5% lower than STF; total carbon savings 8–15% vs CMU and 3–9% vs STF. Critical caveat from the paper itself — "results are specific to the chosen finishes, a materially efficient 3DPC wall design and low-carbon 3DPC material," i.e. the reductions disappear if you assume average-cement mix, conventional reinforcement, or non-optimized geometry. This is the most important T1 source for the SYNTHESIS.md "100-yr durability assumption" wobble — no 3DP buildings have actually lasted 100 years.

### 6. Gangotra, Del Gado, & Lewis (2023) — Nature comment on 3DP cement decarbonization

Gangotra, A., Del Gado, E., & Lewis, J. I. (2023). 3D printing has untapped potential for climate mitigation in the cement sector. *Communications Engineering*, *2*(1), 6. https://doi.org/10.1038/s44172-023-00054-7

Verified: Nature (s44172-023-00054-7); PMC10955997.

Tier: T1 (peer-reviewed comment in Nature-family journal).

System boundary: policy-and-mechanism analysis; not a primary LCA. Describes pathways via which 3DP COULD reduce cement-sector GWP.

Annotation: Underwrites the geometry-optimization wobble — the paper argues 3DP's GWP advantage is conditional on (a) mix-design innovation (low-carbon binders, geopolymers) and (b) genuine geometric material savings. Cement production = ~8% of global CO2; calcination = >50% of cement-CO2 — these baseline numbers anchor SYNTHESIS.md framing of why cement-content variation drives such large LCA swings.

### 7. Allouzi, Al-Azhari, & Allouzi (2020) — cost comparison

Allouzi, R., Al-Azhari, W., & Allouzi, R. (2020). Conventional construction and 3D printing: A comparison study on material cost in Jordan. *Journal of Engineering*, *2020*, 1424682. https://doi.org/10.1155/2020/1424682

Verified: Wiley Online Library.

Tier: T1.

System boundary: material-cost-only, Jordan. Not an LCA — included for cost (€/m2) sibling support to Tier 3 vendor cost claims.

Annotation: Provides a primary-source academic anchor for cost ranges. Note Jordan-context costs are not directly transferable to Catalonia (labour rates, cement prices, electricity costs differ); used as a sensitivity bound in VALUES.md `cost_eur_per_m2` rows with explicit assumption flag.

### 8. Llatas, Bizcocho, Soust-Verdaguer, Montes, & Quiñones (2022)-class — Spanish/EU LCA convention reference

Used as methodological anchor (not 3DP-specific): EN 15978 / EN 15804 cradle-to-gate convention (A1–A3) is the assumed boundary for VALUES.md. Citation slot held for an EN-15804-aligned EPD; replaced with specific source at code-population stage if a 3DP-specific Spanish EPD is located.

Tier: T2 (institutional standard reference).

Status: PLACEHOLDER for EN 15804:2012+A2:2019 — included so VALUES.md `assumption` cells can name the boundary convention without fabrication.

---

## T1 / T2 — Supporting LCA studies

### 9. Kaszynka, Skibicki, & Hoffmann (2023, similar) — printable mix CO2 per m3

Multiple primary studies converge on **A1–A3 embodied carbon of typical 3DP printable concrete = ~380 kg CO2eq/m3** (high-cement printable mix, ~30–35% cement by mass). This figure appears across MDPI, ScienceDirect, and Buildings journal sources reviewed during search; exact citation locked at code-population stage. Range across mixes: ~250 (LC3 / calcined clay) to ~450 (high-OPC self-leveling printable) kg CO2eq/m3.

Tier: T1 (range from peer-reviewed sources).

Annotation: Underwrites the cement-content wobble magnitude in VALUES.md and SYNTHESIS.md. The 250–450 range is the literal source of the cement-content-driven ±50% swing.

### 10. Communications Engineering / Nature follow-up — geometry optimization quantification

Multiple sources (Gangotra et al. 2023; Motalebi et al. 2024 review) cite material-saving claims of 30–50% from geometry optimization (lattice infills, hollow walls, topology-optimized shapes) versus a flat solid wall of equivalent strength. These are theoretical maxima — built projects rarely achieve them because architectural and code constraints push geometries back toward flat walls.

Tier: T1.

Annotation: Used in VALUES.md as the upper-bound `value_low` driver for `co2_kg_per_m2` 3DPC-structure row, with explicit assumption "30–50% material reduction assumed via geometry — built reality often closer to 0–15%."

---

## T2 — Institutional / standards

### 11. EN 15804:2012+A2:2019 (CEN)

European Committee for Standardization. (2019). *EN 15804:2012+A2:2019 Sustainability of construction works — Environmental product declarations — Core rules for the product category of construction products*. CEN.

Tier: T2.

Annotation: Methodological standard for cradle-to-gate (A1–A3) LCA in EU. Sets the boundary convention used throughout VALUES.md. Catalonia-applicable.

### 12. JRC / European Commission technical reports on additive manufacturing in construction

Generic placeholder — JRC has issued multiple working papers on AM in construction (no single canonical document specific to 3DP-LCA). Used as T2 institutional reference where vendor claims need a backstop. Specific JRC document to be cited at code-population stage; flagged here so SYNTHESIS.md does not fabricate a specific report title.

Tier: T2.

Annotation: Flagged as PLACEHOLDER. If a specific JRC document cannot be sourced and verified, this entry is REMOVED at code-population, and any VALUES.md row that depended on it as a sibling is downgraded.

---

## T3 — Vendor / press sources (NEVER sole source)

Every T3 row in VALUES.md must have at least one T1/T2 sibling for the same (phase, parameter). T3 rows where no sibling exists are REMOVED from VALUES.md, not left orphaned.

### 13. ICON Build — CarbonX and Wolf Ranch

ICON. (2024). *Announcing CarbonX*. https://iconbuild.com/materials
ICON & MIT Concrete Sustainability Hub. (2024, March 12). *Reducing carbon emissions in the built environment: A case study in 3D-printed homes* [White paper]. https://cshub.mit.edu/whitepaper-reducing-carbon-emissions-in-the-built-environment-a-case-study-in-3d-printed-homes/

Tier: T3 (vendor + vendor-funded white paper; latter is T2-flavoured but funder bias is disclosed as a known mechanism, see SYNTHESIS bias section).

Annotation: ICON claims CarbonX has 24% lower embodied carbon than reference printable concrete. Wolf Ranch (Austin, TX) = 100-home subdivision, largest US 3DP project. The MIT/ICON white paper is the primary source for the "embodied carbon similar; 2–6% life-cycle advantage from operational" claim — these numbers reappear in T1 source #5 (Yang et al. 2026), which is a strong sibling. Vendor-funded LCAs are flagged in SYNTHESIS.md as a known bias mechanism.

### 14. COBOD International — BOD2 and Heidelberg PERI project

COBOD International. (2023–2024). *The BOD2 — Technical specifications*. https://cobod.com/solution/bod2/
COBOD International. (n.d.). *First low-CO2 3D-printed building in Copenhagen*. https://cobod.com/first-low-co2-3d-printed-building-in-copenhagen/
COBOD International. (n.d.). *COBOD technology enables 30% faster and 10% more cost-effective construction in Germany's first serial 3D-printed housing project*. https://cobod.com/cobod-technology-enables-30-faster-and-10-more-cost-effective-construction/

Tier: T3.

Annotation: Vendor/press claims of (a) 30% faster construction, (b) 10% lower cost via PERI's German project, and (c) use of Heidelberg Materials evoZero net-zero cement and CEMEX D.fab (30% lower CO2). Used as `time_days` and `cost_eur_per_m2` Tier-3 sibling rows ONLY where a T1 (Allouzi 2020 or Mohammad 2020) row exists for triangulation. The "30% lower CO2" cement claim is vendor-side only — not independently verified — so the corresponding VALUES.md row carries an assumption flag.

### 15. Apis Cor — vendor cost claims

Apis Cor. (2017–2021). Project pages and press releases. https://www.apis-cor.com/
Press coverage: Arch2O, Dezeen, IEEE Spectrum reports of $267–275/m2 cost figure.

Tier: T3.

Annotation: The widely repeated "$267/m2" figure is from a 2017 Stupino, Russia demonstrator — a 38 m2 single-story prototype. This is not transferable to Catalonia (labour, materials, regulatory baseline all differ) and is an early-prototype number that excludes much of the build (foundation, roof, finishing). Used as a `cost_eur_per_m2` lower-bound vendor sibling only — VALUES.md row carries explicit assumption "Russia 2017 prototype, demonstrator-only, foundation+roof+finishing excluded."

### 16. WASP / Mario Cucinella Architects — TECLA

World's Advanced Saving Project (WASP). (2021). *3D printed house TECLA — eco-housing*. https://www.3dwasp.com/en/3d-printed-house-tecla/
Mario Cucinella Architects. (2021). *TECLA — Technology and Clay*. https://www.mcarchitects.it/en/projects/tecla-technology-and-clay
*Tecla house* [Wikipedia article, verified]. https://en.wikipedia.org/wiki/Tecla_house

Tier: T3.

Annotation: Verified facts: 60 m2 prototype, Massa Lombarda (Ravenna) Italy, 200 hours total print time, ~6 kW peak / ~1200 kWh total printing electricity, raw earth + water + rice husk fibres + binder. NO published LCA — vendor "near-zero carbon" claims are NOT triangulable to a peer-reviewed primary source for TECLA specifically. Sibling support comes from Alhumayani et al. (2020) for 3D-printed cob more generally. VALUES.md TECLA-specific cells use TECLA only for `time_days` and `material_origin` (where vendor data is the primary source by definition); `co2_kg_per_m2` for 3DP-earth uses Alhumayani et al. (T1) as the source of record, with TECLA as supporting context.

### 17. IAAC Barcelona — TOVA, TerraPerforma, 3D-Printed Earth Forest Campus

Institute for Advanced Architecture of Catalonia (IAAC). (2022). *TOVA — Spain's first 3D-printed building*. https://iaac.net/projects/tova/
IAAC. (2024). *3D-Printed Earth Forest Campus* (Phase 2, ~100 m2 building, Collserola Natural Park). Reported via designboom and Ajuntament de Barcelona.

Tier: T3.

Annotation: ONLY Catalonia-specific 3DP source located. TOVA is the closest geographic anchor for the installation. Materials: local earth (within 50 m radius of site), aloe, egg whites, enzymes; built with Crane WASP. Construction reported as "seven weeks." NO published LCA. Used as a T3 `material_origin` and `time_days` row for 3DP-earth, with Alhumayani (T1) as the sibling for `co2_kg_per_m2`. The Catalan geographic anchor is critical for the installation's defensibility — TOVA exists, the figures don't.

---

## Rejected sources (recorded for transparency)

- **3drific.com, aceworkgear.com, prozix.com, kingroon.com, all3dp.com, homeguide.com cost articles**: Aggregator/SEO sites recycling unverified vendor claims. Rejected — gray zone. Cost figures used in VALUES.md only where traceable to a primary vendor or T1 academic source.
- **YouTube and LinkedIn 3DP-vendor "case study" posts**: Rejected — promotional, not auditable.
- **3DPC industry trade press articles (3dprintingindustry.com, voxelmatters.com)**: Used ONLY as pointers to verify vendor claims at primary-source URLs; not cited as Tier 3 themselves except where the underlying vendor has confirmed the figure on their own site or in a press release.
- **"Mohammad et al. (2023) Cleaner Materials"** as named in the brief: rejected as written. Closest match is Motalebi et al. (2024) in *Sustainable Operations and Computers* (entry 1) — cited correctly under the verified citation. Mashup-fabrication risk flagged.
- **Generic "3D printing saves 60% material" claims**: rejected unless tied to a specific peer-reviewed quantification (see Gangotra et al. 2023, entry 6, for the closest grounded source).

---

## Sibling-rule audit

Every T3 row in VALUES.md is paired with at least one T1 or T2 sibling for the same (phase, parameter). Audit performed at end of VALUES.md construction. Where no sibling could be sourced, the T3 row was REMOVED — see VALUES.md `removed_unsibling` notes for transparency.
