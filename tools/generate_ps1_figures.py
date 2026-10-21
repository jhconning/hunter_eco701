"""
Generate high-resolution matplotlib figures for ECO 701 Problem Set 1 solutions.
Outputs all figures to ps/F26/figs/.

Figures:
  1. ps1_q1_best_responses.png: Lake fishery reaction curves, Nash (16,8), Social Optimum (14.86, 6.29)
  2. ps1_q1_payoff_space.png: 2x2 game payoff space, Pareto frontier, Prisoners' Dilemma
  3. ps1_q2_soc_profit.png: Cubic profit function and marginal profit showing SOC
  4. ps1_q3_budget_sets.png: Targeted subsidy, benefit cliff notch ($2 raise), and set nesting ($4 raise)
  5. ps1_q4_consumer_opt.png: Luz's consumer tangency, expansion path, and indifference curves
  6. ps1_q6_disaster_relief.png: Feasible polygon, kink, capacity tangency (35,35), and slack budget
  7. ps1_bonus_comparative_statics.png: Shift in Ben's reaction curve and move to new Nash
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Output directory
FIG_DIR = Path(r"Y:\Hunter\eco701\ps\F26\figs")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Course color palette
NAVY = "#1a365d"
BRICK = "#c53030"
AMBER = "#d69e2e"
TEAL = "#2b6cb0"
SLATE = "#4a5568"
GREEN = "#2f855a"
PURPLE = "#6b46c1"
LIGHT_BG = "#f7fafc"
FEASIBLE_FILL = "#ebf8ff"
FEASIBLE_EDGE = "#90cdf4"
SHRINK_FILL = "#fed7d7"

# Typography and styling
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica Neue"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "figure.dpi": 200,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": ":",
})

def save_fig(fig, filename):
    out_path = FIG_DIR / filename
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")

# ==============================================================================
# Figure 1: Q1 Lake Fishery Best Responses, Nash & Social Optimum
# ==============================================================================
def make_q1_best_responses():
    fig, ax = plt.subplots(figsize=(6.8, 5.5))
    
    eA_vals = np.linspace(0, 20, 400)
    
    # Ana's BR: eA = 18 - 0.25*eB -> eB = 72 - 4*eA
    eB_Ana = np.linspace(0, 12, 200)
    eA_Ana = 18.0 - 0.25 * eB_Ana
    
    # Ben's BR: eB = 10 - 0.125*eA
    eB_Ben = 10.0 - 0.125 * eA_vals
    
    # Social Planner optimality conditions (internalizing congestion externalities):
    # dW/deA = 18 - eA - 0.5*eB = 0 -> eA = 18 - 0.5*eB
    # dW/deB = 20 - 2*eB - 0.5*eA = 0 -> eB = 10 - 0.25*eA
    eB_planner_Ana = np.linspace(0, 12, 200)
    eA_planner_Ana = 18.0 - 0.5 * eB_planner_Ana
    eB_planner_Ben = 10.0 - 0.25 * eA_vals
    
    # Plot reaction curves
    ax.plot(eA_Ana, eB_Ana, color=TEAL, lw=2.2, label=r"Ana's BR: $e_A^{BR}(e_B) = 18 - \frac{1}{4}e_B$")
    ax.plot(eA_vals, eB_Ben, color=BRICK, lw=2.2, label=r"Ben's BR: $e_B^{BR}(e_A) = 10 - \frac{1}{8}e_A$")
    
    # Plot planner curves (dashed, internalizing externalities)
    ax.plot(eA_planner_Ana, eB_planner_Ana, color=TEAL, lw=1.3, ls="--", alpha=0.7,
            label=r"Planner condition for Ana: $e_A = 18 - \frac{1}{2}e_B$")
    ax.plot(eA_vals, eB_planner_Ben, color=BRICK, lw=1.3, ls="--", alpha=0.7,
            label=r"Planner condition for Ben: $e_B = 10 - \frac{1}{4}e_A$")
    
    # Highlight Nash (16, 8)
    ax.plot(16, 8, marker='o', markersize=8, color=NAVY, zorder=6)
    ax.annotate(r"$\mathbf{Nash\ Equilibrium}$" + "\n" + r"$(e_A^N=16,\, e_B^N=8)$" + "\n" + r"$u_A=128,\, u_B=64$" + "\n" + r"$W = 192$",
                xy=(16, 8), xytext=(12.2, 9.4),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2),
                fontsize=8.8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=NAVY, alpha=0.9))
    
    # Social Optimum (104/7, 44/7) approx (14.86, 6.29)
    eA_so = 104.0 / 7.0
    eB_so = 44.0 / 7.0
    ax.plot(eA_so, eB_so, marker='*', markersize=12, color=PURPLE, zorder=7)
    ax.annotate(r"$\mathbf{Social\ Optimum\ (Pareto\ Efficient)}$" + "\n" +
                r"$(e_A^{SO}=14.86,\, e_B^{SO}=6.29)$" + "\n" +
                r"$W^{SO} = 196.57 > 192$",
                xy=(eA_so, eB_so), xytext=(3.2, 4.2),
                arrowprops=dict(arrowstyle="->", color=PURPLE, lw=1.3),
                fontsize=8.8, color=PURPLE,
                bbox=dict(boxstyle="round,pad=0.3", fc="#faf5ff", ec=PURPLE, alpha=0.95))
    
    # 10% Cut Pareto improvement point (14.4, 7.2)
    ax.plot(14.4, 7.2, marker='s', markersize=6, color=GREEN, zorder=6)
    ax.annotate(r"10% Cut: $(14.4,\, 7.2)$" + "\n" + r"$u_A=129.6,\, u_B=66.2$",
                xy=(14.4, 7.2), xytext=(7.5, 7.8),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0),
                fontsize=8.2, color=GREEN,
                bbox=dict(boxstyle="round,pad=0.25", fc="#f0fff4", ec=GREEN, alpha=0.9))
    
    # Arrow connecting Nash to Social Optimum
    ax.annotate("", xy=(eA_so + 0.1, eB_so + 0.1), xytext=(15.8, 7.8),
                arrowprops=dict(arrowstyle="->", color=PURPLE, lw=2.0, ls="-"))
    
    # Dashed coordinate guides to Nash
    ax.plot([16, 16], [0, 8], color=NAVY, ls=":", lw=1.0)
    ax.plot([0, 16], [8, 8], color=NAVY, ls=":", lw=1.0)
    
    # Intercepts
    ax.plot(18, 0, marker='o', markersize=4, color=TEAL)
    ax.text(18.2, 0.3, "$(18, 0)$", color=TEAL, fontsize=8.0)
    ax.plot(0, 10, marker='o', markersize=4, color=BRICK)
    ax.text(0.3, 10.3, "$(0, 10)$", color=BRICK, fontsize=8.0)
    
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.set_xlabel(r"Ana's Effort, $e_A$ (hours/day)")
    ax.set_ylabel(r"Ben's Effort, $e_B$ (hours/day)")
    ax.set_title("Question 1: Best Responses, Nash Equilibrium & Social Optimum", pad=12)
    ax.legend(loc="lower left", framealpha=0.92, fontsize=8.0)
    
    save_fig(fig, "ps1_q1_best_responses.png")

# ==============================================================================
# Figure 2: Q1.4(c) Payoff Space & Prisoners' Dilemma
# ==============================================================================
def make_q1_payoff_space():
    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    
    # Profiles: (uA, uB, label, strategy)
    pts = [
        (128.0, 64.0, "Nash Equilibrium\n(16, 8) [Defect, Defect]", BRICK, (-20, -32)),
        (129.5, 66.5, "Mutual Restraint\n(14, 7) [Coop, Coop]", GREEN, (10, 10)),
        (132.0, 63.0, "Ana Cheats, Ben Restrains\n(16, 7) [Defect, Coop]", TEAL, (10, -18)),
        (126.0, 68.0, "Ana Restrains, Ben Cheats\n(14, 8) [Coop, Defect]", AMBER, (-35, 12)),
    ]
    
    # Pareto dominant quadrant from Nash
    ax.fill_between([128.0, 134.0], [64.0, 64.0], [70.0, 70.0],
                    color="#f0fff4", alpha=0.7, label="Pareto-dominating region relative to Nash")
    
    # Dashed crosshair at Nash
    ax.axvline(128.0, color=SLATE, ls="--", lw=1.0)
    ax.axhline(64.0, color=SLATE, ls="--", lw=1.0)
    
    # Connect Pareto frontier: (126, 68) -> (129.5, 66.5) -> (132, 63)
    ax.plot([126.0, 129.5, 132.0], [68.0, 66.5, 63.0], color=GREEN, lw=2.0, ls="-.",
            label="Pareto Frontier of $2 \\times 2$ Game")
    
    for uA, uB, lbl, col, offset in pts:
        ax.plot(uA, uB, marker='o', markersize=8, color=col, zorder=5)
        ax.annotate(lbl, xy=(uA, uB), xytext=offset, textcoords='offset points',
                    fontsize=8.5, fontweight='bold', color=col,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=col, alpha=0.85))
    
    ax.set_xlim(124.5, 134.0)
    ax.set_ylim(61.5, 70.0)
    ax.set_xlabel(r"Ana's Payoff, $u_A$ (\$/day)")
    ax.set_ylabel(r"Ben's Payoff, $u_B$ (\$/day)")
    ax.set_title("Question 1.4: Payoff Space & The Prisoners' Dilemma", pad=12)
    ax.legend(loc="lower left", framealpha=0.95)
    
    save_fig(fig, "ps1_q1_payoff_space.png")

# ==============================================================================
# Figure 3: Q2 Cubic Profit & Second-Order Conditions
# ==============================================================================
def make_q2_soc_profit():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 6.0), sharex=True, gridspec_kw={'height_ratios': [2, 1.2]})
    
    q = np.linspace(0, 10, 400)
    pi = - (1.0/3.0)*q**3 + 5.0*q**2 - 16.0*q
    dpi = - q**2 + 10.0*q - 16.0
    
    # --- Top Panel: Profit Function ---
    ax1.plot(q, pi, color=NAVY, lw=2.2, label=r"$\pi(q) = -\frac{1}{3}q^3 + 5q^2 - 16q$")
    ax1.axhline(0, color=SLATE, ls="-", lw=1.0)
    
    # Local min at q=2
    ax1.plot(2, -14.67, marker='o', markersize=7, color=BRICK, zorder=5)
    ax1.annotate(r"$\mathbf{Local\ Minimum}$" + "\n" + r"$q=2,\, \pi=-14.67$" + "\n" + r"$\pi''(2) = +6 > 0$",
                 xy=(2, -14.67), xytext=(2.6, -18.0),
                 arrowprops=dict(arrowstyle="->", color=BRICK),
                 fontsize=8.5, color=BRICK,
                 bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=BRICK, alpha=0.9))
    
    # Local max at q=8
    ax1.plot(8, 21.33, marker='o', markersize=7, color=GREEN, zorder=5)
    ax1.annotate(r"$\mathbf{Global\ Maximum}$" + "\n" + r"$q=8,\, \pi=21.33$" + "\n" + r"$\pi''(8) = -6 < 0$",
                 xy=(8, 20.5), xytext=(6.2, 5.0),
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2),
                 fontsize=8.5, color=GREEN,
                 bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=GREEN, alpha=0.9))
    
    # Boundary q=0
    ax1.plot(0, 0, marker='s', markersize=6, color=SLATE, zorder=5)
    ax1.annotate(r"Shutdown: $q=0,\, \pi=0$", xy=(0, 0), xytext=(0.4, 5.0),
                 fontsize=8.5, color=SLATE)
    
    ax1.set_ylabel(r"Profit, $\pi(q)$ (\$)")
    ax1.set_ylim(-24, 28)
    ax1.set_title("Question 2: Second-Order Conditions (Why the FOC Needs the SOC)", pad=12)
    ax1.legend(loc="upper left")
    
    # --- Bottom Panel: Marginal Profit ---
    ax2.plot(q, dpi, color=PURPLE, lw=2.0, label=r"$\pi'(q) = -q^2 + 10q - 16 = -(q-2)(q-8)$")
    ax2.axhline(0, color=SLATE, ls="-", lw=1.0)
    
    ax2.plot(2, 0, marker='o', markersize=6, color=BRICK)
    ax2.plot(8, 0, marker='o', markersize=6, color=GREEN)
    
    # Shading positive / negative marginal profit
    ax2.fill_between(q, 0, dpi, where=(dpi > 0), color="#e6fffa", alpha=0.6, label=r"$\pi'(q) > 0$ (Profit rising)")
    ax2.fill_between(q, 0, dpi, where=(dpi < 0), color="#fff5f5", alpha=0.6, label=r"$\pi'(q) < 0$ (Profit falling)")
    
    ax2.set_xlabel(r"Output Quantity, $q$")
    ax2.set_ylabel(r"$\pi'(q) = MR - MC$")
    ax2.legend(loc="lower left", fontsize=8.5)
    
    plt.tight_layout()
    save_fig(fig, "ps1_q2_soc_profit.png")

# ==============================================================================
# Figure 4: Q3 Budget Sets, Means-Tested Kink, and Welfare Cliff
# ==============================================================================
def make_q3_budget_sets():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.8))
    
    x1 = np.linspace(0, 20, 400)
    
    # --- Panel A: Targeted Subsidy & $2 Raise Notch ---
    x2_base = 10.0 - 0.5 * x1
    x2_sub = np.where(x1 <= 5, 10.0 - 0.5 * x1, 12.5 - x1)
    x2_sub = np.clip(x2_sub, 0, None)
    
    # $2 wage raise: m=12, full market price $1.00 -> x2 = 12 - x1
    x2_raise2 = np.clip(12.0 - x1, 0, None)
    
    ax1.plot(x1[x1 <= 20], x2_base[x1 <= 20], color=SLATE, lw=1.5, ls="--", label=r"Linear baseline ($m=\$10,\, p_1=\$0.50$)")
    ax1.plot(x1[x1 <= 12.5], x2_sub[x1 <= 12.5], color=TEAL, lw=2.2, label=r"Targeted Subsidy ($m=\$10$, kink at $(5, 7.5)$)")
    ax1.plot(x1[x1 <= 12.0], x2_raise2[x1 <= 12.0], color=BRICK, lw=2.2, label=r"After \$2 Raise ($m=\$12,\, p_1=\$1.00$)")
    
    # Shading the welfare notch / shrink zone between x1=4 and x1=12.5
    notch_x = np.linspace(4.0, 12.5, 200)
    notch_sub = np.where(notch_x <= 5, 10.0 - 0.5 * notch_x, 12.5 - notch_x)
    notch_raise = np.clip(12.0 - notch_x, 0, None)
    ax1.fill_between(notch_x, notch_raise, notch_sub, color=SHRINK_FILL, alpha=0.7,
                     label=r"Poverty Trap / Shrink Zone ($x_1 > 4$)")
    
    # Mark Kink and Crossover
    ax1.plot(5, 7.5, marker='o', markersize=6, color=TEAL)
    ax1.annotate(r"Kink: $(5,\, 7.5)$", xy=(5, 7.5), xytext=(5.8, 8.2), fontsize=8.5, color=TEAL)
    
    ax1.plot(4, 8.0, marker='o', markersize=6, color=BRICK)
    ax1.annotate(r"Crossover: $(4,\, 8)$", xy=(4, 8.0), xytext=(1.0, 6.2),
                 arrowprops=dict(arrowstyle="->", color=BRICK), fontsize=8.5, color=BRICK)
    
    ax1.set_xlim(0, 16)
    ax1.set_ylim(0, 14)
    ax1.set_xlabel(r"Apples, $x_1$ (lbs)")
    ax1.set_ylabel(r"Other Goods, $x_2$ (\$)")
    ax1.set_title("3.2 & 3.3: The Means-Tested Benefit Cliff", pad=10)
    ax1.legend(loc="upper right", fontsize=8.2)
    
    # --- Panel B: Substantial $4 Raise (Set Nesting) ---
    x_14 = x1[x1 <= 14.0]
    x2_raise4_sub = 14.0 - x_14
    x2_old_sub = np.where(x_14 <= 5.0, 10.0 - 0.5 * x_14, np.where(x_14 <= 12.5, 12.5 - x_14, 0.0))
    
    # Shaded old budget set
    x_fill = np.linspace(0, 12.5, 300)
    y_fill = np.where(x_fill <= 5, 10.0 - 0.5 * x_fill, 12.5 - x_fill)
    ax2.fill_between(x_fill, 0, y_fill, color=FEASIBLE_FILL, alpha=0.8, label=r"Old Budget Set $B_{\text{old}}$ ($m=\$10$)")
    
    ax2.plot(x1[x1 <= 12.5], x2_sub[x1 <= 12.5], color=TEAL, lw=2.0, ls="--", label=r"Old Budget Line ($m=\$10$)")
    ax2.plot(x_14, x2_raise4_sub, color=GREEN, lw=2.2, label=r"New Budget Line ($m=\$14,\, p_1=\$1.00$)")
    
    # Shading the strictly expanded region
    ax2.fill_between(x_14, x2_old_sub, x2_raise4_sub,
                     color="#f0fff4", alpha=0.5, label=r"Expanded Budget: $B_{\text{old}} \subset B_{\text{new}}$")
    
    ax2.set_xlim(0, 16)
    ax2.set_ylim(0, 15)
    ax2.set_xlabel(r"Apples, $x_1$ (lbs)")
    ax2.set_ylabel(r"Other Goods, $x_2$ (\$)")
    ax2.set_title(r"3.4: \$4 Raise & Revealed Preference Dominance", pad=10)
    ax2.legend(loc="upper right", fontsize=8.2)
    
    plt.tight_layout()
    save_fig(fig, "ps1_q3_budget_sets.png")

# ==============================================================================
# Figure 5: Q4 Consumer Optimization & Tangency
# ==============================================================================
def make_q4_consumer_opt():
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    
    x = np.linspace(2, 42, 400)
    
    # Budget line: 20x + 40y = 800 -> y = 20 - 0.5*x
    x_b = np.linspace(0, 40, 200)
    y_b = 20.0 - 0.5 * x_b
    ax.plot(x_b, y_b, color=NAVY, lw=2.2, label=r"Budget Line: $20x + 40y = 800$")
    
    # Expansion path ray: x = 2y -> y = 0.5*x
    ax.plot(x, 0.5 * x, color=SLATE, lw=1.5, ls="--", label=r"Expansion Path: $MRS = \frac{p_x}{p_y} \Rightarrow x = 2y$")
    
    # Indifference curves: U = xy -> y = U / x
    u_vals = [(100, AMBER, "$U=100$ (suboptimal)", ":"),
              (200, GREEN, "$U^*=200$ (tangent optimum)", "-"),
              (320, BRICK, "$U=320$ (unaffordable)", ":")]
    
    for u, col, lbl, lstyle in u_vals:
        ax.plot(x, u / x, color=col, lw=2.0 if u==200 else 1.3, ls=lstyle, label=lbl)
    
    # Optimal tangency point
    ax.plot(20, 10, marker='o', markersize=8, color=GREEN, zorder=5)
    ax.annotate(r"$\mathbf{Optimal\ Bundle}$" + "\n" + r"$(x^*=20,\, y^*=10)$" + "\n" + r"$U^* = 200$",
                xy=(20, 10), xytext=(23.5, 4.2),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4),
                fontsize=9.0,
                bbox=dict(boxstyle="round,pad=0.3", fc="#f0fff4", ec=GREEN, alpha=0.9))
    
    # Dashed coordinate guides
    ax.plot([20, 20], [0, 10], color=GREEN, ls=":", lw=1.2)
    ax.plot([0, 20], [10, 10], color=GREEN, ls=":", lw=1.2)
    
    ax.set_xlim(0, 42)
    ax.set_ylim(0, 22)
    ax.set_xlabel(r"Food, $x$ (units)")
    ax.set_ylabel(r"Clothing, $y$ (units)")
    ax.set_title("Question 4: Consumer Optimization & Tangency Condition", pad=12)
    ax.legend(loc="upper right", framealpha=0.95, fontsize=8.8)
    
    save_fig(fig, "ps1_q4_consumer_opt.png")

# ==============================================================================
# Figure 6: Q6 Multi-Constraint Disaster Relief
# ==============================================================================
def make_q6_disaster_relief():
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    
    cW = np.linspace(0, 75, 400)
    
    # Budget: cF + 2*cW <= 120 -> cF = 120 - 2*cW
    cF_budget = 120.0 - 2.0 * cW
    # Transport: cF + cW <= 70 -> cF = 70 - cW
    cF_cargo = 70.0 - cW
    
    # Feasible polygon: (0,0) -> (60,0) -> (50,20) -> (0,70)
    poly_pts = [[0, 0], [60, 0], [50, 20], [0, 70]]
    poly = Polygon(poly_pts, closed=True, facecolor=FEASIBLE_FILL, edgecolor=FEASIBLE_EDGE,
                   lw=1.5, label="Feasible Region (Both Constraints Satisfied)")
    ax.add_patch(poly)
    
    # Plot boundary lines
    ax.plot(cW[cF_budget >= 0], cF_budget[cF_budget >= 0], color=BRICK, lw=2.0, ls="--",
            label=r"Financial Budget: $c_F + 2c_W = 120$")
    ax.plot(cW[cF_cargo >= 0], cF_cargo[cF_cargo >= 0], color=NAVY, lw=2.0, ls="-",
            label=r"Cargo Capacity: $c_F + c_W = 70$")
    
    # Indifference curve tangent to cargo capacity at (35, 35): U = 35*35 = 1225
    cW_ic = np.linspace(18, 70, 300)
    cF_ic = 1225.0 / cW_ic
    ax.plot(cW_ic, cF_ic, color=GREEN, lw=2.0, label=r"Indifference Curve: $U^* = c_W c_F = 1,225$")
    
    # Constrained optimum (35, 35)
    ax.plot(35, 35, marker='o', markersize=8, color=GREEN, zorder=6)
    ax.annotate(r"$\mathbf{Constrained\ Optimum}$" + "\n" + r"$(c_W^*=35,\, c_F^*=35)$" + "\n" +
                r"Cargo Binding ($\mu^*=35$)" + "\n" + r"Budget Slack: \$15K idle ($\lambda^*=0$)",
                xy=(35, 35), xytext=(42, 45),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.3),
                fontsize=8.8,
                bbox=dict(boxstyle="round,pad=0.3", fc="#f0fff4", ec=GREEN, alpha=0.9))
    
    # Kink vertex (50, 20)
    ax.plot(50, 20, marker='s', markersize=6, color=AMBER, zorder=5)
    ax.annotate(r"Kink Vertex:" + "\n" + r"$(50,\, 20)$", xy=(50, 20), xytext=(52, 26),
                fontsize=8.5, color=AMBER, fontweight='semibold')
    
    # Unconstrained budget optimum (30, 60) - infeasible!
    ax.plot(30, 60, marker='x', markersize=8, color=BRICK, mew=2, zorder=5)
    ax.annotate(r"Unconstrained Budget Optimum:" + "\n" + r"$(30,\, 60)$ [Weight = 90 > 70!]",
                xy=(30, 60), xytext=(8, 64),
                arrowprops=dict(arrowstyle="->", color=BRICK, lw=1.0),
                fontsize=8.0, color=BRICK)
    
    ax.set_xlim(0, 75)
    ax.set_ylim(0, 85)
    ax.set_xlabel(r"Clean Water, $c_W$ (tons)")
    ax.set_ylabel(r"High-Calorie Food, $c_F$ (tons)")
    ax.set_title("Question 6: Multi-Constraint Disaster Relief Feasible Region & Optimum", pad=12)
    ax.legend(loc="lower left", framealpha=0.95, fontsize=8.2)
    
    save_fig(fig, "ps1_q6_disaster_relief.png")

# ==============================================================================
# Figure 7: Bonus Comparative Statics of Cost Reduction
# ==============================================================================
def make_bonus_comparative_statics():
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    
    eA_vals = np.linspace(0, 20, 400)
    eB_vals = np.linspace(0, 20, 400)
    
    # Ana's BR: eA = 18 - 0.25*eB -> eB = 72 - 4*eA
    eB_Ana = np.linspace(0, 18, 200)
    eA_Ana = 18.0 - 0.25 * eB_Ana
    
    # Baseline Ben's BR: eB = 10 - 0.125*eA
    eB_Ben_base = 10.0 - 0.125 * eA_vals
    
    # Modified Ben's BR (cost halved): eB = 20 - 0.25*eA
    eB_Ben_mod = 20.0 - 0.25 * eA_vals
    
    ax.plot(eA_Ana, eB_Ana, color=TEAL, lw=2.2, label=r"Ana's BR: $e_A = 18 - \frac{1}{4}e_B$ (unchanged)")
    ax.plot(eA_vals, eB_Ben_base, color=BRICK, lw=1.8, ls="--", label=r"Ben's Baseline BR: $e_B = 10 - \frac{1}{8}e_A$")
    ax.plot(eA_vals, eB_Ben_mod, color=PURPLE, lw=2.2, label=r"Ben's BR with Halved MC: $e_B = 20 - \frac{1}{4}e_A$")
    
    # Baseline Nash (16, 8)
    ax.plot(16.0, 8.0, marker='o', markersize=7, color=BRICK, zorder=5)
    ax.annotate(r"Baseline Nash:" + "\n" + r"$(16.00,\, 8.00)$", xy=(16.0, 8.0), xytext=(12.0, 4.5),
                arrowprops=dict(arrowstyle="->", color=BRICK),
                fontsize=8.8, color=BRICK)
    
    # New Nash (13.87, 16.53)
    ax.plot(13.87, 16.53, marker='o', markersize=8, color=PURPLE, zorder=5)
    ax.annotate(r"New Nash:" + "\n" + r"$(13.87,\, 16.53)$" + "\n" + "Ben expands, Ana contracts!",
                xy=(13.87, 16.53), xytext=(4.0, 15.5),
                arrowprops=dict(arrowstyle="->", color=PURPLE, lw=1.2),
                fontsize=8.8, color=PURPLE,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=PURPLE, alpha=0.9))
    
    # Arrow connecting equilibria
    ax.annotate("", xy=(14.0, 16.0), xytext=(15.8, 8.5),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=2.0, ls="-"))
    
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 22)
    ax.set_xlabel(r"Ana's Effort, $e_A$ (hours/day)")
    ax.set_ylabel(r"Ben's Effort, $e_B$ (hours/day)")
    ax.set_title("Bonus: Comparative Statics (Ben's Marginal Cost Halved)", pad=12)
    ax.legend(loc="lower left", framealpha=0.95, fontsize=8.5)
    
    save_fig(fig, "ps1_bonus_comparative_statics.png")

if __name__ == "__main__":
    print("Generating PS1 solution figures...")
    make_q1_best_responses()
    make_q1_payoff_space()
    make_q2_soc_profit()
    make_q3_budget_sets()
    make_q4_consumer_opt()
    make_q6_disaster_relief()
    make_bonus_comparative_statics()
    print("All figures successfully generated in", FIG_DIR)
