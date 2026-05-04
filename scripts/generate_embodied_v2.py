"""
UPGRADED embodied interaction sketch — richer, more analytical,
connects to course concepts (affordance, 3-second rule, spatial UX).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(20, 8))
fig.patch.set_facecolor('#0f0f1a')

C_BG     = '#0f0f1a'
C_PANEL  = '#161627'
C_ACCENT = '#ff3366'
C_ORANGE = '#ff6b35'
C_CYAN   = '#00d4ff'
C_GREEN  = '#00cc88'
C_PURPLE = '#8855ff'
C_TEXT   = '#f0f0f0'
C_DIM    = '#7a7a9e'
C_YELLOW = '#ffcc00'

# Title
fig.text(0.5, 0.97, 'Embodied Interactions \u2014 Three Non-Screen Examples', ha='center', va='top',
         fontsize=22, fontweight='bold', color=C_TEXT, family='sans-serif')
fig.text(0.5, 0.93, 'Where the body knows what to do without thinking. No label, no tutorial, no screen.',
         ha='center', va='top', fontsize=11, color=C_DIM, family='sans-serif', fontstyle='italic')

examples = [
    {
        'title': 'THE DOOR HANDLE',
        'color': C_ORANGE,
        'concept': 'AFFORDANCE',
        'desc': [
            'Flat plate = push.',
            'Curved grip = pull.',
            '',
            'The form IS the instruction.',
            'Shape communicates action',
            'before thought begins.',
        ],
        'insight': '3-second rule:\nunderstood instantly',
        'course_link': 'Same principle: projected\noutline tells you WHERE\nto place without words.',
    },
    {
        'title': 'THE STAIRCASE',
        'color': C_CYAN,
        'concept': 'SPATIAL MAPPING',
        'desc': [
            'Step height = 17cm.',
            'Your body calibrates after',
            'the first step.',
            '',
            'One wrong height and',
            'you stumble \u2014 the body',
            'expected the pattern.',
        ],
        'insight': 'Feedback is physical:\nstumble = error state',
        'course_link': 'Same principle: each brick\nhas an expected position.\nDeviation = ERROR state.',
    },
    {
        'title': 'THE FAUCET',
        'color': C_GREEN,
        'concept': 'LINEAR MAPPING',
        'desc': [
            'Turn right = more flow.',
            'Turn left = less flow.',
            '',
            'Continuous input maps to',
            'continuous output.',
            'Proportional, immediate,',
            'reversible.',
        ],
        'insight': 'Mapping type: LINEAR\n(equal input = equal output)',
        'course_link': 'Same principle: our system\nuses STEPPED mapping \u2014\neach piece = discrete state.',
    },
]

for idx, (ax, ex) in enumerate(zip(axes, examples)):
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.set_aspect('equal')
    ax.axis('off')

    # Main panel
    rect = mpatches.FancyBboxPatch(
        (0.3, 0.3), 9.4, 13.4,
        boxstyle="round,pad=0.2", facecolor=C_PANEL, edgecolor=ex['color'], linewidth=2
    )
    ax.add_patch(rect)

    # Number
    ax.text(1, 12.8, f'0{idx+1}', ha='left', va='center',
            fontsize=36, fontweight='bold', color=ex['color'], alpha=0.3, family='monospace')

    # Title
    ax.text(5, 12.5, ex['title'], ha='center', va='center',
            fontsize=15, fontweight='bold', color=C_TEXT, family='monospace')

    # Concept tag
    tag_w = len(ex['concept']) * 0.35 + 0.8
    tag_rect = mpatches.FancyBboxPatch(
        (5 - tag_w/2, 11.5), tag_w, 0.7,
        boxstyle="round,pad=0.1", facecolor=ex['color'], edgecolor='none'
    )
    ax.add_patch(tag_rect)
    ax.text(5, 11.85, ex['concept'], ha='center', va='center',
            fontsize=8, fontweight='bold', color=C_BG, family='monospace')

    # Illustration area
    illust_rect = mpatches.FancyBboxPatch(
        (1, 7.5), 8, 3.5,
        boxstyle="round,pad=0.1", facecolor='#0a0a14', edgecolor=ex['color'], linewidth=1, alpha=0.5
    )
    ax.add_patch(illust_rect)

    # Draw simplified illustrations
    if idx == 0:  # Door handle
        # Push door (left)
        door1 = mpatches.FancyBboxPatch((1.5, 8), 2.5, 2.5, boxstyle="round,pad=0.05",
                                         facecolor=C_PANEL, edgecolor=C_DIM, linewidth=1)
        ax.add_patch(door1)
        # Flat plate
        plate = mpatches.FancyBboxPatch((3.3, 8.8), 0.4, 1, boxstyle="round,pad=0.05",
                                         facecolor=ex['color'], edgecolor=C_TEXT, linewidth=1)
        ax.add_patch(plate)
        ax.text(2.75, 10.7, 'PUSH', ha='center', va='center', fontsize=9, fontweight='bold',
                color=ex['color'], family='monospace')
        ax.annotate('', xy=(3.5, 9.3), xytext=(4.8, 9.3),
                    arrowprops=dict(arrowstyle='->', color=ex['color'], lw=2.5))

        # Pull door (right)
        door2 = mpatches.FancyBboxPatch((5.5, 8), 2.5, 2.5, boxstyle="round,pad=0.05",
                                         facecolor=C_PANEL, edgecolor=C_DIM, linewidth=1)
        ax.add_patch(door2)
        # Curved handle
        theta = np.linspace(-np.pi/2, np.pi/2, 50)
        hx = 6.0 + 0.12 * np.cos(theta)
        hy = 9.25 + 0.5 * np.sin(theta)
        ax.plot(hx, hy, color=C_TEXT, linewidth=3, solid_capstyle='round')
        ax.text(6.75, 10.7, 'PULL', ha='center', va='center', fontsize=9, fontweight='bold',
                color=C_CYAN, family='monospace')
        ax.annotate('', xy=(5.3, 9.3), xytext=(5.8, 9.3),
                    arrowprops=dict(arrowstyle='->', color=C_CYAN, lw=2.5))

    elif idx == 1:  # Staircase
        # Steps
        for s in range(5):
            step = mpatches.FancyBboxPatch(
                (2 + s * 1.1, 8.0 + s * 0.45), 1.3, 0.4,
                boxstyle="round,pad=0.02", facecolor=C_PANEL, edgecolor=ex['color'], linewidth=1
            )
            ax.add_patch(step)
        # Height annotation
        ax.annotate('', xy=(1.8, 8.0), xytext=(1.8, 8.45),
                    arrowprops=dict(arrowstyle='<->', color=C_YELLOW, lw=1.5))
        ax.text(1.3, 8.22, '17cm', ha='center', va='center', fontsize=7, color=C_YELLOW, family='monospace')
        # Wrong step highlighted
        wrong = mpatches.FancyBboxPatch(
            (2 + 3 * 1.1, 8.0 + 3 * 0.45 + 0.15), 1.3, 0.4,
            boxstyle="round,pad=0.02", facecolor=C_ACCENT, edgecolor=C_TEXT, linewidth=1, alpha=0.7
        )
        ax.add_patch(wrong)
        ax.text(2 + 3 * 1.1 + 0.65, 8.0 + 3 * 0.45 + 0.7, 'WRONG\nHEIGHT', ha='center', va='center',
                fontsize=6, color=C_ACCENT, family='monospace', fontweight='bold')

    else:  # Faucet
        # Faucet body
        ax.plot([5, 5], [8.3, 9.5], color=C_DIM, linewidth=4, solid_capstyle='round')
        ax.plot([5, 6.5], [9.5, 9.5], color=C_DIM, linewidth=4, solid_capstyle='round')
        ax.plot([6.5, 6.5], [9.5, 9.0], color=C_DIM, linewidth=3, solid_capstyle='round')
        # Handle
        ax.plot([4, 6], [8.3, 8.3], color=ex['color'], linewidth=3, solid_capstyle='round')
        # Rotation arrow
        theta_arc = np.linspace(-0.5, 1.5, 30)
        arc_x = 5 + 1.5 * np.cos(theta_arc)
        arc_y = 8.3 + 0.8 * np.sin(theta_arc)
        ax.plot(arc_x, arc_y, color=C_YELLOW, linewidth=1.5, linestyle='--', alpha=0.6)
        ax.text(3.2, 9.0, 'MORE', ha='center', fontsize=7, color=C_GREEN, family='monospace')
        ax.text(6.8, 9.0, 'LESS', ha='center', fontsize=7, color=C_ACCENT, family='monospace')
        # Water drops
        for dy in [0, 0.35, 0.7]:
            ax.plot(6.5, 8.7 - dy, 'v', color=C_CYAN, markersize=4, alpha=0.7 - dy * 0.3)

    # Description
    y_pos = 7.0
    for line in ex['desc']:
        ax.text(1.2, y_pos, line, ha='left', va='center',
                fontsize=9.5, color=C_TEXT if line else C_DIM, family='sans-serif')
        y_pos -= 0.55

    # Insight box
    insight_rect = mpatches.FancyBboxPatch(
        (1, 2.8), 8, 1.3,
        boxstyle="round,pad=0.1", facecolor='#1a0f2e', edgecolor=C_PURPLE, linewidth=1
    )
    ax.add_patch(insight_rect)
    ax.text(5, 3.7, ex['insight'], ha='center', va='center',
            fontsize=8.5, color=C_PURPLE, family='monospace', linespacing=1.5)

    # Course connection box
    conn_rect = mpatches.FancyBboxPatch(
        (1, 0.8), 8, 1.6,
        boxstyle="round,pad=0.1", facecolor='#0d1a2e', edgecolor=C_CYAN, linewidth=1
    )
    ax.add_patch(conn_rect)
    ax.text(1.3, 2.1, 'CONNECTION TO OUR PROJECT:', ha='left', va='center',
            fontsize=6.5, fontweight='bold', color=C_CYAN, family='monospace')
    ax.text(5, 1.3, ex['course_link'], ha='center', va='center',
            fontsize=8, color=C_TEXT, family='sans-serif', linespacing=1.4)

plt.tight_layout(rect=[0, 0, 1, 0.91])
plt.savefig('Embodied_v2.png', dpi=200, bbox_inches='tight', facecolor=C_BG)
print("Saved Embodied_v2.png")
