"""
FINAL FSM diagram — matches the actual repo FSM states exactly.
IDLE → GUIDING → CHECKING → CONFIRMED → NEXT_PIECE
                      ↓ ERROR
CONFIRMED (last piece) → MODEL_COMPLETE → NEXT_MODEL → GUIDING
NEXT_MODEL (last model) → COMPARISON → IDLE
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(1, 1, figsize=(20, 12))
fig.patch.set_facecolor('#0f0f1a')
ax.set_facecolor('#0f0f1a')
ax.set_xlim(-1, 21)
ax.set_ylim(-2, 13)
ax.set_aspect('equal')
ax.axis('off')

C_BG     = '#0f0f1a'
C_PANEL  = '#161627'
C_ACCENT = '#ff3366'
C_ORANGE = '#ff6b35'
C_CYAN   = '#00d4ff'
C_GREEN  = '#00cc88'
C_PURPLE = '#8855ff'
C_YELLOW = '#ffcc00'
C_RED    = '#cc2244'
C_TEXT   = '#f0f0f0'
C_DIM    = '#7a7a9e'

def draw_state(x, y, name, subtitle, color, w=4.2, h=2.2):
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.2",
        facecolor=color, edgecolor=C_ACCENT, linewidth=2
    )
    ax.add_patch(rect)
    ax.text(x, y + 0.35, name, ha='center', va='center',
            fontsize=14, fontweight='bold', color=C_TEXT, family='monospace')
    ax.text(x, y - 0.45, subtitle, ha='center', va='center',
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

# ─── TOP ROW: Main assembly loop ───
draw_state(2,   10, 'IDLE',      'Waiting for user\nAmbient projection', C_PANEL)
draw_state(7.5, 10, 'GUIDING',   'Projector highlights\nnext piece target', C_PANEL)
draw_state(13,  10, 'CHECKING',  'Camera validates\nplacement', C_PANEL)
draw_state(18.5,10, 'CONFIRMED', 'Data projected\nonto the piece', C_GREEN + '44')

# ─── MIDDLE: Error + Next Piece ───
draw_state(13,  6,  'ERROR',     'Wrong placement\nGhost guide shown', C_RED)
draw_state(18.5,6,  'NEXT_PIECE','Advance to\nnext piece', C_CYAN + '33')

# ─── BOTTOM ROW: Model transitions ───
draw_state(13,  2,  'MODEL\nCOMPLETE', 'Method stats\nsummary shown', C_YELLOW + '33', h=2.4)
draw_state(7.5, 2,  'NEXT_MODEL','Switch construction\nmethod', C_ORANGE + '33')
draw_state(2,   2,  'COMPARISON','Final side-by-side\nall methods compared', C_CYAN + '22')

# ─── TRANSITIONS ───

# IDLE → GUIDING
arrow(4.1, 10, 5.4, 10, 'user detected', offset=(0, 0.65), color=C_DIM)

# GUIDING → CHECKING
arrow(9.6, 10, 10.9, 10, 'piece placed', offset=(0, 0.65), color=C_ORANGE)

# CHECKING → CONFIRMED
arrow(15.1, 10, 16.4, 10, 'position valid', offset=(0, 0.65), color=C_GREEN)

# CHECKING → ERROR
arrow(13, 8.9, 13, 7.1, 'position\ninvalid', offset=(1.1, 0), color=C_RED)

# ERROR → GUIDING (user corrects)
arrow(11.0, 6.5, 9.0, 9.0, 'user corrects\nplacement', offset=(-1.0, 0.3), color=C_ORANGE)

# CONFIRMED → NEXT_PIECE
arrow(18.5, 8.9, 18.5, 7.1, 'more pieces\nremaining', offset=(1.3, 0), color=C_CYAN)

# NEXT_PIECE → GUIDING (loop back for next piece)
arrow(16.4, 6, 9.5, 9.0, 'next piece\ntarget shown', offset=(0, 0.7), color=C_CYAN)

# CONFIRMED (last piece) → MODEL_COMPLETE
arrow(17.0, 9.0, 15.0, 3.2, 'last piece\nof model', offset=(0.8, 0.3), color=C_YELLOW)

# MODEL_COMPLETE → NEXT_MODEL
arrow(10.9, 2, 9.6, 2, 'more models\nremaining', offset=(0, 0.65), color=C_ORANGE)

# NEXT_MODEL → GUIDING (back to top for new method)
arrow(7.5, 3.1, 7.5, 8.9, 'start new\nconstruction method', offset=(1.6, 0), color=C_ORANGE)

# MODEL_COMPLETE (last model) → COMPARISON
arrow(10.9, 2.5, 4.1, 2.5, 'all models\ncompleted', offset=(0, 0.65), color=C_CYAN)

# COMPARISON → IDLE
arrow(2, 3.1, 2, 8.9, 'timeout 60s\nor user leaves', offset=(-1.5, 0), color=C_DIM)

# ─── TITLE ───
ax.text(10.5, 12.5, 'FSM \u2014 Guided Comparative Assembly Installation', ha='center', va='center',
        fontsize=22, fontweight='bold', color=C_TEXT, family='sans-serif')
ax.text(10.5, 12.0, 'Team: Leo \u2022 Elais \u2022 Rafik \u2022 Seid \u2022 Onur \u2022 Nithik', ha='center', va='center',
        fontsize=10, color=C_DIM, family='sans-serif')

# ─── LEGEND ───
legend_items = [
    ('Assembly loop', C_CYAN),
    ('Method transition', C_ORANGE),
    ('Error / correction', C_RED),
    ('Validation', C_GREEN),
    ('Completion', C_YELLOW),
]
lx = 1
for label, color in legend_items:
    ax.plot([lx, lx + 0.6], [-1.2, -1.2], color=color, linewidth=3)
    ax.text(lx + 0.8, -1.2, label, ha='left', va='center',
            fontsize=9, color=color, family='sans-serif')
    lx += 4

ax.text(10.5, -1.8, '9 states  \u00b7  12 transitions  \u00b7  Ref: Parascho (ETH) \u2014 assembly sequence as FSM',
        ha='center', va='center', fontsize=10, color=C_DIM, family='sans-serif')

plt.tight_layout()
plt.savefig('FSM_final.png', dpi=200, bbox_inches='tight', facecolor=C_BG)
print("Saved FSM_final.png")
