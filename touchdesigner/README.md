# touchdesigner/

**Renderer only.** Receives `/state/*` OSC from the Python orchestrator,
composes the 9-panel UI + sketch overlay, drives the projector.

All FSM logic and metric computation moved to the Python orchestrator
(`/orchestrator/`) on 2026-05-28. TouchDesigner no longer owns state —
it reads `owner.fetch('ui_state', dict)` populated by the OSC bridge
and renders.

See [`orchestrator/TD-INTEGRATION.md`](../orchestrator/TD-INTEGRATION.md)
for the bridge wiring details.

## Current .toe

`td_verify_final2.21_ON.toe` (lives in main repo root, not this folder).

Key bridge nodes inside `/project1`:
- `state_in` — OSC In CHOP, port 7001, captures numeric `/state/*` channels
- `state_in_dat` — OSC In DAT, port 7001, captures string `/state/*` channels
- `state_to_storage` — chopexec, mirrors state_in channels into owner storage
- `state_in_dat_callbacks` — text DAT callback, merges string keys into owner.ui_state
- `sketch_render` — Script TOP, draws cyan walls + yellow pucks + meter labels
- `final_composite` — Over TOP, composites sketch_render over render_footprint
- `projector_out` — Window COMP (was `/project1/window1` — fixed via project.performWindowPath)

## Existing UI panels (Onur's work — used as-is)

Onur's 9-panel layout reads from `owner.fetch('ui_state', {})` via
`parent().fetch(me.name, "")` per Text TOP. The orchestrator pushes
panel-specific keys into storage so his rendering works unchanged.

| Panel | Text TOP | Content |
|-------|----------|---------|
| Top phase nav | `text_top_phase_navigation` | "PHASE 3/5" |
| Phase chips 1-5 | `text_top_phase_chip_<i>` | "1" "2" "[Roof]" ... |
| Left info | `text_left_info`, `_hero`, `_details`, `_scale` | Method, floor, puck count, status |
| Right cost chart | `text_right_cost_chart` | Phase-reactive cost breakdown |
| Right current state | `text_right_phase_preview_state` | Method + current phase |
| Right parts/floors | `text_right_phase_preview_left` | PARTS / FLOORS / AREA |
| Bottom status | `text_bar_bottom_status` | Full pipe-separated status line |

See [`PANEL-LAYOUT-GUIDE.md`](PANEL-LAYOUT-GUIDE.md) for Onur's original
panel positions + how to add new panels.

## Conventions

- Save `.toe` files in non-incremental mode (`Ctrl+S`) when possible —
  the auto-versioned `td_verify_final2.*` files are TD's automatic
  increment when MCP modifies the project, not manual saves.
- `.toe` is binary — don't merge in git. Use the Python orchestrator
  as the source of truth; TD changes need to be re-applied via MCP
  or manually if the .toe is overwritten.

## TouchDesigner MCP

The `mcp_webserver_base` component in `/project1` hosts a WebSocket
API on port 9981 used by Claude Code's `touchdesigner-mcp` server.
Lets the AI introspect + modify TD nodes directly without copy-paste
into the textport.

If port 9981 isn't bound: re-import `touchdesigner/touchdesigner-mcp-td/mcp_webserver_base.tox`
and ensure the `parameter1` Table DAT has `Port=9981, Active=1`.
