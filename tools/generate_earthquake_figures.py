"""
Generate clean, modern matplotlib figures for the Earthquake Relief application
in Topic 2 (slides/02_constrained-optimization/deck.qmd and notebooks/topic02_earthquake_relief.ipynb).

Replaces legacy Mathcad screenshot crops:
  1. feasible-region-two-constraints.png
  2. case-transport-binds.png
  3. case-budget-binds.png
  4. case-both-bind.png
  5. earthquake-scipy-solution.png
  6. earthquake-three-regimes-combined.png (for notebook)
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Output directory
FIG_DIR = Path(r"Y:\Hunter\eco701\slides\02_constrained-optimization\figs")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Course color palette
NAVY = "#24325c"
BRICK = "#c0392b"
AMBER = "#b8842a"
SLATE = "#5c6b73"
LIGHT_BG = "#f8f9fa"
FEASIBLE_FILL = "#edf2f7"
FEASIBLE_EDGE = "#cbd5e1"
GREEN = "#2e7d32"

# Typography and styling
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica Neue", "DejaVu Sans"],
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 200,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

def save_fig(fig, filename):
    out_path = FIG_DIR / filename
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")

# ==============================================================================
# Figure 1: Feasible Region with Two Constraints
# ==============================================================================
def make_feasible_region():
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    
    cW = np.linspace(0, 85, 400)
    
    # Constraints
    # Budget: cF + 2*cW <= 100 -> cF = 100 - 2*cW
    cF_budget = 100.0 - 2.0 * cW
    # Transport: cF + cW <= 80 -> cF = 80 - cW
    cF_transport = 80.0 - cW
    
    # Feasible polygon vertices: (0,0) -> (50,0) -> (20,60) -> (0,80)
    poly_pts = [[0, 0], [50, 0], [20, 60], [0, 80]]
    poly = Polygon(poly_pts, closed=True, facecolor=FEASIBLE_FILL, edgecolor=FEASIBLE_EDGE,
                   lw=1.5, zorder=1, label="Feasible Region")
    ax.add_patch(poly)
    
    # Plot lines
    mask_b = (cF_budget >= 0) & (cW <= 52)
    ax.plot(cW[mask_b], cF_budget[mask_b], color=BRICK, lw=2.5, zorder=3,
            label=r"Budget: $c_F + 2c_W \leq 100$")
    
    mask_t = (cF_transport >= 0) & (cW <= 82)
    ax.plot(cW[mask_t], cF_transport[mask_t], color=NAVY, lw=2.5, zorder=3,
            label=r"Transport: $c_F + c_W \leq 80$")
    
    # Highlight vertex (20, 60)
    ax.plot(20, 60, "o", color=NAVY, ms=8, zorder=5)
    ax.annotate(r"Intersection $(20, 60)$", xy=(20, 60), xytext=(28, 68),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2),
                fontweight="bold", color=NAVY, fontsize=10.5)
    
    # Feasible region text inside polygon
    ax.text(14, 25, "FEASIBLE\nREGION", ha="center", va="center",
            color=SLATE, fontsize=11, fontweight="bold", alpha=0.85)
    
    # Intercept markers
    ax.scatter([50, 80], [0, 0], color=[BRICK, NAVY], s=35, zorder=4)
    ax.scatter([0, 0], [100, 80], color=[BRICK, NAVY], s=35, zorder=4)
    
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 110)
    ax.set_xlabel(r"Water / Tents, $c_W$ (tons)")
    ax.set_ylabel(r"Food, $c_F$ (tons)")
    ax.grid(True, linestyle=":", alpha=0.3, zorder=0)
    ax.legend(loc="upper right", frameon=True, framealpha=0.95, edgecolor="#e2e8f0")
    
    save_fig(fig, "feasible-region-two-constraints.png")

# ==============================================================================
# Figures 2, 3, 4: The Three Qualitative Regimes
# ==============================================================================
def make_regime_case1_transport_binds():
    """Case 1: Food is highly valued -> boat capacity binds, budget slack."""
    fig, ax = plt.subplots(figsize=(5.5, 4.8))
    cW = np.linspace(0.1, 85, 400)
    
    poly_pts = [[0, 0], [50, 0], [20, 60], [0, 80]]
    ax.add_patch(Polygon(poly_pts, closed=True, facecolor=FEASIBLE_FILL,
                         edgecolor=FEASIBLE_EDGE, lw=1.2, zorder=1))
    
    # Boundary lines
    ax.plot(cW[100 - 2*cW >= 0], 100 - 2*cW[100 - 2*cW >= 0], color=BRICK, lw=2.2, zorder=2,
            label=r"Budget (slack: $\lambda = 0$)")
    ax.plot(cW[80 - cW >= 0], 80 - cW[80 - cW >= 0], color=NAVY, lw=2.2, zorder=2,
            label=r"Transport (binding: $\mu > 0$)")
    
    cW_curve = np.linspace(2, 28, 200)
    cF_curve = 70 - (cW_curve - 10) + 0.04 * (cW_curve - 10)**2
    ax.plot(cW_curve, cF_curve, color=AMBER, lw=2.5, zorder=4, label="Indifference curve")
    
    # Tangency point
    ax.plot(10, 70, "o", color=GREEN, ms=8, zorder=5)
    ax.annotate("Optimum $(10, 70)$\nBoat full, $10K left",
                xy=(10, 70), xytext=(18, 80),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2),
                fontweight="bold", color=GREEN, fontsize=9.5)
    
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 110)
    ax.set_xlabel(r"Water, $c_W$ (tons)")
    ax.set_ylabel(r"Food, $c_F$ (tons)")
    ax.grid(True, linestyle=":", alpha=0.3, zorder=0)
    ax.legend(loc="upper right", frameon=True, framealpha=0.9, fontsize=9)
    
    save_fig(fig, "case-transport-binds.png")

def make_regime_case2_budget_binds():
    """Case 2: Water is valued -> budget binds, transport slack."""
    fig, ax = plt.subplots(figsize=(5.5, 4.8))
    cW = np.linspace(0.1, 85, 400)
    
    poly_pts = [[0, 0], [50, 0], [20, 60], [0, 80]]
    ax.add_patch(Polygon(poly_pts, closed=True, facecolor=FEASIBLE_FILL,
                         edgecolor=FEASIBLE_EDGE, lw=1.2, zorder=1))
    
    # Boundary lines
    ax.plot(cW[100 - 2*cW >= 0], 100 - 2*cW[100 - 2*cW >= 0], color=BRICK, lw=2.2, zorder=2,
            label=r"Budget (binding: $\lambda > 0$)")
    ax.plot(cW[80 - cW >= 0], 80 - cW[80 - cW >= 0], color=NAVY, lw=2.2, zorder=2,
            label=r"Transport (slack: $\mu = 0$)")
    
    cW_curve = np.linspace(12, 46, 200)
    cF_curve = 1250.0 / cW_curve
    ax.plot(cW_curve, cF_curve, color=AMBER, lw=2.5, zorder=4, label=r"Indifference ($U=1250$)")
    
    # Tangency point
    ax.plot(25, 50, "o", color=GREEN, ms=8, zorder=5)
    ax.annotate("Optimum $(25, 50)$\nMoney spent, 5t boat slack",
                xy=(25, 50), xytext=(32, 60),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2),
                fontweight="bold", color=GREEN, fontsize=9.5)
    
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 110)
    ax.set_xlabel(r"Water, $c_W$ (tons)")
    ax.set_ylabel(r"Food, $c_F$ (tons)")
    ax.grid(True, linestyle=":", alpha=0.3, zorder=0)
    ax.legend(loc="upper right", frameon=True, framealpha=0.9, fontsize=9)
    
    save_fig(fig, "case-budget-binds.png")

def make_regime_case3_both_bind():
    """Case 3: Balanced preferences -> both constraints bind at the vertex (20, 60)."""
    fig, ax = plt.subplots(figsize=(5.5, 4.8))
    cW = np.linspace(0.1, 85, 400)
    
    poly_pts = [[0, 0], [50, 0], [20, 60], [0, 80]]
    ax.add_patch(Polygon(poly_pts, closed=True, facecolor=FEASIBLE_FILL,
                         edgecolor=FEASIBLE_EDGE, lw=1.2, zorder=1))
    
    # Boundary lines
    ax.plot(cW[100 - 2*cW >= 0], 100 - 2*cW[100 - 2*cW >= 0], color=BRICK, lw=2.2, zorder=2,
            label=r"Budget (binding: $\lambda > 0$)")
    ax.plot(cW[80 - cW >= 0], 80 - cW[80 - cW >= 0], color=NAVY, lw=2.2, zorder=2,
            label=r"Transport (binding: $\mu > 0$)")
    
    cW_curve = np.linspace(10, 42, 200)
    cF_curve = (60.0 * np.sqrt(20.0)) / np.sqrt(cW_curve)
    ax.plot(cW_curve, cF_curve, color=AMBER, lw=2.5, zorder=4, label=r"Indifference ($1 < MRS < 2$)")
    
    # Optimum at kink
    ax.plot(20, 60, "o", color=GREEN, ms=8, zorder=5)
    ax.annotate("Optimum at Kink $(20, 60)$\nBoth constraints bind",
                xy=(20, 60), xytext=(28, 72),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2),
                fontweight="bold", color=GREEN, fontsize=9.5)
    
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 110)
    ax.set_xlabel(r"Water, $c_W$ (tons)")
    ax.set_ylabel(r"Food, $c_F$ (tons)")
    ax.grid(True, linestyle=":", alpha=0.3, zorder=0)
    ax.legend(loc="upper right", frameon=True, framealpha=0.9, fontsize=9)
    
    save_fig(fig, "case-both-bind.png")

def make_regimes_combined_3panel():
    """Generates a coordinated 3-panel figure for the notebook."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), sharey=True)
    cW = np.linspace(0.1, 85, 400)
    poly_pts = [[0, 0], [50, 0], [20, 60], [0, 80]]
    
    titles = [
        r"Case 1: Boat Binds ($\lambda=0, \mu>0$)",
        r"Case 2: Money Binds ($\lambda>0, \mu=0$)",
        r"Case 3: Both Bind ($\lambda>0, \mu>0$)"
    ]
    
    for ax, title in zip(axes, titles):
        ax.add_patch(Polygon(poly_pts, closed=True, facecolor=FEASIBLE_FILL,
                             edgecolor=FEASIBLE_EDGE, lw=1.2, zorder=1))
        ax.plot(cW[100 - 2*cW >= 0], 100 - 2*cW[100 - 2*cW >= 0], color=BRICK, lw=2.0, zorder=2, label="Budget")
        ax.plot(cW[80 - cW >= 0], 80 - cW[80 - cW >= 0], color=NAVY, lw=2.0, zorder=2, label="Transport")
        ax.set_xlim(0, 88)
        ax.set_ylim(0, 110)
        ax.set_xlabel(r"Water, $c_W$ (tons)")
        ax.grid(True, linestyle=":", alpha=0.3, zorder=0)
        ax.set_title(title, fontsize=11, fontweight="bold", color=NAVY)
    
    axes[0].set_ylabel(r"Food, $c_F$ (tons)")
    
    # Panel 1 curve
    cW1 = np.linspace(2, 28, 200)
    cF1 = 70 - (cW1 - 10) + 0.04 * (cW1 - 10)**2
    axes[0].plot(cW1, cF1, color=AMBER, lw=2.2, zorder=4)
    axes[0].plot(10, 70, "o", color=GREEN, ms=7.5, zorder=5)
    axes[0].annotate("$(10, 70)$", (10, 70), textcoords="offset points", xytext=(8, 8),
                     fontweight="bold", color=GREEN)
    
    # Panel 2 curve
    cW2 = np.linspace(12, 46, 200)
    cF2 = 1250.0 / cW2
    axes[1].plot(cW2, cF2, color=AMBER, lw=2.2, zorder=4)
    axes[1].plot(25, 50, "o", color=GREEN, ms=7.5, zorder=5)
    axes[1].annotate("$(25, 50)$", (25, 50), textcoords="offset points", xytext=(8, 8),
                     fontweight="bold", color=GREEN)
    
    # Panel 3 curve
    cW3 = np.linspace(10, 42, 200)
    cF3 = (60.0 * np.sqrt(20.0)) / np.sqrt(cW3)
    axes[2].plot(cW3, cF3, color=AMBER, lw=2.2, zorder=4)
    axes[2].plot(20, 60, "o", color=GREEN, ms=7.5, zorder=5)
    axes[2].annotate("$(20, 60)$", (20, 60), textcoords="offset points", xytext=(8, 8),
                     fontweight="bold", color=GREEN)
    
    axes[1].legend(loc="upper right", frameon=True, framealpha=0.9, fontsize=9.5)
    fig.tight_layout()
    save_fig(fig, "earthquake-three-regimes-combined.png")

# ==============================================================================
# Figure 5: SciPy Solution / Choosing the Winner
# ==============================================================================
def make_earthquake_scipy_solution():
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    cW = np.linspace(0.1, 85, 400)
    
    # Feasible region
    poly_pts = [[0, 0], [50, 0], [20, 60], [0, 80]]
    ax.add_patch(Polygon(poly_pts, closed=True, facecolor=FEASIBLE_FILL,
                         edgecolor=FEASIBLE_EDGE, lw=1.2, zorder=1, label="Feasible region"))
    
    # Constraint lines
    ax.plot(cW[100 - 2*cW >= 0], 100 - 2*cW[100 - 2*cW >= 0], color=BRICK, lw=2.4, zorder=3,
            label=r"Budget: $c_F + 2c_W = 100$")
    ax.plot(cW[80 - cW >= 0], 80 - cW[80 - cW >= 0], color=NAVY, lw=2.4, zorder=3,
            label=r"Transport: $c_F + c_W = 80$")
    
    # Indifference curves: U = cF * cW
    # 1. U = 1250 (Optimal, tangent at (25, 50))
    cW_opt = np.linspace(12, 50, 200)
    ax.plot(cW_opt, 1250.0 / cW_opt, color=AMBER, lw=2.5, zorder=4, label=r"$U^* = 1,250$ (Optimal)")
    
    # 2. U = 1200 (Through kink (20, 60))
    cW_kink = np.linspace(11, 48, 200)
    ax.plot(cW_kink, 1200.0 / cW_kink, color="#d4b47c", lw=1.6, linestyle="--", zorder=2,
            label=r"$U = 1,200$ (Kink)")
    
    # 3. U = 1600 (Through (40, 40), boat tangent, infeasible)
    cW_inf = np.linspace(18, 65, 200)
    ax.plot(cW_inf, 1600.0 / cW_inf, color="#94a3b8", lw=1.6, linestyle=":", zorder=2,
            label=r"$U = 1,600$ (Infeasible)")
    
    # Candidates
    # 1. Optimal (25, 50)
    ax.plot(25, 50, "o", color=GREEN, ms=9, zorder=6)
    ax.annotate("Winner: $(c_W^*, c_F^*) = (25, 50)$\n$U^* = 1,250$ (5 tons boat slack)",
                xy=(25, 50), xytext=(32, 58),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.3),
                fontweight="bold", color=GREEN, fontsize=10)
    
    # 2. Kink (20, 60)
    ax.plot(20, 60, "s", color=NAVY, ms=7, zorder=5)
    ax.annotate("Kink $(20, 60)$\n$U = 1,200$", xy=(20, 60), xytext=(3, 60),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.1),
                color=NAVY, fontsize=9, fontweight="bold")
    
    # 3. Infeasible (40, 40)
    ax.plot(40, 40, "X", color=BRICK, ms=8, zorder=5)
    ax.annotate("Infeasible $(40, 40)$\nCost $120K > $100K", xy=(40, 40), xytext=(46, 35),
                arrowprops=dict(arrowstyle="->", color=BRICK, lw=1.1),
                color=BRICK, fontsize=9)
    
    # Slack boat capacity indicator at cW = 25
    ax.vlines(25, 50, 55, color=NAVY, linestyle="--", lw=1.5, zorder=3)
    ax.annotate("5 tons\nslack", xy=(25, 52.5), xytext=(18, 38),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.0),
                color=NAVY, fontsize=8.5)
    
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 110)
    ax.set_xlabel(r"Water / Tents, $c_W$ (tons)")
    ax.set_ylabel(r"Food, $c_F$ (tons)")
    ax.grid(True, linestyle=":", alpha=0.3, zorder=0)
    ax.legend(loc="upper right", frameon=True, framealpha=0.92, edgecolor="#e2e8f0", fontsize=9.5)
    
    save_fig(fig, "earthquake-scipy-solution.png")

if __name__ == "__main__":
    make_feasible_region()
    make_regime_case1_transport_binds()
    make_regime_case2_budget_binds()
    make_regime_case3_both_bind()
    make_regimes_combined_3panel()
    make_earthquake_scipy_solution()
    print("All Earthquake figures successfully generated!")
