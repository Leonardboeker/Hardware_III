"""FSM for the Phase 2 one-puck closed-loop vertical slice.

States:
    WAITING_FOR_PUCK  — projecting target zone, waiting for ArUco puck to appear in zone
    PUCK_CONFIRMED    — puck placed correctly, TD advances to next step

Visual outputs (set on 'visual_state' channel, read by projection node):
    0 = DISCONNECTED   — no vision heartbeat / no puck detected for > TIMEOUT
    1 = PENDING        — puck detected but outside target zone
    2 = INVALID        — puck detected, outside zone, ghost projected
    3 = VALID          — puck inside zone, confirmed

HOW TO USE IN TD:
  - Paste into a Script CHOP or reference via 'Execute Script' on a Timer CHOP.
  - The FSM reads from parent().fetch('pucks') written by osc_handler.py.
  - Output channel 'fsm_state' (int 0-1) and 'visual_state' (int 0-3).
  - Wire 'visual_state' into your projection TOP logic (via Select CHOP).

ANTI-FLAP: puck must stay in-target for CONFIRM_HOLD_FRAMES consecutive frames
           before PUCK_CONFIRMED fires. Prevents single-frame glitches.
"""
from __future__ import annotations

# ── Constants ───────────────────────────────────────────────────────────────
TARGET_PUCK_ID = 0          # ArUco ID of the test puck (change per session)
CONFIRM_HOLD_FRAMES = 5     # frames puck must stay in-target to confirm
LOST_TIMEOUT_FRAMES = 30    # frames without detection before DISCONNECTED


# ── State indices ────────────────────────────────────────────────────────────
FSM_WAITING = 0
FSM_CONFIRMED = 1

VISUAL_DISCONNECTED = 0
VISUAL_PENDING = 1
VISUAL_INVALID = 2
VISUAL_VALID = 3


# ── State (persisted between cooks via TD storage) ───────────────────────────
def _get_state() -> dict:
    return parent().fetch('vsfsm', {
        'fsm': FSM_WAITING,
        'confirm_count': 0,
        'frames_since_seen': 0,
    })


def _set_state(s: dict):
    parent().store('vsfsm', s)


# ── Main cook function (called every TD frame) ───────────────────────────────
def cook(scriptOp):
    """Entry point: TD calls this every frame when a Script CHOP cooks."""
    state = _get_state()
    pucks = parent().fetch('pucks', {})
    vision_alive = parent().fetch('vision_alive', False)

    puck = pucks.get(TARGET_PUCK_ID)

    # ── DISCONNECTED check ───────────────────────────────────────────────────
    if not vision_alive or puck is None or puck.get('lost', False):
        state['frames_since_seen'] += 1
        if state['frames_since_seen'] >= LOST_TIMEOUT_FRAMES:
            state['confirm_count'] = 0
            _set_state(state)
            _output(scriptOp, state['fsm'], VISUAL_DISCONNECTED)
            return
    else:
        state['frames_since_seen'] = 0

    # ── FSM transitions ──────────────────────────────────────────────────────
    if state['fsm'] == FSM_WAITING:
        if puck and puck.get('in_target'):
            state['confirm_count'] += 1
            if state['confirm_count'] >= CONFIRM_HOLD_FRAMES:
                # Transition: WAITING → CONFIRMED
                state['fsm'] = FSM_CONFIRMED
                state['confirm_count'] = 0
                _set_state(state)
                _output(scriptOp, FSM_CONFIRMED, VISUAL_VALID)
                _on_confirmed()
                return
            else:
                # Building up confirmation — show VALID colour but don't advance yet
                _set_state(state)
                _output(scriptOp, FSM_WAITING, VISUAL_VALID)
        else:
            state['confirm_count'] = 0
            visual = VISUAL_PENDING if (puck and not puck.get('in_target')) else VISUAL_DISCONNECTED
            _set_state(state)
            _output(scriptOp, FSM_WAITING, visual)

    elif state['fsm'] == FSM_CONFIRMED:
        # Stays confirmed — projection system takes over from here
        _set_state(state)
        _output(scriptOp, FSM_CONFIRMED, VISUAL_VALID)


def _output(scriptOp, fsm_state: int, visual_state: int):
    """Write output channels."""
    scriptOp['fsm_state'][0] = fsm_state
    scriptOp['visual_state'][0] = visual_state


def _on_confirmed():
    """Hook: called exactly once when puck is confirmed in target zone.

    Extend this to trigger animations, sound, data overlay, etc.
    For Phase 3, the full FSM calls its own transition handler instead.
    """
    print("[FSM] PUCK_CONFIRMED — vertical slice complete")
    # Example: trigger a pulse on a Button COMP
    # op('pulse_trigger').click()
