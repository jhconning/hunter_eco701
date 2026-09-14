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

fig, ax = plt.subplots(figsize=(6.2, 4.8), dpi=150)

# Plot hill
ax.plot(x, f, color=NAVY, lw=2.6, label=r'Hill: $f(x) = 10x - 10 - x^2$', zorder=3)

# Fence at x = 2
fence_x = 2.0
f_fence = 10 * fence_x - 10 - fence_x**2  # 6.0
ax.axvline(fence_x, color=BRICK, lw=2.2, ls='--', zorder=4)

# Infeasible shaded region x > 2
ax.axvspan(fence_x, 9.5, facecolor='#f7f0ef', alpha=0.7, hatch='//', edgecolor='#e2cfcc', zorder=1)
ax.text(5.5, -4, 'Infeasible Region\n($x > 2$)', color=BRICK, fontsize=11, fontweight='bold', ha='center', va='center', alpha=0.85)

# Constrained optimum at x = 2
ax.plot(fence_x, f_fence, 'o', color=BRICK, ms=9, zorder=6)
# Tangent at fence: slope = 10 - 2*2 = 6
t_x = np.linspace(1.0, 3.0, 50)
t_y = f_fence + 6.0 * (t_x - fence_x)
ax.plot(t_x, t_y, color=BRICK, lw=1.4, ls=':', zorder=5)

ax.annotate(r'Constrained Optimum: $x^* = 2$' + '\n' + r'Slope $f\'(2) = 6 > 0$ (not flat!)',
            xy=(fence_x, f_fence), xytext=(fence_x + 0.5, f_fence + 3.5),
            color=BRICK, fontsize=10, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=BRICK, lw=1.5),
            ha='left', va='bottom')

# Unconstrained peak at x = 5
peak_x = 5.0
peak_y = 15.0
ax.plot(peak_x, peak_y, 'o', color=AMBER, ms=8, fillstyle='none', mew=2, zorder=4)
ax.axhline(peak_y, xmin=0.45, xmax=0.62, color=AMBER, lw=1.2, ls=':', zorder=3)
ax.annotate(r'Unconstrained Peak: $x = 5$' + '\n' + r'Slope $f\'(5) = 0$ (flat top)' + '\n' + r'[BLOCKED BY FENCE]',
            xy=(peak_x, peak_y), xytext=(peak_x + 0.3, peak_y + 2.0),
            color='#916315', fontsize=9.5, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.2),
            ha='left', va='bottom')

# Axes styling
ax.axhline(0, color='#999999', lw=0.8, zorder=2)
ax.set_xlim(0, 9.2)
ax.set_ylim(-9, 22)
ax.set_xlabel('Choice variable $x$', fontsize=11)
ax.set_ylabel('Objective $f(x)$', fontsize=11)
ax.set_title(r'The Hill and the Fence: $\max f(x)$ s.t. $x \leq 2$', fontsize=12.5, color=NAVY, pad=12, fontweight='bold')

# Tag fence
ax.text(fence_x + 0.12, -7.5, r'Fence: $x \leq 2$', color=BRICK, fontsize=10.5, fontweight='bold', ha='left')

plt.tight_layout()
out_path = Path('slides/02_constrained-optimization/figs/hill-and-fence-graph.png')
out_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_path, dpi=150)
print(f'Successfully saved {out_path}')
