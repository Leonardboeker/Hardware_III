"""
UPGRADED FSM diagram — more detailed, includes failure states,
method switching, and the bonus features (carbon clock, origin map).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(20, 13))
fig.patch.set_facecolor('#0f0f1a')
ax.set_facecolor('#0f0f1a')
ax.set_xlim(-1, 21)
ax.set_ylim(-2, 13)
ax.set_aspect('equal')
ax.axis('off')

# Colors
C_BG      = '#0f0f1a'
C_PANEL   = '#161627'
C_ACCENT  = '#ff3366'
C_ORANGE  = '#ff6b35'
C_CYAN    = '#00d4ff'
C_GREEN   = '#00cc88'
C_PURPLE  = '#8855ff'
C_YELLOW  = '#ffcc00'
C_RED     = '#cc2244'
C_TEXT    = '#f0f0f0'
C_DIM     = '#7a7a9e'

def draw_state(x, y, name, subtitle, color, w=4.5, h=2.2):
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.2",
        facecolor=color, edgecolor=C_ACCENT, linewidth=2
    )
    ax.add_patch(rect)
    ax.text(x, y + 0.35, name, ha='center', va='center',
            fontsize=16, fontweight='bold', color=C_TEXT, family='monospace')
    ax.text(x, y - 0.5, subtitle, ha='center', va='center',
            fontsize=8.5, color=C_DIM, family='sans-serif', linespacing=1.4)

def arrow(x1, y1, x2, y2, label, offset=(0, 0.4), color=C_ACCENT, curved=0):
    style = f"arc3,rad={curved}"
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.2,
                                connectionstyle=style))
    mx = (x1 + x2) / 2 + offset[0]
    my = (y1 + y2) / 2 + offset[1]
    ax.text(mx, my, label, ha='center', va='center',
            fontsize=8, color=color, family='sans-serif', fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.25', facecolor=C_BG, edgecolor='none', alpha=0.95))

# ─── STATES ───
draw_state(3,  11, 'IDLE',      'Ambient light pattern\n"Approach to begin"\nCarbon clock ticking', C_PANEL)
draw_state(10, 11, 'READY',     'Target outline projected\n"Place piece here"\nMethod indicator active', C_PANEL)
draw_state(17, 11, 'CHECKING',  'Validating position\n(\u2264 0.3s processing)', C_PANEL)

draw_state(17, 7,  'ERROR',     'Red outline + ghost\nof correct position\nFailure cost displayed', C_RED)
draw_state(10, 7,  'CONFIRMED', 'Green pulse\nLCA data ON the piece\nOrigin map projected', C_GREEN + '33', w=5, h=2.4)

draw_state(3,  4,  'METHOD\nCOMPLETE', 'Method stats summary\nTransition to next method\nor final comparison', C_PURPLE + '44', h=2.5)
draw_state(10, 1,  'COMPARE',   'Side-by-side dashboard\nAll 4 methods compared\nCO\u2082 \u00b7 hours \u00b7 cost \u00b7 origin', '#1a3050', w=5.5, h=2.2)
draw_state(17, 4,  'ANIMATE',   'Projected animation\nof non-built methods\nSame table, adjacent zone', C_ORANGE + '44')

# ─── TRANSITIONS ───
# IDLE → READY
arrow(5.25, 11, 7.75, 11, 'user detected\n(webcam presence)', offset=(0, 0.7))

# READY → CHECKING
arrow(12.25, 11, 14.75, 11, 'piece placed\n(ArUco detected)', offset=(0, 0.7))

# CHECKING → ERROR
arrow(17, 9.9, 17, 8.1, 'position\ninvalid', offset=(1.2, 0))

# ERROR → CHECKING (user corrects)
arrow(15.5, 8.0, 15.5, 10.0, 'user corrects\nplacement', offset=(-1.3, 0))

# CHECKING → CONFIRMED
arrow(14.75, 10.3, 12.5, 7.8, 'position\nvalid', offset=(-0.7, 0.5), color=C_GREEN)

# CONFIRMED → READY (next piece in same method)
arrow(10, 8.2, 10, 9.9, 'next piece\n\u2192 new target', offset=(1.4, 0), color=C_GREEN)

# CONFIRMED → METHOD COMPLETE (last piece of method)
arrow(7.5, 6.5, 5.25, 5.0, 'last piece\nof method', offset=(-0.5, 0.6), color=C_PURPLE)

# METHOD COMPLETE → READY (next method — physical build)
arrow(3, 5.25, 3, 9.9, 'next method\n(physical build)', offset=(-1.5, 0), color=C_ORANGE)

# METHOD COMPLETE → ANIMATE (next method — projected)
arrow(5.25, 3.7, 14.75, 4, 'next method\n(projected animation)', offset=(0, 0.7), color=C_ORANGE)

# ANIMATE → METHOD COMPLETE (animation done)
arrow(14.75, 3.3, 5.25, 3.0, 'animation\ncomplete', offset=(0, -0.6), color=C_YELLOW)

# METHOD COMPLETE → COMPARE (all methods done)
arrow(3, 2.75, 7.25, 1.2, 'all 4 methods\ncompleted', offset=(-0.3, 0.6), color=C_CYAN)

# COMPARE → IDLE (timeout)
arrow(10, 2.1, 3, 9.9, 'timeout 60s\nno presence', offset=(-1.5, 0), color=C_DIM)

# ─── TITLE ───
ax.text(10.5, 12.7, 'FSM \u2014 MATTER & METHOD', ha='center', va='center',
        fontsize=24, fontweight='bold', color=C_TEXT, family='sans-serif')

# ─── LEGEND ───
legend_items = [
    ('Physical build path', C_GREEN),
    ('Method transition', C_ORANGE),
    ('Error / correction', C_ACCENT),
    ('Comparison / timeout', C_CYAN),
]
lx = 1
for label, color in legend_items:
    ax.plot([lx, lx + 0.6], [-1.2, -1.2], color=color, linewidth=3)
    ax.text(lx + 0.8, -1.2, label, ha='left', va='center',
            fontsize=9, color=color, family='sans-serif')
    lx += 5

# Stats
ax.text(10.5, -1.8, '7 states  \u00b7  12 transitions  \u00b7  Handles method switching, failure costs, and projected animations',
        ha='center', va='center', fontsize=10, color=C_DIM, family='sans-serif')

plt.tight_layout()
plt.savefig('FSM_v2.png', dpi=200, bbox_inches='tight', facecolor=C_BG)
print("Saved FSM_v2.png")
