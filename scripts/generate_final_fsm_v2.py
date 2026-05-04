"""
FSM diagram — updated after professor meeting.
New states: METHOD_SELECTED, FOOTPRINT_DEFINED, HEIGHT_SET, MATERIALS_CHOSEN,
VALIDATED, PHASE_DISPLAY, BUILDING_COMPLETE, COMPARISON
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(1, 1, figsize=(22, 14))
fig.patch.set_facecolor('#FAFAF8')
ax.set_facecolor('#FAFAF8')
ax.set_xlim(-1, 23)
ax.set_ylim(-2, 15)
ax.set_aspect('equal')
ax.axis('off')

C_INK    = '#1A1A1A'
C_PENCIL = '#4A4A4A'
C_LIGHT  = '#9A9A9A'
C_PAPER  = '#FAFAF8'
C_RED    = '#CC3333'
C_BG     = '#F0EDE8'

def draw_state(x, y, name, subtitle, filled=False, error=False, w=4.0, h=2.0):
    ec = C_RED if error else C_INK
    fc = C_INK if filled else C_PAPER
    tc = C_PAPER if filled else C_INK
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.15",
        facecolor=fc, edgecolor=ec, linewidth=2
    )
    ax.add_patch(rect)
    # Shadow
    shadow = mpatches.FancyBboxPatch(
        (x - w/2 + 3/50, y - h/2 - 3/50), w, h,
        boxstyle="round,pad=0.15",
        facecolor='none', edgecolor=C_LIGHT, linewidth=1, linestyle='--'
    )
    ax.add_patch(shadow)

    ax.text(x, y + 0.3, name, ha='center', va='center',
            fontsize=12, fontweight='bold', color=tc, family='monospace')
    sc = C_RED if error else (C_LIGHT if filled else C_PENCIL)
    ax.text(x, y - 0.4, subtitle, ha='center', va='center',
            fontsize=8, color=sc, family='sans-serif', linespacing=1.3)

def arrow(x1, y1, x2, y2, label, offset=(0, 0.35), color=C_PENCIL):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.8))
    mx = (x1 + x2) / 2 + offset[0]
    my = (y1 + y2) / 2 + offset[1]
    ax.text(mx, my, label, ha='center', va='center',
            fontsize=7.5, color=color, family='sans-serif', fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=C_PAPER, edgecolor='none'))

# ─── STATES ───

# Row 1: Setup flow
draw_state(2,   12, 'IDLE',             'Waiting for user\nAmbient projection')
draw_state(7.5, 12, 'METHOD\nSELECTED', 'RFID pedestal\ntriggers method', h=2.2)
draw_state(13,  12, 'FOOTPRINT\nDEFINED', '10 ArUco pucks\ndefine floor plan', h=2.2)
draw_state(18.5,12, 'HEIGHT\nSET',       'Floor marker\nselects stories', h=2.2)

# Row 2: Validation + phases
draw_state(2,   8,  'MATERIALS\nCHOSEN', 'Material controller\nsets foundation + main', h=2.2)
draw_state(7.5, 8,  'VALIDATED',         'System confirms\nfeasibility', filled=True)
draw_state(13,  8,  'PHASE\nDISPLAY',    'Animation plays\ndata shown (×5)', h=2.2)
draw_state(18.5,8,  'ERROR',             'Not feasible\nadjust parameters', error=True)

# Row 3: Completion
draw_state(7.5, 4,  'BUILDING\nCOMPLETE', 'Final output\nsave dataset', h=2.2)
draw_state(13,  4,  'COMPARISON',         'Side-by-side\nmulti-build compare', filled=True)

# ─── TRANSITIONS ───

# IDLE → METHOD_SELECTED
arrow(4.0, 12, 5.5, 12, 'model placed\non RFID', offset=(0, 0.6))

# METHOD_SELECTED → FOOTPRINT_DEFINED
arrow(9.5, 12, 11.0, 12, 'pucks placed\non table', offset=(0, 0.6))

# FOOTPRINT_DEFINED → HEIGHT_SET
arrow(15.0, 12, 16.5, 12, 'area calculated\nheight marker', offset=(0, 0.6))

# HEIGHT_SET → MATERIALS_CHOSEN
arrow(18.5, 10.9, 2, 9.1, 'material marker\nplaced', offset=(0, 0.5))

# MATERIALS_CHOSEN → VALIDATED
arrow(4.0, 8, 5.5, 8, 'system checks\nfeasibility', offset=(0, 0.55))

# VALIDATED → PHASE_DISPLAY
arrow(9.5, 8, 11.0, 8, 'begin phase\nwalkthrough', offset=(0, 0.55))

# VALIDATED → ERROR (invalid)
arrow(9.0, 8.8, 17.0, 8.8, 'not possible', offset=(0, 0.5), color=C_RED)

# ERROR → MATERIALS_CHOSEN (adjust)
arrow(17.0, 7.2, 3.5, 7.2, 'user adjusts\nparameters', offset=(0, -0.55), color=C_RED)

# PHASE_DISPLAY → PHASE_DISPLAY (next phase, loop)
ax.annotate('', xy=(14.8, 9.1), xytext=(14.8, 7.0),
            arrowprops=dict(arrowstyle='->', color=C_PENCIL, lw=1.8,
                            connectionstyle='arc3,rad=-0.8'))
ax.text(15.8, 8, 'user accepts\nnext phase', ha='center', va='center',
        fontsize=7.5, color=C_PENCIL, family='sans-serif', fontstyle='italic',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=C_PAPER, edgecolor='none'))

# PHASE_DISPLAY → BUILDING_COMPLETE (last phase)
arrow(12.0, 6.9, 9.0, 5.1, 'all phases\ncomplete', offset=(-0.5, 0.4))

# BUILDING_COMPLETE → COMPARISON (save + compare)
arrow(9.5, 4, 11.0, 4, 'save dataset\ncompare builds', offset=(0, 0.55))

# BUILDING_COMPLETE → IDLE (build another)
arrow(7.5, 2.9, 2, 10.9, 'build another\nconfiguration', offset=(-1.5, 0))

# COMPARISON → IDLE
arrow(13, 2.9, 2, 10.9, 'timeout 60s\nor reset', offset=(0.5, 0), color=C_LIGHT)

# ─── TITLE ───
ax.text(11.5, 14.5, 'FSM — Guided Comparative Assembly Installation', ha='center', va='center',
        fontsize=22, fontweight='bold', color=C_INK, family='serif')
ax.text(11.5, 13.8, 'Updated after Session 2 discussion  |  Team: Leo · Elais · Rafik · Seid · Onur · Nithik',
        ha='center', va='center', fontsize=10, color=C_LIGHT, family='sans-serif')

# ─── LEGEND ───
legend_items = [
    ('Setup flow', C_PENCIL),
    ('Validation', C_INK),
    ('Error / correction', C_RED),
    ('Completion', C_LIGHT),
]
lx = 2
for label, color in legend_items:
    ax.plot([lx, lx + 0.6], [-1.2, -1.2], color=color, linewidth=3)
    ax.text(lx + 0.8, -1.2, label, ha='left', va='center',
            fontsize=9, color=color, family='sans-serif')
    lx += 5.5

ax.text(11.5, -1.8, '10 states  ·  User configures building → system validates → guided phases → compare',
        ha='center', va='center', fontsize=10, color=C_LIGHT, family='sans-serif')

plt.tight_layout()
plt.savefig('FSM_updated.png', dpi=200, bbox_inches='tight', facecolor=C_PAPER)
print("Saved FSM_updated.png")
