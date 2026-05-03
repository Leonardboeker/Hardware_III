# 05 — LCA Visualization for Non-Experts

## Scope

This review covers how Life Cycle Assessment (LCA) and embodied carbon information are visualized and communicated to non-expert audiences (general public, students, clients, decision-makers, children). It examines (1) the dominant building-LCA tools and their interfaces, (2) general-audience climate/carbon visualization practice, (3) the contested empirical evidence for "real-world equivalents" framing (X cars, Y trees), (4) physical and tactile data representation as a communication mode, (5) museum and exhibition installations of measurable environmental data, (6) evidence on whether feedback actually shifts architect/client behavior, (7) color encoding and accessibility considerations, and (8) the comprehension consequences of per-phase versus whole-life framing. The team's tabletop projection installation overlays LCA layers (CO2, labor, cost, time, origin) onto physical building models phase by phase; the review is organized to feed that design directly.

## Search strategy

Searches were run via WebSearch across journals (Building Research & Information, Buildings & Cities, Journal of Cleaner Production, Risk Analysis, Climatic Change, Environmental Communication, Journal of Science Communication), conferences (ACM CHI, IEEE VIS, TEI), and project sites (buildingtransparency.org, oneclicklca.com, carbonleadershipforum.org, ipcc.ch, realworldvisuals.com, giorgialupi.com). Search terms combined "embodied carbon," "LCA," "visualization," "non-expert," "real-world equivalents," "data physicalization," "tangible interface," "metaphor comprehension," "psychological distance," and named authors (Dietz, Schuldt, Cox, Spence, Pidgeon, Jansen, Dragicevic, Lupi, Posavec, Miebach). Where access to peer-reviewed full text was not possible from the agent, abstracts and authoritative secondary descriptions are cited and flagged.

## Key works (annotated, in chronological order)

### Dietz, Gardner, Gilligan, Stern, Vandenbergh, 2009 — "Household actions can provide a behavioral wedge to rapidly reduce US carbon emissions"
- **Tier:** Peer-reviewed (PNAS).
- **Citation:** Dietz, T., et al. (2009). PNAS 106(44): 18452-18456.
- **What it is:** Quantifies the carbon-reduction potential of 17 specific household actions, expressing impacts in concrete, comparable units (% of US national emissions; tons CO2 per year per action).
- **Why it matters for the team:** This is the canonical citation for translating abstract emissions into actionable, comparable quantities. It supports the team's "phase-by-phase" decomposition: granular per-action impacts beat lump totals.
- **What to reuse:** The framing of impacts as a normalized fraction of a familiar baseline (national emissions, household totals) — a direct analog to "this column = X% of the building's whole-life carbon."
- **Limitations:** US-centric; says nothing directly about visualization design.

### Spence & Pidgeon, 2010 — "Framing and communicating climate change: distance and outcome frame manipulations"
- **Tier:** Peer-reviewed (Global Environmental Change).
- **Citation:** Spence, A. & Pidgeon, N. (2010). Global Environmental Change 20(4): 656-667.
- **What it is:** Experimental study showing that gain-framed and locally proximal climate messages produce more positive mitigation attitudes than loss-framed or distant ones, but loss frames are recalled better.
- **Why it matters for the team:** Tabletop installations make impact spatially proximal — the team should exploit this. But the result that loss frames aid recall complicates a purely "positive" presentation.
- **What to reuse:** Pair every "good" projection (low-carbon scenario) with an explicit loss reference so visitors retain the contrast.
- **Limitations:** UK student sample; effects are modest in size.

### Jansen, Dragicevic, et al., 2015 — "Opportunities and Challenges for Data Physicalization"
- **Tier:** Peer-reviewed (ACM CHI).
- **Citation:** Jansen, Y., Dragicevic, P., et al. (2015). Proc. CHI '15: 3227-3236.
- **What it is:** The foundational survey of data physicalization as a research field. Defines a physicalization as "a physical artifact whose geometry or material properties encode data."
- **Why it matters for the team:** Provides theoretical legitimacy for the team's choice of a physical model + projection over a screen-only display, and catalogs which encodings (height, mass, density, light) work best for which audiences.
- **What to reuse:** The survey's argument that physicalizations excel at "engagement, accessibility, and meaning-making" for non-experts — exactly the team's audience.
- **Limitations:** Pre-2015 examples; the field has matured rapidly since.

### Carbon Visuals / Real World Visuals, 2012-onwards — "New York City's CO2 in real time"
- **Tier:** Practitioner project (widely cited in trade press; not peer-reviewed for effectiveness).
- **Citation:** Carbon Visuals / Real World Visuals (2012). Film / animation. realworldvisuals.com.
- **What it is:** Renders each ton of CO2 as a 10-meter blue sphere; shows NYC emitting one sphere every 0.58 seconds, accumulating into a mountain over Manhattan.
- **Why it matters for the team:** The most-cited contemporary example of "abstract gas → tangible volume." Direct precedent for the team's "X tons = Y trees / Z cars" overlay.
- **What to reuse:** Volume scaling that uses a familiar landmark (Empire State, Statue of Liberty) as the reference object — the team can use the building model itself as the reference, with equivalents stacked on or beside it.
- **Limitations:** No published comprehension study attached; viral appeal does not prove decision change. [unverified — effectiveness data].

### Schuldt, Konrath, Schwarz, 2011 — "'Global warming' or 'climate change'? Whether the planet is warming depends on question wording"
- **Tier:** Peer-reviewed (Public Opinion Quarterly).
- **Citation:** Schuldt, J. P., Konrath, S. H., & Schwarz, N. (2011). Public Opinion Quarterly 75(1): 115-124.
- **What it is:** Documents that subtle word choice ("global warming" vs "climate change") significantly shifts belief and concern, especially across political identity.
- **Why it matters for the team:** Labels matter as much as numbers. "Embodied carbon" reads as jargon; "carbon locked into the building" or "the building's hidden carbon" may land better with non-experts.
- **What to reuse:** A/B-test the on-projector labels with at least two non-expert pilot visitors before fixing them.
- **Limitations:** US polling context; not specifically about LCA.

### Kahan, Peters, Wittlin, Slovic, et al., 2012 — "The polarizing impact of science literacy and numeracy on perceived climate change risks"
- **Tier:** Peer-reviewed (Nature Climate Change).
- **Citation:** Kahan, D. M., et al. (2012). Nature Climate Change 2: 732-735.
- **What it is:** Higher numeracy does not converge views on climate risk; it amplifies prior-belief polarization.
- **Why it matters for the team:** More numbers ≠ more agreement. For mixed audiences (children, architects, decision-makers), narrative anchoring beats statistical density.
- **What to reuse:** Lead with one anchor number per phase, not a panel of statistics.
- **Limitations:** US sample; risk-perception not behavior change.

### IPCC WGI Technical Support Unit (InfoDesignLab), 2018 / updated 2022 — "IPCC Visual Style Guide for Authors"
- **Tier:** Authoritative grey literature (institutional standard).
- **Citation:** IPCC WGI TSU (2022). IPCC Visual Style Guide for WGI Authors, June 2022 update.
- **What it is:** Codifies color palettes (with explicit colorblind-safe variants), figure-construction rules, and uncertainty-language pairings developed for AR6 by InfoDesignLab and cognitive scientists.
- **Why it matters for the team:** Provides a vetted, citation-ready palette and a defensible reason not to default to red-green.
- **What to reuse:** Adopt the IPCC AR6 colorblind-safe palette directly; cite it on the installation panel as "palette: IPCC AR6."
- **Limitations:** Designed for static report figures, not real-time projection — luminance values may need recalibration for projector throw.

### EC3 (Embodied Carbon in Construction Calculator), Building Transparency, 2019-present
- **Tier:** Practitioner tool with extensive industry adoption (>19,000 users in 70 countries per Building Transparency).
- **Citation:** Building Transparency. EC3 Tool. https://buildingtransparency.org/ec3
- **What it is:** Free open-access search/sort interface over Environmental Product Declarations (EPDs), allowing material-by-material carbon comparison.
- **Why it matters for the team:** Demonstrates the dominant interface paradigm in practice — searchable database + bar charts + uncertainty whiskers (best/typical/worst). Non-experts find this overwhelming; the UI is built for specifiers.
- **What to reuse:** The "best / typical / worst" tri-band representation of embodied-carbon uncertainty translates well to physical light intensity bands.
- **Limitations:** Confirms the gap the team is filling: no consumer-facing equivalent exists.

### One Click LCA / Tally / Athena Impact Estimator — comparative tool reviews (Carbon Leadership Forum / Priopta, 2021-2024)
- **Tier:** Practitioner reviews + comparative grey-literature reports (Priopta report; CBE Berkeley WBLCA primer).
- **Citation:** Carbon Leadership Forum community review, Priopta comparison report. carbonleadershipforum.org.
- **What it is:** Side-by-side reviews of the three dominant whole-building LCA tools.
- **Why it matters for the team:** All three primarily output stacked bar charts by EN 15978 stages (A1-A3, A4, A5, B, C, D) — exactly the per-phase decomposition the team wants. None present material-origin or labor-hour data well.
- **What to reuse:** EN 15978 stage labels are the de-facto standard; match them so a visiting architect sees a familiar structure under the playful overlay.
- **Limitations:** Tool reviews are usability-anecdotal, not controlled studies.

### Reijnierse et al., 2025 — "The differential effects of metaphor on comprehensibility and comprehension of environmental concepts"
- **Tier:** Peer-reviewed (Journal of Science Communication).
- **Citation:** Reijnierse, W. G., et al. (2025). JCOM 24(04): A01.
- **What it is:** Experiment (N=510) comparing metaphor types ("carbon footprint," "greenhouse," etc.) on perceived comprehensibility versus actual comprehension of three environmental concepts including carbon footprint.
- **Why it matters for the team:** Found small significant effects on perceived comprehension and comprehensibility but no effect on actual comprehension. Concrete metaphors feel clearer without making people understand more.
- **What to reuse:** Treat "X trees / Y cars" as engagement bait, not as teaching. Pair every equivalent with the absolute number so understanding is not sacrificed for resonance.
- **Limitations:** Tests text, not interactive physical installations — generalization is suggestive.

### Lupi & Posavec — "Dear Data" (2014-2015) and Lupi's microplastics installation
- **Tier:** Practitioner art / design (widely covered MoMA, TED, Dezeen).
- **Citation:** Lupi, G. & Posavec, S. (2016). Dear Data. Princeton Architectural Press.
- **What it is:** Hand-drawn data postcards demonstrating the "Data Humanism" approach — datasets shown as expressive, imperfect, contextual artifacts.
- **Why it matters for the team:** Establishes that non-expert audiences engage more deeply with data shown as authored, idiosyncratic, even decorative — counter to dashboard convention.
- **What to reuse:** Hand-drawn or hand-rendered overlays for the "human cost" layer (labor hours, material origin); reserve clean geometric encoding for the carbon and cost layers.
- **Limitations:** No comprehension data; the lesson is aesthetic and rhetorical.

### Miebach, Nathalie — woven climate-data sculptures (ongoing)
- **Tier:** Practitioner art (museum-exhibited; documented in Colossal, STIRworld, university talks).
- **Citation:** Miebach, N. Sculptural works using NOAA / weather-station data. nathaliemiebach.com.
- **What it is:** Three-dimensional baskets that translate meteorological data into woven structures, often with paired musical scores.
- **Why it matters for the team:** Direct precedent for "data made physical at room scale" with measurable provenance, shown in museum settings to mixed audiences.
- **What to reuse:** Multi-modal encoding — Miebach pairs sculpture with sound; the team could pair projection with audio cues per phase.
- **Limitations:** Art rather than informational tool; comprehension is intentionally ambiguous.

### Yale Program on Climate Change Communication — museum partnership findings, and "Hopeful Future" / Wild Center "Climate Solutions" exit interviews (2023-2024)
- **Tier:** Practitioner research (audience studies, Visitor Studies journal).
- **Citation:** Yale PCCC publications; Visitor Studies 28(2), 2024.
- **What it is:** Museum-visitor research finding that climate exhibits work best when they (1) name a local impact, (2) offer rational hope and visible action, (3) end at a "what you can do" wall.
- **Why it matters for the team:** The installation should not end on the carbon total. It needs an action prompt — "in your next project, swap material X for Y to halve this column."
- **What to reuse:** The closing "Climate Action Wall" pattern — a final layer in the projection sequence dedicated to alternatives, not totals.
- **Limitations:** Measures self-reported attitude shift, not downstream behavior.

## Do "real-world equivalents" actually work? (Evidence summary)

The honest answer is: **they reliably increase engagement and perceived understanding, but the evidence that they improve actual comprehension or change decisions is weak and contested.**

**For:** Dietz et al. (2009) treats concrete, decomposed equivalents as a precondition for behaviorally relevant communication. Carbon Visuals' NYC sphere film achieved viral reach because volume-as-landmark renders an abstract figure intuitively. Material-metaphor research argues that translating invisible global impacts into local, felt experiences "bypasses cognitive distance" (a claim well-aligned with Spence & Pidgeon, 2010 on psychological distance).

**Against:** Reijnierse et al. (2025) is the single strongest controlled finding: across 510 participants and three environmental concepts including carbon footprint, metaphors increased perceived comprehensibility but not actual comprehension. Kahan et al. (2012) shows that more sophisticated framings can polarize rather than converge views in mixed audiences. Practitioner critiques of "X trees" framing are widespread — tree-equivalent claims often understate variance (a temperate tree sequesters ~10-40 kg CO2/year depending on species, age, climate; presenting "1 tree = X kg" as a fixed constant is technically misleading). The "1.5 billion cars off the road" type comparison from forest-protection campaigns is similarly criticized for collapsing spatial/temporal context.

**Practical implication for the team:** Use equivalents as a hook, not as the load-bearing claim. Always show the absolute number (tons CO2e, kg/m2) alongside the equivalent, and explicitly disclose the equivalency assumption ("assumes a temperate tree, 40 years, ~22 kg CO2/yr — Forest Service"). This converts the equivalent from a misleading shortcut into a teaching moment.

## Patterns that recur across effective LCA visualizations

- **Spatial proximity:** the data is rendered onto or near a familiar object (NYC skyline, the building itself).
- **Per-stage decomposition** that follows EN 15978 (A1-A3, A4-A5, B, C, D) — familiar to specifiers, intuitive to lay audiences as "make / move / use / dispose."
- **Tri-band uncertainty** (best / typical / worst) rather than a single point estimate.
- **Action prompt at the end** ("swap this material to halve this band").
- **Multi-modal encoding** — combining visual with sound, light intensity, or physical motion improves dwell time at museum installations.
- **Provenance pinning** — every number can be clicked or pointed-to and yields its source.

## Patterns that recur across INEFFECTIVE ones

- **Stacked-bar dashboards** as the only output (EC3, OneClickLCA default views): high information density, low affective punch.
- **Red-green color encoding without secondary cues** — fails ~4.5% of viewers and conflates "good/bad" with technical magnitude.
- **Single-equivalent shock claims** ("equivalent to X cars") with no absolute number and no source.
- **Whole-life totals only**, no phase breakdown — visitors cannot see where the impact comes from or what to change.
- **Dense uncertainty whiskers** without explanation — read by non-experts as "the scientists don't know."
- **Jargon labels** ("GWP100," "A1-A3 cradle-to-gate") presented without glossing.

## Cross-cutting themes

1. **Engagement and comprehension are not the same outcome.** Most effective installations win on engagement; few demonstrate comprehension gains, and almost none demonstrate behavior change. Be explicit about which the team is optimizing for.
2. **Physical presence matters.** Data physicalization research (Jansen, Dragicevic et al., 2015) and museum visitor studies converge on this: tangible artifacts attract groups, prompt conversation, and increase dwell time relative to screens.
3. **Decomposition beats totals.** Both LCA practitioner tools and behavioral-wedge research (Dietz et al.) converge on per-stage / per-action breakdowns as the unit of useful insight.
4. **Local and proximal beats global and distant.** Spence & Pidgeon and the museum literature agree.
5. **Color is not a sufficient channel on its own.** IPCC AR6 guidance and accessibility literature both insist on shape/position/label redundancy.

## What's missing in this literature

- Almost no controlled studies of physical / projection-based LCA installations specifically — the team's installation will itself be a contribution.
- Very little on how non-experts read **labor hours** or **material origin** (vs carbon and cost). The LCA literature is overwhelmingly carbon-focused.
- Few longitudinal studies linking exposure-to-visualization with downstream design decisions by architects or specifiers.
- Limited comparative work on whether per-phase animation (impact accumulating over time) versus static stacked display improves understanding.

## Direct recommendations for the team

1. **Adopt EN 15978 stage labels** under the playful overlay so a visiting architect recognizes the structure (A1-A3 product, A4-A5 construction, B use, C end-of-life).
2. **Use a single anchor number per phase**, with the equivalent ("≈ X trees over 40 years") in smaller type beside it and the source citation visible. Treat the equivalent as a hook, not the headline.
3. **Pair every equivalent with its assumption.** "1 tree = ~22 kg CO2e/yr (temperate, 40-year)" is honest; "= X trees" alone is not.
4. **Avoid red-green as the sole encoding.** Adopt the IPCC AR6 colorblind-safe palette and add redundant cues (column height, light intensity, an icon).
5. **Render uncertainty as a tri-band light intensity** (best / typical / worst) on the physical model — borrowing EC3's data convention but rendering it tactile.
6. **End every sequence with an alternative scenario projection** ("if this column were CLT instead of concrete, watch what happens") — the museum literature is consistent that an action wall outperforms a doom wall.
7. **Use multi-modal encoding for distinct LCA layers.** Carbon and cost as geometric overlays (precise); labor hours and material origin as Lupi/Posavec-style hand-rendered, expressive overlays (relational); an audio cue marking each phase transition.
8. **Show the phase animation, not only the total.** Animate accumulation across A1 -> C4 so visitors see *where* the carbon comes from. This is the team's strongest differentiator from EC3-style outputs.
9. **A/B test labels with at least two non-expert pilot visitors before fixing them** — Schuldt et al. (2011) shows wording effects are large.
10. **Document the installation as a study.** Capture dwell time, visitor questions, and (where possible) post-visit recall — this addresses a real gap in the literature.

## Sources requiring verification

- Carbon Visuals / Real World Visuals NYC project: viral reach is well-documented; **no peer-reviewed effectiveness study located**. Treat as a design precedent, not as evidence of comprehension or behavior change. [unverified — effectiveness]
- Tree-sequestration constants used in any "X trees" overlay: range widely (10-40 kg CO2/year per tree depending on species, climate, age). Do not present as a fixed constant without source.
- "1.5 billion cars" forest-protection comparison (WEF, 2017): widely repeated; underlying calculation should be re-derived from the source paper before citation. [unverified in this review]
- Reijnierse et al. (2025) finding of "no effect on actual comprehension" is based on text-stimulus experiments; generalization to interactive installations is plausible but unverified.
- Specific user counts and adoption figures for EC3 (>19,000 users / 70 countries) come from Building Transparency's own materials; cite as self-reported.
- "Hopeful Future" / Wild Center exit-interview findings: published in Visitor Studies 28(2), 2024; the underlying methodology should be checked before strong claims are made about effectiveness.
- Dear Data and Miebach references are well-documented as artworks; their pedagogical effects on non-experts are not formally measured.

