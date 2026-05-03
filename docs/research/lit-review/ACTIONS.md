# ACTIONS — Path Forward (derived from the lit review)

**Compiled:** 2026-05-03
**For:** IAAC Hardware III, Group 3
**Final demo:** 2026-05-22 (19 days from compile date)
**Source:** `OVERVIEW.md` and the six per-strand reports (`01`–`06`) in this folder

---

## Locked decisions

These four positions are taken. The rationale lives in the strand files cited next to each.

1. **Closed-loop computer vision from day one.** Every FSM transition is gated by camera confirmation against a projected target — no "press a button to advance" baseline. (See 01, 02, 06: object-aware feedback is the project's novelty contribution. See 03 for the brittleness warning.)
2. **Reclaimed brick is a baseline toggle, not a fourth competitor.** A bake-off where reused materials win is foregone-conclusion theater; the framing instead is "every other method is measured against this floor." (See 04 — De Wolf, Hoxha, Fivet 2020 line.)
3. **Methodology-wobble is a first-class projection layer, not a footnote.** A toggleable overlay that exposes how the LCA numbers swing by 2–4× depending on system boundary, lifespan, biogenic carbon, and grid mix is *the pedagogical contribution*. (See 04, 05, 06 — three strands converged unprompted on this.)
4. **AI-generated phase animations are paused** until the LCA numbers themselves are sourced and locked. Numbers without sources is the bigger demo risk. (See 06: tiered sourcing discipline.)

---

## What "closed-loop CV from the get-go" buys and costs

**Buys.** The genuine novelty. Strands 01, 02, and 06 each independently identified that closing the loop on what the human *actually placed* — vs what they were told to place — is where existing TUI tabletops, AR-assembly research, and LCA installations don't currently meet. The combination is the flag we plant.

**Costs.** The lit review was explicit (strand 03) — closed-loop fails when calibration drifts, lighting changes, or hands occlude markers. Augmented Bricklaying took multiple publications and years to get reliable. We have 19 days. Plan accordingly: calibration is now the highest-leverage engineering task.

---

## Week 1 (May 4 – May 10) — close the loop end-to-end on ONE puck

The goal at end of Week 1 is *not* a finished system. It is **a single puck whose placement triggers a single state transition through closed-loop CV**, in the actual hardware setup we'll demo on. If that doesn't work, scaling to 10 pucks won't either.

| # | Task | Owner | Backed by |
|---|---|---|---|
| 1 | **Camera-projector calibration rig.** Checkerboard for camera intrinsics + ArUco board for projector-to-camera homography. Document the procedure so any team member can re-calibrate in <30 min. | Vision | 03 |
| 2 | **One puck → one target → one transition.** Minimum closed-loop demo: ArUco puck on table, camera detects, position compared against projected target zone, projector confirms (green) or rejects (red, with ghost of correct position), TD state advances. | Vision + TD | 02, 03 |
| 3 | **Error-feedback visual language.** Decide *now* what wrong-placement looks like (color, ghost projection, audio feedback?). Augmented Bricklaying's pattern is the right reference. | TD + Curation | 02 |
| 4 | **LCA data — Catalonia tier-1 sources.** CYPE, BEDEC (ITeC), publicly available EPDs. Build `data/methods/*.csv` with a mandatory `source` column. Vendor claims (Apis Cor, ICON, TECLA) flagged. | Data | 06 |
| 5 | **3D-print 3 ArUco pucks** as test pieces (not the final 10). Lock physical dimensions and marker size based on Week 1 detection-distance tests. | CAD | 01 |
| 6 | **Tonight: fix the proposal slide references.** "reacTable" not "Swiss museum DJ table". Drop "Brick Vault" and "Discrete Wood" — replace with Augmented Bricklaying and EPFL IBOIS Augmented Carpentry. | Coordination | 01, 02, 04 |

**Week 1 exit criterion:** demo a 30-second video of one puck moving on a table, projection responding in real time with valid/invalid states. If we can't demo that on May 10, scope must shrink.

---

## Week 2 (May 11 – May 17) — scale the loop and add the pedagogical layer

| # | Task | Owner | Backed by |
|---|---|---|---|
| 7 | **Full FSM in TouchDesigner**, validity check on every transition, anchored conceptually on Parascho's assembly-as-state-machine framing. States: IDLE → METHOD → FOOTPRINT → HEIGHT → MATERIALS → VALIDATED → PHASE_DISPLAY ×5 → BUILDING_COMPLETE → COMPARISON. | TD | 03 |
| 8 | **All 10 footprint pucks + height marker + material controller.** This is the scaling step from Week 1's single puck. | Vision + Hardware | 01 |
| 9 | **RFID pedestal + ESP integration.** OSC over WiFi to TouchDesigner. Method-selection state. | Firmware | – |
| 10 | **Methodology-wobble layer built as first-class TD component.** Toggleable. Shows the assumption set behind each number, the swing range, and the source tier. | TD + Curation | 04, 05, 06 |
| 11 | **Real-world equivalents — paired**, never alone. Every "X trees" is shown alongside the absolute number AND the assumption that produces it (per Reijnierse 2025 strand 05). | TD + Curation | 05 |
| 12 | **Reclaimed-brick baseline overlay.** Comparable-method projections relative to the reclaimed floor. | Curation | 04 |

---

## Week 3 (May 18 – May 22) — harden, rehearse, demo

| # | Task | Owner | Backed by |
|---|---|---|---|
| 13 | **Demo-day robustness pass.** Re-calibrate in actual exhibition lighting. Stress-test hand occlusion. Failure-recovery on marker loss. | Vision + TD | 03 |
| 14 | **Manual override hotkey.** A keyboard shortcut that advances the FSM without CV — hidden, only used by the demoer if calibration drifts under stage lights. The runtime is closed-loop; this is emergency insurance. ~1 hour to build. | TD | – |
| 15 | **End-to-end rehearsal.** Run the demo three times back-to-back. Time it. Note every failure mode. | Whole team | – |
| 16 | **Final deck refresh.** Cite Parascho (DOI 10.3929/ethz-b-000364322), Mitterberger et al. 2020 (Augmented Bricklaying), Jordà et al. 2007 (reacTable), Garrido-Jurado et al. 2014 (ArUco), Pomponi et al. (LCA caveats). These five anchor the academic positioning. | Coordination | 01, 02, 03, 06 |
| 17 | **AI disclosure** in any submitted text — required by the lit review's own quality standard, and almost certainly by IAAC submission rules. | Coordination | OVERVIEW.md |

---

## The one safeguard: manual override

Closed-loop without a fallback is a real demo-day risk. The cheap insurance is task #14 above: a hidden manual state-advance hotkey that lets the demoer talk through the experience even if CV silently fails on stage. The runtime stays closed-loop. The override exists only for the human in front of the projector when something physical breaks.

This is **not** the open-loop baseline we explicitly rejected. It is a parallel emergency path that costs ~1 hour to build and saves the demo if calibration drifts under exhibition lighting.

---

## Things to stop spending time on

- ❌ Hunting for the "Swiss museum DJ table" — it doesn't exist as cited (strand 01).
- ❌ Anemone / Firefly in Grasshopper for FSM — strand 03 confirms TouchDesigner is the right runtime; don't split.
- ❌ A 4th-method bake-off with reclaimed brick — see locked decision #2.
- ❌ AI-generated phase animations until LCA numbers are sourced — see locked decision #4.
- ❌ Citing "Brick Vault" or "Discrete Wood" — unverifiable per strand 04.

---

## Open verification work (non-blocking, but tidy up before finals)

Aggregate of every "Sources requiring verification" item across the strands. None of these are load-bearing for the build, but they should be resolved before any academic submission.

- "Swiss museum DJ table" — confirm with whoever cited it which museum they actually visited
- "Brick Vault" (Gramazio Kohler) — likely a misattribution; identify the actual project
- "Discrete Wood" (EPFL CRCL) — likely Augmented Carpentry (IBOIS); confirm
- ETH Research Collection direct fetch for Parascho returned a 500 during research — re-verify the DOI lands at a live page before citing
- Coros as Parascho co-examiner — flagged unverified in strand 03

---

## How to use this document

- This is the canonical action doc. The OVERVIEW.md and per-strand files are the *evidence* — this is the *plan*.
- Update it as decisions change. Each row should have an owner; assign them in the next group meeting.
- When something deviates from this plan, update CONTRIBUTING.md's locked-decisions section *and* this file in the same commit.
