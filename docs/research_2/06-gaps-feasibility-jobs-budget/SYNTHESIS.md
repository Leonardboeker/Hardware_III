# Synthesis — Strand 06: Feasibility, Origin, Transport, Jobs, Carbon Budget

This strand fills five fields that the prior LCA-method strands (01 Masonry, 02 3D-printed, 03 Prefab, 04 Reclaimed brick) did not cover. The five sub-strands intentionally have different shapes: feasibility is a constraint table, origin and transport are geographic, jobs is politically charged, and carbon budget is sector-narrative framing. Below, each sub-strand gets an evidence landscape, named biases, a magnitude-of-wobble note, and a brief-revisit verdict on whether the installation can defensibly display the data and with what caveats.

---

## Sub-strand 6 — Feasibility constraints

### Evidence landscape

The feasibility envelope of each method is governed by four overlapping evidence types: (a) primary structural Eurocodes and the Spanish CTE, (b) emerging or in-process technology-specific codes (ICC 1150, ICC-ES ESR-4652), (c) built precedents that establish what is _physically_ achievable, and (d) manufacturer specifications that bound the practical envelope of the printer or factory.

For **masonry (M1)**, the picture is mature and stable. EN 1996-1-1 + CTE DB-SE-F set a slenderness ceiling (λ ≤ 27, where λ = effective height / effective thickness) and a minimum wall thickness (115 mm absolute, 240 mm typical for buildings of more than two storeys). In practice, Catalan low-rise residential masonry tops out at four storeys load-bearing unreinforced (five with reinforcing). The constraint is well-documented and uncontested.

For **3DPC (M2-C)**, the picture is fragmented. There is _no Eurocode_ for 3D-printed concrete as of May 2026. The most authoritative document is ICC 1150 (US, public-comment-draft November 2024), which permits 3DPC in single-storey and multi-storey load-bearing roles _provided_ specific reinforcement and acceptance-testing regimes are followed. ICC-ES ESR-4652 evaluates ICON's Lavacrete; equivalent EU evaluations for COBOD and Apis Cor systems exist on a project-by-project basis but no continent-wide standard. The de-facto upper-bound built precedent is Apis Cor's two-storey Dubai Municipality building (640 m², 9.5 m, 2019). The COBOD BOD2 specification (12 m × 27 m × 9 m printable envelope) gives a hard manufacturer-imposed limit on single-print volume.

For **3D-printed earth (M2-E)**, the situation is even more uncertain: there is no formal earth-construction Eurocode and no published precedent of a printed-earth dwelling that has been certified for residential occupation. TECLA (WASP × Mario Cucinella, 2021) is single-storey, 4.2 m peak, ~60 m². TOVA (IAAC, 2022) is single-storey, used as a research artefact at Valldaura Labs rather than a permitted dwelling. Earth construction has national-annex frameworks in France, Germany, and Italy for rammed earth and adobe — but printed earth specifically falls outside.

For **modular concrete MiC (M3-C)**, the built-precedent envelope is wide. InnoCell at HKSTP (Hong Kong, 2020, 17 storeys, 418 modules) is the verified built reference; Chun Wo declares design capacity to 40 storeys via "wall connection technology". Transport is the binding constraint outside Asia: Spanish road regulations (RD 970/2020 + 2024 update) permit modules up to 2.55 m × 4.0 m × 16.5 m without permit, or up to 3.0 m × 4.5 m × 20.55 m under a "Genérica" permit. Most factory-built rooms exceed 2.55 m wide, so the Genérica permit is the working envelope.

For **modular CLT (M3-T)**, EN 1995-1-1 (Eurocode 5) covers structural design and EN 1995-1-2 covers fire. There is no fixed storey ceiling; the binding constraint is fire-engineered alternate-means approval. Mjøstårnet (Norway, 2019, 18 storeys, 85.4 m, pure timber) and HoHo Wien (Austria, 2019, 24 storeys, 84 m, hybrid CLT + concrete core) both required negotiated approvals because pre-2008 Vienna code limited timber to four storeys.

For **reclaimed brick (M4)**, the formal limit is unwritten in modern European codes — reclaimed bricks fall under the same masonry codes as new bricks _if_ they pass strength testing. The Brick Industry Association (US) Tech Note 15 recommends 50 % of equivalent-new working stress as a conservative default. Practical built precedents in Europe top out at 2-3 storeys for fully load-bearing re-laid reclaimed brick, often less because individual brick variability constrains design.

### Named biases

- **Built-precedent bias.** Mjøstårnet, HoHo, Apis Cor Dubai, InnoCell are all used as "yes, you can do that" datapoints. They each represent the apex of an envelope, not the median; pretending they are reproducible is _selection-on-the-dependent-variable_.
- **Manufacturer-spec bias.** COBOD BOD2 specifications are used to bound single-print envelope. Manufacturers report nominal envelopes assuming idealised site conditions. Real Catalan job-site data (operator-experience, weather windows, mix-rheology variance) reduces the envelope by 10-20 %.
- **Code-translation bias.** Treating ICC 1150 (US draft) as a proxy for European 3DPC permitting silently imports US-specific reinforcement assumptions. In Catalonia, no equivalent text exists; permits are case-by-case.

### Wobble magnitude

Methodology wobble in feasibility is **categorical** rather than numerical: the meaningful wobble is whether a method passes or fails the gate. Storey-count headlines should be displayed as bands (e.g. "M3-T: 4 storeys typical, 24 demonstrated") not as points.

### Brief-revisit verdict

Defensibly displayable. The installation can show, for each method: (a) typical built envelope (where the method comfortably operates), (b) demonstrated maximum (the apex precedent), and (c) the binding constraint (code, transport, supply, certification). Avoid implying that the demonstrated maximum is achievable for a standard Catalan project — that would be selection-on-the-precedent.

---

## Sub-strand 7 — Material origin

### Evidence landscape

For Catalan-built projects, the four methods source materials over wildly different distances. Brick and OPC cement are dominantly Spanish and Catalan: Hispalyt's member network covers ~85 % of Spanish sectoral production (the previously-circulated "89 %" figure could not be re-verified at primary URL on 2026-05-04 and is treated as superseded by the 85 % figure). Cementos Molins's Sant Vicenç dels Horts plant — 15 km from central Barcelona — has been in operation since 1928. Cemex Spain runs Alcanar (Tarragona, ~200 km).

CLT's origin geography is starkly different. Stora Enso operates two CLT mills at Bad St. Leonhard (Carinthia) and Ybbs (Lower Austria); Hasslacher and Binderholz also operate principally from Austria and Germany. Sweden and Finland (Stora Enso Gruvön, Setra, Metsä Wood) are alternative origins, ~2 500-3 200 km away.

Earth (3DP) is the ground-truth opposite: TOVA, the IAAC project at Valldaura Labs (Collserola, on the Barcelona city margin), used material from a 50 m radius. Even without that empirical claim, the physics of earth construction means hauling sub-soil more than a few kilometres erases the carbon advantage immediately.

Modular concrete is, in Catalonia, a thin market. There is no widely-cited Spanish concrete-MiC supplier dominating the market the way Hong Kong's CIMC or Chun Wo do; high-rise concrete-MiC projects in Catalonia would currently require imports. The brief flagged this and the brief's claim is consistent with what was findable in 70 minutes of search.

Reclaimed brick is, by definition, urban-mined locally; the supply-chain constraint is that there is no centralised Catalan supplier and the BEDEC catalogue (Catalan industry standard reference) has no entry for `totxo recuperat` (locked from prior strand 04).

The brief's claim that ArcelorMittal Sagunto supplies rebar was found to be _factually incorrect_: Sagunto is a flat-products mill, not a long-products / rebar mill. Spanish-consumed rebar comes principally from ArcelorMittal Warsaw (Poland), Sonasid (Morocco), and Zenica (Bosnia-Herzegovina). This is a meaningful correction to the input brief.

### Named biases

- **Trade-association coverage bias.** Hispalyt's "85 % of Spanish sectoral production" is self-reported; the figure has not been audited by an independent body. The remaining 15 % includes both small Catalan cooperatives and imports — imports likely under-counted.
- **Mill-page bias.** Stora Enso and Hasslacher's location pages show the production mill but not the European distribution centres they ship through. Real CLT shipments to Barcelona may originate at a logistics yard 300 km closer than the production mill.
- **Survivorship bias on TOVA's 50 m radius.** TOVA is one project at one site (Valldaura). It was selected because the soil was print-friendly. A typical Catalan job site may not have print-grade subsoil within 50 m, requiring a quarry haul of several kilometres.
- **Brief-input verification gap.** The "ArcelorMittal Sagunto rebar" claim in the brief was carried forward from a prior strand without verification; this strand catches the error but cannot retroactively correct prior strands.

### Wobble magnitude

Origin granularity is wobble-low for Catalan brick and cement (well-located) and wobble-high for 3DP-mix admixtures, modular concrete, and rebar (multi-origin networks where any specific shipment's origin depends on procurement).

### Brief-revisit verdict

Defensibly displayable for brick, OPC, CLT, and 3DP-earth. Should be displayed with explicit "default origin assumed" labels for 3DP-concrete admixtures, modular concrete, and rebar, because these vary by procurement and the projection should not pretend to a precision the data does not support.

---

## Sub-strand 8 — Transport distance to Barcelona

### Evidence landscape

Transport distances follow directly from Sub-strand 7. Brick-Catalan-to-Barcelona is ~50 km. OPC from Sant Vicenç dels Horts is ~15 km. CLT from Austrian mills is ~1 850 km road or ~2 200 km via rail-truck. 3DP-mix in Spain is dominated by Spanish OPC at ~150 km; specialty admixtures travel further but represent a small fraction of mass and embodied transport. Earth at TOVA was <50 m. Realistic Catalan earth-printing projects are likely 1-20 km.

The Salmio & Huuhka (2026) paper provides the only peer-reviewed transport-threshold figure available for reclaimed brick: GWP-fossil savings vs virgin brick persist up to **480 km for hand-tool deconstruction (T1)** and **up to 315 km for excavator (T2)**. These are upper bounds; the carbon-positive zone narrows quickly past them. The brief's "100 km starts to erase advantage" framing is more conservative than the peer-reviewed thresholds — using the 480/315 km figures is more rigorous.

For modular components, Spain's Reglamento General de Vehículos sets the working road envelope: 2.55 m × 4.0 m × 16.5 m without permit, 3.0 m × 4.5 m × 20.55 m with a Genérica oversize permit (45 t gross). Most factory-built MiC modules require the Genérica permit. Above that, the "Específica" permit (up to 5 m wide × 40 m long × 110 t) exists but requires route approval and escorts — adding time and cost.

The Hispalyt EPD A4 baseline (87 km, claimed in the brief) could not be re-verified in this session because the GlobalEPD 008-016 PDF returned as binary and was not extractable. The figure is plausible (consistent with Catalan-plant-to-Catalan-site averages and with the AENOR GlobalEPD methodology) but is recorded as `UNKNOWN, source = NA` in VALUES.md to satisfy the iron rule against unverifiable references.

### Named biases

- **Single-route bias.** All road-distance figures here are point-to-point Google-Maps-grade and assume a single representative route. Real shipments are multimodal (rail-truck for >800 km, sea for >1 500 km from Sweden/Finland) and the LCA-A4 figure should be ±20 %.
- **Salmio-Huuhka generalisability bias.** The 480/315 km thresholds are computed against the Finnish electricity mix. Spanish electricity is less coal-intensive, so the carbon-erasure threshold could shift upward (i.e. reclaimed brick remains advantageous further) — but this has not been independently computed.
- **EPD-baseline bias.** Hispalyt's EPD-baseline transport distance is an industry-weighted average. Specific projects can be much closer (Piera ↔ Barcelona = 50 km) or further (Andalusian plants ↔ Barcelona ≥ 800 km). The point estimate hides this distribution.

### Wobble magnitude

Transport wobble is **medium-high**: ±20 % for road-only, ±50 % when multimodal. The reclaimed-brick threshold has its own wobble: the Salmio-Huuhka figure depends on grid-mix assumptions and could shift by 30 % or more in different national contexts.

### Brief-revisit verdict

Defensibly displayable. The installation should explicitly bracket transport bands (low/typical/high), and for reclaimed brick should display the threshold as a coloured zone (carbon-positive ≤ 480 km) rather than a hard line. The Hispalyt EPD-baseline figure should be re-verified before use as a numeric anchor.

---

## Sub-strand 9 — Jobs / employment impact

### Evidence landscape

This sub-strand is the most politically charged and the least empirically clean. There is no peer-reviewed Spanish-construction FTE-per-100m² table comparing the four methods at peer-review precision. What exists is:

1. **Spanish productivity benchmarks.** CaixaBank Research / BBVA Research report Spanish construction labour productivity at ≈ €112 400 GVA per FTE per year (2023), with productivity having dropped >20 % since 2013 in real GVA-per-hour terms. Spanish construction unemployment (INE 2024 Q1) is 14.8 %, vs national 13.1 %.
2. **Modular industry studies.** McKinsey's 2019 report and the WEF's January 2025 update both quote ~80 % of activity moves off-site, ~30 % fewer on-site labour hours, ~20-25 % total labour-cost reduction, factory labour ~2× as productive as in-situ. These are McKinsey-ecosystem figures and are _industry-favourable_ — they tend to LOWBALL labour-displacement effects because they re-classify on-site bricklayers replaced by factory operators as "preserved jobs", even if the worker cohort changes entirely.
3. **3DPC literature.** Hossain et al. (2020, _Sustainability_) reviews the 3DPC-construction literature and reports headline figures of 50-80 % labour-cost reduction. The authors are honest that these figures count direct on-site bricklayers + general-labour reduction, but rarely the offsetting tech-and-engineering FTE. So Hossain-and-similar are _BIASED HIGH_ on displacement.
4. **Case-study anecdotes.** Apis Cor Dubai (2019): 640 m², 2 storeys, "about half the usual number of construction workers, only 15." ICON: "single-story, 2 000 ft² home in 7-10 days with two operators." These are vendor-favourable case studies and substantiate the claim that 3DPC reduces _on-site count_, but say nothing about total system FTE (including factory-mix preparation, BIM modelling, machine maintenance, scaffold erection for non-printed elements).
5. **ILO labour-displacement framing.** ILO 2018 (`wcms_579554`) flags construction as one of the highest automation-risk sectors and explicitly warns that displacement is unevenly distributed: low-skill on-site labour (often immigrant, often informally contracted) bears the brunt. ILO 2025 (`WP140`) updates this with GenAI-exposure findings and confirms construction's _physical_-automation exposure is high while GenAI exposure is low.

### Named biases (with explicit direction per iron-rule 4)

- **McKinsey 2019, WEF 2025**: industry-favourable, _LOWBALL_ on labour displacement. McKinsey services modular-industry clients; WEF aligns with its corporate membership. Numerically reliable for productivity gains, but their framing of "preserved" jobs treats a Polish factory operator and a Catalan bricklayer as interchangeable — they are not.
- **Hossain et al. 2020**: peer-reviewed but vendor-data-derived; _BIASED HIGH_ on displacement.
- **ILO 2018 / 2025**: worker-protection multilateral; _BIASED toward labour-protective framing_, but quantitative method is Frey-Osborne-style (contested but neutral).
- **CaixaBank / BBVA Research**: bank-research-house framing emphasises productivity-and-investment; _BIASED toward investment-favourable narrative_, numerically reliable.
- **INE / OECD**: official statistics, bias-low.

The single most under-explored evidence type is _the Spanish labour-political voice_ (CCOO Construcción, UGT-FICA). They are not deeply searchable in English-language sources within this time budget. A second-pass Catalan-language search of CCOO and UGT-FICA position papers on automation and prefabrication is recommended.

### Wobble magnitude

FTE-per-100m² wobble is **±50 %** for all four methods. Skill-mix wobble is **±15 absolute percentage points**. Catalonia-specific data is essentially absent at peer-review precision. Treat all numbers as bands; do not display point estimates without ranges.

### Brief-revisit verdict

Conditionally displayable. The installation _should_ display jobs data, because the sub-strand connects to the S1 peer-review political-dimension critique that explicitly demands jobs visibility. But the projection layer must:

1. Show ranges, not points (e.g. "M2-C: 0.10-0.20 FTE/100m²" not "0.15").
2. Show the on-site / factory split explicitly (the on-site number is what the visitor's grandparent who lays brick for a living will lose).
3. Show the skill-distribution shift, not just total count (3DPC and modular don't just reduce headcount — they re-class labour from masonry-skilled to machine-tech-skilled).
4. Disclose its sources and their bias direction inline (e.g. "industry-source estimates lowball displacement; advocacy-source estimates overstate it; range here brackets both").

See `NARRATIVE-IMPLICATIONS.md` for the political framing.

---

## Sub-strand 10 — Remaining 1.5 °C carbon budget

### Evidence landscape

The Global Carbon Budget 2025 (released November 2025 by the Global Carbon Project, the canonical annual update) reports:

- 2025 fossil-fuel CO₂ emissions: 38.1 Gt; LUC 4.1 Gt; total +1.1 % vs 2024 (record high).
- Remaining 1.5 °C budget at start-2025 (50 % chance): "virtually exhausted" — breached within 4 years at the current rate. Headline residual quoted as ~170 Gt CO₂ at start-2025 (Climate Change Tracker arithmetic on the GCB-2025 numbers). Architecture 2030's earlier figure of 340-400 Gt at start-2020 has been consumed by the intervening five years of emissions.
- Remaining 1.7 °C budget: 525 Gt CO₂ (~12 yr at 2025 rate).
- Remaining 2.0 °C budget: 1 055 Gt CO₂ (~25 yr).

The construction sector's share of the global total, per UNEP Global Status Report 2024/25 (released March 2025):

- Buildings + construction: 32 % of global energy, 34 % of energy-and-process CO₂.
- Buildings sector emissions reached ~10 Gt CO₂ in 2023 (operational + embodied combined).
- Construction-only embodied (cement, steel, aluminium) ≈ 2.5 Gt/yr; brick + glass adds ~1.2 Gt/yr.
- New-construction-only emissions ≈ 7 % of global ≈ 2.5 Gt/yr.
- 28 % reduction by 2030 needed for Paris alignment.
- 2023 was the first decoupling year (sector emissions flat while floor-area grew 1 %).

### Named biases

- **Probability-threshold bias.** The "virtually exhausted" headline assumes 50 % chance of staying under 1.5 °C. For 67 % the budget is _already negative_ — exhausted late 2024. Headlines should always specify the threshold.
- **Baseline-temperature bias.** GCB / IPCC use 1850-1900 baseline; some sources use 1986-2005 (≈ 0.6 °C warmer). Not aligning baselines under-states the budget by ≈ 200 Gt.
- **UNEP framing bias.** UNEP is decarbonisation-advocacy; numbers are neutral but framing emphasises sector culpability. Use the numbers, not the frame.
- **Architecture-2030 advocacy bias.** Architecture 2030's "embodied carbon must reach zero by 2040" is an advocacy target, not a verified carbon-arithmetic conclusion. Verified carbon math (GCB) does not name a sectoral net-zero year; that is normative.

### Wobble magnitude

Carbon-budget wobble is **structurally large**: ±100 Gt for 1.5 °C across probability thresholds and modelling choices. The headline "virtually exhausted" is robust to those choices; specific point estimates are not.

### Brief-revisit verdict

Defensibly displayable as a live counter, _provided_:

- The displayed number is updated annually (GCB releases each November).
- The probability threshold and baseline-temperature window are shown next to the number.
- The construction-sector share is shown disaggregated (operational vs embodied) so the visitor can see what fraction of "the construction sector" is the buildings-method comparison the installation is actually about.
- The "1.5 °C virtually exhausted" framing is owned by the installation: it is the truth. Softer framings under-state the urgency.

A concrete recommended display: "Construction is 34 % of global CO₂. The 1.5 °C budget (50 % chance) is virtually exhausted as of January 2025 (Global Carbon Budget 2025-11). At the current emissions rate it will be breached within 4 years."

---

## Cross-cutting reflections

Three cross-cutting points emerge from the five sub-strands.

First, **the installation's epistemic asymmetry between methods is large**. Masonry feasibility, origin, transport, and even labour data are well-mapped (decades of code + EPD + INE statistics). 3D-printed earth has _no formal Eurocode_, _no Spanish FTE-per-m² literature_, _no peer-reviewed transport baseline_, and only experimental built precedents. The wobble layer is not a decoration — it is the truth of the data state. If the installation displays methods at apparent equal precision, it is lying.

Second, **the "factory shift" of jobs is not a magnitude question, it is a personhood question**. McKinsey-style numbers (~80 % activity offsite, ~30 % fewer on-site hours) are not wrong. But the 30 % of on-site labour that disappears is _not_ the same person who shows up at a Hasslacher mill in Carinthia or a Polish module factory. Catalan bricklayers do not transparently retrain into Austrian CLT-mill CNC operators. The political-dimension critique is asking the installation to make this visible.

Third, **the Salmio & Huuhka (2026) reclaimed-brick paper is the most quantitatively useful single source in this strand**. It anchors both feasibility (yield/labour for two deconstruction methods), origin (urban-mining), transport (the 480 / 315 km thresholds), and indirectly jobs (T1 deconstruction is labour-intensive and skilled — the opposite of 3DPC's vector). The installation's reclaimed-brick comparison method should lean on this paper explicitly.
