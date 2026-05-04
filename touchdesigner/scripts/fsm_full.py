"""Full 8-state FSM for the Phase 3 TouchDesigner assembly logic.

State machine: IDLE → METHOD → FOOTPRINT → HEIGHT → MATERIALS → VALIDATED → PHASE_N → COMPARISON
Per ROADMAP.md Phase 3 success criteria and FSM_updated.png.

INTEGRATION POINTS:
  - Reads from parent().fetch('pucks') — written by osc_handler.py
  - Reads from parent().fetch('vision_alive') — written by osc_handler.py
  - Reads from parent().fetch('rfid_method') — written by firmware OSC handler
  - Writes 'fsm_state_name' (str) and 'visual_state' (int) for projection
  - Writes 'lca_trigger' (int, pulsed) to kick off data layer for each confirmed piece
  - Writes 'current_method' (str: 'masonry'|'3d_printed'|'prefab') for projection

STATES:
  IDLE          — installation waiting for first interaction (no pieces, idle animation)
  METHOD        — user places method-selector ArUco on RFID pedestal
  FOOTPRINT     — user places 10 footprint pucks in sequence
  HEIGHT        — user places height marker
  MATERIALS     — user places material controller ArUco
  VALIDATED     — all pieces confirmed for this model; show summary + data
  PHASE_N       — cycling through 5 sub-phases of the assembly (repeating loop)
  COMPARISON    — all 3 methods complete; full comparison view

PUCK ID CONVENTION (lock with cad/PUCK-SPEC.md):
  0–9    = footprint corners / edges (10 pucks per model)
  10     = height marker
  11     = material controller
  20–22  = method selectors (20=masonry, 21=3d_printed, 22=prefab)

VISUAL STATE CODES (read by projection/visual_state.py):
  0  DISCONNECTED    no vision
  1  PENDING         waiting for puck
  2  INVALID         wrong placement, ghost shown
  3  VALID           correct placement confirmed
  4  IDLE_ANIM       idle loop animation
  5  SUMMARY         validated — summary data on screen
  6  COMPARISON      comparison view

ANTI-FLAP: all transitions require CONFIRM_HOLD_FRAMES consecutive in-target frames.
MANUAL OVERRIDE: set parent().store('manual_advance', True) from a hotkey Script DAT.
"""
from __future__ import annotations

from enum import IntEnum, auto

# ── Config ───────────────────────────────────────────────────────────────────
CONFIRM_HOLD_FRAMES = 5
LOST_TIMEOUT_FRAMES = 30
NUM_FOOTPRINT_PUCKS = 10
FOOTPRINT_IDS = list(range(0, 10))   # ArUco IDs 0..9
HEIGHT_ID = 10
MATERIAL_ID = 11
METHOD_IDS = {20: 'masonry', 21: '3d_printed', 22: 'prefab'}
NUM_METHODS = 3     # masonry, 3d_printed, prefab (reclaimed is baseline toggle, not a full model)
NUM_PHASES = 5      # sub-phases per model

METHODS_ORDER = ['masonry', '3d_printed', 'prefab']


# ── State enum ───────────────────────────────────────────────────────────────
class State(IntEnum):
    IDLE = auto()
    METHOD = auto()
    FOOTPRINT = auto()
    HEIGHT = auto()
    MATERIALS = auto()
    VALIDATED = auto()
    PHASE_N = auto()
    COMPARISON = auto()


class Visual(IntEnum):
    DISCONNECTED = 0
    PENDING = 1
    INVALID = 2
    VALID = 3
    IDLE_ANIM = 4
    SUMMARY = 5
    COMPARISON = 6


# ── FSM storage helpers ───────────────────────────────────────────────────────
def _get_fsm() -> dict:
    return parent().fetch('fsm', {
        'state': State.IDLE,
        'method': None,             # current method string
        'methods_done': [],         # list of completed method strings
        'footprint_confirmed': [],  # list of confirmed puck IDs
        'height_confirmed': False,
        'material_confirmed': False,
        'current_phase': 0,         # 0..4 within PHASE_N
        'confirm_counts': {},       # {puck_id: int}
        'frames_since_seen': 0,
        'manual_advance': False,
    })


def _set_fsm(s: dict):
    parent().store('fsm', s)


# ── Main cook ─────────────────────────────────────────────────────────────────
def cook(scriptOp):
    """TD calls this every frame. Wire into a Script CHOP."""
    fsm = _get_fsm()
    pucks: dict = parent().fetch('pucks', {})
    vision_alive: bool = parent().fetch('vision_alive', False)
    manual_advance: bool = parent().fetch('manual_advance', False)

    if manual_advance:
        parent().store('manual_advance', False)
        _manual_advance(fsm, scriptOp)
        return

    # Vision dead check
    if not vision_alive:
        fsm['frames_since_seen'] += 1
        if fsm['frames_since_seen'] >= LOST_TIMEOUT_FRAMES:
            _output(scriptOp, fsm, Visual.DISCONNECTED)
            _set_fsm(fsm)
            return
    else:
        fsm['frames_since_seen'] = 0

    state = State(fsm['state'])

    if state == State.IDLE:
        _state_idle(fsm, pucks, scriptOp)
    elif state == State.METHOD:
        _state_method(fsm, pucks, scriptOp)
    elif state == State.FOOTPRINT:
        _state_footprint(fsm, pucks, scriptOp)
    elif state == State.HEIGHT:
        _state_height(fsm, pucks, scriptOp)
    elif state == State.MATERIALS:
        _state_materials(fsm, pucks, scriptOp)
    elif state == State.VALIDATED:
        _state_validated(fsm, pucks, scriptOp)
    elif state == State.PHASE_N:
        _state_phase_n(fsm, pucks, scriptOp)
    elif state == State.COMPARISON:
        _state_comparison(fsm, scriptOp)

    _set_fsm(fsm)


# ── State handlers ────────────────────────────────────────────────────────────

def _state_idle(fsm: dict, pucks: dict, scriptOp):
    """IDLE: show idle animation. Any method-selector puck starts the sequence."""
    _output(scriptOp, fsm, Visual.IDLE_ANIM)
    for mid, method_name in METHOD_IDS.items():
        p = pucks.get(mid)
        if p and not p.get('lost') and p.get('in_target'):
            if _increment_confirm(fsm, mid):
                _transition(fsm, State.METHOD, scriptOp)
                fsm['method'] = method_name
                return


def _state_method(fsm: dict, pucks: dict, scriptOp):
    """METHOD: method-selector puck must stay in RFID pedestal zone."""
    method_id = _method_id_for(fsm['method'])
    if method_id is None:
        _output(scriptOp, fsm, Visual.PENDING)
        return

    p = pucks.get(method_id)
    if p and not p.get('lost') and p.get('in_target'):
        if _increment_confirm(fsm, method_id):
            _transition(fsm, State.FOOTPRINT, scriptOp)
            _trigger_lca(scriptOp, fsm['method'], 'method_selected')
    else:
        _reset_confirm(fsm, method_id)
        _output(scriptOp, fsm, Visual.PENDING)


def _state_footprint(fsm: dict, pucks: dict, scriptOp):
    """FOOTPRINT: all 10 footprint pucks must be placed in order."""
    remaining = [pid for pid in FOOTPRINT_IDS if pid not in fsm['footprint_confirmed']]
    if not remaining:
        _transition(fsm, State.HEIGHT, scriptOp)
        return

    next_puck_id = remaining[0]
    p = pucks.get(next_puck_id)

    if p and not p.get('lost'):
        if p.get('in_target'):
            if _increment_confirm(fsm, next_puck_id):
                fsm['footprint_confirmed'].append(next_puck_id)
                _reset_confirm(fsm, next_puck_id)
                _trigger_lca(scriptOp, fsm['method'], f'footprint_{next_puck_id}')
                _output(scriptOp, fsm, Visual.VALID)
        else:
            _reset_confirm(fsm, next_puck_id)
            _output(scriptOp, fsm, Visual.INVALID)   # ghost shown by projection layer
    else:
        _output(scriptOp, fsm, Visual.PENDING)


def _state_height(fsm: dict, pucks: dict, scriptOp):
    """HEIGHT: height marker puck must be placed in correct zone."""
    p = pucks.get(HEIGHT_ID)
    if p and not p.get('lost') and p.get('in_target'):
        if _increment_confirm(fsm, HEIGHT_ID):
            fsm['height_confirmed'] = True
            _trigger_lca(scriptOp, fsm['method'], 'height_placed')
            _transition(fsm, State.MATERIALS, scriptOp)
    else:
        _reset_confirm(fsm, HEIGHT_ID)
        visual = Visual.INVALID if (p and not p.get('in_target')) else Visual.PENDING
        _output(scriptOp, fsm, visual)


def _state_materials(fsm: dict, pucks: dict, scriptOp):
    """MATERIALS: material controller ArUco placed."""
    p = pucks.get(MATERIAL_ID)
    if p and not p.get('lost') and p.get('in_target'):
        if _increment_confirm(fsm, MATERIAL_ID):
            fsm['material_confirmed'] = True
            _trigger_lca(scriptOp, fsm['method'], 'materials_placed')
            _transition(fsm, State.VALIDATED, scriptOp)
    else:
        _reset_confirm(fsm, MATERIAL_ID)
        visual = Visual.INVALID if (p and not p.get('in_target')) else Visual.PENDING
        _output(scriptOp, fsm, visual)


def _state_validated(fsm: dict, pucks: dict, scriptOp):
    """VALIDATED: all pieces for this model confirmed. Show summary, then start PHASE_N."""
    _output(scriptOp, fsm, Visual.SUMMARY)
    # After summary dwell time (controlled by a Timer CHOP), projection triggers PHASE_N
    # via parent().store('advance_to_phase_n', True). Check that flag here.
    if parent().fetch('advance_to_phase_n', False):
        parent().store('advance_to_phase_n', False)
        fsm['current_phase'] = 0
        _transition(fsm, State.PHASE_N, scriptOp)


def _state_phase_n(fsm: dict, pucks: dict, scriptOp):
    """PHASE_N: cycle through 5 assembly phases for the current model.

    Each phase is triggered externally (Timer CHOP or user interaction).
    After phase 4, record the method as done.
    If all methods done → COMPARISON, else → METHOD for the next one.
    """
    _output(scriptOp, fsm, Visual.VALID)
    if parent().fetch('advance_phase', False):
        parent().store('advance_phase', False)
        fsm['current_phase'] += 1
        if fsm['current_phase'] >= NUM_PHASES:
            fsm['methods_done'].append(fsm['method'])
            _reset_model_state(fsm)
            if len(fsm['methods_done']) >= NUM_METHODS:
                _transition(fsm, State.COMPARISON, scriptOp)
            else:
                fsm['method'] = None
                _transition(fsm, State.METHOD, scriptOp)


def _state_comparison(fsm: dict, scriptOp):
    """COMPARISON: all models done, show comparison view."""
    _output(scriptOp, fsm, Visual.COMPARISON)
    # Reset for next visitor via parent().store('reset_fsm', True)
    if parent().fetch('reset_fsm', False):
        parent().store('reset_fsm', False)
        _hard_reset(fsm, scriptOp)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _increment_confirm(fsm: dict, pid: int) -> bool:
    """Increment confirm counter for puck. Returns True when threshold reached (once)."""
    counts = fsm.setdefault('confirm_counts', {})
    counts[pid] = counts.get(pid, 0) + 1
    if counts[pid] == CONFIRM_HOLD_FRAMES:
        return True
    return False


def _reset_confirm(fsm: dict, pid: int):
    fsm.setdefault('confirm_counts', {})[pid] = 0


def _method_id_for(method_name: str | None) -> int | None:
    if method_name is None:
        return None
    for mid, name in METHOD_IDS.items():
        if name == method_name:
            return mid
    return None


def _transition(fsm: dict, new_state: State, scriptOp):
    print(f"[FSM] {State(fsm['state']).name} → {new_state.name}")
    fsm['state'] = int(new_state)
    fsm['confirm_counts'] = {}


def _trigger_lca(scriptOp, method: str, event: str):
    """Pulse lca_trigger channel so the data layer knows to update."""
    parent().store('lca_event', {'method': method, 'event': event})
    scriptOp['lca_trigger'][0] = 1  # projection layer resets this after reading


def _reset_model_state(fsm: dict):
    fsm['footprint_confirmed'] = []
    fsm['height_confirmed'] = False
    fsm['material_confirmed'] = False
    fsm['current_phase'] = 0
    fsm['confirm_counts'] = {}


def _hard_reset(fsm: dict, scriptOp):
    """Full reset for next visitor."""
    fsm.update({
        'state': State.IDLE,
        'method': None,
        'methods_done': [],
        'footprint_confirmed': [],
        'height_confirmed': False,
        'material_confirmed': False,
        'current_phase': 0,
        'confirm_counts': {},
        'frames_since_seen': 0,
    })
    _output(scriptOp, fsm, Visual.IDLE_ANIM)


def _manual_advance(fsm: dict, scriptOp):
    """Emergency manual override — advances FSM by one step without CV confirmation.

    Hidden hotkey for demo day insurance. Runtime stays closed-loop normally.
    Only used if CV fails silently on stage.
    """
    state = State(fsm['state'])
    print(f"[FSM] MANUAL OVERRIDE in state {state.name}")
    next_map = {
        State.IDLE: State.METHOD,
        State.METHOD: State.FOOTPRINT,
        State.FOOTPRINT: State.HEIGHT,
        State.HEIGHT: State.MATERIALS,
        State.MATERIALS: State.VALIDATED,
        State.VALIDATED: State.PHASE_N,
        State.PHASE_N: State.COMPARISON,
        State.COMPARISON: State.IDLE,
    }
    new_state = next_map.get(state, State.IDLE)
    _transition(fsm, new_state, scriptOp)
    _set_fsm(fsm)


def _output(scriptOp, fsm: dict, visual: Visual):
    """Write output channels to Script CHOP."""
    scriptOp['fsm_state'][0] = int(fsm['state'])
    scriptOp['visual_state'][0] = int(visual)
    scriptOp['current_phase'][0] = fsm.get('current_phase', 0)
    scriptOp['methods_done_count'][0] = len(fsm.get('methods_done', []))
    scriptOp['footprint_count'][0] = len(fsm.get('footprint_confirmed', []))
    # Write method string to a Text DAT for projection to read
    parent().store('fsm_state_name', State(fsm['state']).name)
    parent().store('current_method', fsm.get('method') or '')
