# Contributing — Guided Comparative Assembly

Six of us, one repo, ~3 weeks. Here's how we keep it from becoming chaos.

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

**Rule:** never push directly to `main`. Always branch + PR. The folder primary reviews.

---

## Branching

- `main` is always working / demo-able.
- Branch off `main` for any change. Name pattern: `<initials>/<short-topic>` — e.g., `rk/aruco-tracking`, `lb/rfid-pedestal`.
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
