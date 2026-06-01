# data/SOURCES.md

This registry is used by the normalized metrics pipeline under `data/methods/`.
Each `source_key` below maps to a citation label or an explicit import placeholder.

Format:

`source-key - citation - tier - notes`

alhumayani-2020 - Alhumayani 2020. - Tier 1 - 3D-printed earth proxy row and local-material argument.
allouzi-2020 - Allouzi 2020. - Tier 1 - 3D-printed labour and cost directionality.
andersen-2022 - Andersen 2022. - Tier 1 - Prefab / CLT embodied-carbon and lifecycle references.
apis-cor - Apis Cor / ICON vendor-style demonstrator references cited in imported 3D-printing notes. - Tier 3 - Vendor-style shell-duration and cost references; use as directional only.
bedec-2026 - ITeC Banco BEDEC 2025/2026 release. - Tier 1 - Catalonia baseline for cost, material quantity, and proxy construction rates.
bedec-2026-proxy - ITeC Banco BEDEC 2025/2026 release used as an explicit proxy row. - Tier 2 - Use when the imported row is a BEDEC-derived analogue rather than a direct method match.
binderholz-epd - Binderholz EPD. - Tier 1 - CLT panel embodied-carbon triangulation.
brutting-2020 - Brutting 2020. - Tier 1-2 - Reclaimed-brick structure duration / stock-matching design overhead reference.
concular-2026 - Concular 2026 as cited in the imported reclaimed-brick cost proxy. - Tier 2 - Reclaimed-brick cost proxy input.
cybe-cobod-vendor - CyBe / COBOD vendor claims as cited in imported 3D-printed notes. - Tier 3 - Vendor-only labour/time/cost sibling rows.
cype-spain-fef010 - CYPE Spain FEF010 cost/labour reference line. - Tier 1-2 - Masonry load-bearing perforated-brick labour and cost proxy.
cype-spain-ffz010 - CYPE Spain FFZ010 facade reference line. - Tier 1-2 - Masonry facade labour and cost proxy.
de-wolf-2017 - De Wolf 2017 as referenced in the imported masonry/openings notes. - Tier 2 - Openings embodied-carbon proxy.
de-wolf-2020 - De Wolf 2020. - Tier 1-2 - Reclaimed-brick avoided-burden / system-expansion comparison.
devenes-2022 - Devenes 2022 as cited in the imported reclaimed-brick strand. - Tier 1-2 - Reclaimed-brick scoping and regional sourcing context.
devenes-2022-analogous-scoping - Devenes 2022 analogous-scoping reference as cited in imported reclaimed-brick notes. - Tier 1-2 - Out-of-scope reclaimed-foundation qualitative placeholder.
devos-2024 - Devos 2024 as cited in imported reclaimed-brick finishing notes. - Tier 1-2 - Hydraulic-lime compatibility note for reclaimed-brick finishing.
en-15804 - EN 15804 reference mentioned in the imported source string. - Tier methodology - Methodology-standard anchor preserved when the import cited the standard directly.
engineering-judgement-import - Imported engineering-judgement row without a single resolvable citation token. - Tier provisional - Use only as explicit low-confidence proxy data.
hemmati-2024 - Hemmati 2024. - Tier 1-2 - Prefab / CLT site assembly and reuse notes.
hispalyt-008-001 - Hispalyt GlobalEPD 008-001. - Tier 1 - Spanish clay roof-tile embodied-carbon reference.
hispalyt-008-016 - Hispalyt GlobalEPD 008-016. - Tier 1 - Spanish fired-clay brick / transport proxy for masonry.
hispalyt-008-017 - Hispalyt GlobalEPD 008-017. - Tier 1 - Spanish perforated-brick structural masonry embodied-carbon reference.
iaac-mat-mining - IAAC material-mining project reference as cited in imported reclaimed-brick notes. - Tier 2-3 - Reclaimed-brick structure and finishing context.
iaac-tova - IAAC TOVA project reference. - Tier 2-3 - Catalonia-specific earth-printing material-origin reference.
iaac-tova-wasp-tecla - IAAC TOVA and WASP TECLA project references. - Tier 2-3 - 3D-printed material-origin notes and Catalonia-relevant earth proxy context.
industry-data - Imported industry-data placeholder without a single citable publication. - Tier provisional - Keep as a low-confidence manufacturing proxy until a real plant dataset replaces it.
izaola-2023 - Izaola 2023 as cited in Rafik's imported masonry strand. - Tier 1-2 - Masonry foundation, roof, openings, and finishing proxy values.
k118-insitu - K.118 / in situ project reference as cited in imported reclaimed-brick notes. - Tier 2 - Reclaimed lintel / urban-mining opening reference.
klh-epd - KLH EPD. - Tier 1 - CLT panel fossil and biogenic references.
liu-2021 - Liu 2021. - Tier 1-2 - Prefab end-of-life and methodological allocation notes.
masonry-strand-01 - Imported masonry strand 01 synthesis from Rafik's branch. - Tier provisional - Internal imported synthesis used as a carry-over proxy for non-printed 3D-printing phases.
mateus-2023 - Mateus 2023 as cited in Rafik's imported masonry strand. - Tier 1-2 - Masonry embodied-carbon and finishing-range triangulation.
mohammad-2020 - Mohammad et al. 2020. - Tier 1 - Primary 3D-printed concrete structure row and printer-electricity references.
moodul-vendor - Moodul / modular-concrete vendor references cited in imported prefab notes. - Tier 3 - Spanish prefab transport and cost proxies.
motalebi-2024-review - Motalebi 2024 review. - Tier 1 - 3D-printed concrete material-level per-m3 range.
pan-hon-2012 - Pan and Hon 2012. - Tier 2 - Prefab factory, transport, and site labour/time references.
rbc-epd-2024 - RBC EPD 2024. - Tier 1 - Reclaimed-brick default cut-off baseline and finishing references.
rejected-cype-roof - Imported roof-rate proxy where the original CYPE fetch was unavailable. - Tier 3 - Retained as a provisional import proxy only.
restado-2026 - Restado 2026 as cited in the imported reclaimed-brick cost proxy. - Tier 2 - Reclaimed-brick cost proxy input.
rossi-2024 - Rossi 2024. - Tier 1 - 3D-printed whole-building comparison sanity-check row.
salmio-huuhka-2026 - Salmio and Huuhka 2026. - Tier 1 - Reclaimed-brick allocation-rule, labour, and transport-sensitivity references.
stora-enso-epd - Stora Enso EPD. - Tier 1 - CLT panel carbon, transport, and end-of-life references.
unknown_import - Imported raw source string could not be normalized into a reliable single source key. - Tier provisional - Use when raw import data had missing, compound, or unresolved citations.
wei-2024 - Wei 2024. - Tier 1 - Modular-concrete lifecycle references and reuse sensitivity.
wei-2024-footnote - Wei 2024 footnote / appendix reference as cited in imported prefab notes. - Tier 1-2 - Use when the imported row explicitly relies on the reuse-sensitivity footnote instead of the main table.
wikipedia-tecla - Imported TECLA summary source string from Rafik's 3D-printing strand. - Tier mixed - Used when the imported row names TECLA first in a mixed-source duration proxy.
wikipedia-tecla-icon-press - Imported TECLA / ICON press synthesis row. - Tier mixed - 3D-printed structure total-duration proxy from mixed sources.

---

## Tier 1 — verified academic citations with DOIs / URLs

Audited 2026-05-18. Each entry below was confirmed to correspond to a real published paper by web search of title + author + year. Numbers in `data/methods/*.csv` should be re-checked against the paper before any final jury defence.

### 3D-printed concrete + earth

- **alhumayani-2020** — Alhumayani, H., Gomaa, M., Soebarto, V., Jabi, W. (2020). *Environmental assessment of large-scale 3D printing in construction: A comparative study between cob and concrete*. Journal of Cleaner Production, 270, 122463.
  - DOI: 10.1016/j.jclepro.2020.122463
  - URL: https://www.sciencedirect.com/science/article/abs/pii/S0959652620325105

- **allouzi-2020** — Allouzi, R., Al-Azhari, W., Allouzi, R. (2020). *Conventional Construction and 3D Printing: A Comparison Study on Material Cost in Jordan*. Journal of Engineering (Hindawi / Wiley), 2020, 1424682.
  - DOI: 10.1155/2020/1424682
  - URL: https://onlinelibrary.wiley.com/doi/10.1155/2020/1424682

- **mohammad-2020** — Mohammed, M., Rahman, R., Mohamed, S. F., Ahmad, M. (2020). *3D Concrete Printing Sustainability: A Comparative Life Cycle Assessment of Four Construction Method Scenarios*. Buildings, 10(12), 245.
  - DOI: 10.3390/buildings10120245
  - URL: https://www.mdpi.com/2075-5309/10/12/245
  - Note: paper reports the 44.42 kg CO₂eq/m² wall value for 3DCP without reinforcement using lightweight printable concrete, anchoring the structure row in `3d-printed.csv`.

- **motalebi-2024-review** — Motalebi, A., Khondoker, M. A. H., Kabir, G. (2024). *A systematic review of life cycle assessments of 3D concrete printing*. Sustainable Operations and Computers, 5, 41–50.
  - URL: https://www.sciencedirect.com/science/article/pii/S2666412723000132
  - Open access via DOAJ: https://doaj.org/article/3efb9742bdde4fca87d0dca7f8740c56

- **rossi-2024** — Rossi, B., et al. (2024). *Comparison of Embodied Carbon of 3D-printed vs. Conventionally Built Houses*. Findings, Feb 2024.
  - DOI: 10.32866/001c.89707
  - URL: https://findingspress.org/article/89707-comparison-of-embodied-carbon-of-3d-printed-vs-conventionally-built-houses

### Masonry

- **izaola-2023** — Izaola, B., Akizu-Gardoki, O., Oregi, X. (2023). *Setting baselines of the embodied, operational and whole life carbon emissions of the average Spanish residential building*. Sustainable Production and Consumption, 40, 252–264.
  - URL: https://www.sciencedirect.com/science/article/pii/S2352550923001574

- **mateus-2023** — Ferreira, A., Pinheiro, M. D., de Brito, J., Mateus, R. (2023). *Embodied vs. Operational Energy and Carbon in Retail Building Shells: A Case Study in Portugal*. Energies, 16(1), 378.
  - DOI: 10.3390/en16010378
  - URL: https://www.mdpi.com/1996-1073/16/1/378

### Prefab — CLT + modular concrete

- **andersen-2022** — Andersen, J. H., Rasmussen, N. L., Ryberg, M. W. (2022). *Comparative life cycle assessment of cross laminated timber building and concrete building with special focus on biogenic carbon*. Energy and Buildings, 254, 111604.
  - URL: https://www.sciencedirect.com/science/article/pii/S0378778821008884
  - Note: paper reports 903.7 vs 454.2 kg CO₂eq/m² for concrete vs CLT base scenario.

- **hemmati-2024** — Hemmati, M., Messadi, T., Gu, H., Seddelmeyer, J., Hemmati, M. (2024). *Comparison of Embodied Carbon Footprint of a Mass Timber Building Structure with a Steel Equivalent*. Buildings, 14(5), 1276.
  - DOI: 10.3390/buildings14051276
  - URL: https://www.mdpi.com/2075-5309/14/5/1276

- **wei-2024** — Wei, J., Ge, B., Zhong, Y., et al. (2024). *Comparative analysis of embodied carbon in modular and conventional construction methods in Hong Kong*. Scientific Reports, 14, 22833.
  - DOI: 10.1038/s41598-024-73906-7
  - URL: https://www.nature.com/articles/s41598-024-73906-7

- **pan-hon-2012** — RESOLVED as likely typo for **Pan & Gibb 2012**. No "Pan & Hon" paper exists. The 2012 paper that matches the context (Hong Kong prefab + factory/transport/site labour):
  - Pan, W., Gibb, A.G.F., Dainty, A.R.J. (2012). *Strategies for integrating the use of off-site production technologies in house building*. Journal of Construction Engineering and Management, 138(11), 1331–1340.
  - DOI: 10.1061/(ASCE)CO.1943-7862.0000544
  - Note: this key is not referenced by any row in `data/methods/*.csv`, so dropping or renaming is safe.

- **liu-2021** — UNRESOLVED. Used by three rows in `prefab.csv` (CLT biogenic-stripped A1-A3, modular-concrete EoL no-reuse, reuse allocation discussion). No single 2021 Liu paper covers all three. Most likely candidate by topic match:
  - Liu, Y., et al. (2021). *Life Cycle Assessment of Different Prefabricated Rates for Building Construction*. Buildings 11(11), 552.
  - DOI: 10.3390/buildings11110552
  - URL: https://www.mdpi.com/2075-5309/11/11/552
  - **Action required**: data team must locate the original Liu 2021 PDF used and either confirm this DOI or replace the citation. Until then, treat Liu-2021-sourced rows as Tier 2.

---

## CSV transcription audit — 2026-05-18

Spot-check of three Tier-1 citations against the paper findings reported in the verification web search.

### Mohammad 2020 (3d-printed.csv structure row, co2_kg_per_m2 44 to 90)
- CSV claim: "Mohammad 2020 — 44.42 lightweight unreinforced 3DCP to 58.89 conventional concrete kg CO₂eq/m² wall A1-A3"
- Paper finding: 44.42 kg CO₂eq for 3DCP without reinforcement with lightweight printable concrete; 4-scenario design (conventional, 3DCP-reinforced, 3DCP-no-reinforcement, 3DCP-no-reinforcement-lightweight)
- **Verdict: MATCH.**

### Allouzi 2020 (3d-printed.csv structure rows, labor_hours_per_m2 0.3 to 1.2 and cost_eur_per_m2 200 to 600)
- CSV claim: "Apis Cor 2017 ~250 EUR/m² shell only" + 2-operator print 0.3 h/m² wall + 65% material cost reduction in Jordan context
- Paper finding: 65% material cost reduction; 230 m² home in ~18-19 h with ~4 people. Implied labour productivity 72 worker-h / 230 m² = 0.31 h/m² GFA.
- **Verdict: MATCH on cost-reduction and labour-rate magnitude.**
- Caveat: paper figures are h/m² GFA, CSV labels h/m² wall. Convert via wall:GFA ratio (~0.6 to 0.8) before quoting from the table at the jury.

### Andersen 2022 (prefab.csv A1-A3 rows, embodied_carbon_with_biogenic 130 to 220 and _no_biogenic 220 to 350)
- CSV claim: 130-220 with biogenic credit, 220-350 fossil-only A1-A3 (CLT mid-rise residential)
- Paper finding: base-scenario whole-life emissions **903.7 vs 454.2 kg CO₂eq/m²** for concrete vs CLT; materials contribute 2% vs -54% on GWP with biogenic
- **Verdict: PARTIAL.** The CSV values do not appear directly in the paper's headline numbers (which are whole-LC, not A1-A3 only). Two interpretations: (a) CSV used a sub-table breaking out A1-A3, (b) CSV mixed Andersen 2022 with another anchor.
- **Action required**: data team open Andersen 2022 PDF and locate the table the 130-220 / 220-350 numbers came from. If the table doesn't exist, attribute to the right paper.

### EPDs and vendor / institutional sources

These are not academic papers. Listed for completeness; verifiable via their publishers' EPD registries (S-P-xxxxx codes).

- **binderholz-epd**, **klh-epd**, **stora-enso-epd** — CLT panel EPDs from Binderholz, KLH, Stora Enso. Available via EPD Norway, IBU, or each manufacturer's registry.
- **hispalyt-008-001**, **hispalyt-008-016**, **hispalyt-008-017** — Hispalyt GlobalEPD codes for Spanish fired-clay products. Available via Hispalyt / Global EPD registry.
- **rbc-epd-2024** — Reclaimed brick EPD 2024. (Reclaimed brick dropped from v1 deliverable; left here for archive.)
- **bedec-2026** — ITeC Banco BEDEC 2025/2026 release. Public Catalonia construction-cost database. URL: https://www.itec.cat/nouBedec.c/bedec.aspx
- **cype-spain-fef010**, **cype-spain-ffz010** — CYPE Arquímedes / Generador de precios cost-reference lines. URL: http://www.generadordeprecios.info/

### Reclaimed brick references — kept for archive only

Reclaimed brick was dropped from the v1 jury deliverable on 2026-05-18. The references below remain in the CSVs but are not used at runtime: **brutting-2020**, **concular-2026**, **de-wolf-2017**, **de-wolf-2020**, **devenes-2022**, **devenes-2022-analogous-scoping**, **devos-2024**, **iaac-mat-mining**, **k118-insitu**, **rbc-epd-2024**, **restado-2026**, **salmio-huuhka-2026**.
