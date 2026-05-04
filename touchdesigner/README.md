# touchdesigner/

Primary runtime. Receives ArUco tracking from `vision/`, RFID events over OSC from `firmware/`, drives the projector output, runs the FSM.

## Files (suggested split)

One `.toe` per major subsystem so two people can work in parallel without colliding:

```
tracker.toe       # ArUco intake + footprint + height detection
fsm.toe           # state machine + validation
projection.toe    # top-down projection + phase animations
ui.toe            # any on-screen / side-display GUI
main.toe          # composes the above as TOX components
```

## Read this before opening a .toe

`.toe` files are **binary** — they don't merge. Coordinate in the group chat before opening one someone else is editing.

Backup files (`*.toe.1`, `*.toe.2`, ...) are gitignored intentionally. If you need to roll back, `git log` is the source of truth.

## External dependencies

- TouchDesigner build version: _TBD — pin the version everyone installs once decided_
- YOLO plugin: install per the plugin's docs, link them here once installed
- OSC In CHOP for ESP comms

## Conventions

- Save `.toe` files in the **non-incremental** save mode (Ctrl+S, not Ctrl+Shift+S) so we don't pile backups into the repo.
- TOX components for reusable pieces — drop them in a `tox/` subfolder.
