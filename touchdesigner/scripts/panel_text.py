"""panel_text — text content generators for every UI panel.

How to use in TD:
    1. Add → DAT → Text  →  rename to `panel_text`
    2. Set its **File** param to:  touchdesigner/scripts/panel_text.py
    3. Set **Load on Start: On**, **Sync to File: On**
    4. In each text_<panel_id> Text TOP, click `=` on the Text param
       and use the matching function below, e.g.:
           op('panel_text').module.right_comparison()

Edit this file → all panels update on next cook.

Reads from:
    op('methods_db')    Text DAT with methods_db.json content   (required)
    op('compute_state') Script CHOP — vision2_state_chop output (optional)
"""
import json


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _db():
    try:
        return json.loads(op('methods_db').text)
    except Exception:
        return {}


def _state(channel, default=0):
    try:
        return op('compute_state')[channel][0]
    except Exception:
        return default


def _method(method_id=None):
    db = _db()
    methods = db.get('methods', [])
    if method_id is None:
        method_id = int(_state('method_id', 0))
    method_id = max(0, min(method_id, len(methods) - 1))
    return methods[method_id] if methods else {}


def _midpoint(range_str):
    """Parse '205-490 kg…' → midpoint number, or None on failure."""
    if not range_str:
        return None
    s = range_str.split()[0].replace('–', '-')
    try:
        lo, hi = s.split('-')
        return (float(lo) + float(hi)) / 2.0
    except Exception:
        return None


def _short_range(range_str, drop_unit=True):
    """Take '205-490 kgCO2e/m2 GFA' → '205–490'."""
    if not range_str:
        return '—'
    return range_str.split()[0].replace('-', '–')


# ---------------------------------------------------------------------------
# Top phase navigation — horizontal bar with active phase highlighted
# ---------------------------------------------------------------------------
def top_phase_navigation():
    db = _db()
    phases = db.get('phases', [])
    if not phases:
        return 'READY'

    # fsm_state from vision2_state_chop: 5=PHASE_N. Use phase_index sub-channel
    # if it exists, else default to phase 1.
    phase_idx = int(_state('phase_index', 0))
    active = max(0, min(phase_idx, len(phases) - 1))

    parts = []
    for i, p in enumerate(phases):
        name = p['name']
        parts.append(f'[ {name} ]' if i == active else name)
    return '   ·   '.join(parts)


# ---------------------------------------------------------------------------
# Left info — selected method metrics block (LCA at a glance)
# ---------------------------------------------------------------------------
def left_info():
    m = _method()
    mid = m.get('id', 0)
    if mid == 0:
        return ('NO METHOD\n\n'
                'Place an RFID tag\n'
                'on the reader to\n'
                'select a construction\n'
                'method.')

    area_m2 = round(_state('area_m2', 0.0), 1)
    co2  = _short_range(m.get('co2_per_m2_range'))
    cost = _short_range(m.get('cost_per_m2_range'))
    labr = _short_range(m.get('labor_hours_range'))
    time = _short_range(m.get('time_range'))

    return (
        f"{m['name']}\n"
        f"\n"
        f"Footprint  {area_m2} m²\n"
        f"\n"
        f"CO₂\n{co2} kgCO₂e/m²\n"
        f"\n"
        f"Cost\n{cost} €/m²\n"
        f"\n"
        f"Labour\n{labr} h/m²\n"
        f"\n"
        f"Time\n{time}"
    )


# ---------------------------------------------------------------------------
# Method selection — short name (sits next to the color block)
# ---------------------------------------------------------------------------
def method_selection():
    m = _method()
    return m.get('name', 'NO METHOD')


# ---------------------------------------------------------------------------
# Right comparison — all 3 competitive methods side-by-side + baseline
# ---------------------------------------------------------------------------
def right_comparison():
    db = _db()
    methods = db.get('methods', [])
    if not methods:
        return 'COMPARISON\n\n(no data loaded)'

    def row(m):
        n   = m['name'][:12].ljust(12)
        co2 = _short_range(m.get('co2_per_m2_range')).ljust(11)
        cst = _short_range(m.get('cost_per_m2_range'))
        return f"{n} {co2} {cst}"

    lines = ['COMPARISON', '',
             '             CO₂/m²       €/m²',
             '─' * 32]
    for m in methods:
        if m.get('id', 0) in (1, 2, 3):
            lines.append(row(m))

    # Baseline (reclaimed) sits below the comparison line
    baseline = next((m for m in methods if m.get('id', 0) == 4), None)
    if baseline:
        lines.append('─' * 32)
        lines.append(row(baseline))
        lines.append('(reclaimed = baseline)')

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Right cost chart — total cost (midpoint of method's range) + breakdown
# ---------------------------------------------------------------------------
def right_cost_chart():
    m = _method()
    if m.get('id', 0) == 0:
        return 'TOTAL COST\n\nSelect a method'

    mid_cost = _midpoint(m.get('cost_per_m2_range'))
    area_m2  = _state('area_m2', 0.0)

    if mid_cost is None:
        cost_line = '—'
    elif area_m2 > 0:
        total = int(mid_cost * area_m2)
        cost_line = f"€ {total:,} total\n€ {int(mid_cost)} / m² · {area_m2:.1f} m²"
    else:
        cost_line = f"€ {int(mid_cost)} / m²"

    return (
        f"TOTAL COST\n\n"
        f"{m['name']}\n\n"
        f"{cost_line}\n\n"
        f"(material + labour + logistics)"
    )


# ---------------------------------------------------------------------------
# Right phase preview — checklist with active phase marker
# ---------------------------------------------------------------------------
def right_phase_preview():
    db = _db()
    phases = db.get('phases', [])
    if not phases:
        return 'PHASE STEPS\n\n(no phases loaded)'

    phase_idx = int(_state('phase_index', 0))
    active = max(0, min(phase_idx, len(phases) - 1))

    lines = ['PHASE CHECKLIST', '']
    for i, p in enumerate(phases):
        mark = '●' if i == active else '○'
        lines.append(f"{mark} {p['id']}. {p['name']}")
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Left assembly sequence — per-method 5-step build sequence
# ---------------------------------------------------------------------------
_ASSEMBLY = {
    1: ('MASONRY ASSEMBLY',
        '1  Foundation pour',
        '2  Brick coursing',
        '3  Lintels + openings',
        '4  Roof structure',
        '5  Finishing'),
    2: ('3D PRINT ASSEMBLY',
        '1  Foundation pour',
        '2  Print wall shell',
        '3  Cure + reinforce',
        '4  Roof structure',
        '5  Finishing'),
    3: ('PREFAB ASSEMBLY',
        '1  Foundation pour',
        '2  Factory fabrication',
        '3  Transport to site',
        '4  Crane + assembly',
        '5  Finishing'),
    4: ('RECLAIMED BRICK',
        '1  Salvage + clean',
        '2  Re-laying',
        '3  Openings',
        '4  Roof',
        '5  Finishing'),
}


def left_assembly_sequence():
    m = _method()
    seq = _ASSEMBLY.get(m.get('id', 0))
    if seq is None:
        return 'ASSEMBLY\n\nSelect a method\nto see the build\nsequence.'
    return '\n\n'.join([seq[0], '\n'.join(seq[1:])])


# ---------------------------------------------------------------------------
# Bottom status bar — live state line
# ---------------------------------------------------------------------------
def bar_bottom_status():
    alive = int(_state('hb_alive', 0))
    pucks = int(_state('puck_count', 0))
    area  = round(_state('area_m2', 0.0), 1)
    floor = int(_state('floor', 1))
    phase_index = int(_state('phase_index', 1))
    m     = _method()
    method_name = m.get('name', 'NONE')
    n_phases = int(m.get('n_phases', 5))

    status = 'LIVE' if alive else 'OFFLINE'
    return (f"VISION {status}   ·   "
            f"METHOD {method_name}   ·   "
            f"PUCKS {pucks}   ·   "
            f"AREA {area} m²   ·   "
            f"FLOOR {floor}   ·   "
            f"PHASE {phase_index}/{n_phases}")
