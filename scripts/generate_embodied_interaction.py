"""Generate an illustrated sketch of a non-screen embodied interaction: the door handle."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(12, 8))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.set_aspect('equal')
ax.axis('off')

# Title
ax.text(6, 7.5, 'Embodied Interaction — The Door Handle', ha='center', va='center',
        fontsize=20, fontweight='bold', color='#eaeaea', family='sans-serif')
ax.text(6, 7.0, 'A non-screen interaction where the body knows what to do without thinking',
        ha='center', va='center', fontsize=11, color='#a3a3c2', family='sans-serif', fontstyle='italic')

# ─── LEFT: PUSH (flat plate) ───
# Door frame
door_left = mpatches.FancyBboxPatch((0.8, 1), 3.5, 5, boxstyle="round,pad=0.05",
                                     facecolor='#16213e', edgecolor='#e94560', linewidth=2)
ax.add_patch(door_left)

# Flat push plate
plate = mpatches.FancyBboxPatch((3.3, 3.0), 0.5, 1.5, boxstyle="round,pad=0.05",
                                 facecolor='#e94560', edgecolor='#eaeaea', linewidth=1.5)
ax.add_patch(plate)

# Hand pushing (simplified)
# Palm shape
ax.annotate('', xy=(3.55, 3.75), xytext=(5.0, 3.75),
            arrowprops=dict(arrowstyle='->', color='#f97316', lw=3))
ax.text(5.1, 3.75, 'PUSH', ha='left', va='center', fontsize=14, fontweight='bold',
        color='#f97316', family='monospace')

ax.text(2.5, 6.3, 'FLAT PLATE', ha='center', va='center',
        fontsize=12, fontweight='bold', color='#eaeaea', family='monospace')
ax.text(2.5, 0.6, 'Flat surface = palm pushes.', ha='center', va='center',
        fontsize=9.5, color='#a3a3c2', family='sans-serif')
ax.text(2.5, 0.3, 'No instruction needed.', ha='center', va='center',
        fontsize=9.5, color='#a3a3c2', family='sans-serif')

# ─── RIGHT: PULL (curved handle) ───
door_right = mpatches.FancyBboxPatch((7.2, 1), 3.5, 5, boxstyle="round,pad=0.05",
                                      facecolor='#16213e', edgecolor='#e94560', linewidth=2)
ax.add_patch(door_right)

# Curved handle (arc)
theta = np.linspace(-np.pi/2, np.pi/2, 50)
handle_x = 7.7 + 0.15 * np.cos(theta)
handle_y = 3.75 + 0.75 * np.sin(theta)
ax.plot(handle_x, handle_y, color='#eaeaea', linewidth=4, solid_capstyle='round')

# Mounting points
ax.plot(7.7, 3.0, 'o', color='#eaeaea', markersize=6)
ax.plot(7.7, 4.5, 'o', color='#eaeaea', markersize=6)

# Hand pulling
ax.annotate('', xy=(6.5, 3.75), xytext=(7.5, 3.75),
            arrowprops=dict(arrowstyle='->', color='#06b6d4', lw=3))
ax.text(6.4, 3.75, 'PULL', ha='right', va='center', fontsize=14, fontweight='bold',
        color='#06b6d4', family='monospace')

ax.text(8.95, 6.3, 'CURVED HANDLE', ha='center', va='center',
        fontsize=12, fontweight='bold', color='#eaeaea', family='monospace')
ax.text(8.95, 0.6, 'Curved grip = fingers wrap and pull.', ha='center', va='center',
        fontsize=9.5, color='#a3a3c2', family='sans-serif')
ax.text(8.95, 0.3, 'Shape IS the instruction.', ha='center', va='center',
        fontsize=9.5, color='#a3a3c2', family='sans-serif')

# Center divider
ax.plot([5.85, 5.85], [1.2, 5.8], color='#e94560', linewidth=1, linestyle='--', alpha=0.4)
ax.text(5.85, 4.8, 'VS', ha='center', va='center', fontsize=16, fontweight='bold',
        color='#e94560', family='monospace',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', edgecolor='#e94560', linewidth=1.5))

# Bottom insight box
insight_box = mpatches.FancyBboxPatch((1.5, -0.6), 9, 1.0, boxstyle="round,pad=0.1",
                                       facecolor='#2a1a3e', edgecolor='#8b5cf6', linewidth=1.5)
ax.add_patch(insight_box)
ax.text(6, 0.0, 'The form factor communicates the affordance. No label, no screen, no tutorial.',
        ha='center', va='center', fontsize=10, color='#eaeaea', family='sans-serif')
ax.text(6, -0.3, 'This is embodied interaction: the body reads the shape and knows the action.',
        ha='center', va='center', fontsize=10, color='#a3a3c2', family='sans-serif', fontstyle='italic')

ax.set_ylim(-0.8, 8)

plt.tight_layout()
plt.savefig('Embodied_interaction.png', dpi=200, bbox_inches='tight', facecolor='#1a1a2e')
print("Saved Embodied_interaction.png")
