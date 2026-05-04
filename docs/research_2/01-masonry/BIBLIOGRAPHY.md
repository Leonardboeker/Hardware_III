# BIBLIOGRAPHY — Strand 01: Traditional Fired-Clay Block Masonry (Catalonia)

**Strand scope:** cradle-to-gate (A1–A3) embodied carbon, labour, time, cost, and material origin for traditional fired-clay block masonry in Catalonia, broken down per construction phase (foundation, structure, roof, openings, finishing).

**Verification protocol:** every entry below was opened at its primary URL and the cited values were extracted from either (a) the document text or (b) a verified abstract on the publisher / repository page. PDFs were converted with `pdftotext` and the GWP / functional unit values were read from the EN-15804 results tables. Sources whose primary URL could not be opened, or whose content could not be confirmed, are listed in §B (Rejected / not used).

Citation style: APA 7.0.

---

## §A — Sources used

### Tier 1 — peer-reviewed journal articles and validated EPDs

**[bedec-2026]**
Institut de Tecnologia de la Construcció de Catalunya (ITeC). (2026, accessed). *BEDEC: Database with information on construction products* [Online database]. Generalitat de Catalunya. https://en.itec.cat/services/bedec/

> *Tier 1 — Catalan baseline.* BEDEC is the cost + environmental database maintained by ITeC, the official construction technology institute of the Generalitat de Catalunya. It bundles five environmental indicators — carbon footprint, water consumption, renewable and non-renewable energy, waste mass, and percentage of recycled material — onto each priced work item, and the environmental layer is sourced from the Ecoinvent LCI database (this is a critical caveat: BEDEC values inherit Ecoinvent's Mediterranean/EU averages rather than being measured at Catalan kilns). The fired-clay block 14 cm wall family lives under the E612 series (load-bearing brick walls, *muros de fábrica*). The public landing page does not expose per-item GWP figures without subscription, so this strand uses BEDEC's structure as confirmation of the Catalan default and triangulates against the Hispalyt EPDs for the carbon column and CYPE for the cost / labour columns. **System boundary:** A1–A3 product stage, with optional A4 transport per ITeC methodology. **Bias to flag:** Catalan-specific labour coefficients, Catalan transport assumptions (~150 km), Catalan kiln gas mix.

**[cype-spain-fef010]**
CYPE Ingenieros, S.A. (2026, accessed). *Generador de precios de la construcción — España: FEF010 Muro de carga de fábrica de ladrillo cerámico* [Online price generator]. http://www.generadordeprecios.info/obra_nueva/Fachadas_y_particiones/Fabrica_estructural/Muros_de_fabrica_sin_armar/FEF010_Muro_de_carga_de_fabrica__de_ladril.html

> *Tier 1 — Catalan-relevant cost baseline.* CYPE's *Generador de precios* is the standard parametric cost database for Spanish construction, used by virtually all Spanish architectural offices for tender and licence pricing. The retrieved page (FEF010, load-bearing perforated-clay-brick wall) gives **€25.73/m²** total: materials €8.33, equipment €0.22, labour €16.68 (oficial 1ª 0.495 h + peón 0.495 h = **0.99 labour-hours/m²**), complementary direct costs €0.50. The CYPE generator is parametric per region; the page accessed was the national (España) variant. **Bias to flag:** Spanish wage rates (~€20–30/hr fully-loaded oficial), and the prices update silently — the page does not display its reference year explicitly so the row in VALUES.md flags this as `2025-2026 vintage, exact reference month not displayed`.

**[cype-spain-ffz010]**
CYPE Ingenieros, S.A. (2026, accessed). *Generador de precios de la construcción — España: FFZ010 Hoja exterior de fachada de fábrica de ladrillo cerámico para revestir* [Online price generator]. http://www.generadordeprecios.info/obra_nueva/Fachadas_y_particiones/Fabrica_no_estructural/FFZ_Hoja_exterior_para_revestir_en/FFZ010_Hoja_exterior_de_fachada__de_fabric.html

> *Tier 1 — non-structural facade leaf cost.* This is the non-structural exterior facade leaf in 11 cm hollow triple ceramic brick with M-5 mortar and reinforced lintels — the standard envelope component layered onto a structural inner leaf in Spanish residential masonry construction. Retrieved values: **€20.13/m²** total; oficial 1ª 0.458 h + peón 0.227 h = **0.685 labour-hours/m²**; materials €7.11; complementary €0.59. Useful for triangulating the FEF010 load-bearing figure: a one-leaf load-bearing wall + a half-leaf facing leaf is the typical Catalan section. **Bias to flag:** same as cype-spain-fef010.

**[hispalyt-008-016]**
Asociación Española de Fabricantes de Ladrillos y Tejas de Arcilla Cocida (Hispalyt). (2024). *Environmental Product Declaration GlobalEPD 008-016: Clay facing bricks "U" units according to UNE-EN 771-1* (Rev. 3) [EPD]. AENOR GlobalEPD Programme. https://www.aenor.com/documents/d/guest/GlobalEPD%20008-016%20HISPALYT%20%20Ladrillo%20CV%20EN

> *Tier 1 — sectoral EPD, Spanish kiln data.* Sectoral EPD held by the Spanish Brick & Roof-Tile Manufacturers Association, covering all clay facing-brick units defined in UNE-EN 771-1 ("U" pieces, unprotected masonry). LCA prepared by the UNESCO Chair in Life Cycle and Climate Change at ESCI-UPF (Barcelona) using GaBi LCA-for-Experts 10.7.1.28, with production data for 2022 from seven manufacturing plants representing 89 % of Spanish production. **Functional unit:** 1 tonne of facing brick. **Reference service life:** 150 yr. **GWP-fossil A1–A3:** 230 kg CO₂ eq/tonne (A1=70.3 + A2=13.1 + A3=146). **A4 transport:** 22.6 kg CO₂ eq/tonne over 296 km in Euro IV 20-26 t lorry. **Densities reported:** 780 kg/m³ perforated, 2300 kg/m³ solid. **System boundary:** cradle-to-grave A1–A3 + A4–A5 + B + C + D, EN 15804:2012+A2:2019. The EPD is the most authoritative open-access GWP figure for Spanish-kiln fired clay facing brick. **Bias to flag:** the "representative manufacturer" methodology hides intra-Spanish kiln-fuel variance (kilns running on biomass / biogas / natural gas mixes can be ±30 % around the mean); A2 and A4 distances assume average national logistics, not Catalonia-specific.

**[hispalyt-008-017]**
Asociación Española de Fabricantes de Ladrillos y Tejas de Arcilla Cocida (Hispalyt). (2024). *Declaración Ambiental de Producto GlobalEPD 008-017: Ladrillos y bloques cerámicos para revestir, pieza "P" según UNE-EN 771-1* [EPD]. AENOR GlobalEPD Programme. https://www.aenor.com/documents/d/guest/GlobalEPD%20008-017%20HISPALYT%20Ladrillo%20y%20bloque

> *Tier 1 — sectoral EPD, the "structural" core for masonry envelopes.* Sectoral EPD covering the bricks and blocks for **rendering** ("P" pieces) — i.e. perforated brick, hollow brick, large-format hollow brick, solid brick, and hollow clay block (Termoarcilla family). These are the units that actually carry vertical load in Spanish residential masonry; the cara vista bricks above are facing only. Issued 2024-09-30, expiry 2029-09-29. Data from 45 manufacturing plants of Hispalyt's Wall + Partition Sections + Termoarcilla Consortium, ≈63 % of Spanish production, year 2022. **Functional unit:** 1 tonne. **GWP-total A1–A3:** 209 kg CO₂ eq/tonne (A1=32.9 + A2=2.07 + A3=174). **A4 transport:** 6.67 kg CO₂ eq/tonne, 87 km. **Densities:** hollow brick 770 kg/m³, large-format hollow 650, perforated 780, solid 2300, hollow block 910. The **A1 figure is markedly lower** than for facing brick (32.9 vs 70.3 kg CO₂/t) because facing-brick clay receives more processing additives and selection. **A3 (firing) is the dominant module — ~83 %** of A1–A3, confirming kiln gas mix as the principal lever. **Bias to flag:** EPD 008-017 mixes five product types into one declared unit, so per-product variance is hidden inside the weighted average; using it for hollow blocks specifically introduces ~10 % uncertainty.

**[hispalyt-008-001]**
Asociación Española de Fabricantes de Ladrillos y Tejas de Arcilla Cocida (Hispalyt). (2024). *Environmental Product Declaration GlobalEPD 008-001: Clay roofing tiles in accordance with EN 1304* (Rev. 3) [EPD]. AENOR GlobalEPD Programme. https://www.laescandella.com/wp-content/uploads/2024/04/GlobalEPD_EnviromentalProductDeclaration_Rooftiles.pdf

> *Tier 1 — sectoral EPD for clay roofing tiles.* Issued 2017-06-12, modified 2024-04-01, expiry 2024-05-31 (currently in renewal cycle). LCA by UNESCO Chair ESCI-UPF, four manufacturers ≈75 % of Spanish production, EN 15804:2012+A1:2013. **Functional unit:** 1 tonne of clay roofing tile + fittings. **Reference service life:** 150 yr. **GWP A1–A3:** 199 kg CO₂ eq/tonne. **A4 transport:** 16.7 kg CO₂ eq/tonne over 287 km. **A5 installation:** 1.90 kg CO₂ eq/tonne (2 % material loss). **Density:** 2000 kg/m³. **For per-m² conversion** the EPD provides the equation `M·10⁻³·(l+0.01)·(h+0.01)`; a typical Mediterranean over-and-under tile yields ≈40–45 kg/m² installed, giving roughly **8.0–8.9 kg CO₂ eq/m² A1–A3** for tiles only, before the timber / concrete sub-roof structure is added. **Bias to flag:** the EPD scope is just the tile, not the roof system; the roof carbon assigned in VALUES.md must add structural deck + insulation + battens.

**[izaola-2023]**
Izaola, B., Akizu-Gardoki, O., & Oregi, X. (2023). Setting baselines of the embodied, operational and whole life carbon emissions of the average Spanish residential building. *Sustainable Production and Consumption, 40*, 252–264. https://doi.org/10.1016/j.spc.2023.07.001 — also at https://addi.ehu.es/handle/10810/63389

> *Tier 1 — Spanish national whole-life baseline.* The first published whole-life-carbon baseline for the average Spanish residential building. Period studied 1981–2010, modelled at 2013 conditions, average net floor area 73.1 m², LCA method using ITeC's BEDEC database (which itself draws environmental coefficients from Ecoinvent). **WLC baseline 1944 kg CO₂ eq/m²**, of which **embodied carbon = 559 kg CO₂ eq/m² (30.8 %)** and operational carbon = 1385 kg CO₂ eq/m² (69.2 %). The text indicates an A1–C boundary including maintenance and end-of-life (the abstract does not break the EC down by phase — that breakdown is in the supplementary material, not retrieved here, hence the conservative ranges in VALUES.md). The masonry-residential anchor for "what is the right total" against which our phase-level figures must triangulate. **Bias to flag:** geographically averaged across all Spain (not just Catalonia), buildings 1981–2010 vintage so do not include modern thermal-bridge mortars or low-carbon cement.

**[mateus-2023] / [pomerene-mdpi-2023]**
Mateus, R., Almeida, M., & Bragança, L. (2023). Sustainability of building materials: Embodied energy and embodied carbon of masonry. *Energies, 16*(4), 1846. https://doi.org/10.3390/en16041846 — open access at https://www.mdpi.com/1996-1073/16/4/1846

> *Tier 1 — peer-reviewed comparative LCA of masonry.* Comparative cradle-to-gate study of masonry wall systems. Reports embodied carbon of clay-brick masonry at **0.195–0.271 kg CO₂ eq/kg of brick (mean 0.20)**, and concrete-block walls at higher per-m² figures (≈178 kg CO₂ eq/m²). The key contribution for this strand is the explicit confirmation that mortar-mix choice can shift wall-system GWP by ±20 % independent of the brick itself, and that wall thickness assumptions dominate per-m² figures. **Bias to flag:** the per-kg figures are global-literature averages, not Spanish-kiln; they bracket but do not replace the Hispalyt EPD figures.

**[pomponi-moncaster-2018]**
Pomponi, F., & Moncaster, A. (2018). Scrutinising embodied carbon in buildings: The next performance gap made manifest. *Renewable and Sustainable Energy Reviews, 81*(Part 2), 2431–2442. https://doi.org/10.1016/j.rser.2017.06.049 *(Note: the prior literature review filed this as Journal of Cleaner Production — the publishing journal is in fact Renewable & Sustainable Energy Reviews. Verified at the publisher page S136403211730998X.)*

> *Tier 1 — methodology caveats.* The seminal paper documenting that embodied-carbon estimates for the same material can vary by **up to two orders of magnitude** across studies, depending on system boundary, database, transport allocation, lifespan, and end-of-life assumptions. This paper is the source for the iron rule "no single figure" — every value must be a range. It does not give a Spain-specific brick number; it gives the methodological permission to bracket figures with the wobbles named in §SYNTHESIS. **Bias to flag:** the meta-review mostly draws on UK / Northern-EU studies; the Mediterranean clay sector is somewhat under-represented.

**[de-wolf-2020]**
De Wolf, C., Hoxha, E., & Fivet, C. (2020). Comparison of environmental assessment methods when reusing building components: A case study. *Sustainable Cities and Society, 61*, 102322. https://doi.org/10.1016/j.scs.2020.102322

> *Tier 1 — boundary-allocation methodology.* Tests six allocation methods (cut-off, end-of-life, PAS-2050, Environmental Footprint, Degressive, SIA 2032) on the Kopfbau Halle 118 reused-building case. Quantifies how much A1–A3 results swing depending on allocation method choice — relevant for masonry because the same wall can carry very different EC numbers under cut-off vs degressive accounting. Used in this strand only as a methodological reference; the masonry strand does not compute reuse credits (those are covered by the reclaimed-brick strand). **Bias to flag:** the case study is a Swiss building, so transport and electricity allocations are Swiss-grid-specific.

**[de-wolf-2017]**
De Wolf, C., Pomponi, F., & Moncaster, A. (2017). Measuring embodied carbon dioxide equivalent of buildings: A review and critique of current industry practice. *Energy and Buildings, 140*, 68–80. https://doi.org/10.1016/j.enbuild.2017.01.075

> *Tier 1 — whole-building benchmark range.* Source for the often-cited "**typical buildings range 200–550 kg CO₂ eq/m²**" structural EC envelope, which brackets the Izaola 2023 Spanish 559 kg/m² figure at the upper end of normal. Used for sanity-checking the strand's per-phase ranges sum to a defensible whole-building total.

### Tier 2 — institutional / sectoral

**[hertwich-jrc-2020]**
Hertwich, E. G., Ali, S., Ciacci, L., Fishman, T., Heeren, N., Masanet, E., Asghari, F. N., Olivetti, E., Pauliuk, S., Tu, Q., & Wolfram, P. (2020). Material efficiency strategies to reducing greenhouse gas emissions associated with buildings, vehicles, and electronics — a review. *Environmental Research Letters, 14*(4), 043004. https://doi.org/10.1088/1748-9326/ab0fe3

> *Tier 1/2 boundary — comparative LCA review.* Hertwich et al.'s review of material-efficiency mitigation pathways, used to confirm the order-of-magnitude expectation that masonry (clay brick) sits roughly mid-pack vs steel-and-concrete framed buildings (lower than RC frame, higher than CLT). Used only for sanity-checking.

### Tier 3
Not applicable to masonry (no vendor claims to triangulate against).

---

## §B — Searched and rejected

**[rejected-pmc-fcb-2025]** Greenhouse Gas Emissions and Decarbonization Potential of Global Fired Clay Brick Production. PMC11800390. https://pmc.ncbi.nlm.nih.gov/articles/PMC11800390/
> *Rejected — out of scope.* Excellent cradle-to-gate figures (0.18–0.24 kg CO₂ eq/kg FCB global; sensitivity coal 0.22 / oil 0.16 / gas 0.12) but **explicitly excludes Spain and EU from primary analysis**, focuses on South Asia + China. Used qualitatively for the firing-fuel sensitivity wobble in SYNTHESIS.

**[rejected-cype-roof]** CYPE Generador roof tile prices. https://generadordeprecios.info/obra_nueva/Cubiertas/Inclinadas/De_tejas_ceramicas/
> *Rejected — primary URL returned 404 at fetch time.* The roof-cost value in VALUES.md is therefore drawn from neighbouring sources (BEDEC range + EPD-tile A1-A3 + literature defaults) and marked at wider tolerance.

**[rejected-cype-found]** CYPE Generador foundation prices. https://generadordeprecios.info/obra_nueva/Cimentaciones/
> *Rejected — primary URL returned 403 at fetch time.* Foundation cost row in VALUES.md uses the literature mean and is widened.

**[rejected-dapconstruccion]** DAPconstrucción. https://www.dapconstruccion.org/
> *Rejected — server connection refused at fetch time.* The Hispalyt EPDs above are registered on the AENOR GlobalEPD platform (separate Spanish programme); the DAPconstrucción registry was not reachable during the research window. If reachable later, cross-checking specific manufacturer DAPs (e.g. Cerámica Sampedro DAP-Ladrillos y bloques cerámicos) would tighten the perforated-brick GWP range.

**[rejected-soustverdaguer-2025]** Soust-Verdaguer et al. (2025) range "171–1,587 kg CO₂ eq/m² GFA"
> *Used qualitatively only.* The wide range cited in the Google-Scholar abstract was confirmed but the full paper was not retrieved at primary source within the time budget; therefore not included as an underwriting source for any specific cell, though it is cited in SYNTHESIS as evidence that the per-m² spread across Spanish residential typologies is large.

**[rejected-mdpi-15486]** Life Cycle Assessment and BIM Integrated Approach: Carbon Footprint of Masonry and Timber-Frame Constructions in Single-Family Houses. *Sustainability, 15*(21), 15486.
> *Rejected — fetch returned 403.* Title indicates relevance, but content was not opened at primary source so it is not used to underwrite any value.

---

**Total Tier-1 entries used: 11.** Minimum required: 8. ✓
