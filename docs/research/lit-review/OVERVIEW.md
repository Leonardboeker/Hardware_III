# Literature Review — Guided Comparative Assembly

> Synthesis of a six-strand lit review conducted by an academic research team. The six per-strand reports (01–06) provide the depth; this document is the briefing the team should read before building.

**Compiled:** 2026-05-03
**For:** IAAC Hardware III, Group 3 (Leo, Elais, Rafik, Seid, Onur, Nithik)
**Final demo:** 2026-05-22

---

## How to read this document

This OVERVIEW is the briefing — the synthesised, opinionated version. The six per-strand files behind it are where the citations and the nuance live:

- `01-tui-tabletops.md` — the interaction-grammar lineage (Ishii → reacTable → ArUco)
- `02-augmented-assembly.md` — AR-guided assembly (Gramazio Kohler, Fologram, EPFL)
- `03-projection-guided-construction.md` — projection mapping, calibration, and the assembly-as-FSM framing (Parascho)
- `04-reuse-and-reclaimed-materials.md` — circular construction (EPFL SXL, Re:Crete, baubüro in situ)
- `05-lca-visualization.md` — communicating environmental data to non-experts
- `06-comparative-lca-and-museum-interactives.md` — the actual numbers + museum precedents

Whenever a claim below cites a strand (e.g. "see 02"), the underlying citation is in that strand file. Drill in there before quoting on a panel or in a paper.

---

## TL;DR — Five things the team needs to internalize

1. **Project the labels, don't print them.** Across 25 years of TUI work — Urp, reacTable, SLAP Widgets, Augmented Bricklaying — the consistent division of labour is *tokens carry identity and pose; projection carries meaning*. Putting fixed labels on the pucks throws away your single biggest design lever (see 01).
2. **Object-aware feedback is the contribution; pure open-loop is the v1.** The most current AR-assembly systems (Augmented Bricklaying, Augmented Carpentry) close the loop on what the human *actually did*, not what they were told to do. Aim there conceptually but ship a baseline (project step N → button → step N+1) for the May 22 demo (see 02, 03).
3. **The numbers are unstable; the methodology is the message.** Three independent strands (04, 05, 06) converge on the same warning: comparative LCA results swing by factors of 2–4 depending on system boundary, lifespan, biogenic carbon, and grid mix. Showing the wobble *is* the sustainability lesson. Bake Pomponi's caveats into the projection as a toggleable "why these numbers wobble" layer (see 06).
4. **Engagement and comprehension are not the same outcome.** Real-world equivalents ("X trees / Y cars") reliably increase engagement and *perceived* understanding but the controlled evidence (Reijnierse et al. 2025, N=510) shows they do not improve actual comprehension. Use them as hooks; pair every equivalent with the absolute number and its assumption (see 05).
5. **The "Swiss museum DJ table" you keep citing is almost certainly the reacTable, and almost certainly not Swiss.** It's on permanent display at ZKM Karlsruhe and Game Science Center Berlin — not at any verified Swiss venue (see 01). Either confirm the actual museum the team member visited, or re-anchor the precedent on the reacTable proper. Don't keep using a citation you cannot back.

---

## The novelty space — where the team can plant a flag

The honest framing: this project sits squarely *downstream* of two well-established lineages and that is a feature, not a bug. The interaction grammar (pucks + overhead camera + top-down projector) descends directly from Urp (Underkoffler & Ishii 1999) and the reacTable (Jordà et al. 2007), with ArUco (Garrido-Jurado et al. 2014) as the modern detection layer. The assembly logic descends from Parascho (2019) via the "assembly = constrained state-space" framing. The interaction loop (project next position → human places → CV confirms → advance) is lifted almost verbatim from Augmented Bricklaying (Mitterberger et al. 2020). None of these are stretches; all three are the right lineage to claim, and citing them legitimises the work rather than diluting it.

The novelty is in the *combination*. Three strands independently surfaced the same gap: (a) "LCA / construction-method comparison as a domain is essentially absent from the TUI tabletop literature" (01); (b) "no surveyed paper combines AR assembly guidance with live LCA data" (02); (c) "no published peer-reviewed LCA installation that does pedagogical-scale comparison of masonry vs 3DCP vs modular on the same plan" (06). The defensible flag is therefore: **a tangible, multi-user, projection-mapped tabletop that uses the AR-guided-assembly interaction loop to teach the methodological *instability* of comparative construction LCA to a non-expert audience.** Three small contributions, no big single one — but the intersection appears to be unoccupied.

A second, smaller novelty hook worth keeping in reserve: most TUI tabletops show *state* (the city now, the landscape now). Showing a *time-evolving construction process* — embodied carbon accumulating across A1 → C4 phases on a physical model — is uncommon in this lineage and is exactly what the FSM phase walkthrough is built for (see 01, 05).

---

## Cross-cutting themes (across all six strands)

1. **Valid intermediate states as a first-class concept.** Parascho's structural-validity FSM (03), Choreo's CSP planner (03), Block Research Group's discrete shells (03), and Augmented Bricklaying's object-aware update loop (02, 03) all converge on the same move: enumerate the legitimate partial states, refuse transitions that produce nonsense. This is the through-line that justifies the team's FSM choice and is what to lead with conceptually.

2. **Calibration is the hidden time-sink.** Both 02 and 03 single out projector-camera calibration as the underestimated step. Moreno & Taubin (2012) plus the Brown reference implementation gives the team a half-day of work — but only a half-day if they mount everything rigidly first and don't move it again (03). Plan accordingly.

3. **Tokens encode pose; projection encodes meaning.** Theme 2 of strand 01 is the same theme strand 02 surfaces about "the model becomes the drawing" and strand 05 surfaces about "spatial proximity beats spatial dashboards." Three independent literatures point at the same design rule.

4. **Comparative numbers are fragile and the wobble is the lesson.** Pomponi & Moncaster (2016, 2017) underwrite the methodological side; De Wolf, Hoxha & Fivet (2020) underwrite the reuse side; the practitioner LCA-tool reviews (One Click LCA, EC3, Tally) underwrite the visualization side. All three strands (04, 05, 06) explicitly recommend disclosing the methodology, not hiding it.

5. **Reuse and lifespan dominate any honest LCA story.** Modular's biggest carbon win comes from second-life reuse (Wang 2024); CLT's biggest comes from biogenic accounting + 60-yr lifespan; 3DCP's only comes from geometry optimisation. Strand 04 and strand 06 agree: the rank order of the three methods is not stable, and the levers that move it are not the ones the marketing materials emphasise.

6. **AR assembly really does reduce errors — when calibration is right.** The headline numbers from 02 (Funk et al. 2016: ~82% reduction in cumulative errors with in-situ projection; Doshi et al. 2017: 52% reduction in std-dev of weld placement) are reproducible across a decade of HCI studies. They are the team's strongest empirical wall-panel claim.

---

## What the literature says works

- **Top-down projection on passive tokens, with ArUco for tracking** (01, 02, 03). This is the team's planned setup and it sits on the well-trodden path. `cv2.aruco` with `DICT_4X4_50` or `DICT_5X5_50` is the default.
- **A "tool token" pattern** — one puck whose role is to switch the projected overlay between LCA dimensions (CO₂ / cost / labor / time). Validated by Urp's wand (01) and Augmented Bricklaying's mode controls (02). Saves you from inventing a separate menu UI.
- **The Augmented Bricklaying interaction loop** — project next position → user places → CV confirms → advance — at table scale. Most current published precedent for what the team is doing (02, 03).
- **EN 15978 stage labels under the playful overlay** (A1–A3 product, A4–A5 construction, B use, C end-of-life). A visiting architect sees a familiar structure; a non-expert sees "make / move / use / dispose" (05).
- **Tri-band uncertainty rendered tactile** — best/typical/worst as a light-intensity band around each method's data, borrowing EC3's data convention (05).
- **Closing the sequence with an alternative scenario** ("if this column were CLT instead of concrete, watch what happens"). Museum-visitor research is consistent: an action wall outperforms a doom wall (05, 06).
- **Designing for 3–5 simultaneous viewers, not single-user** — Falk & Dierking, Allen, and the entire DiamondTouch / reacTable lineage agree that successful tabletops are social objects (01, 06).
- **Local-baseline data over global averages.** For a Catalan jury, BEDEC line items beat US RMI averages; cite by ITeC item code on the projector caption (06).
- **Open-source code reuse where possible.** Augmented Carpentry (https://github.com/ibois-epfl/augmented-carpentry) and the Brown procam-calibration codebase are both close enough to lift before writing custom CV (02, 03).

## What the literature says fails

- **Putting labels on the tokens themselves.** Throws away the projection's reconfigurability and forces hardware changes for content changes (01).
- **Stacked-bar dashboards as the only output.** EC3 and One Click LCA default views; high information density, low affective punch (05). Don't mimic this on the tabletop.
- **Red-green color coding without secondary cues.** Fails ~4.5% of viewers and conflates "good/bad" with technical magnitude (05). Adopt the IPCC AR6 colorblind-safe palette and add redundant cues (column height, light intensity, icon).
- **Single-equivalent shock claims** ("equivalent to X cars") with no absolute number and no source. Reijnierse et al. (2025) shows these increase perceived comprehension without increasing actual comprehension (05).
- **Whole-life totals only, no phase breakdown.** Visitors can't see *where* the carbon comes from or what to change (05).
- **Hand-occlusion pretending it isn't a problem.** Top-down rigs occlude badly. Plan camera and projector at slight offsets so a hand blocking one rarely blocks the other (01).
- **TUIO for v1.** Adds a layer that a 3-week build doesn't need; ship a direct OpenCV → renderer pipeline first, adopt TUIO only if you split sensing and rendering (01).
- **Quoting per-m² CO₂ figures from vendor press releases** (TECLA, ICON, Apis Cor, COBOD). They are not peer-reviewed. Use as image precedent only (06).
- **Citing "Brick Vault" by Gramazio Kohler.** Strand 04 could not match this to a known GKR project — likely confused with *Iridescence Print* (3DP, not reclaimed) or *Rock Print* (granular, not reclaimed in the salvage sense). Drop it or replace with *Augmented Bricklaying*.
- **Citing "EPFL CRCL Discrete Wood".** Strand 04 could not verify a CRCL project under that name; the closest verifiable match is EPFL IBOIS's Augmented Carpentry. Don't conflate the two labs in the documentation.

---

## The "fourth method" question

**Position: add reclaimed brick, but stage it as the *baseline* against which the other three methods are measured — not as a fourth competitor in a four-way bake-off.**

Rationale, drawing on strand 04:

- The peer-reviewed evidence is consistent that reuse avoids the bulk of cradle-to-gate emissions (Modules A1–A3), which dominate embodied carbon for masonry and concrete. Re:Crete (Küpfer, Bastien-Masse & Fivet, 2021) shows roughly 1/3 the GHG of equivalent new RC and parity with glulam; baubüro in situ's K.118 reports ~60% GHG reduction at building scale. These are the two strongest single-project anchor numbers available.
- So on a single-axis (cradle-to-gate kg CO₂e/m²) reading, reclaimed brick will almost certainly outperform 3DP concrete and likely 3DP earth too. A strict bake-off therefore produces a foregone conclusion that doesn't teach the visitor anything they didn't already suspect.
- However, three caveats from De Wolf, Hoxha & Fivet (2020) and Pomponi & Moncaster (2016) push against a naïve "reuse wins everything" frame: (i) allocation rules swing the result, (ii) use-phase and end-of-life are usually omitted, and (iii) stock availability is geographic and political. A four-way bake-off invites the peer-reviewer to say "you cherry-picked the allocation."
- Reframing reuse as the *baseline* — "this is what the building stock around us already contains, and what every other method is competing against" — does three useful things at once: (a) it makes the political point ("we already have the materials; the question is why we don't use them") sharper than a bake-off would; (b) it makes the methodological point about allocation rules visible without leaning on it; (c) it lets the team cite Catalan stock data (PRECAT20, Concular-equivalent listings) and anchor the political point in Barcelona, not Switzerland.

Operationally: keep three pucks for the three production methods and add a fourth, visually distinct token (different colour, different geometry) for the reuse baseline. When the reuse token is on the table, the projection shows the comparator as a horizontal line across all three method bars. When it is not, the comparison is between the three production methods alone. This treats reuse as a *condition* of the visualization rather than a fourth contestant — which is exactly what the literature suggests is the more defensible framing.

---

## Risk register from the literature

| Risk | Surfaced by | Mitigation pointer |
|---|---|---|
| Projector-camera misalignment ruins overlays | 02, 03 | Moreno-Taubin Gray-code calibration, mount rigidly, don't move it. Brown reference implementation + `kamino410/procam-calibration`. |
| Hand occlusion of top-down camera | 01 | Offset camera and projector; if visible-light fails under stage lighting, consider IR + IR-reflective markers. Test under final lighting early. |
| Peer reviewer attacks LCA cherry-picking | 04, 06 | Cite De Wolf/Hoxha/Fivet (2020) and Pomponi/Moncaster (2016) on the projector itself; show "best / typical / worst" tri-band, not point estimates. |
| Vendor press-release LCA numbers leak into documentation | 06 | Tag every per-m² number with source tier (peer-reviewed / EPD / vendor). Drop TECLA/ICON/Apis Cor numerical claims. |
| "Real-world equivalents" mislead more than they teach | 05 | Always pair the equivalent with the absolute number and the assumption ("1 tree ≈ 22 kg CO₂e/yr, temperate, 40 yr — Forest Service"). |
| Unverified citations (Swiss DJ table, Brick Vault, Discrete Wood, "Don't waste a thing!") propagate into final deliverables | 01, 04 | Aggregated in "Open questions" below. Resolve before final-presentation slide deck. |
| FSM rejects user actions silently and visitors get stuck | 03 | Keep transitions pure functions of `(current_state, event, world_state)`; reject invalid events *explicitly* with projected feedback. |
| Feature creep dilutes learning per Allen (2004) | 06 | Three methods, three phases, two trade-off axes is already at the limit. Resist adding a fourth method *as a competitor* (see "fourth method" above). |
| 3-week build slips on calibration day | 02, 03 | Budget half a day for calibration, with a fallback day. Don't do calibration the night before. |
| Top-down ArUco fails under installation lighting | 01 | The published academic ArUco-tabletop work is almost all lab prototypes; ergonomics for public-installation lighting is barely documented. Test under demo lighting before demo week. |

---

## Action items for the team (next 19 days)

Ordered by priority. Each item cites the strand or paper that supports it.

1. **Calibrate the projector-camera rig using Moreno & Taubin (2012) Gray-code procedure** with the Brown reference implementation or `kamino410/procam-calibration`. Mount everything rigidly first; budget half a day. (03)
2. **Implement the FSM as a pure function `(state, event, world) → state`** with explicit rejection of invalid transitions. Either Derivative's TouchDesigner Table-Driven FSM asset or an equivalent in your runtime. Cite Parascho (2019) as the conceptual anchor and Huang et al. (2018) Choreo as the readable companion. (03)
3. **Lift the Augmented Bricklaying interaction loop** for v1: project next position → user places → CV confirms → advance. Ship the open-loop baseline first; aim for object-aware confirmation as the stretch goal. (02, 03)
4. **Adopt EN 15978 stage labels under the playful overlay** (A1–A3 / A4–A5 / B / C). A visiting architect recognises the structure; a non-expert reads "make / move / use / dispose." (05)
5. **Default the LCA numbers to BEDEC line items for the Catalan baseline.** Cite by ITeC item code on the projector caption rather than generic "brick." (06)
6. **Default LCA claims to the conservative range** (3DCP modest 5–10% advantage per ScienceDirect 2026; CLT 30–40% with biogenic; modular 5–10% initial / 20–25% with reuse). Show optimistic numbers as a separate "best case" toggle, not the headline. (06)
7. **Add reclaimed brick as a baseline-condition token, not a fourth competitor.** See "the fourth method question" above. Anchor with Re:Crete (Küpfer et al. 2021) and Halle 118 (baubüro in situ 2021). (04)
8. **Build Pomponi's five disclosures into a toggleable "why these numbers wobble" layer** of the projection — system boundary, lifespan, biogenic carbon, functional unit, geography/grid mix. This is the team's strongest novelty in the LCA-visualization literature. (06, 05)
9. **A/B-test labels with at least two non-expert pilot visitors before fixing them** ("embodied carbon" vs "the building's hidden carbon" etc.). Schuldt et al. (2011) shows wording effects are large and the team should not guess. (05)
10. **Resolve the unverified citations** (Swiss DJ table, "Brick Vault", "Discrete Wood", "Don't waste a thing!", Küpfer 2023 venue) before the final-presentation slide deck. See "Open questions" below.

---

## Open questions / sources still requiring verification

Aggregated from each strand. The team should resolve these before the May 22 deliverable.

- **The "Swiss museum DJ table"** could not be matched to a Swiss venue. The reacTable is at ZKM Karlsruhe and Game Science Center Berlin. Possibilities: confused with ZKM; temporary exhibition at Museum für Gestaltung Zürich or Vitra (just over the German border); a different installation entirely. *Action: ask the team member who saw it for the museum name and year.* (01)
- **Maquil et al. (2018)** DOI 10.1007/s10109-018-0265-6 verified via Springer link in search but full PDF not fetched. (01)
- **ArUcoTUI (TEI '25)** DOI 10.1145/3731459.3779317 surfaced in search but full paper not opened. (01)
- **COPSE (PACMHCI 2017)** author list cited from search snippet; re-check against ACM record before citing. (01)
- **Settimi et al. 2025 (Augmented Carpentry)** *Automation in Construction* DOI inferred from journal/volume; arXiv preprint (2503.07473) is verified, journal DOI is not. (02, 03, 04)
- **The "82% cumulative-error reduction" figure** widely re-quoted to Funk; locate the original Funk publication and confirm before publishing. (02)
- **Holographic Construction (Jahn et al. 2019, DMSB)** page numbers given are best-estimate; confirm against the front-matter. (02)
- **Cooperative Augmented Assembly (2024)** author list is partial; confirm from Springer landing page. (02)
- **Iowa State / Hoover HoloLens evaluation** DOI inferred from secondary citation; verify. (02)
- **Parascho dissertation co-examiner** (Stelian Coros reported, advisors of record are Gramazio + Kohler). Verify against the front matter at ETH Research Collection (live page returned a server error during the review). (03)
- **Salvi, Pagès & Batlle (2004)** DOI not directly fetched. (03)
- **Augmented Carpentry peer-reviewed venue** verified at project-page level only. (03)
- **Küpfer, Bastien-Masse, Fivet (2023)** exact venue and DOI to confirm via EPFL Infoscience. (04)
- **"Don't waste a thing!"** exact title not located; *Upcycling* (Stockhammer 2020) used as the closest verifiable substitute. Confirm the original reference the team meant. (04)
- **Liu et al. (2025) LCA of prefab 3DP unit with CDW aggregates** journal name to confirm. (04)
- **Gramazio Kohler "Brick Vault"** could not be matched to a specific GKR project. Likely confused with *Iridescence Print* or *Rock Print*. Drop or replace with *Augmented Bricklaying*. (04)
- **EPFL CRCL "Discrete Wood"** could not be confirmed under that exact name; verify against crcl.epfl.ch publication list. The team may be conflating CRCL with EPFL IBOIS's Augmented Carpentry. (04)
- **Carbon Visuals NYC project effectiveness data** — viral reach is documented; no peer-reviewed effectiveness study located. Treat as design precedent only. (05)
- **Tree-sequestration constants** range 10–40 kg CO₂/year per tree depending on species/climate/age. Do not present as a fixed constant without source. (05)
- **EC3 adoption figures** (>19,000 users / 70 countries) are self-reported by Building Transparency. (05)
- **Visitor Studies 28(2), 2024 Wild Center exit-interview methodology** should be checked before strong claims. (05)
- **DFAB House whole-building LCA** — per-element studies exist (Smart Slab) but a single peer-reviewed whole-house LCA was not located. (06)
- **TECLA per-m² CO₂ figures** appear to derive from press materials, not peer-reviewed LCA. (06)
- **Liu et al. 2021 46.5% biogenic figure** — check against original Energy & Buildings paper for boundary specification. (06)
- **Findings (2024) "factor of 2.5" headline** (58 vs 147 kg CO₂-eq/m²) cross-check against underlying mix design — appears to assume an aggressive low-cement printable mix. (06)
- **Disseny Hub *Matter Matters* IAAC role** — cross-check curatorial credits in person before final-presentation slide. (06)
- **BEDEC 2026 indicator count (22) and EN 15804+A2 alignment** from ITeC press release; verify in current online database before quoting. (06)

Two minor cross-strand discrepancies worth flagging: strands 02, 03, and 04 each cite Augmented Bricklaying (Mitterberger et al. 2020) and converge on the same DOI; strands 02 and 03 each cite Bimber & Raskar (2005) and converge on the same ISBN and free PDF. No conflicting citations were found across strands.

---

## How this lit review positions the project for grading

For the final-presentation literature/precedents slide, the team should name-check three citations in three sentences. The first sentence should establish the *interaction lineage*: cite **Underkoffler & Ishii (1999) Urp** as the direct ancestor of the puck-on-table-with-overhead-projection idea, and **Jordà et al. (2007) reacTable** as the most public-facing exemplar of fiducial-tracked tabletops. The second sentence should establish the *assembly-as-FSM framing*: cite **Parascho (2019) Cooperative Robotic Assembly** for the conceptual move of treating valid intermediate states as a first-class concept (not a technical inheritance — explicitly a framing inheritance, which is honest and defensible), and add **Mitterberger et al. (2020) Augmented Bricklaying** as the closest published interaction precedent. The third sentence should establish the *LCA-honesty* contribution: cite **Pomponi & Moncaster (2016, 2017)** and **De Wolf, Hoxha & Fivet (2020)** as the methodological backbone, with **Küpfer, Bastien-Masse & Fivet (2021) Re:Crete** as the reuse anchor and **BEDEC** as the Catalan local-baseline source.

This is a defensible positioning because it (a) avoids overclaiming novelty by citing the right ancestors, (b) explicitly distinguishes framing inheritance from technical inheritance (which a serious reviewer will respect), and (c) names the methodological scaffolding that lets the team pre-empt the "you cherry-picked the LCA" attack. It also frees the team from the unverified "Swiss museum DJ table" and lets them put the reacTable in the slide instead — a stronger, citable precedent.

---

## Full reference list (deduplicated, alphabetized by first author)

Tier annotations: **[Peer-rev]** peer-reviewed venue; **[Book]** book or book chapter; **[Diss]** doctoral dissertation; **[Project]** built work or project page; **[Practitioner]** practitioner / industry / vendor; **[Grey]** institutional grey literature.

- Alhumayani, H., et al. (2020). Environmental assessment of large-scale 3D printing in construction: A comparative study between cob and concrete. *Journal of Cleaner Production*. **[Peer-rev]** (06)
- Allen, S. (2004). Designs for Learning: Studying Science Museum Exhibits That Do More Than Entertain. *Science Education* 88(S1). https://doi.org/10.1002/sce.20016 **[Peer-rev]** (06)
- ArUcoTUI (TEI '25). https://dl.acm.org/doi/10.1145/3731459.3779317 **[Peer-rev — unverified]** (01)
- BAMB (Buildings as Material Banks), EU Horizon 2020 grant 642384, 2015–2019. https://bamb2020.eu **[Practitioner / policy]** (04)
- baubüro in situ (2021). K.118 Kopfbau Halle 118, Winterthur. https://insitu.ch **[Project]** (04)
- Bencina, R., Kaltenbrunner, M., & Jordà, S. (2005). Improved topological fiducial tracking in the reacTIVision system. *2005 IEEE CVPR Workshops*, vol. 3, 99. https://doi.org/10.1109/CVPR.2005.475 **[Peer-rev]** (01)
- BEDEC / ITeC (2025–2026). Banco BEDEC. https://en.itec.cat/services/bedec/ **[Grey / institutional]** (06)
- Bhattacherjee, S. et al. / Kuzmenko et al. (2020). 3D Concrete Printing Sustainability: A Comparative Life Cycle Assessment of Four Construction Method Scenarios. *Buildings* 10(12), 245. https://www.mdpi.com/2075-5309/10/12/245 **[Peer-rev]** (06)
- Bimber, O., & Raskar, R. (2005). *Spatial Augmented Reality: Merging Real and Virtual Worlds*. A K Peters/CRC Press. ISBN 978-1-56881-230-4. https://pages.cs.wisc.edu/~dyer/cs534/papers/SAR.pdf **[Book]** (02, 03)
- Brütting, J., Desruelle, J., Senatore, G., & Fivet, C. (2019). Design of truss structures through reuse. *Structures* 18, 128–137. **[Peer-rev]** (04)
- Building Transparency. EC3 (Embodied Carbon in Construction Calculator). https://buildingtransparency.org/ec3 **[Practitioner]** (05)
- Carbon Leadership Forum / Priopta. Whole-building LCA tool comparison reviews. https://carbonleadershipforum.org **[Practitioner]** (05)
- Carbon Visuals / Real World Visuals (2012). NYC's CO₂ in real time. https://realworldvisuals.com **[Practitioner]** (05)
- Climate Museum, NYC. https://www.climatemuseum.org/work/exhibitions **[Project / institutional]** (06)
- Concular / Restado. Marketplace for reclaimed building materials. https://concular.de , https://restado.de **[Practitioner]** (04)
- Cooper Hewitt. *Nature — Design Triennial* (2019–2020); *Designing Peace* (2022–2023). https://www.cooperhewitt.org **[Project / institutional]** (06)
- Derivative. Table-Driven Finite State Machine (FSM). https://derivative.ca/community-post/asset/table-driven-finite-state-machine-fsm-manage-interactive-logic-cleanly-free **[Practitioner]** (03)
- De Wolf, C., Hoxha, E., & Fivet, C. (2020). Comparison of environmental assessment methods when reusing building components. *Sustainable Cities and Society* 61, 102322. **[Peer-rev]** (04)
- De Wolf, C., Hertwich, E., et al. (2023). Reducing embodied carbon in structural systems. MIT preprint. https://dspace.mit.edu/bitstream/handle/1721.1/152266/2023-06-09%20preprint.pdf **[Peer-rev preprint]** (06)
- Dietz, P., & Leigh, D. (2001). DiamondTouch: a multi-user touch technology. *Proc. UIST '01*, 219–226. https://doi.org/10.1145/502348.502389 **[Peer-rev]** (01)
- Dietz, T., Gardner, G. T., Gilligan, J., Stern, P. C., & Vandenbergh, M. P. (2009). Household actions can provide a behavioral wedge to rapidly reduce US carbon emissions. *PNAS* 106(44): 18452–18456. **[Peer-rev]** (05)
- Disseny Hub Barcelona. *Matter Matters: Designing with the World* (2025). https://www.dissenyhub.barcelona/ **[Project / institutional]** (06)
- Dörfler, K., Sandy, T., Giftthaler, M., Gramazio, F., Kohler, M., & Buchli, J. (2016). Mobile Robotic Brickwork. In *Robotic Fabrication in Architecture, Art and Design 2016*, Springer. https://doi.org/10.1007/978-3-319-26378-6_15 **[Peer-rev]** (02)
- Doshi, A., Smith, R. T., Thomas, B. H., & Bouras, C. (2017). Use of projector-based augmented reality to improve manual spot-welding precision and accuracy. *Int. J. Adv. Manuf. Technol.* 89, 1279–1293. https://doi.org/10.1007/s00170-016-9164-5 **[Peer-rev]** (02)
- Eden Project, Cornwall. https://www.edenproject.com/ **[Project / institutional]** (06)
- Falk, J. H., & Dierking, L. D. (2013/2016). *The Museum Experience Revisited*. Routledge. https://www.routledge.com/The-Museum-Experience-Revisited/Falk-Dierking/p/book/9781611320459 **[Book]** (06)
- Findings (2024). Comparison of Embodied Carbon of 3D-printed vs. Conventionally Built Houses. https://findingspress.org/article/89707 **[Peer-rev]** (06)
- Fologram (Jahn, G., Newnham, C.). *Steampunk Pavilion*, Tallinn Architecture Biennale 2019. https://www.archdaily.com/926191/ **[Project]** (02)
- Follmer, S., Leithinger, D., Olwal, A., Hogge, A., & Ishii, H. (2013). inFORM: dynamic physical affordances and constraints through shape and object actuation. *Proc. UIST '13*, 417–426. https://doi.org/10.1145/2501988.2502032 **[Peer-rev]** (01)
- Funk, M., Bächler, A., Bächler, L., Kosch, T., Heidenreich, T., & Schmidt, A. (2016). Interactive worker assistance: comparing the effects of in-situ projection, head-mounted displays, tablet, and paper instructions. *Proc. UbiComp '16*, 934–939. https://doi.org/10.1145/2971648.2971706 **[Peer-rev]** (02)
- Funk, M., & Lischke, L. (2017). *Teach Me How!* Springer book chapter. https://doi.org/10.1007/978-981-10-6404-3_4 **[Book chapter]** (02)
- Garrido-Jurado, S., Muñoz-Salinas, R., Madrid-Cuevas, F. J., & Marín-Jiménez, M. J. (2014). Automatic generation and detection of highly reliable fiducial markers under occlusion. *Pattern Recognition* 47(6), 2280–2292. https://doi.org/10.1016/j.patcog.2014.01.005 **[Peer-rev]** (01)
- Giftthaler, M., Sandy, T., Dörfler, K., et al. (2017). Mobile robotic fabrication at 1:1 scale: the In situ Fabricator. *Construction Robotics* 1, 3–14. https://doi.org/10.1007/s41693-017-0003-5 **[Peer-rev]** (02)
- Helm, V., Ercan, S., Gramazio, F., & Kohler, M. (2014). In-Situ Robotic Fabrication. In *Gearing Up and Accelerating Cross-fertilization between Academic and Industrial Robotics Research in Europe*, Springer Tracts in Advanced Robotics 94. https://doi.org/10.1007/978-3-319-03838-4_4 **[Book chapter]** (02)
- Hemmati, M. et al. (2024). Comparison of Embodied Carbon Footprint of a Mass Timber Building. USDA Forest Products Lab / Buildings. https://www.fpl.fs.usda.gov/documnts/pdf2024/fpl_2024_hemmati002.pdf **[Peer-rev]** (06)
- Hilliges, O., Baur, D., & Butz, A. (2007). PhotoHelix: browsing, sorting and sharing digital photo collections. *2nd IEEE Tabletop Workshop*, 87–94. https://doi.org/10.1109/TABLETOP.2007.18 **[Peer-rev]** (01)
- Huang, Y., Garrett, C. R., & Mueller, C. T. (2018). Automated sequence and motion planning for robotic spatial extrusion of 3D trusses (Choreo). *Construction Robotics* 2, 15–39. https://doi.org/10.1007/s41693-018-0012-z ; arXiv:1810.00998 **[Peer-rev]** (03)
- IPCC WGI Technical Support Unit (2022). IPCC Visual Style Guide for WGI Authors. **[Grey / institutional]** (05)
- Ishii, H., & Ullmer, B. (1997). Tangible bits: towards seamless interfaces between people, bits and atoms. *Proc. CHI '97*, 234–241. https://doi.org/10.1145/258549.258715 **[Peer-rev]** (01)
- Ishii, H., Lakatos, D., Bonanni, L., & Labrune, J.-B. (2012). Radical atoms: beyond tangible bits, toward transformable materials. *Interactions* 19(1), 38–51. https://doi.org/10.1145/2065327.2065337 **[Magazine]** (01)
- Jahn, G., Newnham, C., van den Berg, N., Iraheta, M., & Wells, J. (2019). Holographic Construction. In *Impact: Design With All Senses — Proc. DMSB 2019*, Springer, 314–324. https://doi.org/10.1007/978-3-030-29829-6_25 **[Peer-rev]** (02)
- Jansen, Y., Dragicevic, P., et al. (2015). Opportunities and challenges for data physicalization. *Proc. CHI '15*, 3227–3236. **[Peer-rev]** (05)
- Jordà, S., Geiger, G., Alonso, M., & Kaltenbrunner, M. (2007). The reacTable: exploring the synergy between live music performance and tabletop tangible interfaces. *Proc. TEI '07*, 139–146. https://doi.org/10.1145/1226969.1226998 **[Peer-rev]** (01)
- Kahan, D. M., et al. (2012). The polarizing impact of science literacy and numeracy on perceived climate change risks. *Nature Climate Change* 2, 732–735. **[Peer-rev]** (05)
- Kaltenbrunner, M., Bovermann, T., Bencina, R., & Costanza, E. (2005). TUIO: a protocol for table-top tangible user interfaces. *Proc. 6th Int. Workshop on Gesture in HCI and Simulation*. https://modin.yuri.at/publications/tuio_gw2005.pdf **[Peer-rev]** (01)
- Kaltenbrunner, M., & Echtler, F. (2018). The TUIO 2.0 Protocol. *Proc. ACM HCI* 2 (EICS), Article 8. https://doi.org/10.1145/3229090 **[Peer-rev]** (01)
- Kato, H., & Billinghurst, M. (1999). Marker tracking and HMD calibration for a video-based augmented reality conferencing system. *Proc. IWAR '99*, 85–94. https://doi.org/10.1109/IWAR.1999.803809 **[Peer-rev]** (01)
- Küpfer, C., Bastien-Masse, M., Devènes, J., & Fivet, C. (2021). Re:Crete Footbridge. EPFL SXL & Smart Living Lab. **[Project]** (04)
- Küpfer, C., Bastien-Masse, M., & Fivet, C. (2023). Reuse of cut concrete (journal article — venue unverified). **[Peer-rev — venue unverified]** (04)
- Liu, Y. et al. (2021). Comparative LCA of cross laminated timber building and concrete building with special focus on biogenic carbon. *Energy & Buildings*. https://www.sciencedirect.com/science/article/pii/S0378778821008884 **[Peer-rev]** (06)
- Liu et al. (2025). LCA of prefabricated 3D-printed structural units using recycled CDW aggregates. **[Peer-rev — venue unverified]** (04)
- Lupi, G., & Posavec, S. (2016). *Dear Data*. Princeton Architectural Press. **[Book]** (05)
- Madaster Foundation (NL). https://madaster.com **[Practitioner]** (04)
- Maquil, V., Tobias, E., De Sousa, L., Schwartz, L., & Zephir, O. (2018). Towards a framework for geospatial tangible user interfaces in collaborative urban planning. *Journal of Geographical Systems* 20(2), 185–206. https://doi.org/10.1007/s10109-018-0265-6 **[Peer-rev]** (01)
- Mensah-Attipoe, J., et al. (2025). Recycled Components in 3D Concrete Printing Mixes: A Review. *Materials* 18(19), 4517. **[Peer-rev]** (04)
- Merrill, D., Kalanithi, J., & Maes, P. (2007). Siftables: towards sensor network user interfaces. *Proc. TEI '07*, 75–78. https://doi.org/10.1145/1226969.1226984 **[Peer-rev]** (01)
- Microsoft Surface / PixelSense (2007–2012). https://en.wikipedia.org/wiki/Microsoft_PixelSense **[Practitioner]** (01)
- Miebach, N. Sculptural works using NOAA / weather-station data. https://nathaliemiebach.com **[Practitioner / art]** (05)
- Mitterberger, D., Dörfler, K., Sandy, T., Salveridou, F., Hutter, M., Gramazio, F., & Kohler, M. (2020). Augmented bricklaying. *Construction Robotics* 4, 151–161. https://doi.org/10.1007/s41693-020-00035-8 **[Peer-rev]** (02, 03, 04)
- Mitterberger, D., et al. (2022). Interactive Robotic Plastering. *Proc. CHI 2022*. https://doi.org/10.1145/3491102.3501842 **[Peer-rev]** (02, 03)
- Mitterberger, D., et al. (2024). Cooperative augmented assembly (CAA). *Construction Robotics* 8. https://doi.org/10.1007/s41693-024-00138-6 **[Peer-rev]** (02)
- Mohammad, M., et al. (2023). A systematic review of life cycle assessments of 3D concrete printing. *Cleaner Materials*. https://www.sciencedirect.com/science/article/pii/S2666412723000132 **[Peer-rev]** (06)
- Moreno, D., & Taubin, G. (2012). Simple, accurate, and robust projector-camera calibration. *Proc. 3DIMPVT 2012*. http://mesh.brown.edu/calibration/ **[Peer-rev]** (03)
- Parascho, S. (2019). *Cooperative Robotic Assembly: Computational Design and Robotic Fabrication of Spatial Metal Structures*. ETH Zurich, Diss. ETH No. 25839. https://doi.org/10.3929/ethz-b-000364322 **[Diss]** (03)
- Parascho, S., et al. (2020). LightVault. *AAG 2020 Proceedings*. https://thinkshell.fr/wp-content/uploads/2019/10/AAG2020_18_Parascho.pdf **[Peer-rev]** (03)
- Piper, B., Ratti, C., & Ishii, H. (2002). Illuminating clay: a 3-D tangible interface for landscape analysis. *Proc. CHI '02*, 355–362. https://doi.org/10.1145/503376.503439 **[Peer-rev]** (01)
- Pomponi, F., & Moncaster, A. (2016). Embodied carbon mitigation and reduction in the built environment. *Journal of Environmental Management* 181, 687–700. **[Peer-rev]** (04)
- Pomponi, F., & Moncaster, A. (2017). Scrutinising embodied carbon in buildings: the next performance gap made manifest. *Journal of Cleaner Production*. https://www.sciencedirect.com/science/article/abs/pii/S136403211730998X **[Peer-rev]** (06)
- Ragan, M. (2019). TouchDesigner Case Study: Custom Parameters and Cues. https://matthewragan.com/2019/05/06/touchdesigner-case-study-custom-parameters-and-cues/ **[Practitioner]** (03)
- Reijnierse, W. G., et al. (2025). The differential effects of metaphor on comprehensibility and comprehension of environmental concepts. *JCOM* 24(04): A01. **[Peer-rev]** (05)
- Salvi, J., Pagès, J., & Batlle, J. (2004). Pattern codification strategies in structured light systems. *Pattern Recognition* 37(4), 827–849. **[Peer-rev — DOI unverified]** (03)
- ScienceDirect (2026). On the sustainability of digital construction: Whole building life cycle carbon emissions according to three construction techniques. https://www.sciencedirect.com/science/article/abs/pii/S2352710226004845 **[Peer-rev]** (06)
- Schuldt, J. P., Konrath, S. H., & Schwarz, N. (2011). 'Global warming' or 'climate change'? *Public Opinion Quarterly* 75(1): 115–124. **[Peer-rev]** (05)
- Settimi, A., Gamerro, J., & Weinand, Y. (2025). Augmented Carpentry. *Automation in Construction* 179. arXiv:2503.07473. https://github.com/ibois-epfl/augmented-carpentry **[Peer-rev — DOI unverified]** (02, 03, 04)
- Spence, A., & Pidgeon, N. (2010). Framing and communicating climate change. *Global Environmental Change* 20(4): 656–667. **[Peer-rev]** (05)
- Stockhammer, D. (Ed.) (2020). *Upcycling: Reuse and Repurposing as a Design Principle in Architecture*. University of Liechtenstein. **[Book]** (04)
- SXL EPFL. Reuse of cut concrete research line. https://sxl.epfl.ch/research/reuse-of-concrete **[Project / institutional]** (04)
- TECLA (Mario Cucinella Architects + WASP, 2021). 3D-printed earth house, Massa Lombarda. https://www.3dwasp.com/en/3d-printed-house-tecla/ **[Practitioner / vendor]** (06)
- Tissoires, B. et al. (2017). COPSE: software framework for instantiating problem-solving microworlds on tangible tabletops. *PACMHCI*. https://doi.org/10.1145/3095808 **[Peer-rev]** (01)
- Triennale di Milano. *Broken Nature* (2019). https://triennale.org/en/events/broken-nature **[Project / institutional]** (06)
- Underkoffler, J., & Ishii, H. (1999). Urp: a luminous-tangible workbench for urban planning and design. *Proc. CHI '99*, 386–393. https://doi.org/10.1145/302979.303114 **[Peer-rev]** (01)
- Vitra Design Museum. *Plastic: Remaking Our World* (2022); *Garden Futures* (2023). https://www.design-museum.de/ **[Project / institutional]** (06)
- Wang, X., et al. (2024). Comparative analysis of embodied carbon in modular and conventional construction methods in Hong Kong. *Scientific Reports* 14. https://www.nature.com/articles/s41598-024-73906-7 **[Peer-rev]** (06)
- Weiss, M., Wagner, J., Jansen, Y., Jennings, R., Khoshabeh, R., Hollan, J. D., & Borchers, J. (2009). SLAP widgets: bridging the gap between virtual and physical controls on tabletops. *Proc. CHI '09*, 481–490. https://doi.org/10.1145/1518701.1518779 **[Peer-rev]** (01)
- Yale Program on Climate Change Communication / Wild Center *Climate Solutions* exit interviews. *Visitor Studies* 28(2), 2024. **[Peer-rev]** (05)

---

## AI disclosure

This literature review was conducted by Claude (Anthropic) on 2026-05-03 using a six-agent research pipeline orchestrated through the deep-research skill. Six sub-area researcher agents independently produced the strand files (`01-tui-tabletops.md` through `06-comparative-lca-and-museum-interactives.md`); a synthesis agent (also Claude) produced this OVERVIEW from those six inputs. Sources were retrieved via web search and verified at the citation-detail level by each per-strand agent. All citations should be independently verified by the team before being used in academic submissions, course deliverables, or public-facing materials. Unverified claims are explicitly flagged in each strand file under "Sources requiring verification" and aggregated above under "Open questions / sources still requiring verification." DOIs and venue details that the strand agents could not personally fetch are tagged accordingly in the reference list. The team is responsible for the final accuracy of any claim that ends up on the May 22 demo, in the project documentation, or in any submitted paper.
