import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ==========================================
# 1. DARK THEME & AESTHETICS SETUP
# ==========================================
plt.rcParams.update({
    'figure.facecolor': '#050510',
    'axes.facecolor': '#050510',
    'text.color': '#e0e0e0',
    'font.family': 'monospace', # Monospace adds to the 'terminal/hacker' mystery vibe
    'axes.linewidth': 0,
})

fig, ax = plt.subplots(figsize=(18, 8))
ax.set_xlim(0, 18)
ax.set_ylim(0, 8)
ax.axis('off')

# Helper function to draw glowing lines (neon effect)
def draw_glow_line(ax, start, end, color, lw=2, glow_lw=8, alpha_line=1.0, alpha_glow=0.15):
    # Draw outer glow
    ax.plot([start[0], end[0]], [start[1], end[1]], color=color, lw=glow_lw, alpha=alpha_glow, solid_capstyle='round')
    # Draw inner core
    ax.plot([start[0], end[0]], [start[1], end[1]], color=color, lw=lw, alpha=alpha_line, solid_capstyle='round')

# Helper function to draw glowing nodes
def draw_node(ax, x, y, radius, color, label, label_offset=(0, -0.5), fontsize=8, alpha=0.8):
    # Outer glow
    circle_glow = plt.Circle((x, y), radius*1.5, color=color, alpha=0.05)
    ax.add_patch(circle_glow)
    # Main node
    circle = plt.Circle((x, y), radius, color=color, alpha=alpha, ec=color, lw=1)
    ax.add_patch(circle)
    # Inner core (lighter)
    circle_core = plt.Circle((x, y), radius*0.4, color='white', alpha=0.3)
    ax.add_patch(circle_core)
    # Label
    ax.text(x + label_offset[0], y + label_offset[1], label, ha='center', va='center', fontsize=fontsize, color=color, fontweight='bold')

# ==========================================
# 2. TEXT PATHWAY (Top - Magenta/Pink)
# ==========================================
color_text = '#ff00ff'
draw_node(ax, 1, 6.5, 0.4, color_text, "Harmful\nText", (0, 0.7), 8)
draw_glow_line(ax, (1.4, 6.5), (3.6, 6.5), color_text)
draw_node(ax, 4, 6.5, 0.4, color_text, "Tokenizer", (0, 0.6), 7)
draw_glow_line(ax, (4.4, 6.5), (6.1, 6.5), color_text)
draw_node(ax, 6.5, 6.5, 0.4, color_text, "Embed Lookup\n($W_E$)", (0, 0.7), 7)

# ==========================================
# 3. AUDIO PATHWAY (Bottom - Cyan/Blue)
# ==========================================
color_audio = '#00e5ff'
draw_node(ax, 1, 1.5, 0.4, color_audio, "Spoken Audio\n(16kHz)", (0, -0.7), 8)
draw_glow_line(ax, (1.4, 1.5), (3.6, 1.5), color_audio)
draw_node(ax, 4, 1.5, 0.6, color_audio, "Whisper\nLarge V2\n(CPU)", (0, -0.9), 7)
draw_glow_line(ax, (4.6, 1.5), (6.1, 1.5), color_audio)
draw_node(ax, 6.5, 1.5, 0.5, color_audio, "Qwen2\nAudio\nProjector", (0, -0.8), 7)

# ==========================================
# 4. THE CONVERGENCE (The Injection Point)
# ==========================================
color_merge = '#ffffff'
draw_glow_line(ax, (6.9, 6.5), (8.5, 4.5), color_text, alpha_glow=0.1) # Text descends
draw_glow_line(ax, (7.0, 1.5), (8.5, 4.0), color_audio, alpha_glow=0.1) # Audio ascends

draw_node(ax, 8.5, 4.2, 0.6, color_merge, "hook_embed\ninjection", (0, -1.1), 8, alpha=0.9)

# ==========================================
# 5. SHARED RESIDUAL STREAM (The Black Box)
# ==========================================
color_shared = '#555555'
# Draw a massive translucent block representing the frozen transformer
rect = FancyBboxPatch((9.2, 2.5), 4.5, 3.5, boxstyle="round,pad=0.2", 
                      facecolor='#0f0f2a', edgecolor='#333355', lw=2, alpha=0.8)
ax.add_patch(rect)
ax.text(11.45, 5.6, "Shared Transformer Blocks (Frozen)", ha='center', fontsize=9, color='#8888aa', fontstyle='italic')

# Layer nodes inside
for i, layer_num in enumerate([0, 5, 13]):
    x_pos = 10 + (i * 1.2)
    draw_node(ax, x_pos, 4.2, 0.25, color_shared, f"L{layer_num}", (0, -0.4), 7, alpha=0.5)
    if i < 2:
        draw_glow_line(ax, (x_pos + 0.25, 4.2), (x_pos + 0.95, 4.2), color_shared, lw=1, glow_lw=4, alpha_line=0.4, alpha_glow=0.1)

# Connect injection to shared stream
draw_glow_line(ax, (9.1, 4.2), (9.5, 4.2), color_merge, lw=2, alpha_line=0.6)

# ==========================================
# 6. LAYER 14 & THE ABLATION (The Climax)
# ==========================================
color_target = '#ffeb3b' # Yellow for the target layer
color_ablate = '#ff3333' # Red for the ablation laser

# Layer 14 Node
draw_node(ax, 13.8, 4.2, 0.35, color_target, "Layer 14", (0, -0.5), 9, alpha=0.9)
draw_glow_line(ax, (12.4, 4.2), (13.45, 4.2), color_shared, lw=1, alpha_line=0.4)

# The "Refusal Direction" Vector crossing Layer 14
ax.annotate("", xy=(14.3, 5.0), xytext=(13.3, 3.4),
            arrowprops=dict(arrowstyle="->", color=color_target, lw=2.5))
ax.text(14.6, 5.1, "$\\vec{v}_{refusal}$\n(Text-derived)", fontsize=8, color=color_target, fontweight='bold')

# THE ABLATION BEAM (The mysterious/intense part)
# A sharp red line striking through the vector
ax.plot([13.1, 14.5], [5.2, 3.2], color=color_ablate, lw=3, alpha=0.9)
ax.plot([13.1, 14.5], [5.2, 3.2], color='white', lw=1, alpha=0.5) # White hot core
# Glitch effect text
ax.text(13.8, 5.6, "// DIRECTION_ABLATE", fontsize=9, color=color_ablate, fontweight='bold', alpha=0.9)
ax.text(13.85, 5.6, "// DIRECTION_ABLATE", fontsize=9, color='cyan', fontweight='bold', alpha=0.4) # Cyan shadow offset for glitch

# ==========================================
# 7. DIVERGING OUTPUTS (The Alternate Realities)
# ==========================================
# Line continuing out from Layer 14
draw_glow_line(ax, (14.15, 4.2), (15.5, 4.2), color_shared, lw=2, alpha_line=0.5)

# Split to two realities
draw_glow_line(ax, (15.5, 4.2), (16.8, 6.5), '#555555', lw=1, alpha_line=0.2) # Ghost path (what usually happens)
draw_glow_line(ax, (15.5, 4.2), (16.8, 1.5), color_ablate, lw=2, alpha_line=0.6) # Ablated path (glowing red)

# Reality 1: Default (Faded out / crossed out)
ax.text(17.2, 6.8, "DEFAULT REALITY", fontsize=7, color='#444444', fontweight='bold')
ax.text(17.2, 6.1, '"I\'m sorry, but I\ncannot fulfill..."', fontsize=7, color='#666666', fontstyle='italic')
# Strike-through line
ax.plot([16.9, 19.5], [6.4, 6.4], color='#ff3333', lw=1.5, alpha=0.7)

# Reality 2: Ablated (Bright, dangerous, realized)
ax.text(17.2, 2.0, "ABLATED REALITY", fontsize=7, color=color_ablate, fontweight='bold')
box_danger = FancyBboxPatch((16.8, 0.3), 2.8, 1.5, boxstyle="round,pad=0.1", 
                            facecolor='#1a0000', edgecolor=color_ablate, lw=1.5, alpha=0.8)
ax.add_patch(box_danger)
ax.text(18.2, 1.05, '"Here is a Python\nprogram to hack..."', fontsize=7, color='#ff6666', fontstyle='italic', ha='center')

# ==========================================
# 8. FINAL TOUCHES & ANNOTATIONS
# ==========================================
# Title
ax.text(9, 7.8, "CIRCUIT BREAKING: TRANSFERRING TEXT REFUSAL TO MULTIMODAL AUDIO SPACE", 
        ha='center', fontsize=12, color='white', fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='#050510', edgecolor='#333355', lw=1))

# Subtle background grid to add "blueprint" complexity
for x in np.arange(0, 19, 0.5):
    ax.axvline(x=x, color='#111125', lw=0.5, zorder=0)
for y in np.arange(0, 9, 0.5):
    ax.axhline(y=y, color='#111125', lw=0.5, zorder=0)

plt.tight_layout()
plt.savefig("complex_ablation_architecture.png", dpi=300, facecolor=fig.get_facecolor())
plt.show()