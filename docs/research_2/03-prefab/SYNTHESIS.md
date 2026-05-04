# SYNTHESIS — Strand 03 Prefab (Modular Concrete + CLT)

> Research question: What are the defensible cradle-to-gate (A1–A3) embodied
> carbon, labour-hours, time, cost, and material-origin ranges for (a)
> volumetric concrete modular construction and (b) cross-laminated-timber
> (CLT) panel construction, broken down per construction phase, with biogenic
> carbon and reuse-allocation methodology wobbles named, and Catalan /
> European geographic context where possible?

This synthesis sits between `BIBLIOGRAPHY.md` (sources) and `VALUES.md`
(numerical cells). Its job is to (a) lay out the evidence landscape split by
sub-method, (b) name the central methodology issue for each sub-method, (c)
disclose the biases the values carry, and (d) tell the projection layer what
caveat it must surface to the visitor.

---

## 1. Evidence landscape

### 1.1 Volumetric concrete modular (MiC)

The peer-reviewed literature on volumetric modular embodied carbon is
**dominated by Hong Kong**. The headline reference cited in the brief — Wei,
Ge, Zhong, Lee, & Zhang (2024) in *Scientific Reports* — is the Kai Tak
Community Isolation Facility, a 110,000 m² emergency-response complex of
steel-framed modular blocks compared against a counter-factual cast-in-place
reinforced-concrete equivalent. The paper reports a **20.7 % reduction** in
total cradle-to-end-of-construction embodied carbon (46,024 vs 58,005 tCO₂e),
which back-calculates to **~418 kg CO₂e/m² for MiC vs ~527 kg CO₂e/m²
conventional**. The reduction breaks down distinctively by phase: **6.1 %**
reduction in A1–A4 materials (modest, driven by structural-steel optimisation),
**58.1 %** in A5a on-site activity emissions (compressed schedule), and
**39.5 %** in A5w waste emissions (factory control). A second Hong Kong study
(Tang, Pan, Chan, & Liu, 2024, *Building and Environment*) frames a
**169–569 kg CO₂e/m²** range for similar concrete-modular high-rise typologies
and cites the wider literature range of **105–864 kg CO₂e/m²** across
modular case studies — confirming that "modular embodied carbon" is not a
single number; structural choice (steel-frame vs concrete-frame modules) and
module-size economy dominate the variance.

Two important transferability caveats:

- **Hong Kong typology does not transfer cleanly to Catalonia.** Hong Kong
  modular is high-rise residential, designed for vertical density and seismic
  loads peculiar to that market. European low-rise modular (Daiwa House
  Modular Europe, Plegt-Vos, Heijmans) builds different envelopes, different
  module sizes, and different structural systems.
- **The brief's "20–26 % with reuse" figure is real but lives in a different
  paper.** Wei et al. explicitly excludes B and C modules; they cannot make
  the second-life claim. The 20–26 % annualised figure comes from
  longitudinal modular-reuse studies (Pan & Hon, Hong Kong; Quale et al.
  2012 in *J. Industrial Ecology*) where two design lifespans of 25–50 yr each
  are assumed end-to-end. The wobble layer must surface this — single-life
  LCAs miss the lever entirely.

For European context, the supplementary UK figure that is most useful is
**405 kg CO₂e/m² for a modular timber-frame three-bedroom semi-detached
house, 34 % below traditional methods** (cited in WEF / industry synthesis,
underlying source UK BRE case study). This sits below the Hong Kong concrete-
modular range because of the timber-frame substitution, and confirms that for
European low-rise the modular advantage is real but the absolute number drops.

### 1.2 Mass-timber CLT

The CLT literature is structurally different. Three things matter:

1. **Validated EPDs exist for the dominant European mills** — KLH (Austria),
   Stora Enso (Austria/Sweden), Binderholz (Austria), Rubner (Italy/Austria),
   plus several Swedish producers. Stora Enso's 2024 EPD declares
   **A1–A3 GWP-fossil of ~60 kg CO₂eq per m³ of CLT**, with biogenic carbon
   storage of **−731 to −762 kg CO₂eq/m³**. Density ~470 kg/m³. KLH and
   Binderholz triangulate within ~10 % of these figures. The numerical
   anchor for CLT cells is therefore robust at the panel-product level.
2. **Whole-building studies are dominated by North America and China**, not
   the EU. Hemmati, Messadi, & Gu (2024) in *Buildings* report
   **198 kg CO₂eq/m² mass-timber vs 243 kg CO₂eq/m² steel** (A1–A4) for
   Adohi Hall in Arkansas — a **19 % reduction**. Andersen, Rasmussen, &
   Ryberg (2022) in *Energy and Buildings* report a **34 % reduction** for
   CLT vs concrete in Danish mid-rise residential **only when the GWP-bio
   factor is applied**. Liu et al. (2022) in *Sustainability* report ~46 %
   reduction in a Chinese case (likely the source of the brief's misattributed
   "46.5 %" figure).
3. **A4 transport from Austria to Catalonia is non-trivial and is excluded
   from most published LCAs.** Austria → Barcelona by road is roughly
   1,800–2,200 km. At ~0.06 kg CO₂eq per tonne-km for a diesel HGV, and
   panel mass per m² of GFA in the order of 0.5–1.0 t (depending on panel
   thickness and structural strategy), the A4 add-on lands at
   **~25–60 kg CO₂eq/m² GFA**. This is the Catalonia-specific penalty that
   the projection layer must show — and that an Iberian CLT mill would
   eliminate, but no such mill exists at production scale as of 2026.

### 1.3 Catalonia-specific signal

There is one direct case study: the **ARRIASA project**, the tallest
structural-timber social-housing building in Spain (Barcelona / Catalonia
adjacent), which procured CLT under a tender that introduced embedded
emissions as evaluation criteria — a regional first. Spanish modular-concrete
fabricators (Moodul Castelldefels, Modular Home Valencia, Casas inHaus) are
active and growing, but no peer-reviewed LCA of a Spanish modular building
exists in the searched literature; the cost data therefore comes from
aggregator sources (idealista, modularhome.es) and is Tier 3.

---

## 2. The biogenic carbon debate (CLT methodology issue)

This is the central wobble for the CLT row of the installation.

The numerical question: when a tree absorbs CO₂ during growth and that carbon
is locked in a CLT panel, **does the LCA count the absorbed CO₂ as a deduction
against the panel's emissions?**

There are three defensible answers, each used by serious practitioners:

- **EN 15804+A2 dynamic accounting (the Andersen approach):** A1 reports a
  large negative biogenic value (~−700 kg CO₂eq/m³), and C3 reports the
  matching positive value at incineration end-of-life. If the panel is
  reused or landfilled, the carbon stays sequestered — and the
  cradle-to-grave net is genuinely negative. This is what Stora Enso's EPD
  reports.
- **GWP-fossil only (the Hemmati / "fossil-only" approach):** Biogenic
  carbon is excluded from the headline figure entirely. CLT still beats
  steel and concrete because of low manufacturing energy and low cement, but
  the advantage drops to 19 % rather than 34–46 %.
- **Dynamic LCA with the GWP-bio factor (the academic frontier):** Accounts
  for the *timing* of carbon release and absorption, applies a discount rate.
  The advantage of CLT shrinks further if forest regrowth lags harvest.

These three views give materially different headline numbers for the same
building. **Andersen et al. (2022) puts the swing at 34 % of the comparative
result** (their "Base scenario" vs "Biogenic carbon scenario" delta is
exactly the wobble overlay needed for the visitor).

The installation cannot pick one and claim it is "the" answer. The wobble
overlay must surface both at minimum: a "with biogenic" CLT bar and a
"without biogenic" CLT bar, with the visitor able to toggle. The values
table provides both ranges as sibling rows precisely so the projection layer
can render this without re-querying.

---

## 3. The reuse / second-life allocation lever (modular-concrete methodology issue)

The mirror-image wobble for modular concrete.

A volumetric concrete module — once fabricated — is in principle relocatable.
The Nam Cheong 220 project in Hong Kong demonstrated practical relocation;
Daiwa House Modular Europe markets relocatability as a feature. **If the LCA
allocates one design life of 25–50 years and stops, the module's environmental
budget is amortised over that single life. If the LCA allocates two lives of
25–50 years each, every kg of CO₂eq spent on factory production is divided
across roughly twice the floor-area-years of service.**

Wei et al. (2024) explicitly excludes the second-life calculation. The
literature that includes it (Pan & Hon; Quale et al. 2012) reports the
"20–26 % annualised reduction" the brief cites. **The lever is real, but it
depends on a very specific allocation choice** (cut-off vs avoided-burden vs
PEF Circular Footprint Formula) that EN 15804+A2 module D handles only
partially. Pomponi & Moncaster (2018) demonstrated that this allocation
choice swings building-level results by up to two orders of magnitude.

The wobble overlay should therefore offer the visitor a "single-life" vs
"two-life" toggle on the modular bar — and the values table provides paired
end-of-life cells (`eol_carbon_modular_with_reuse: −150 to −50` vs
`eol_carbon_modular_no_reuse: +30 to +80`) precisely to make this rendering
possible.

---

## 4. Named biases

These are mechanism-level statements of where the data comes from and what
direction it might be skewed. They appear here as first-class findings, not
as boilerplate hedging.

- **CLT advocacy bias.** The forest-products industry actively funds
  favourable LCAs. Hemmati et al. (2024) is co-authored with USDA Forest
  Products Lab; Stora Enso, KLH, and Binderholz own their own EPDs. None of
  these are fraudulent — they are EN 15804+A2 verified — but they are made
  by parties with a commercial interest in the sequestration credit being
  large. The independent academic studies (Andersen, Liu) report smaller
  CLT advantages than the industry-adjacent ones.
- **Hong Kong over-representation in modular concrete literature.** The
  Wei et al. (2024) and Tang et al. (2024) numbers cannot be uncritically
  extrapolated to European context. Hong Kong's MiC programme runs at scale
  (Kai Tak, Nam Cheong, the planned Tung Chung New Town) under specific
  high-rise residential typology and seismic / fire / typhoon loadings.
  European low-rise modular reports lower per-m² emissions but the dataset
  is thinner.
- **"Speed advantage" claims confuse on-site time with total time.** WEF
  and McKinsey report "20–60 % time reduction" but the comparison usually
  pits on-site-only modular against on-site-plus-design conventional.
  Honest factory-plus-on-site modular timelines are similar to conventional
  timelines for the first project of a given factory; the speed advantage
  shows up on the second and subsequent projects.
- **Material-origin opacity for modular vendors.** Spanish prefab vendors
  rarely publish where their concrete cement or rebar mill comes from.
  Tier 3 cost data has to be paired with disclosure that origin is unknown.
- **A4 exclusion bias.** The dominant journal-reported headline number for
  CLT excludes Austria→Catalonia transport. Including A4 narrows the CLT
  advantage by ~25–60 kg CO₂eq/m². Reporting the headline without the
  caveat is a category of bias by omission.

---

## 5. Brief-revisit — can the installation defensibly compare prefab to other methods?

Yes — but only if the projection layer takes the methodology wobbles
seriously. Specifically:

1. **The visitor must be able to toggle "with biogenic / without biogenic"
   on the CLT column.** Showing CLT with biogenic alone risks the visitor
   leaving with the impression that CLT is carbon-negative full-stop; that
   is true only for Stora Enso's A1–A3 cradle-to-gate stage and does not
   hold across cradle-to-grave if the building is incinerated at end-of-life.
   Showing CLT without biogenic alone strips the most-cited environmental
   selling point of mass timber. The wobble overlay must show both.
2. **The visitor must be able to toggle "single-life / two-life" on the
   modular column.** Showing modular at single-life undercounts its
   primary structural advantage (relocatability). Showing it at two-life
   bakes in an assumption (the second life will happen) that is not
   guaranteed in practice.
3. **The Catalonia A4 transport row should default to ON for CLT.**
   Most published LCAs strip A4. For a Catalonia-specific installation
   that purports to compare what visitors could actually build in the
   region, A4 is non-optional. Showing the +25 to +60 kg CO₂eq/m² A4
   bar collapses the CLT advantage materially and is the most regionally
   honest framing.
4. **The values are ranges, not points.** Modular concrete from Hong Kong
   case studies clusters at 280–569 kg CO₂eq/m² A1–A3, but the literature
   spread is 105–864. CLT clusters at 130–220 with biogenic, 220–350
   without. The projection layer must render the ranges as bands (whisker
   plots, density bands, or stacked uncertainty), not as bars with single
   heights. Anything else will visually overstate the precision of what
   the literature actually supports.

What the installation **cannot** defensibly claim:

- That prefab is unconditionally lower-carbon than other methods. The 105
  kg CO₂eq/m² floor exists; so does the 864 kg ceiling.
- That CLT is "carbon negative" without immediately specifying the system
  boundary.
- That the Hong Kong MiC numbers describe a Catalan modular project.
- That "construction is 50–90 % faster" is a like-for-like comparison.

What it **can** defensibly claim, and what the values support:

- Modular and CLT both reduce on-site waste materially (10–15 kg/m² vs
  25–30 kg/m² conventional).
- Modular and CLT both reduce on-site labour time materially (1–4 h/m²
  vs 5–10 h/m² conventional, where conventional is masonry / cast-in-place).
- CLT delivers a real and large biogenic carbon credit at A1–A3 — the
  question is what happens to that credit at end-of-life.
- Modular delivers a real reuse-allocation lever — the question is whether
  the second life is actually realised in the project's lifetime.

These are the claims the wobble layer can render; the headline numbers in
the values table support each claim with a sourced range and a tier.

---

## 6. Provenance summary

Source-tier distribution across populated cells: **14 Tier 1, 13 Tier 2,
4 Tier 3 (sibling-required), 3 explicitly missing**. Every Tier 3 row has a
Tier 1 or Tier 2 sibling. No vibe-citing — every numerical claim in
`VALUES.md` traces to a source key in `BIBLIOGRAPHY.md`. The two corrections
to the brief's source list (Wang→Wei; "Liu 2021 46.5 %" → Andersen et al.
2022, 34 %) are documented in the bibliography and reflected in the values.
