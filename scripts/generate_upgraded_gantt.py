"""
UPGRADED Gantt chart — cleaner, with session alignment,
course layer mapping, and deliverable callouts.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime, timedelta

fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor('#0f0f1a')

# Two subplots
gs = fig.add_gridspec(2, 1, height_ratios=[1.2, 0.8], hspace=0.25)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

for ax in [ax1, ax2]:
    ax.set_facecolor('#0f0f1a')
    ax.spines[:].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# Colors
C_ACCENT  = '#ff3366'
C_ORANGE  = '#ff6b35'
C_CYAN    = '#00d4ff'
C_GREEN   = '#00cc88'
C_PURPLE  = '#8855ff'
C_YELLOW  = '#ffcc00'
C_TEXT    = '#f0f0f0'
C_DIM     = '#7a7a9e'
C_PANEL   = '#161627'

# ═══════════════════════════════════════════════
# FULL TERM
# ═══════════════════════════════════════════════
ax1.set_xlim(-10, 46)
ax1.set_ylim(-2.5, 14)

ax1.text(18, 13.5, 'MATTER & METHOD \u2014 Full Term Schedule', ha='center', va='center',
         fontsize=18, fontweight='bold', color=C_TEXT, family='sans-serif')

# Session columns (background bands)
sessions = [
    ('S1', 'Apr 10', 0, 7, C_ACCENT),
    ('S2', 'Apr 17', 7, 24, C_ORANGE),
    ('S3', 'May 4', 24, 31, C_PURPLE),
    ('S4', 'May 11', 31, 38, C_CYAN),
    ('S5', 'May 18', 38, 42, C_GREEN),
    ('FIN', 'May 22', 42, 44, C_YELLOW),
]

for label, date, start, end, color in sessions:
    # Subtle background band
    rect = mpatches.FancyBboxPatch(
        (start, -1.5), end - start, 13.5,
        boxstyle="round,pad=0", facecolor=color, alpha=0.04
    )
    ax1.add_patch(rect)
    # Session marker at top
    ax1.axvline(x=start, color=color, linewidth=0.8, linestyle=':', alpha=0.3, ymin=0.05, ymax=0.95)
    # Label
    ax1.text(start, 12.5, label, ha='center', va='center', fontsize=11, fontweight='bold',
             color=color, family='monospace')
    ax1.text(start, 11.8, date, ha='center', va='center', fontsize=8, color=C_DIM, family='monospace')

# Course layer labels
layers = [
    (3.5, 'Concept\n& Proposal', C_ACCENT),
    (15.5, 'Input &\nMapping', C_ORANGE),
    (27.5, 'FSM &\nLogic', C_PURPLE),
    (34.5, 'Projection &\nFeedback', C_CYAN),
    (40, 'Integration', C_GREEN),
    (43, 'Final', C_YELLOW),
]
for x, label, color in layers:
    ax1.text(x, 10.8, label, ha='center', va='center', fontsize=7.5, color=color,
             family='sans-serif', alpha=0.7, linespacing=1.3)

# Tasks
tasks = [
    ('Concept & Proposal',          0,   9,  C_ACCENT,  'DONE'),
    ('Module Design + Fabrication',  7,  26,  C_ORANGE,  ''),
    ('ArUco + Camera Pipeline',      7,  20,  C_CYAN,    ''),
    ('LCA Data (ranges + sources)',  7,  26,  C_GREEN,   ''),
    ('Input Mapping (webcam CV)',    10,  26,  C_ORANGE,  ''),
    ('FSM Logic Implementation',    24,  35,  C_PURPLE,  ''),
    ('Projection Mapping Setup',    31,  40,  C_YELLOW,  ''),
    ('Feedback Loop + Data Overlay', 31,  40,  C_CYAN,    ''),
    ('Animation System (3 methods)',33,  40,  C_ORANGE,  ''),
    ('Integration & Testing',       38,  43,  C_GREEN,   ''),
    ('Final Presentation',          40,  44,  C_YELLOW,  ''),
]

for i, (name, start, end, color, status) in enumerate(tasks):
    y = 9 - i * 0.85
    # Bar
    bar = mpatches.FancyBboxPatch(
        (start, y - 0.25), end - start, 0.5,
        boxstyle="round,pad=0.1", facecolor=color, alpha=0.85
    )
    ax1.add_patch(bar)
    # Label
    ax1.text(-0.5, y, name, ha='right', va='center', fontsize=9.5, color=C_TEXT, family='sans-serif')
    # Status
    if status:
        ax1.text(end + 0.5, y, status, ha='left', va='center', fontsize=8,
                 color=color, family='monospace', fontweight='bold')

# Deliverable markers
deliverables = [
    (7, 'Proposal due', C_ACCENT),
    (24, 'FSM implemented', C_PURPLE),
    (38, 'Full prototype', C_GREEN),
    (42, 'Final demo', C_YELLOW),
]
for x, label, color in deliverables:
    ax1.plot(x, -1, 's', color=color, markersize=8, zorder=5)
    ax1.text(x, -1.8, label, ha='center', va='center', fontsize=7.5, color=color,
             family='sans-serif', fontstyle='italic')

# ═══════════════════════════════════════════════
# THIS WEEK DETAIL
# ═══════════════════════════════════════════════
ax2.set_xlim(-10, 9)
ax2.set_ylim(-1.5, 10)

ax2.text(3.5, 9.5, 'This Week Detail \u2014 April 10\u201317', ha='center', va='center',
         fontsize=16, fontweight='bold', color=C_TEXT, family='sans-serif')

# Day columns
days = ['Thu 10', 'Fri 11', 'Sat 12', 'Sun 13', 'Mon 14', 'Tue 15', 'Wed 16', 'Thu 17']
for i, day in enumerate(days):
    ax2.axvline(x=i, color=C_DIM, linewidth=0.4, linestyle=':', alpha=0.3)
    ax2.text(i, -0.8, day, ha='center', va='center', fontsize=8, color=C_DIM, family='monospace')

# Today marker
ax2.axvline(x=6, color=C_ACCENT, linewidth=2.5, alpha=0.8)
ax2.text(6, 9, 'TODAY', ha='center', va='center', fontsize=9, fontweight='bold',
         color=C_ACCENT, family='monospace',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='#0f0f1a', edgecolor=C_ACCENT))

week_tasks = [
    ('Write proposal (3 slides)',      0, 3, C_ACCENT,  'DONE'),
    ('Design module geometry',          1, 5, C_ORANGE,  'WIP'),
    ('Research LCA data + sources',     1, 5, C_GREEN,   'WIP'),
    ('Draw FSM on paper',               3, 6, C_PURPLE,  'DONE'),
    ('Test ArUco detection',            3, 7, C_CYAN,    'WIP'),
    ('Gantt chart',                     5, 7, C_YELLOW,  'DONE'),
    ('Embodied interaction sketch',     5, 7, C_ORANGE,  'DONE'),
    ('Submit all deliverables',         7, 8, C_ACCENT,  'Apr 17'),
]

for i, (name, start, end, color, status) in enumerate(week_tasks):
    y = 8 - i * 0.95
    bar = mpatches.FancyBboxPatch(
        (start, y - 0.25), end - start, 0.5,
        boxstyle="round,pad=0.1", facecolor=color, alpha=0.85
    )
    ax2.add_patch(bar)
    ax2.text(-0.3, y, name, ha='right', va='center', fontsize=9.5, color=C_TEXT, family='sans-serif')
    ax2.text(end + 0.2, y, status, ha='left', va='center', fontsize=8,
             color=color, family='monospace', fontweight='bold')

plt.savefig('Gantt_v2.png', dpi=200, bbox_inches='tight', facecolor='#0f0f1a')
print("Saved Gantt_v2.png")
