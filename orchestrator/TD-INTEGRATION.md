# TD-side integration (Day 2 work)

This document explains how to wire TouchDesigner to consume the orchestrator's `/state/*` OSC stream. Not yet executed in the live `.toe` — captured here so it's ready when you want to do Phase B.

## Goals

- Keep the existing `vision_in` (port 7000) network intact — vision pipeline still flows directly.
- Add a new path: **orchestrator → TD via UDP 7001** with `/state/<key>` messages.
- Onur's `panel_text.py` functions read from `owner.fetch('ui_state', dict)` — we feed that dict from the orchestrator.

## Step 1 — Add a `state_in` OSC In CHOP

In `/project1/`:
1. Right-click in network → `Add Operator` → `CHOP` → `OSC In`.
2. Name it `state_in`.
3. Parameters:
   - Active: **On**
   - Network Port: **7001**
   - OSC Address Scope: `/state/*`
   - Active = On

After the orchestrator is running you should see ~15 channels appearing on `state_in`, e.g. `state/method_id`, `state/floor`, `state/phase_index`, `state/wrapper_state`, `state/bar_bottom_text` (string), …

## Step 2 — Add a callbacks DAT that mirrors `/state/*` into owner storage

This is what makes Onur's `panel_text.py` work without modification — his functions read from `owner.fetch('ui_state', {})`, so we just publish the dict ourselves.

Create a `state_in_callbacks` Text DAT with this content (set `Module on Start = On`):

```python
"""state_in callbacks — mirror /state/<key> OSC messages into owner storage.

Wired as the 'Callbacks DAT' parameter on state_in OSC In CHOP.
"""

# Build the dict by reading every channel from state_in each cook.
# Then store it where Onur's panel_text.py / footprint_viz_v5.py expect it.

def onValueChange(channel, sampleIndex, val, prev):
    # Optional: react to specific channel changes. Not needed for our case.
    return

def onCook(scriptOp):
    # Not used — state_in is the CHOP, no Script CHOP cook here.
    return
```

…actually for OSC-In-CHOP the simpler path is a small **Execute DAT** that runs on every frame and copies channels into storage. Add an `Execute DAT` named `state_to_storage`:

```python
def onFrameStart(frame):
    state_chop = op('state_in')
    owner = op('/project1')
    if state_chop is None:
        return

    # Collect everything into a dict
    payload = {}
    for chan in state_chop.chans('*'):
        # OSC In CHOP names channels like 'state/method_id', 'state/floor', etc.
        key = chan.name
        if key.startswith('state/'):
            key = key[len('state/'):]
        payload[key] = chan[0]

    # Stash for Onur's panel_text / footprint_viz to pick up
    owner.store('ui_state', payload)
    owner.store('hb_alive', int(payload.get('hb_alive', 0)))
    owner.store('current_method', _method_key_from_id(int(payload.get('method_id', 0))))


_METHOD_KEYS = {
    0: None, 1: 'masonry', 2: '3d_printed', 3: 'prefab', 4: 'reclaimed_brick',
}

def _method_key_from_id(mid):
    return _METHOD_KEYS.get(mid)
```

Configure the Execute DAT:
- **Frame Start** parameter: **On**

## Step 3 — Verify

In TD textport:
```python
root = op('/project1')
print(root.fetch('ui_state', {}))
```

You should see a dict with ~15 keys: `method_id`, `floor`, `phase_index`, `puck_count`, `hb_alive`, `bar_bottom_text`, etc. Updated continuously by the orchestrator.

## Step 4 — Wire one text TOP to the new pipeline (test)

Right-click `text_bar_bottom_status` Text TOP → Customize Parameters → "Text" parameter. Set it as Python expression mode:
```python
op('/project1').fetch('ui_state', {}).get('bar_bottom_text', '')
```

The bottom bar will now display whatever the orchestrator computed — bypassing the old `panel_text.bar_bottom_status()` call. Same content, simpler chain.

## Step 5 — Migrate panel_text functions one by one

Once Step 4 works, switch the other `text_*` TOPs to read from `ui_state` directly. Onur's `panel_text.py` already does `_state(key, default)` which reads from compute_state — same idea but reading from owner storage:

```python
# Adapter: drop into a new helper or replace panel_text._state
def _state(channel, default=None):
    val = op('/project1').fetch('ui_state', {}).get(channel, None)
    return val if val is not None else default
```

If you replace `_state` in panel_text.py, every `panel_text.bar_bottom_status()` / `panel_text.left_info()` / etc. automatically reads from the orchestrator-fed dict. **No other changes needed** in TD — Onur's UI rendering chain is untouched.

## Step 6 — Disable the old metrics_engine + refresh_metrics_ui

These are no longer needed (orchestrator does their job). To stop the error spam:
1. Right-click `metrics_engine` Text DAT → `Bypass` (or set `Module on Start = Off`).
2. Same for `refresh_metrics_ui`.
3. In `vision2_state_chop.py`, comment out the `refresh.module.refresh(owner=owner)` call inside `_sync_owner_state`.

## Resulting architecture (after Day 2)

```
       Python orchestrator
              │
              ↓ OSC /state/*
       state_in (OSC In CHOP)
              │
              ↓ via Execute DAT every frame
       owner.fetch('ui_state', dict)
              │
              ↓
       panel_text.py functions
              │
              ↓
       text_* Text TOPs render
              │
              ↓
       render_footprint composes
              │
              ↓
       projector_out → Beamer
```

Compute_state Script CHOP is no longer doing logic — it can be deleted entirely, or kept as a debug viewer. Vision_in still receives raw vision packets in case TD wants to render them directly (footprint puck circles for example).
