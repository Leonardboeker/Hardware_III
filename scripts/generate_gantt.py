"""Generate Gantt chart as PNG for the Interactive Assembly Installation."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
import numpy as np

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 14), gridspec_kw={'height_ratios': [1, 0.7]})
fig.patch.set_facecolor('#1a1a2e')

# ─── FULL TERM GANTT (top) ────────────────────────────────────

ax1.set_facecolor('#1a1a2e')

sessions = [
    ('S1\nApr 10', 0),
    ('S2\nApr 17', 7),
    ('', 14),  # gap week
    ('S3\nMay 4', 24),
    ('S4\nMay 11', 31),
    ('S5\nMay 18', 38),
    ('Finals\nMay 22', 42),
]

tasks = [
    ('Concept & Proposal',          0,  9,  '#e94560'),
    ('Module Design & Fabrication', 7,  24, '#f97316'),
    ('ArUco Marker System',         7,  18, '#eab308'),
    ('Input Mapping (webcam+CV)',   7,  24, '#22c55e'),
    ('LCA Data Collection',         7,  24, '#06b6d4'),
    ('FSM Logic Implementation',   24,  35, '#8b5cf6'),
    ('Projection Mapping Setup',   31,  40, '#ec4899'),
    ('Feedback Loop Integration',  31,  40, '#f43f5e'),
    ('Integration & Testing',      38,  43, '#64748b'),
    ('Final Presentation',         38,  43, '#a855f7'),
]

y_positions = list(range(len(tasks)-1, -1, -1))

for i, (name, start, end, color) in enumerate(tasks):
    y = y_positions[i]
    ax1.barh(y, end - start, left=start, height=0.6, color=color, alpha=0.85, edgecolor='none', zorder=3)
    ax1.text(-1, y, name, ha='right', va='center', fontsize=10, color='#eaeaea', family='sans-serif')

# Session markers
for label, day in sessions:
    if label:
        ax1.axvline(x=day, color='#e94560', linewidth=0.8, linestyle='--', alpha=0.5, zorder=2)
        ax1.text(day, len(tasks) + 0.3, label, ha='center', va='bottom', fontsize=8.5,
                color='#e94560', family='monospace', fontweight='bold')

ax1.set_xlim(-12, 45)
ax1.set_ylim(-0.8, len(tasks) + 1.5)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.spines[:].set_visible(False)
ax1.set_title('Full Term — April 10 to May 22', fontsize=16, fontweight='bold',
              color='#eaeaea', family='sans-serif', pad=20)

# Course layer labels
layers = [
    (7,  'Mapping\n(S2)', '#f97316'),
    (24, 'FSM\n(S3)', '#8b5cf6'),
    (31, 'Projection\n(S4)', '#ec4899'),
    (38, 'Integration\n(S5)', '#64748b'),
]
for day, label, color in layers:
    ax1.text(day, -1.3, label, ha='center', va='top', fontsize=7.5, color=color, family='monospace')

# ─── THIS WEEK DETAIL (bottom) ────────────────────────────────

ax2.set_facecolor('#1a1a2e')

week_tasks = [
    ('Proposal (3 slides)',              0, 3, '#e94560',  'DONE'),
    ('Module geometry (3 types)',         1, 4, '#f97316',  'WIP'),
    ('Research LCA data sources',         1, 4, '#06b6d4',  'WIP'),
    ('Draw FSM on paper',                3, 5, '#8b5cf6',  'WIP'),
    ('ArUco detection prototype',         3, 6, '#22c55e',  ''),
    ('Gantt chart finalization',          4, 6, '#eab308',  'WIP'),
    ('Embodied interaction photo',        5, 7, '#ec4899',  ''),
]

days_labels = ['Apr 10', 'Apr 11', 'Apr 12', 'Apr 13', 'Apr 14', 'Apr 15', 'Apr 16', 'Apr 17']

for i, (name, start, end, color, status) in enumerate(week_tasks):
    y = len(week_tasks) - 1 - i
    ax2.barh(y, end - start, left=start, height=0.5, color=color, alpha=0.85, edgecolor='none', zorder=3)
    ax2.text(-0.2, y, name, ha='right', va='center', fontsize=9.5, color='#eaeaea', family='sans-serif')
    if status:
        ax2.text(end + 0.15, y, status, ha='left', va='center', fontsize=8,
                color=color, family='monospace', fontweight='bold')

for i, label in enumerate(days_labels):
    ax2.axvline(x=i, color='#e94560', linewidth=0.5, linestyle=':', alpha=0.3, zorder=2)
    ax2.text(i, -1, label, ha='center', va='top', fontsize=8, color='#a3a3c2', family='monospace')

# Highlight today
ax2.axvline(x=6, color='#e94560', linewidth=2, linestyle='-', alpha=0.8, zorder=4)
ax2.text(6, len(week_tasks) - 0.3, 'TODAY', ha='center', va='bottom', fontsize=9,
        color='#e94560', family='monospace', fontweight='bold')

ax2.set_xlim(-8, 8)
ax2.set_ylim(-1.5, len(week_tasks) + 0.5)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines[:].set_visible(False)
ax2.set_title('This Week Detail — April 10–17', fontsize=14, fontweight='bold',
              color='#eaeaea', family='sans-serif', pad=15)

plt.tight_layout(h_pad=3)
plt.savefig('Gantt_chart.png', dpi=200, bbox_inches='tight', facecolor='#1a1a2e')
print("Saved Gantt_chart.png")
