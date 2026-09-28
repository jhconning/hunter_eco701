import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

NAVY = '#24325c'
AMBER = '#b8842a'
BRICK = '#a04434'
GRAY = '#5a6578'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.edgecolor': '#888888',
    'axes.labelcolor': '#222222',
    'mathtext.fontset': 'cm'
})

x = np.linspace(0, 9.2, 400)
f = 10 * x - 10 - x**2

fig, ax = plt.subplots(figsize=(6.0, 4.4), dpi=150)

# Plot hill
ax.plot(x, f, color=NAVY, lw=2.6, zorder=3)

# Fence at x = 2
fence_x = 2.0
f_fence = 10 * fence_x - 10 - fence_x**2  # 6.0
ax.axvline(fence_x, color=BRICK, lw=2.0, ls='--', zorder=4)

# Infeasible shaded region x > 2 (soft, clean, no heavy text)
ax.axvspan(fence_x, 9.5, facecolor='#fcf4f2', alpha=0.8, edgecolor='none', zorder=1)
ax.text(6.0, -5, 'Infeasible', color='#b88078', fontsize=11, fontstyle='italic', ha='center')

# Constrained optimum at x = 2
ax.plot(fence_x, f_fence, 'o', color=BRICK, ms=8, zorder=6)
# Tangent at fence: slope = 6
t_x = np.linspace(1.1, 2.9, 50)
t_y = f_fence + 6.0 * (t_x - fence_x)
ax.plot(t_x, t_y, color=BRICK, lw=1.5, ls=':', zorder=5)

ax.annotate(r'$x^* = 2$', xy=(fence_x, f_fence), xytext=(fence_x - 0.25, f_fence + 1.2),
            color=BRICK, fontsize=11, fontweight='bold', ha='right', va='bottom')

# Unconstrained peak at x = 5
peak_x = 5.0
peak_y = 15.0
ax.plot(peak_x, peak_y, 'o', color=AMBER, ms=8, fillstyle='none', mew=2, zorder=4)
ax.axhline(peak_y, xmin=0.45, xmax=0.62, color=AMBER, lw=1.2, ls=':', zorder=3)
ax.annotate(r'Peak ($x = 5$)', xy=(peak_x, peak_y), xytext=(peak_x + 0.3, peak_y + 1.2),
            color='#916315', fontsize=10.5, ha='left', va='bottom')

# Axes styling
ax.axhline(0, color='#aaaaaa', lw=0.8, zorder=2)
ax.set_xlim(0, 9.2)
ax.set_ylim(-8, 19.5)
ax.set_xlabel('Choice variable $x$', fontsize=11)
ax.set_ylabel(r'$f(x)$', fontsize=11)

# Fence label inside plot
ax.text(fence_x - 0.15, 17.5, r'Fence: $x \leq 2$', color=BRICK, fontsize=10.5,
        fontweight='bold', ha='right', va='center')

plt.tight_layout()
out_path = Path('slides/02_constrained-optimization/figs/hill-and-fence-graph.png')
out_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_path, dpi=150)
print(f'Successfully saved {out_path}')
