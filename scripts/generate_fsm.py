"""Generate FSM diagram as a clean PNG for the Interactive Assembly Installation."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(16, 10))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')
ax.set_xlim(-1, 17)
ax.set_ylim(-1, 11)
ax.set_aspect('equal')
ax.axis('off')

# Colors
STATE_COLOR = '#16213e'
BORDER_COLOR = '#e94560'
TEXT_COLOR = '#eaeaea'
ARROW_COLOR = '#0f3460'
LABEL_COLOR = '#e94560'
SUBTITLE_COLOR = '#a3a3c2'
CONFIRM_COLOR = '#2d6a4f'
ERROR_COLOR = '#9b2226'

# State definitions: (x, y, name, subtitle, color)
states = [
    (2, 9, 'IDLE', 'Ambient light pattern\n"Approach to begin"', STATE_COLOR),
    (8, 9, 'READY', 'Target outline projected\n"Place piece here"', STATE_COLOR),
    (14, 9, 'CHECKING', 'Validating position\n(≤ 0.3s blink)', STATE_COLOR),
    (14, 5, 'ERROR', 'Red outline + ghost\nof correct position', ERROR_COLOR),
    (8, 5, 'CONFIRMED', 'Green pulse + LCA data\nCO₂ · labor · origin map', CONFIRM_COLOR),
    (2, 2, 'COMPLETE', 'Side-by-side comparison\nof all 3 methods', STATE_COLOR),
]

# Draw states
box_w, box_h = 4.2, 2.0
for (x, y, name, subtitle, color) in states:
    rect = mpatches.FancyBboxPatch(
        (x - box_w/2, y - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.15",
        facecolor=color, edgecolor=BORDER_COLOR, linewidth=2.5
    )
    ax.add_patch(rect)
    ax.text(x, y + 0.35, name, ha='center', va='center',
            fontsize=16, fontweight='bold', color=TEXT_COLOR, family='monospace')
    ax.text(x, y - 0.45, subtitle, ha='center', va='center',
            fontsize=8.5, color=SUBTITLE_COLOR, family='sans-serif', linespacing=1.4)

# Arrow helper
def draw_arrow(x1, y1, x2, y2, label, label_offset=(0, 0.35), curved=False, color=ARROW_COLOR):
    style = "arc3,rad=0.2" if curved else "arc3,rad=0"
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=LABEL_COLOR, lw=2,
                                connectionstyle=style))
    mx = (x1 + x2) / 2 + label_offset[0]
    my = (y1 + y2) / 2 + label_offset[1]
    ax.text(mx, my, label, ha='center', va='center',
            fontsize=8, color=LABEL_COLOR, family='sans-serif',
            fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#1a1a2e', edgecolor='none', alpha=0.9))

# Transitions
# IDLE → READY
draw_arrow(4.1, 9, 5.9, 9, 'user detected\n(webcam)', label_offset=(0, 0.55))

# READY → CHECKING
draw_arrow(10.1, 9, 11.9, 9, 'piece placed\n(ArUco detected)', label_offset=(0, 0.55))

# CHECKING → ERROR
draw_arrow(14, 8.0, 14, 6.0, 'position\ninvalid', label_offset=(0.9, 0))

# ERROR → CHECKING
draw_arrow(12.5, 5.8, 12.5, 8.2, 'user corrects\nplacement', label_offset=(-1.0, 0), curved=False)

# CHECKING → CONFIRMED
draw_arrow(11.9, 8.3, 10.1, 5.7, 'position\nvalid', label_offset=(-0.5, 0.4))

# CONFIRMED → READY (next piece)
draw_arrow(8, 6.0, 8, 8.0, 'next piece\n→ new target', label_offset=(1.1, 0))

# CONFIRMED → COMPLETE (last piece)
draw_arrow(5.9, 5, 4.1, 3.0, 'last piece placed\nall methods done', label_offset=(-0.5, 0.5))

# COMPLETE → IDLE (timeout)
draw_arrow(2, 3.0, 2, 8.0, 'timeout 60s\nno presence', label_offset=(-1.3, 0))

# Title
ax.text(8, 10.5, 'FSM — Interactive Assembly Installation', ha='center', va='center',
        fontsize=20, fontweight='bold', color=TEXT_COLOR, family='sans-serif')
ax.text(8, -0.3, '5 states  ·  8 transitions  ·  Hand-draw this diagram on paper for Session 2',
        ha='center', va='center', fontsize=10, color=SUBTITLE_COLOR, family='sans-serif')

plt.tight_layout()
plt.savefig('FSM_diagram.png', dpi=200, bbox_inches='tight', facecolor='#1a1a2e')
print("Saved FSM_diagram.png")
