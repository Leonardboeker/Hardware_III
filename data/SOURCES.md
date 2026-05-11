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
