# Data Inventory — Hardware III LCA Installation

**Project:** Group 3 tabletop interactive LCA installation, MRAC 2025/26
**Inventory date:** 2026-05-04
**Owner:** Role 6 (Data Research + Narrative)
**Status:** 6 of 7 strands complete; strand 07 (Spanish/Catalan superpowers, 6 agents) running

---

## 1. Decision unit

| Axis | Unit |
|------|------|
| Spatial | kg CO₂eq / m² of GFA, broken down per construction phase (foundation / structure / roof / openings / finishing) |
| Temporal | A1–A3 cradle-to-gate at minimum; A4 transport noted; B/C/D where data exists |
| Methodological | Every value as a low/high range + named assumption text — single figures forbidden (locked decision #4) |
| Geographic priority | Catalonia ▸ Spain ▸ EU ▸ global — widest only when no regional data exists |
| Methods | Masonry · 3D-printed · Prefab (modular concrete + CLT) · Reclaimed brick (baseline floor) |

**2× resolution rule:** every value must be attributable to a *specific phase × specific method*. Whole-building studies require explicit back-calculation with stated reference baseline.

---

## 2. Strand-by-strand inventory

### Strand 01 — Masonry (✅ complete)

`docs/research_2/01-masonry/` → `BIBLIOGRAPHY.md` (11 entries) + `VALUES.md` (15 of 25 cells populated) + `SYNTHESIS.md` (2,662 words)

**Anchor sources (all verified at primary source):**

| Source | Type | Tier | Geo | Provenance | Resolution | Coverage | Licence | Bias | Total |
|---|---|---|---|---|---|---|---|---|---|
| Hispalyt GlobalEPD 008-016 (clay facing brick) | EPD ISO 14025 | 1 | 🇪🇸 ES | 3 | 3 | 2 | 3 (free PDF) | 1 (industry-published, third-party verified) | **12/15** |
| Hispalyt GlobalEPD 008-017 (clay block + perforated) | EPD ISO 14025 | 1 | 🇪🇸 ES | 3 | 3 | 2 | 3 | 1 | **12/15** |
| Hispalyt GlobalEPD 008-001 (clay roof tile) | EPD ISO 14025 | 1 | 🇪🇸 ES | 3 | 3 | 2 | 3 | 1 | **12/15** |
| CYPE FEF010 + FFZ010 | Commercial database | 1 | 🇪🇸 ES | 3 | 3 | 3 | 1 (paid) | 2 | **12/15** |
| BEDEC ITeC | Institutional | 1 | 🇪🇸 ES (Catalan) | 3 | 3 | 3 | 2 (account required) | 2 | **13/15** |
| Izaola et al. 2023 (whole-life carbon Spanish residential) | Peer-reviewed | 1 | 🇪🇸 ES | 3 | 2 | 2 | 3 | 2 | **12/15** |
| Mateus 2023 (literature mean 200 kg/tonne) | Peer-reviewed | 1 | 🇪🇺 EU | 3 | 2 | 2 | 3 | 2 | **12/15** |
| Pomponi & Moncaster 2018 (methodology) | Peer-reviewed | 1 | 🇪🇺 EU | 3 | 1 | 3 | 3 | 2 | **12/15** |

**Verdict:** Masonry is **the strongest method** in this corpus. Catalan provenance is real, peer-reviewed triangulation holds (Hispalyt 209 ↔ Mateus 200, within 5%).

### Strand 02 — 3D-printed (✅ complete)

`docs/research_2/02-3d-printed/` → 17 sources (8 T1, 2 T2, 5 T3 + rejected) + 34 phase rows

**Anchor sources:**

| Source | Type | Tier | Geo | Provenance | Resolution | Coverage | Licence | Bias | Total |
|---|---|---|---|---|---|---|---|---|---|
| Motalebi, Khondoker & Kabir 2024 (meta-review) | Peer-reviewed | 1 | 🌍 GLOBAL | 3 | 2 | 3 | 3 | 2 | **13/15** |
| Alhumayani, Gomaa, Soebarto, Jabi 2020 (cob vs concrete) | Peer-reviewed | 1 | 🇬🇧 UK/Saudi | 3 | 2 | 1 (wall-only) | 3 | 2 | **11/15** |
| Mohammad, Masad, Al-Ghamdi 2020 (Buildings 10(12)) | Peer-reviewed | 1 | 🇶🇦 Qatar | 3 | 3 | 2 | 3 | 2 | **13/15** |
| Rossi 2024 (Findings press, 2.5× claim) | Peer-reviewed (small sample) | 1 | 🇺🇸 US | 2 | 2 | 1 | 3 | 1 (most contested) | **9/15** |
| Yang et al. 2026 (whole-building 100-yr) | Peer-reviewed | 1 | 🇺🇸 US | 3 | 3 | 3 | 2 (paywalled) | 2 | **13/15** |
| MIT/ICON white paper 2024 | Industry-academic hybrid | 2 | 🇺🇸 US | 2 | 2 | 2 | 3 | 1 (vendor-funded) | **10/15** |
| TECLA / WASP 2021 | Vendor | 3 | 🇮🇹 IT | 2 | 1 | 1 | 3 | 1 | **8/15** |
| TOVA / IAAC 2022 | Institutional (no LCA) | 2 | 🇪🇸 ES (Catalan) | 2 | 2 | 1 | 3 | 2 | **10/15** |

**Verdict:** 3DP corpus is global, no Spanish peer-reviewed LCA exists. TOVA (IAAC, 50m local-material radius) is the only Catalan demonstrator. **YES-WITH-CAVEATS** — methodology-wobble overlay essential (5-source contradiction triangle).

### Strand 03 — Prefab (✅ complete)

`docs/research_2/03-prefab/` → 14 sources (8 T1, 3 EPDs, 3 institutional) + 33 rows + sub_method column

**Anchor sources:**

| Source | Type | Tier | Geo | Provenance | Resolution | Coverage | Licence | Bias | Total |
|---|---|---|---|---|---|---|---|---|---|
| Wei, Ge, Zhong, Lee, Zhang 2024 (modular Hong Kong) | Peer-reviewed | 1 | 🇭🇰 HK | 3 | 3 | 2 | 3 | 1 (HK-specific) | **12/15** |
| Andersen, Rasmussen, Ryberg 2022 (CLT vs concrete biogenic) | Peer-reviewed | 1 | 🇩🇰 DK | 3 | 3 | 2 | 3 | 2 | **13/15** |
| Hemmati 2024 (mass timber vs steel) | Peer-reviewed | 1 | 🇺🇸 US | 3 | 2 | 2 | 3 | 2 | **12/15** |
| Stora Enso EPD (CLT) | EPD ISO 14025 | 1 | 🇸🇪 SE / 🇦🇹 AT | 3 | 3 | 2 | 3 | 1 (industry) | **12/15** |
| Pan & Hon, Quale 2012 (modular reuse lever) | Peer-reviewed | 1 | 🇺🇸 US | 3 | 1 | 1 | 3 | 2 | **10/15** |

**Verdict:** Prefab corpus is mixed-geo. CLT is unavoidably Austrian/Swedish (no Spanish CLT mills exist). Modular concrete dominated by Hong Kong literature. **Defensible only with 4 projection-layer toggles:** with/without biogenic, single-life vs two-life, A4-to-Catalonia ON, ranges as bands.

### Strand 04 — Reclaimed brick (✅ complete)

`docs/research_2/04-reclaimed-brick/` → 12 sources + 25 cells + extra `allocation_rule` column

**Anchor sources:**

| Source | Type | Tier | Geo | Provenance | Resolution | Coverage | Licence | Bias | Total |
|---|---|---|---|---|---|---|---|---|---|
| Devènes et al. 2022 (Re:Crete Structures) | Peer-reviewed | 1 | 🇨🇭 CH | 3 | 3 | 2 | 3 | 2 (showcase) | **13/15** |
| Salmio & Huuhka 2026 (Buildings & Cities) | Peer-reviewed | 1 | 🇫🇮 FI | 3 | 3 | 3 | 3 | 2 | **14/15** |
| De Wolf, Hoxha & Fivet 2020 (allocation methods) | Peer-reviewed | 1 | 🇨🇭 CH | 3 | 2 | 3 | 3 | 2 | **13/15** |
| Devos et al. 2024 | Peer-reviewed | 1 | 🇧🇪 BE | 3 | 2 | 2 | 1 (403-blocked at fetch) | 2 | **10/15** |
| Reclaimed Brick Company UK EPD | EPD ISO 14025 | 1 | 🇬🇧 UK | 3 | 3 | 1 | 3 | 1 (industry) | **11/15** |
| baubüro in situ K.118 / Halle 118 | Institutional | 2 | 🇨🇭 CH | 2 | 2 | 2 | 3 | 1 (advocate-published) | **10/15** |

**Verdict:** Reclaimed brick is **NOT in BEDEC** (`totxo recuperat` confirmed absent). Catalan tier-1 LCA does not exist. Swiss anchors with allocation-rule wobble. **Allocation swing is ~5×** across cut-off / avoided-burden / system-expansion → this *is* the projection finding, not a footnote.

### Strand 05 — Animations + gesture (✅ complete)

`docs/research_2/05-animations-and-gesture/` → 22 sources + 4 sub-strands

**Critical findings:**
- **MediaPipe Hands via Blankensmith TouchDesigner plugin** (`torinmb/mediapipe-touchdesigner`) — production path for the gesture pivot
- **MediaPipe FAILS on IR/grayscale** (issue #2008) — RGB-only; Ultraleap Leap Motion 2 is the documented fallback
- **Sora discontinued** (web/app 2026-04-26, API 2026-09-24) — removed from candidate set
- **Kling 3.0** (Feb 2026) leads on physics fidelity for AI animation
- **HOPs at ~2.5 Hz** (Hullman 2015 + Kale 2019, IEEE TVCG) — empirical basis for the methodology-wobble visualization
- **Augmented Bricklaying / Kitrvs Winery** + **UC Davis AR Sandbox** are the two precedents to study most closely

### Strand 06 — Gap-filling (✅ complete)

`docs/research_2/06-gaps-feasibility-jobs-budget/` → 24 sources, 5 sub-strand tables, NARRATIVE-IMPLICATIONS.md

**Critical findings:**
- **1.5°C carbon budget**: Global Carbon Budget 2025 → **~170 Gt CO₂ remaining (50% probability)**, **breached within ~4 years at current rate**. This is the framing-layer narrative anchor.
- **Spanish rebar correction**: ArcelorMittal **Sagunto is flat-products**, not rebar. Spanish-consumed rebar comes from ArcelorMittal Warsaw (PL), Sonasid (MA), Zenica (BA).
- **Salmio & Huuhka transport thresholds confirmed**: GWP-fossil savings persist to **480 km hand-held / 315 km excavator** for reclaimed brick — much wider than my brief's 100 km rule.
- **Hispalyt market share**: 85% (not 89% as my brief stated).
- **Source-bias direction explicit on jobs data**: McKinsey 2019 / WEF 2025 lowball displacement; Hossain 2020 biases high; ILO labour-protective.

### Strand 07 — Spanish/Catalan superpowers (⏳ running, 6 agents)

`docs/research_2/07-spanish-catalan-superpowers/` (writing in progress)

6 parallel agents in castellano + català covering 3 methods (fábrica de ladrillo · impresión 3D · hormigón prefabricado): Academic literature · Industry/market · Technical · Contrarian · Historical · Future. Targeting Dialnet, CSIC, IETcc, ITeC, UPC, UPM, Hispalyt, CTE, PNIEC, ERESEE, etc.

---

## 3. Geographic provenance summary per method

| Method | Strongest geographic provenance | Catalan/Spanish data status |
|---|---|---|
| **Masonry** | 🇪🇸 ES — Hispalyt EPDs, BEDEC, CYPE, Izaola 2023 | **Strong** — primary Catalan/Spanish data |
| **3D-printed** | 🇺🇸 US (ICON-MIT) + 🇮🇹 IT (TECLA) + 🇶🇦 Qatar academic | **Zero peer-reviewed Catalan LCA.** TOVA is the only Catalan demonstrator (no published LCA). |
| **Prefab — modular concrete** | 🇭🇰 HK (Wei 2024) | **None** — Spanish modular industry small, no Tier-1 Spanish LCA found |
| **Prefab — CLT** | 🇸🇪 SE / 🇦🇹 AT (Stora Enso EPD) | **No Spanish CLT mills** — must use Austrian/Swedish primary EPDs |
| **Reclaimed brick** | 🇨🇭 CH (Re:Crete, K.118) | **BEDEC has no entry confirmed.** No Catalan tier-1 LCA exists. |

The Spanish/Catalan superpowers strand (running) targets specifically the gaps in 3DP, prefab, and ladrillo Spanish-language literature.

---

## 4. Cumulative attribution corrections to project source list

The strands together caught **9 attribution errors** in the existing project lit-review and Plan 02-02 SOURCES list:

| Original key | Corrected attribution |
|---|---|
| `kupfer-2021-recrete` | **Devènes et al. (2022)** *Structures* 43, 1854–1867 — different first author, peer-reviewed 2022 not 2021 |
| `pomponi-2017-wobble` (Cleaner Production) | Actually *Renewable & Sustainable Energy Reviews* 81(P2), 2017 — DOI 10.1016/j.rser.2017.06.049 |
| `wang-2024-modular` | **Wei, Ge, Zhong, Lee, Zhang (2024)** — 20.7% reduction, not 6%. "20–26% with reuse" *not in this paper* (Pan & Hon, Quale 2012). |
| `liu-2021-clt` | **Andersen, Rasmussen, Ryberg (2022)** — 34%, not 46.5% |
| `hemmati-2024-mass-timber` "vs concrete" | Actually vs **steel** — 19% reduction |
| `mohammad-2023-3dp-review` (Cleaner Materials) | **Motalebi, Khondoker & Kabir (2024)** *Sustainable Operations and Computers* 5, 41–58 |
| `sciencedirect-2026-3dp` "2.5× advantage" | **Yang et al. (2026)** — 2–10% advantage |
| ArcelorMittal Sagunto rebar | Sagunto is **flat products**; rebar from Warsaw/Sonasid/Zenica |
| Hispalyt market share 89% | Verified at **85%** |

These corrections will land in `data/SOURCES.md` during the synthesis pass.

---

## 5. Critical methodology wobbles per method

These are the wobbles the projection layer MUST surface to be honest:

| Method | Load-bearing wobble | Magnitude |
|---|---|---|
| Masonry | Mortar mix (cement vs lime) · finishes inclusion · brick firing energy mix | ±20–30% |
| 3D-printed | **Cement content + reinforcement boundary + functional unit** (wall vs GFA) | **±150% (factor 2.5×)** — three peer-reviewed papers, three radically different magnitudes |
| Prefab — modular concrete | Reuse / second-life allocation lever | +20-26% if 25-50yr reuse counted |
| Prefab — CLT | Biogenic carbon convention · A4 transport | ±30% on biogenic alone; A4 adds 25–60 kg CO₂eq/m³ |
| Reclaimed brick | **Allocation rule** (cut-off / avoided-burden / system-expansion) | **~5× swing** (8–25 vs 18–45 vs 35–70 kg CO₂eq/m²) |

All wobbles documented with named assumption text in each strand's `VALUES.md`.

---

## 6. Brief-revisit per method (Step 10 of earn-the-data)

Can the installation defensibly say *"Method X produces Y kg CO₂/m²"*?

| Method | Verdict | Required projection-layer caveat |
|---|---|---|
| Masonry | ✅ **Yes, unchanged** | Catalan-anchored EPD data, just disclose Hispalyt 85% market-share basis |
| 3D-printed | ⚠️ **Yes, but narrower** | Must surface cement-content + reinforcement + functional-unit wobbles. "Numbers from US/Italy/Qatar — no Catalan LCA exists yet" disclosure |
| Prefab — modular | ⚠️ **Yes, but narrower** | "Numbers from Hong Kong typology — Catalan modular industry is smaller" disclosure |
| Prefab — CLT | ⚠️ **Yes, but narrower** | A4 transport from Austria/Sweden defaulted ON. Biogenic-carbon toggle visible. |
| Reclaimed brick | ⚠️ **Yes, with allocation disclosure** | Allocation-rule selector visible to visitor. "Same brick, three numbers, here's why" is the finding, not a problem to hide. |

---

## 7. Open data status

| Source type | Coverage in strands 01–06 | Notes |
|---|---|---|
| Peer-reviewed academic | ~60% | English-dominant; Spanish/Catalan being addressed in strand 07 |
| Industry-published EPDs (free) | ~20% | Hispalyt, Stora Enso, Reclaimed Brick Co UK — third-party verified |
| Institutional / practitioner | ~10% | EPFL SXL, baubüro in situ, IAAC, MIT-ICON |
| Commercial subscription | ~5% | CYPE (Spain) |
| Vendor (Tier 3) | ~5% | TECLA, COBOD, ICON, Apis Cor |
| Open-government data | ~0% (in 01–04) | Strand 06 hits CTE Spain, IPCC, IEA, ILO; strand 07 will hit data.gencat.cat, data.gob.es, DAPconstrucción |

**Open-data sources NOT yet swept** (deferred to strand 07 + synthesis pass):
- ICE Database (Bath, UK) — primary international embodied-carbon DB; useful for **cross-validation** of Spanish numbers, NOT as primary source
- ÖKOBAUDAT (German federal) — same role, cross-validation
- INIES (French national EPD registry) — cross-validation
- ELCD (EU JRC reference DB) — cross-validation
- DAPconstrucción (Spanish national EPD registry) — primary, was 403-blocked in strand 01, retry queued

---

## 8. Pending work

- **Strand 07 (Spanish/Catalan, 6 agents)** — running, ETA ~60 min
- **Synthesis pass** (data-inventory rubric extension, brief-revisit consolidation, attribution corrections to `data/SOURCES.md`) — blocked by 07
- **CSV population** — `data/methods/*.csv` from each strand's `VALUES.md` — blocked by synthesis
- **Per-piece visitor copy** (Role 6 narrative deliverable) — short text shown next to each piece on projection
- **Handoff memo to Role 1** (System Architecture + Integration Lead) — pivot implications + interface contract data

---

*Inventory written 2026-05-04 by Role 6 (Data Research + Narrative). Will be updated when strand 07 returns with Spanish/Catalan findings.*
