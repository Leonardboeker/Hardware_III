---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: Pending — to be planned via `/gsd-plan-phase 2`
last_updated: "2026-05-03T21:57:31.724Z"
progress:
  total_phases: 6
  completed_phases: 0
  total_plans: 8
  completed_plans: 0
  percent: 0
---

# Project State: Hardware III

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-05-03)

**Core value:** Working interactive prototype where projection guides closed-loop comparative assembly in real time, with LCA data — including methodology wobble — overlaid per phase.
**Current focus:** Phase 2 — Data Research & Physical Model Design (deadline May 4, 2026 — TOMORROW)

**Canonical state model:** `IDLE -> METHOD -> FOOTPRINT -> HEIGHT -> MATERIALS -> VALIDATED -> PHASE_N -> COMPARISON`
**State layering:** wrapper states and visual feedback states are tracked separately from the canonical content FSM.

## Current Phase

**Phase 2** — Data Research & Physical Model Design
**Status:** Pending — to be planned via `/gsd-plan-phase 2`
**Deadline:** May 4, 2026

## Progress

| Phase | Status | Deadline |
|-------|--------|----------|
| 1 — Proposal & FSM Foundation | ✅ Complete | April 17 (submitted) |
| 2 — Data Research & Physical Model Design | ○ Active — planning | May 4 |
| 3 — FSM Implementation & Assembly Logic (TouchDesigner) | ○ Pending | May 4 |
| 4 — Human-in-the-Loop Assembly & Sound | ○ Pending | May 11 |
| 5 — Projection Mapping & Comparison View | ○ Pending | May 18 |
| 6 — Integration, Testing & Finals | ○ Pending | May 22 |

## Immediate Next Action

Run `/gsd-plan-phase 2` to create a detailed plan for Phase 2 (data sourcing + physical model design + first closed-loop CV vertical slice).

## Locked decisions (2026-05-03)

Backed by `docs/research/lit-review/` (six per-strand reports + OVERVIEW.md + ACTIONS.md):

1. **Closed-loop CV from day one** — every FSM transition gated by camera confirmation. Manual hotkey override exists only as emergency demo insurance.
2. **TouchDesigner is the runtime** — replaces the originally-planned Anemone (FSM) and Firefly (vision).
3. **Reclaimed brick is a baseline toggle**, not a 4th competitor.
4. **Methodology-wobble is a first-class projection layer**, not a footnote.
5. **AI-generated phase animations paused** until tier-1 LCA numbers are sourced.

## Notes

- Phase 1 deliverables submitted April 17 (`Group_3_Hardware_III_Proposal.pdf` on master).
- Lit review by 6-agent academic research pipeline completed 2026-05-03 — see `docs/research/lit-review/OVERVIEW.md` for synthesis, `ACTIONS.md` for week-by-week priorities.
- Three reference corrections needed in slide deck before next presentation: "Swiss museum DJ table" → reacTable; "Brick Vault" → Augmented Bricklaying; "Discrete Wood" → Augmented Carpentry (EPFL IBOIS).
- Git remote: https://github.com/Leonardboeker/Hardware_III.git (default branch: master). Local branch `treethreetree` has 2 commits ahead, push blocked pending collaborator access for `elkhouryrafik-boop`.

---
*State updated: 2026-05-03 — Phase 1 closed, Phase 2 active, locked decisions integrated*

**Planned Phase:** 2 (Data Research & Physical Model Design) — 8 plans — 2026-05-03T21:57:31.713Z
