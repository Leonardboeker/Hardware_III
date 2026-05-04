---
phase: 2
plan: 01
title: Slide-deck reference corrections (reacTable, Augmented Bricklaying, Augmented Carpentry)
owner: _TBD_
wave: 1
depends_on: []
files_modified:
  - deliverables/proposal.html
  - deliverables/CITATION-CORRECTIONS.md
autonomous: false
requirements:
  - SC-07
estimated_effort_hours: 1
---

<objective>
Apply the three slide-deck reference corrections that the lit review (OVERVIEW.md TL;DR item 5; ACTIONS.md task #6) flagged as misattributions in the existing Phase 1 proposal materials. **This plan addresses ROADMAP Success Criterion #7 (slide-deck reference corrections); no formal REQ-ID exists in REQUIREMENTS.md for it — SC-07 is used here as the traceability anchor.** These three citations leak into every future presentation if not fixed now: (a) "Swiss museum DJ table" is the reacTable (Jordà et al. 2007, on permanent display at ZKM Karlsruhe and Game Science Center Berlin — not Swiss); (b) "Brick Vault" by Gramazio Kohler does not exist as cited and is most likely confused with Iridescence Print or Rock Print — replace with Augmented Bricklaying (Mitterberger et al. 2020); (c) "Discrete Wood" by EPFL CRCL could not be verified — replace with Augmented Carpentry (Settimi et al. 2025, EPFL IBOIS, not CRCL). This plan does not regenerate slides — it documents the exact text replacements and produces a CITATION-CORRECTIONS.md the slide owner uses on the next deck refresh. Phase 6 task #16 will do the final deck rebuild; this plan unblocks any presentation in the meantime by making the corrections explicit.
</objective>

<must_haves>
- File `deliverables/CITATION-CORRECTIONS.md` exists and lists the three before/after text changes with exact citation strings (DOIs, author lists, venues).
- The three citations contain DOIs/URLs verified to land at live pages (or marked `[unverified]` with a documented reason).
- `deliverables/proposal.html` is searched for the three offending strings ("Swiss museum DJ table", "Brick Vault", "Discrete Wood"); if any are present they are replaced inline AND the change logged in CITATION-CORRECTIONS.md. If none are present, the corrections doc still exists for the next deck refresh.
- The corrections doc references back to `docs/research/lit-review/OVERVIEW.md` "TL;DR item 5" and `ACTIONS.md` task #6 so future maintainers can see why the change was made.
</must_haves>

<tasks>

<task type="auto">
  <name>Task 1.1: Audit deliverables/proposal.html for the three offending strings</name>
  <action>Open `deliverables/proposal.html` and grep (or view-source) for each of these three exact substrings, case-insensitive: `Swiss museum DJ table`, `Brick Vault`, `Discrete Wood`. Record for each: (a) whether it is present; (b) the surrounding sentence; (c) the line number. If a variant appears (e.g. "Swiss DJ table at the museum"), record that too. Do NOT modify the file in this task — produce a findings note that Task 1.3 acts on. Save findings as a markdown comment block at the top of `deliverables/CITATION-CORRECTIONS.md` (created in Task 1.2).</action>
  <read_first>
    - deliverables/proposal.html (full file)
    - docs/research/lit-review/OVERVIEW.md lines 26-34 (TL;DR item 5)
    - docs/research/lit-review/04-reuse-and-reclaimed-materials.md "Sources requiring verification" section
  </read_first>
  <acceptance_criteria>
    - `deliverables/CITATION-CORRECTIONS.md` exists.
    - Its first section "## Audit findings (2026-05-03)" contains exactly three subsections — one per offending string — each stating "PRESENT in proposal.html line N: <surrounding sentence>" OR "NOT PRESENT in proposal.html (no occurrence found)".
    - The audit subsection for each string also lists any near-variants found (e.g. "Swiss DJ table" without "museum").
  </acceptance_criteria>
  <rationale>Don't modify the slide source until we've documented what's actually in there — the proposal.html may already be partially corrected, or the offending strings may live in the .pptx (which is binary) instead.</rationale>
</task>

<task type="auto">
  <name>Task 1.2: Write CITATION-CORRECTIONS.md with exact replacement text</name>
  <action>Create `deliverables/CITATION-CORRECTIONS.md` with three subsections under "## Replacements". For each, give the exact wrong-text (as cited in the original proposal language) and the exact replacement-text (with full citation). Use this content verbatim:

  ```
  ### Replacement 1 — "Swiss museum DJ table" → reacTable

  WRONG (any variant): "Swiss museum DJ table", "the DJ table at the Swiss museum", "Swiss museum's DJ-style installation"

  RIGHT: The reacTable (Jordà, Geiger, Alonso & Kaltenbrunner, 2007). On permanent display at ZKM Karlsruhe (Germany) and Game Science Center Berlin (Germany) — NOT at any verified Swiss venue.

  CITATION (use exactly): Jordà, S., Geiger, G., Alonso, M., & Kaltenbrunner, M. (2007). The reacTable: exploring the synergy between live music performance and tabletop tangible interfaces. *Proc. TEI '07*, 139–146. https://doi.org/10.1145/1226969.1226998

  WHY: lit-review/01-tui-tabletops.md and OVERVIEW.md TL;DR item 5 — could not match "Swiss museum DJ table" to any verified venue. If a team member visited a different installation, ask them for the museum name and year and update this doc.

  ### Replacement 2 — "Brick Vault" → Augmented Bricklaying

  WRONG (any variant): "Brick Vault by Gramazio Kohler", "Gramazio Kohler's Brick Vault"

  RIGHT: Augmented Bricklaying (Mitterberger, Dörfler, Sandy, Salveridou, Hutter, Gramazio & Kohler, 2020). Kitrvs winery facade, Greece — 13,596 hand-laid rotated bricks at 225 m² in under three months.

  CITATION (use exactly): Mitterberger, D., Dörfler, K., Sandy, T., Salveridou, F., Hutter, M., Gramazio, F., & Kohler, M. (2020). Augmented bricklaying: human–machine interaction for in situ assembly of complex brickwork using object-aware augmented reality. *Construction Robotics*, 4, 151–161. https://doi.org/10.1007/s41693-020-00035-8

  WHY: lit-review/04-reuse-and-reclaimed-materials.md "Sources requiring verification" — "Brick Vault" could not be matched to any GKR project; likely confused with Iridescence Print (3DP, not reclaimed) or Rock Print (granular, not reclaimed in the salvage sense). Augmented Bricklaying is the right precedent for our interaction loop and is already in our reference set.

  ### Replacement 3 — "Discrete Wood" → Augmented Carpentry (EPFL IBOIS, not CRCL)

  WRONG (any variant): "Discrete Wood by EPFL CRCL", "EPFL CRCL's Discrete Wood project"

  RIGHT: Augmented Carpentry (Settimi, Gamerro & Weinand, 2025, EPFL IBOIS — Laboratory for Timber Constructions). Open-source AR system for sub-mm-precision joint fabrication on irregular timber.

  CITATION (use exactly): Settimi, A., Gamerro, J., & Weinand, Y. (2025). Augmented Carpentry. *Automation in Construction*, 179. arXiv:2503.07473. Code: https://github.com/ibois-epfl/augmented-carpentry. (Journal DOI to verify — arXiv preprint is verified; see lit-review/02 "Sources requiring verification".)

  WHY: lit-review/04 — could not verify a CRCL "Discrete Wood" project under that exact name; closest verifiable match is EPFL IBOIS's Augmented Carpentry. Don't conflate the two labs.
  ```

  Then add a "## How to apply" section explaining: for HTML, edit `deliverables/proposal.html` directly via Task 1.3 below; for `Proposal.pptx` (binary), the slide owner (any team member) opens it in PowerPoint, applies the three replacements manually using the text above verbatim, and re-exports `screenshot_slide*.png`. The .pptx itself is not modified by this plan.</action>
  <read_first>
    - deliverables/CITATION-CORRECTIONS.md (will be partially created in Task 1.1)
    - docs/research/lit-review/OVERVIEW.md
    - docs/research/lit-review/01-tui-tabletops.md (for reacTable citation detail)
    - docs/research/lit-review/02-augmented-assembly.md (for Mitterberger 2020 citation detail)
  </read_first>
  <acceptance_criteria>
    - `deliverables/CITATION-CORRECTIONS.md` contains a "## Replacements" section with exactly three subsections matching the structure above.
    - Each subsection contains a verbatim CITATION line with author list, year, venue, and DOI (or arXiv ID for the unverified one).
    - The `## How to apply` section names both the HTML and PPTX paths and explains who is responsible for the .pptx update.
    - The doc references `docs/research/lit-review/OVERVIEW.md` and `ACTIONS.md` so future readers can trace the rationale.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 1.3: Apply HTML replacements inline (only if Task 1.1 found occurrences)</name>
  <action>For each of the three offending strings that Task 1.1 marked PRESENT in `deliverables/proposal.html`: edit the HTML and replace the string with the RIGHT text from `CITATION-CORRECTIONS.md`. Use the citation form in CITATION-CORRECTIONS.md verbatim (don't shorten or paraphrase). Wrap the citation in a `<cite>` tag if the surrounding HTML pattern uses `<cite>` for other refs; otherwise plain text is fine. After editing, append a "## Applied changes (2026-05-03)" section to `CITATION-CORRECTIONS.md` listing each line number changed and the before/after one-liner. If Task 1.1 found ZERO occurrences, skip the HTML edit and append "## Applied changes (2026-05-03): no occurrences found in proposal.html — corrections doc remains as the canonical reference for next deck refresh".</action>
  <read_first>
    - deliverables/proposal.html
    - deliverables/CITATION-CORRECTIONS.md (Tasks 1.1 + 1.2 output)
  </read_first>
  <acceptance_criteria>
    - If `deliverables/proposal.html` contained any of the three offending strings, none of them are present after this task (verify by re-grepping for the same case-insensitive substrings).
    - `deliverables/CITATION-CORRECTIONS.md` ends with an "## Applied changes (2026-05-03)" section that either lists line-by-line edits OR explicitly states no occurrences were found.
  </acceptance_criteria>
</task>

<task type="checkpoint:human-action">
  <name>Task 1.4: Manual .pptx update by slide owner (HUMAN — Proposal.pptx is binary)</name>
  <what-built>The CITATION-CORRECTIONS.md doc is written and the HTML version is patched. The .pptx is binary and cannot be edited by Claude.</what-built>
  <how-to-verify>
    1. Open `deliverables/Proposal.pptx` in PowerPoint or Keynote.
    2. For each replacement in `deliverables/CITATION-CORRECTIONS.md` "## Replacements", search for the WRONG text variants in the slide deck.
    3. If found, replace with the RIGHT text + CITATION verbatim from the corrections doc.
    4. Re-export `deliverables/screenshot_slide1.png`, `screenshot_slide2.png`, `screenshot_slide3.png` if they reference any changed slide.
    5. Append the manual edit log to `deliverables/CITATION-CORRECTIONS.md` under "## Applied changes — .pptx (YYYY-MM-DD by NAME)".
  </how-to-verify>
  <resume-signal>Type "pptx-corrected" when the .pptx and screenshots are updated, or "no-pptx-occurrences" if the wrong strings were never in the .pptx.</resume-signal>
</task>

</tasks>

<verification>
- `grep -c -i "Swiss museum DJ table\|Brick Vault\|Discrete Wood" deliverables/proposal.html` returns 0.
- `deliverables/CITATION-CORRECTIONS.md` exists and is non-empty.
- `deliverables/CITATION-CORRECTIONS.md` contains the three citation strings: `Jordà`, `Mitterberger`, `Settimi` (one per replacement).
- `deliverables/CITATION-CORRECTIONS.md` contains a `## Applied changes` section.
</verification>
