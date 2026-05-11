"""panel_text — text content generators for every UI panel.

How to use in TD:
    1. Add → DAT → Text  →  rename to `panel_text`
    2. Set its **File** param to:  touchdesigner/scripts/panel_text.py
    3. Set **Load on Start: On**, **Sync to File: On**
    4. In each text_<panel_id> Text TOP, click `=` on the Text param
       and use the matching function below, e.g.:
           op('panel_text').module.right_comparison()

Edit this file → reload the panel_text DAT → all panels update.

Reads from:
    op('methods_db')   Text DAT with methods_db.json content (required)
    op('compute_state') Script CHOP (optional — for live state)
"""
import json


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _db():
    """Parse methods_db.json from the methods_db Text DAT. Returns {} on failure."""
    try:
        return json.loads(op('methods_db').text)
    except Exception:
        return {}


def _state(channel, default=0):
    """Read a channel from compute_state CHOP. Returns default on failure."""
    try:
        return op('compute_state')[channel][0]
    except Exception:
        return default


def _method(method_id=None):
    """Return the methods_db entry for the current (or given) method_id."""
    db = _db()
    methods = db.get('methods', [])
    if method_id is None:
        method_id = int(_state('method_id', 0))
    method_id = max(0, min(method_id, len(methods) - 1))
    return methods[method_id] if methods else {}


# ---------------------------------------------------------------------------
# Panel: top phase navigation
# ---------------------------------------------------------------------------
def top_phase_navigation():
    """Current build phase. Phases are static — eventually driven by FSM."""
    db = _db()
    phases = db.get('phases', [])
    # Use compute_state.fsm_state if it exists, otherwise default to phase 1
    fsm_state = int(_state('fsm_state', 0))
    # Phase index lives in compute_state once the FSM module is wired up.
    # For now show "READY" if no phase context, else the phase name.
    if not phases:
        return 'READY'
    idx = max(0, min(int(_state('phase_index', 0)), len(phases) - 1))
    return f"PHASE {phases[idx]['id']}  ·  {phases[idx]['name']}"


# ---------------------------------------------------------------------------
# Panel: left info (selected method explainer)
# ---------------------------------------------------------------------------
def left_info():
    m = _method()
    if not m or m.get('id', 0) == 0:
        return 'METHOD\n\nPlace an RFID tag\non the reader to\nselect a method.'

    lines = [m['name'], '', m.get('description', '').strip()]
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Panel: method selection (just the method name — already wired in earlier)
# ---------------------------------------------------------------------------
def method_selection():
    m = _method()
    return m.get('name', 'NO METHOD')


# ---------------------------------------------------------------------------
# Panel: right comparison (all 3 methods side-by-side)
# ---------------------------------------------------------------------------
def right_comparison():
    db = _db()
    methods = db.get('methods', [])
    if not methods:
        return 'COMPARISON\n\n(no data)'

    competitive = [m for m in methods if m.get('id', 0) in (1, 2, 3)]
    if not competitive:
        return 'COMPARISON\n\n(no methods loaded)'

    lines = ['COMPARISON', '', 'CO2 per m² GFA:']
    for m in competitive:
        co2 = m.get('co2_per_m2_range') or '—'
        lines.append(f"  {m['name']}: {co2}")

    lines.extend(['', 'Labour h/m²:'])
    for m in competitive:
        lab = m.get('labor_hours_range') or '—'
        lines.append(f"  {m['name']}: {lab}")

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Panel: right cost chart (current method's cost data)
# ---------------------------------------------------------------------------
def right_cost_chart():
    m = _method()
    if not m or m.get('id', 0) == 0:
        return 'TOTAL COST\n\nSelect a method'

    cost = m.get('cost_per_m2_range') or '—'
    time = m.get('time_range') or '—'
    return f"COST · TIME\n\n{m['name']}\n\n{cost}\n{time}"


# ---------------------------------------------------------------------------
# Panel: right phase preview (per-phase checklist — static for now)
# ---------------------------------------------------------------------------
def right_phase_preview():
    return ('PHASE STEPS\n\n'
            '1. FOUNDATION\n'
            '2. STRUCTURE\n'
            '3. ROOF\n'
            '4. OPENINGS\n'
            '5. FINISHING')


# ---------------------------------------------------------------------------
# Panel: left assembly sequence (just placeholder for now)
# ---------------------------------------------------------------------------
def left_assembly_sequence():
    pucks = int(_state('puck_count', 0))
    return f"ASSEMBLY\n\nPucks placed: {pucks}\n\nDefine footprint,\nthen advance through\nphases."


# ---------------------------------------------------------------------------
# Panel: bottom status bar
# ---------------------------------------------------------------------------
def bar_bottom_status():
    alive = int(_state('hb_alive', 0))
    pucks = int(_state('puck_count', 0))
    area  = int(_state('area_px2', 0))
    m     = _method()
    method_name = m.get('name', 'NONE')

    status = 'LIVE' if alive else 'OFFLINE'
    return (f"VISION {status}   ·   "
            f"METHOD {method_name}   ·   "
            f"PUCKS {pucks}   ·   "
            f"AREA {area} px²")
