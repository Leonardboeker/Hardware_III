# Contributing — Guided Comparative Assembly

Six of us, one repo, ~3 weeks. Here's how we keep it from becoming chaos.

---

## Locked project decisions

These positions are taken. Backing rationale + lit-review citations live in `docs/research/lit-review/ACTIONS.md`. If you want to change one of these, propose it in a meeting and we update both files in the same commit — don't quietly drift.

1. **Closed-loop computer vision from day one.** Every FSM transition is gated by camera confirmation against a projected target. No "press a button to advance" baseline. A keyboard manual-override hotkey exists only as emergency demo-day insurance, not as a runtime mode.
2. **Reclaimed brick is a baseline toggle, not a fourth competitor.** Framing: "every method is measured against this reuse-based floor."
3. **Methodology-wobble is a first-class projection layer.** A toggleable overlay that shows how LCA numbers swing with system boundary, lifespan, biogenic carbon, and grid mix. This is the project's pedagogical contribution, not a footnote.
4. **AI-generated phase animations are paused** until tier-1 LCA numbers are sourced (Catalonia: CYPE / BEDEC / ITeC / EPDs).

Date locked: 2026-05-03.

---

## Folder ownership

Each top-level folder has one **primary** (final say, merges PRs touching it) and any number of contributors. Fill in your name when you claim a slot.

| Folder | Primary | Contributors |
|---|---|---|
| `firmware/` (ESP, RFID) | _TBD_ | |
| `touchdesigner/` | _TBD_ | |
| `vision/` (camera, ArUco, YOLO) | _TBD_ | |
| `rhino-gh/` | _TBD_ | |
| `cad/` (3D prints) | _TBD_ | |
| `data/` (LCA datasets) | _TBD_ | |
| `docs/` | shared | everyone |

**Rule:** never push directly to `master`. Always branch + PR. The folder primary reviews.

---

## Branching

- `master` is always working / demo-able.
- Branch off `master` for any change. Name pattern: `<initials>/<short-topic>` — e.g., `rk/aruco-tracking`, `lb/rfid-pedestal`.
- Merge via PR. At least one reviewer (the folder primary) approves before merge.
- Delete branches after merging.

---

## Commits

Short imperative subject + a sentence of context if non-obvious.

```
add ArUco corner-detection prototype

Tested on overhead webcam with 4 pucks. Gets ~30fps on Rafik's laptop.
Distance calc still naive — assumes flat plane.
```

Don't commit broken code to `main`. Feature branches can be messy; rebase/squash if you care.

---

## TouchDesigner files (.toe) — read this

`.toe` files are **binary** and **don't merge**. If two people edit the same `.toe` on different branches, one of you will lose work.

Rules:
1. Coordinate in the group chat before opening a `.toe` someone else is working on.
2. One `.toe` per subsystem when possible (e.g., `tracker.toe`, `projection.toe`) so people work on different files.
3. Backup files (`*.toe.1`, `*.toe.2`, ...) are gitignored — don't commit them.

---

## Large files

Keep individual files under ~50 MB. If you have huge media (raw video, dense point clouds), don't commit them — drop them in shared Drive/cloud and link from the relevant README.

---

## Issues / tasks

Use GitHub Issues. Label with the subsystem (`firmware`, `vision`, `td`, `data`, ...) and assign to one person. The Gantt in `deliverables/` is the higher-level plan; Issues are the day-to-day breakdown.
