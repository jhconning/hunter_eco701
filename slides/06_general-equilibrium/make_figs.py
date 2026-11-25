"""
Generate 4 publication-grade PNG figures for ECO 701 Lecture 06 (General Equilibrium).
Palette matches the ECO 701 Quarto Reveal.js theme:
  - Background: #fdfdfb
  - Navy (primary): #24325c
  - Amber (accent): #b8842a
  - Terracotta / Rust: #a04434
  - Forest Green: #2d6a4f
  - Slate / Muted: #5a6578
  - Gridlines: #e5e9f0
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ---------------------------------------------------------------------------
# Global style & palette
# ---------------------------------------------------------------------------
BG = "#fdfdfb"
NAVY = "#24325c"
AMBER = "#b8842a"
RUST = "#a04434"
GREEN = "#2d6a4f"
SLATE = "#5a6578"
GRID = "#e5e9f0"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "savefig.dpi": 220,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "mathtext.fontset": "cm",
    "axes.edgecolor": NAVY,
    "axes.linewidth": 1.0,
    "axes.labelcolor": NAVY,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "text.color": NAVY,
    "axes.titlesize": 11.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 10.5,
    "xtick.labelsize": 8.8,
    "ytick.labelsize": 8.8,
    "legend.fontsize": 8.5,
})

OUT_DIR = r"Y:\Hunter\eco701\slides\06_general-equilibrium\figs"
os.makedirs(OUT_DIR, exist_ok=True)


def style_axes_clean(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(NAVY)
    ax.spines["bottom"].set_color(NAVY)
    ax.tick_params(colors=SLATE, length=3.5)


# ===========================================================================
# FIGURE 1: Trade & Stolper-Samuelson (Skilled H vs. Non-College L)
# ===========================================================================
def make_fig_stolper_samuelson():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.6))
    fig.subplots_adjust(left=0.065, right=0.95, bottom=0.14, top=0.88, wspace=0.28)

    # Technology: x = L_x^0.25 H_x^0.75 (Skill-intensive goods/services, alpha=0.75)
    #             y = L_y^0.75 H_y^0.25 (Labor-intensive manufactures, beta=0.25)
    # Total L = 100, H = 100.
    # Contract curve: h_x = 9 * l_x / (1 + 8 * l_x)
    l_grid = np.linspace(0.0, 1.0, 600)
    h_grid = 9.0 * l_grid / (1.0 + 8.0 * l_grid)

    def outputs(l_val):
        h_val = 9.0 * l_val / (1.0 + 8.0 * l_val)
        x = 100.0 * (l_val ** 0.25) * (h_val ** 0.75)
        y = 100.0 * ((1.0 - l_val) ** 0.75) * ((1.0 - h_val) ** 0.25)
        return x, y, h_val

    def rpt_at(l_val, eps=1e-5):
        x1, y1, _ = outputs(l_val - eps)
        x2, y2, _ = outputs(l_val + eps)
        return -(y2 - y1) / (x2 - x1)

    x_ppf, y_ppf, _ = outputs(l_grid)

    # Autarky E (skill-abundant country: cheap skill-intensive x, flatter autarky price)
    # Free trade A (higher world p_x/p_y, steeper price line, expands x)
    l_E = 0.14
    x_E, y_E, h_E = outputs(l_E)
    p_E = rpt_at(l_E)

    l_A = 0.45
    x_A, y_A, h_A = outputs(l_A)
    p_A = rpt_at(l_A)

    # Community utility U = x^gamma y^(1-gamma) tangent at E
    ratio_g = p_E * x_E / y_E
    gamma = ratio_g / (1.0 + ratio_g)
    U1 = (x_E ** gamma) * (y_E ** (1.0 - gamma))

    # Free trade consumption B maximizing U subject to p_A * x + y = p_A * x_A + y_A
    M_prime = p_A * x_A + y_A
    x_B = gamma * M_prime / p_A
    y_B = (1.0 - gamma) * M_prime
    U2 = (x_B ** gamma) * (y_B ** (1.0 - gamma))

    # ---------------- Left Panel: PPF & Trade ----------------
    ax1.plot(x_ppf, y_ppf, color=NAVY, lw=2.3)
    ax1.fill_between(x_ppf, 0, y_ppf, color=NAVY, alpha=0.035)

    # Domestic autarky price line through E
    x_dom = np.linspace(4, 108, 100)
    y_dom = y_E - p_E * (x_dom - x_E)
    mask_d = (y_dom >= 5) & (y_dom <= 108)
    ax1.plot(x_dom[mask_d], y_dom[mask_d], color=RUST, lw=1.45, ls="--", zorder=3)

    # World price line through A and B
    x_wld = np.linspace(20, 108, 120)
    y_wld = y_A - p_A * (x_wld - x_A)
    mask_w = (y_wld >= 5) & (y_wld <= 108)
    ax1.plot(x_wld[mask_w], y_wld[mask_w], color=GREEN, lw=1.55, ls="--", zorder=3)

    # Community ICs U1 (at E) and U2 (at B)
    x_ic1 = np.linspace(14, 106, 200)
    y_ic1 = (U1 / (x_ic1 ** gamma)) ** (1.0 / (1.0 - gamma))
    m1 = y_ic1 <= 106
    ax1.plot(x_ic1[m1], y_ic1[m1], color=SLATE, lw=1.4, alpha=0.85)

    x_ic2 = np.linspace(22, 108, 200)
    y_ic2 = (U2 / (x_ic2 ** gamma)) ** (1.0 / (1.0 - gamma))
    m2 = y_ic2 <= 106
    ax1.plot(x_ic2[m2], y_ic2[m2], color=AMBER, lw=1.85)

    # Trade triangle (A -> B: exports of x, imports of y)
    ax1.annotate("", xy=(x_B + 0.8, y_A), xytext=(x_A - 1.2, y_A),
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4, mutation_scale=11))
    ax1.annotate("", xy=(x_B, y_B - 1.5), xytext=(x_B, y_A + 0.8),
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4, mutation_scale=11))

    ax1.text(0.5 * (x_A + x_B), y_A - 3.5, "Skill-int.\nexports", color=GREEN,
             fontsize=8.2, ha="center", va="top", fontweight="bold")
    ax1.text(x_B - 3.0, 0.5 * (y_A + y_B), "Labor-int.\nimports", color=GREEN,
             fontsize=8.2, ha="right", va="center", fontweight="bold")

    # Curved production shift arrow E -> A along PPF
    arrow_ea = FancyArrowPatch((x_E + 5, y_E - 3), (x_A - 4, y_A + 5),
                               connectionstyle="arc3,rad=-0.18",
                               arrowstyle="->", mutation_scale=12,
                               color=RUST, lw=1.5, zorder=4)
    ax1.add_patch(arrow_ea)

    # Key points with non-overlapping labels
    ax1.scatter([x_E], [y_E], s=50, color=RUST, edgecolor=BG, linewidth=1.0, zorder=6)
    ax1.scatter([x_A], [y_A], s=50, color=GREEN, edgecolor=BG, linewidth=1.0, zorder=6)
    ax1.scatter([x_B], [y_B], s=50, color=AMBER, edgecolor=BG, linewidth=1.0, zorder=6)

    ax1.annotate("$E$ (Autarky)", xy=(x_E + 1.2, y_E + 1.2), xytext=(x_E + 16, y_E + 16),
                 color=RUST, fontsize=8.8, fontweight="bold", ha="left", va="bottom",
                 arrowprops=dict(arrowstyle="-", color=RUST, lw=0.9, alpha=0.8),
                 bbox=dict(boxstyle="round,pad=0.12", facecolor=BG, edgecolor="none", alpha=0.85))
    ax1.text(x_A + 3.5, y_A + 2.0, "$A$ (Prod.)", color=GREEN, fontsize=8.8, fontweight="bold", va="center")
    ax1.text(x_B + 1.5, y_B + 5.5, "$B$ (Cons.)", color=AMBER, fontsize=8.8, fontweight="bold", ha="left", va="bottom")

    # Slope & IC labels in open whitespace
    ax1.text(98, y_E - p_E * (98 - x_E) + 4.0, r"$-p_x^*/p_y^*$", color=RUST, fontsize=8.8, ha="center")
    ax1.text(x_A + 16, y_A - p_A * 16 + 1.5, r"$-p_x'/p_y'$", color=GREEN, fontsize=8.8, ha="left")
    ax1.text(98, (U1 / (98 ** gamma)) ** (1.0 / (1.0 - gamma)) - 4.5, "$U_1$", color=SLATE, fontsize=9.2, fontweight="bold")
    ax1.text(98, (U2 / (98 ** gamma)) ** (1.0 / (1.0 - gamma)) + 3.5, "$U_2$", color=AMBER, fontsize=9.2, fontweight="bold")

    ax1.set_xlim(0, 118)
    ax1.set_ylim(0, 112)
    ax1.set_xlabel("Skill-Intensive Output ($x$)")
    ax1.set_ylabel("Labor-Intensive Output ($y$)")
    ax1.set_title("North–South Trade: Output Shift", pad=8)
    style_axes_clean(ax1)
    ax1.grid(True, color=GRID, lw=0.6, alpha=0.8)

    # ---------------- Right Panel: Production Edgeworth Box ----------------
    L_tot, H_tot = 100.0, 100.0
    ax2.plot([0, L_tot, L_tot, 0, 0], [0, 0, H_tot, H_tot, 0], color=NAVY, lw=1.2)
    ax2.plot([0, L_tot], [0, H_tot], color=GRID, lw=1.1, ls=":")
    ax2.plot(l_grid * L_tot, h_grid * H_tot, color=NAVY, lw=2.3, zorder=3)

    Lx_E, Hx_E = l_E * L_tot, h_E * H_tot
    Lx_A, Hx_A = l_A * L_tot, h_A * H_tot

    # Rays from O_x (0,0) and O_y (100,100)
    ax2.plot([0, Lx_E], [0, Hx_E], color=RUST, lw=1.35, ls="--", zorder=2)
    ax2.plot([0, Lx_A], [0, Hx_A], color=GREEN, lw=1.35, ls="--", zorder=2)
    ax2.plot([L_tot, Lx_E], [H_tot, Hx_E], color=RUST, lw=1.35, ls="--", zorder=2)
    ax2.plot([L_tot, Lx_A], [H_tot, Hx_A], color=GREEN, lw=1.35, ls="--", zorder=2)

    # Arrow along contract curve from E to A
    arrow_box = FancyArrowPatch((Lx_E + 3.5, Hx_E + 4.5), (Lx_A - 4.0, Hx_A - 1.5),
                                connectionstyle="arc3,rad=-0.14",
                                arrowstyle="->", mutation_scale=13,
                                color=AMBER, lw=1.9, zorder=5)
    ax2.add_patch(arrow_box)

    # Points E and A
    ax2.scatter([Lx_E], [Hx_E], s=52, color=RUST, edgecolor=BG, linewidth=1.0, zorder=6)
    ax2.scatter([Lx_A], [Hx_A], s=52, color=GREEN, edgecolor=BG, linewidth=1.0, zorder=6)
    ax2.text(Lx_E + 3.0, Hx_E - 5.5, "$E$", color=RUST, fontsize=10.5, fontweight="bold")
    ax2.text(Lx_A + 3.0, Hx_A - 5.5, "$A$", color=GREEN, fontsize=10.5, fontweight="bold")

    # Ray slope annotations cleanly offset from lines
    ax2.text(23, 41, r"$(H/L)_x \downarrow$", color=GREEN, fontsize=8.8, fontweight="bold",
             rotation=62, ha="center", va="center",
             bbox=dict(boxstyle="round,pad=0.12", facecolor=BG, edgecolor="none", alpha=0.8))
    ax2.text(72, 91, r"$(H/L)_y \downarrow$", color=GREEN, fontsize=8.8, fontweight="bold",
             rotation=13, ha="center", va="center")

    # Origin labels
    ax2.text(-3, -5, "$O_x$", color=NAVY, fontsize=10, fontweight="bold", ha="right", va="top")
    ax2.text(103, 104, "$O_y$", color=NAVY, fontsize=10, fontweight="bold", ha="left", va="bottom")

    # Stolper-Samuelson takeaway callout box
    ax2.text(
        96, 8,
        "$H/L \\downarrow$ in both sectors\n$\\Rightarrow$ skilled wage $w_H \\uparrow$, non-college $w_L \\downarrow$",
        fontsize=8.6, color=NAVY, ha="right", va="bottom",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#f7f4eb", edgecolor=AMBER, lw=1.1)
    )

    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.set_xlabel("Non-college labor ($L_x$ from $O_x$)")
    ax2.set_ylabel("College labor ($H_x$ from $O_x$)")
    ax2.set_title("Production Box: Stolper–Samuelson", pad=12)
    ax2.spines["top"].set_color(NAVY)
    ax2.spines["right"].set_color(NAVY)
    ax2.set_xticks([0, 25, 50, 75, 100])
    ax2.set_yticks([0, 25, 50, 75, 100])

    out_path = os.path.join(OUT_DIR, "fig_stolper_samuelson.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 2: Ana & Ben Exact Edgeworth Box (PS3 Q2-Q3)
# ===========================================================================
def make_fig_ana_ben_box():
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    fig.subplots_adjust(left=0.09, right=0.88, bottom=0.14, top=0.86)

    C1_MAX, C2_MAX = 100.0, 120.0

    # Grid for lens shading
    c1_g = np.linspace(0.5, C1_MAX - 0.5, 400)
    c2_g = np.linspace(0.5, C2_MAX - 0.5, 400)
    C1, C2 = np.meshgrid(c1_g, c2_g)

    # Initial endowment E = (20, 96) for Ana, (80, 24) for Ben
    E = (20.0, 96.0)
    U_A_E = E[0] * E[1]  # 1920
    U_B_E = (C1_MAX - E[0]) * (C2_MAX - E[1])  # 1920

    lens_mask = (C1 * C2 >= U_A_E) & ((C1_MAX - C1) * (C2_MAX - C2) >= U_B_E)
    ax.contourf(C1, C2, lens_mask.astype(float), levels=[0.5, 1.5],
                colors=[AMBER], alpha=0.14, zorder=1)

    # Indifference curves through E
    c1_a = np.linspace(U_A_E / C2_MAX, C1_MAX, 300)
    ax.plot(c1_a, U_A_E / c1_a, color=SLATE, lw=1.2, ls=":", zorder=2)

    c1_b = np.linspace(0.0, C1_MAX - U_B_E / C2_MAX, 300)
    c2_b = C2_MAX - U_B_E / (C1_MAX - c1_b)
    ax.plot(c1_b, c2_b, color=SLATE, lw=1.2, ls=":", zorder=2)

    # Contract curve: c2^A = 1.2 c1^A
    ax.plot([0, C1_MAX], [0, C2_MAX], color=NAVY, lw=2.2, label="Contract curve ($c_2^A = 1.2\\,c_1^A$)", zorder=3)

    # Walrasian equilibrium E* = (50, 60), budget line c2 = 120 - 1.2 c1
    E_star = (50.0, 60.0)
    ax.plot([0, 100], [120, 0], color=GREEN, lw=1.8, label="Budget line ($r^* = 20\\%$)", zorder=4)

    # Tangent ICs through E* (U = 3000)
    U_star = 50.0 * 60.0
    c1_as = np.linspace(U_star / C2_MAX, C1_MAX, 300)
    ax.plot(c1_as, U_star / c1_as, color=NAVY, lw=1.35, alpha=0.72, zorder=3)

    c1_bs = np.linspace(0.0, C1_MAX - U_star / C2_MAX, 300)
    ax.plot(c1_bs, C2_MAX - U_star / (C1_MAX - c1_bs), color=NAVY, lw=1.35, alpha=0.72, zorder=3)

    # Second Welfare Theorem redistribution: E' = (10, 96), parallel budget line c2 = 108 - 1.2 c1, E** = (45, 54)
    E_prime = (10.0, 96.0)
    E_dstar = (45.0, 54.0)
    ax.plot([0, 90], [108, 0], color=RUST, lw=1.6, ls="--",
            label="Post-transfer budget (same $r^*=20\\%$)", zorder=4)

    # Clean dashed transfer arrow E -> E'
    transfer_arrow = FancyArrowPatch((E[0] - 1.3, E[1]), (E_prime[0] + 1.3, E_prime[1]),
                                     arrowstyle="->", mutation_scale=12,
                                     color=RUST, lw=1.8, ls="--", zorder=6)
    ax.add_patch(transfer_arrow)
    ax.text(15.0, 104.5, "$-10$ transfer", color=RUST, fontsize=8.4, ha="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.14", facecolor=BG, edgecolor="none", alpha=0.88))

    # Key points
    pts = [
        (E, AMBER, "$E=(20,96)$", 3.0, 3.0, "left"),
        (E_prime, RUST, "$E'=(10,96)$", -1.5, -10.5, "left"),
        (E_star, GREEN, "$E^*=(50,60)$", 3.5, 5.5, "left"),
        (E_dstar, RUST, "$E^{**}=(45,54)$", -3.0, -9.5, "right"),
    ]
    for (px, py), col, lbl, dx, dy, ha in pts:
        ax.scatter([px], [py], s=55, color=col, edgecolor=BG, linewidth=1.1, zorder=7)
        ax.text(px + dx, py + dy, lbl, color=col, fontsize=9.0, fontweight="bold", ha=ha, va="center",
                bbox=dict(boxstyle="round,pad=0.16", facecolor=BG, edgecolor="none", alpha=0.86))

    # Label Pareto lens in open shaded area
    ax.text(65.5, 52.0, "Pareto-improving\nlens", color="#8a5f14", fontsize=8.3,
            fontweight="bold", ha="center", va="center")

    # Top and right axes for Ben
    ax_top = ax.twiny()
    ax_top.set_xlim(C1_MAX, 0)
    ax_top.set_xlabel("Ben's Date-1 Consumption ($c_1^B$)", labelpad=6)
    ax_top.tick_params(colors=SLATE, length=3.5)

    ax_right = ax.twinx()
    ax_right.set_ylim(C2_MAX, 0)
    ax_right.set_ylabel("Ben's Date-2 Consumption ($c_2^B$)", labelpad=8)
    ax_right.tick_params(colors=SLATE, length=3.5)

    ax.set_xlim(0, C1_MAX)
    ax.set_ylim(0, C2_MAX)
    ax.set_xlabel("Ana's Date-1 Consumption ($c_1^A$)")
    ax.set_ylabel("Ana's Date-2 Consumption ($c_2^A$)")
    ax.set_title("Ana & Ben Intertemporal Edgeworth Box (PS3 Q2–Q3)", pad=26)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.8)

    # Origin labels
    ax.text(-2.0, -4.5, "$O_A$", color=NAVY, fontsize=9.5, fontweight="bold", ha="right", va="top")
    ax.text(102.0, 124.5, "$O_B$", color=NAVY, fontsize=9.5, fontweight="bold", ha="left", va="bottom")

    ax.legend(loc="lower right", frameon=True, facecolor=BG, edgecolor=GRID, framealpha=0.96)

    out_path = os.path.join(OUT_DIR, "fig_ana_ben_box.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 3: Edgeworth Box + Utility Possibilities Frontier & SWFs
# ===========================================================================
def make_fig_upf_swf():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.5))
    fig.subplots_adjust(left=0.065, right=0.96, bottom=0.14, top=0.88, wspace=0.26)

    X_TOT, Y_TOT = 10.0, 15.0

    def uA(x, y):
        return (x * y) ** 0.25

    def uB(x, y):
        return ((X_TOT - x) * (Y_TOT - y)) ** 0.25

    z = (9.0, 1.0)
    uA_z = uA(*z)
    uB_z = uB(*z)

    x_tB = np.sqrt((z[0] * z[1]) / 1.5)
    y_tB = 1.5 * x_tB
    x_i, y_i = 5.0, 7.5
    x_tA = X_TOT - np.sqrt(((X_TOT - z[0]) * (Y_TOT - z[1])) / 1.5)
    y_tA = 1.5 * x_tA

    uA_tB, uB_tB = uA(x_tB, y_tB), uB(x_tB, y_tB)
    uA_i, uB_i = uA(x_i, y_i), uB(x_i, y_i)
    uA_tA, uB_tA = uA(x_tA, y_tA), uB(x_tA, y_tA)

    # ---------------- Left Panel: Exchange Box ----------------
    xg = np.linspace(0.05, X_TOT - 0.05, 350)
    yg = np.linspace(0.05, Y_TOT - 0.05, 350)
    XG, YG = np.meshgrid(xg, yg)
    lens = (XG * YG >= z[0] * z[1]) & ((X_TOT - XG) * (Y_TOT - YG) >= (X_TOT - z[0]) * (Y_TOT - z[1]))
    ax1.contourf(XG, YG, lens.astype(float), levels=[0.5, 1.5], colors=[AMBER], alpha=0.16, zorder=1)

    xa_ic = np.linspace(9.0 / Y_TOT, X_TOT, 250)
    ax1.plot(xa_ic, 9.0 / xa_ic, color=SLATE, lw=1.3, ls="--", zorder=2)
    xb_ic = np.linspace(0.0, X_TOT - 14.0 / Y_TOT, 250)
    ax1.plot(xb_ic, Y_TOT - 14.0 / (X_TOT - xb_ic), color=SLATE, lw=1.3, ls="--", zorder=2)

    ax1.plot([0, X_TOT], [0, Y_TOT], color=SLATE, lw=1.2, alpha=0.45, zorder=2)
    ax1.plot([x_tB, x_tA], [y_tB, y_tA], color=NAVY, lw=2.8, zorder=4)
    ax1.plot([0, X_TOT, X_TOT, 0, 0], [0, 0, Y_TOT, Y_TOT, 0], color=NAVY, lw=1.1)

    for pt, col, lbl, dx, dy, ha in [
        (z, RUST, "$z=(9,1)$", -0.35, 0.95, "right"),
        ((x_tB, y_tB), NAVY, "$t_B$", -0.55, 0.25, "right"),
        ((x_i, y_i), AMBER, "$i$", -0.45, 0.75, "right"),
        ((x_tA, y_tA), NAVY, "$t_A$", -0.55, 0.85, "right"),
    ]:
        ax1.scatter(*pt, s=50, color=col, edgecolor=BG, linewidth=1.0, zorder=6)
        ax1.text(pt[0] + dx, pt[1] + dy, lbl, color=col, fontsize=9.5, fontweight="bold", ha=ha)

    ax1.text(6.6, 5.4, "Pareto-improving\nlens", color="#8a5f14", fontsize=8.3, fontweight="bold", ha="center")
    ax1.text(-0.3, -0.7, "$O_A$", color=NAVY, fontsize=9.5, fontweight="bold", ha="right", va="top")
    ax1.text(10.3, 15.5, "$O_B$", color=NAVY, fontsize=9.5, fontweight="bold", ha="left", va="bottom")

    ax1.set_xlim(0, X_TOT)
    ax1.set_ylim(0, Y_TOT)
    ax1.set_xlabel("Good $x$ (Ana)")
    ax1.set_ylabel("Good $y$ (Ana)")
    ax1.set_title("Exchange Box & Core ($X=10, Y=15$)", pad=10)
    ax1.spines["top"].set_color(NAVY)
    ax1.spines["right"].set_color(NAVY)

    # ---------------- Right Panel: UPF & Social Welfare Functions ----------------
    R = (X_TOT * Y_TOT) ** 0.25
    theta = np.linspace(0, np.pi / 2, 400)
    uA_upf = R * np.cos(theta)
    uB_upf = R * np.sin(theta)

    ax2.fill_between(uA_upf, 0, uB_upf, color=NAVY, alpha=0.045, zorder=1)
    ax2.plot(uA_upf, uB_upf, color=NAVY, lw=2.3, zorder=3, label="UPF")

    mask_core = (uA_upf >= uA_z) & (uB_upf >= uB_z)
    ax2.fill_between(uA_upf[mask_core], uB_z, uB_upf[mask_core], color=AMBER, alpha=0.22, zorder=2)

    # Participation constraint lines
    ax2.plot([uA_z, uA_z], [uB_z, uB_tB], color=RUST, lw=1.25, ls=":", zorder=3)
    ax2.plot([uA_z, uA_tA], [uB_z, uB_z], color=RUST, lw=1.25, ls=":", zorder=3)
    ax2.plot([uA_z, uA_z], [0, uB_z], color=GRID, lw=1.0, ls=":")
    ax2.plot([0, uA_z], [uB_z, uB_z], color=GRID, lw=1.0, ls=":")

    # Three contrasting SWF contours touching at i
    u_sum = uA_i + uB_i
    ua_util = np.linspace(1.15, 3.85, 100)
    ax2.plot(ua_util, u_sum - ua_util, color=SLATE, lw=1.45, ls="--", zorder=4, label="Utilitarian ($u_A+u_B$)")

    u_prod = uA_i * uB_i
    ua_cd = np.linspace(1.55, 3.95, 200)
    ub_cd = u_prod / ua_cd
    m_cd = ub_cd <= 3.95
    ax2.plot(ua_cd[m_cd], ub_cd[m_cd], color=AMBER, lw=1.8, zorder=4, label="Cobb–Douglas ($u_A u_B$)")

    ax2.plot([uA_i, uA_i, 3.95], [3.95, uB_i, uB_i], color=GREEN, lw=1.8, zorder=4, label="Rawlsian ($\\min(u_A,u_B)$)")

    # Points z, t_B, i, t_A with clean non-overlapping positions
    for pt, col, lbl, dx, dy, ha in [
        ((uA_z, uB_z), RUST, "$z$", -0.10, -0.18, "right"),
        ((uA_tB, uB_tB), NAVY, "$t_B$", -0.16, 0.14, "right"),
        ((uA_i, uB_i), AMBER, "$i$", 0.14, 0.14, "left"),
        ((uA_tA, uB_tA), NAVY, "$t_A$", 0.15, -0.14, "left"),
    ]:
        ax2.scatter(*pt, s=50, color=col, edgecolor=BG, linewidth=1.0, zorder=7)
        ax2.text(pt[0] + dx, pt[1] + dy, lbl, color=col, fontsize=9.5, fontweight="bold", ha=ha)

    ax2.text(2.14, 2.25, "Bargaining\nset (Core)", color="#8a5f14", fontsize=8.0, fontweight="bold", ha="center", va="center")
    ax2.text(uA_z, 0.15, "$u_A^z$", color=RUST, fontsize=8.8, ha="center")
    ax2.text(0.14, uB_z, "$u_B^z$", color=RUST, fontsize=8.8, va="center")

    ax2.set_xlim(0, 4.0)
    ax2.set_ylim(0, 4.0)
    ax2.set_xlabel("Ana's Utility ($u_A$)")
    ax2.set_ylabel("Ben's Utility ($u_B$)")
    ax2.set_title("Utility Possibilities Frontier & SWFs", pad=10)
    style_axes_clean(ax2)
    ax2.grid(True, color=GRID, lw=0.6, alpha=0.8)
    ax2.legend(loc="lower left", frameon=True, facecolor=BG, edgecolor=GRID, framealpha=0.95, fontsize=7.8)

    out_path = os.path.join(OUT_DIR, "fig_upf_swf.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 4: Exchange Edgeworth Box Nested Inside PPF (NS Fig. 13.10)
# ===========================================================================
def make_fig_nested_ppf_box():
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    fig.subplots_adjust(left=0.10, right=0.95, bottom=0.13, top=0.90)

    # Concave PPF: (X/100)^2 + (Y/85)^2 = 1
    X_MAX, Y_MAX = 100.0, 85.0
    x_ppf = np.linspace(0, X_MAX, 400)
    y_ppf = Y_MAX * np.sqrt(np.maximum(0.0, 1.0 - (x_ppf / X_MAX) ** 2))

    # Efficient output point A = (X*, Y*)
    X_star = 70.0
    Y_star = Y_MAX * np.sqrt(1.0 - (X_star / X_MAX) ** 2)
    rpt = (Y_MAX ** 2 / X_MAX ** 2) * (X_star / Y_star)

    # Inside the Exchange Box [0, X*] x [0, Y*]:
    aA, aB = 0.40, 0.60
    k = ((aB / (1.0 - aB)) / (aA / (1.0 - aA)))
    s_grid = np.linspace(0, 1, 300)
    x_cc = s_grid * X_star
    y_cc = (k * s_grid / (1.0 + (k - 1.0) * s_grid)) * Y_star

    # Exact allocation C* where MRS^A = MRS^B = RPT
    rhs = (Y_star / X_star) * (aB / (1.0 - aB)) / rpt
    s_star = (rhs - 1.0) / (k - 1.0)
    x_c = s_star * X_star
    y_c = (k * s_star / (1.0 + (k - 1.0) * s_star)) * Y_star

    # Plot PPF
    ax.plot(x_ppf, y_ppf, color=NAVY, lw=2.4, zorder=3)
    ax.fill_between(x_ppf, 0, y_ppf, color=NAVY, alpha=0.03, zorder=1)

    # Nested Exchange Edgeworth Box
    ax.add_patch(plt.Rectangle((0, 0), X_star, Y_star, facecolor="#f8f5ec",
                               edgecolor=NAVY, lw=1.4, zorder=2))

    # Contract curve inside box
    ax.plot(x_cc, y_cc, color=AMBER, lw=2.0, zorder=4)

    # Indifference curves through C*
    uA_c = (x_c ** aA) * (y_c ** (1.0 - aA))
    uB_c = ((X_star - x_c) ** aB) * ((Y_star - y_c) ** (1.0 - aB))

    xa_rng = np.linspace(max(3.5, x_c - 18), min(X_star - 3, x_c + 24), 200)
    ya_ic = (uA_c / (xa_rng ** aA)) ** (1.0 / (1.0 - aA))
    ma = (ya_ic >= 2.0) & (ya_ic <= Y_star - 1.5)
    ax.plot(xa_rng[ma], ya_ic[ma], color=NAVY, lw=1.45, zorder=4)

    xb_rng = np.linspace(max(3.0, x_c - 22), min(X_star - 3.5, x_c + 22), 200)
    yb_ic = Y_star - (uB_c / ((X_star - xb_rng) ** aB)) ** (1.0 / (1.0 - aB))
    mb = (yb_ic >= 2.0) & (yb_ic <= Y_star - 1.5)
    ax.plot(xb_rng[mb], yb_ic[mb], color=RUST, lw=1.45, zorder=4)

    # Tangent price line at A (slope = -RPT = -p_x*/p_y*)
    x_tanA = np.linspace(X_star - 17, min(106, X_star + 26), 100)
    y_tanA = Y_star - rpt * (x_tanA - X_star)
    m_tA = (y_tanA >= 0) & (y_tanA <= 92)
    ax.plot(x_tanA[m_tA], y_tanA[m_tA], color=GREEN, lw=1.7, ls="--", zorder=5)

    # Parallel price line through C* (exact same slope = -p_x*/p_y*)
    x_tanC = np.linspace(max(2, x_c - 20), min(X_star - 2, x_c + 24), 100)
    y_tanC = y_c - rpt * (x_tanC - x_c)
    m_tC = (y_tanC >= 2) & (y_tanC <= Y_star - 2)
    ax.plot(x_tanC[m_tC], y_tanC[m_tC], color=GREEN, lw=1.7, ls="--", zorder=5)

    # Points A and C*
    ax.scatter([X_star], [Y_star], s=58, color=NAVY, edgecolor=BG, linewidth=1.1, zorder=7)
    ax.scatter([x_c], [y_c], s=58, color=GREEN, edgecolor=BG, linewidth=1.1, zorder=7)

    # Annotations
    ax.text(X_star + 2.5, Y_star + 3.5, "$A = (X^*, Y^*) = O_B$", color=NAVY,
            fontsize=9.3, fontweight="bold", va="bottom")
    ax.text(x_c + 2.5, y_c + 3.0, "$C^*$", color=GREEN, fontsize=10.5, fontweight="bold")
    ax.text(-2.0, -3.5, "$O_A$", color=NAVY, fontsize=10.0, fontweight="bold", ha="right", va="top")

    # IC & slope labels in clear open spaces
    ax.text(x_c + 20, ya_ic[ma][-1] + 2.5, "$U_A^*$", color=NAVY, fontsize=9.2, fontweight="bold")
    ax.text(x_c - 17, yb_ic[mb][0] - 4.5, "$U_B^*$", color=RUST, fontsize=9.2, fontweight="bold")
    ax.text(X_star + 15, Y_star - rpt * 15 + 4.5, "slope $= -RPT$\n$= -p_x^*/p_y^*$",
            color=GREEN, fontsize=8.5, ha="left")
    ax.text(x_c + 20, y_c - rpt * 20 - 5.5, "parallel:\n$-p_x^*/p_y^*$",
            color=GREEN, fontsize=8.3, ha="center", va="top")

    # Efficiency condition callout cleanly separated from tangent line
    ax.text(
        34, 87,
        "$MRS^A = MRS^B = \\dfrac{p_x^*}{p_y^*} = RPT$",
        fontsize=9.8, color=NAVY, ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#f7f4eb", edgecolor=AMBER, lw=1.2)
    )

    ax.set_xticks([0, X_star, X_MAX])
    ax.set_xticklabels(["0", "$X^*$", "100"])
    ax.set_yticks([0, Y_star, Y_MAX])
    ax.set_yticklabels(["0", "$Y^*$", "85"])

    ax.set_xlim(0, 108)
    ax.set_ylim(0, 95)
    ax.set_xlabel("Total Output of Good $X$")
    ax.set_ylabel("Total Output of Good $Y$")
    ax.set_title("General Equilibrium: Production & Exchange Efficiency", pad=10)
    style_axes_clean(ax)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.7)

    out_path = os.path.join(OUT_DIR, "fig_nested_ppf_box.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 5: Plain-Vanilla Exchange Edgeworth Box (goods 1 & 2, prices p1, p2)
# ===========================================================================
def make_fig_exchange_vanilla():
    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    fig.subplots_adjust(left=0.10, right=0.89, bottom=0.13, top=0.85)

    X1, X2 = 10.0, 10.0
    aA, aB = 0.6, 0.4
    e1, e2 = 2.0, 8.0          # Endowment E for A; B gets (8, 2)
    eq1, eq2 = 6.0, 4.0        # Walrasian equilibrium E* at p1/p2 = 1

    uA_E = (e1 ** aA) * (e2 ** (1 - aA))
    uB_E = ((X1 - e1) ** aB) * ((X2 - e2) ** (1 - aB))
    uA_S = (eq1 ** aA) * (eq2 ** (1 - aA))
    uB_S = ((X1 - eq1) ** aB) * ((X2 - eq2) ** (1 - aB))

    # Contract curve: x2A = 8 * x1A / (18 - x1A)
    x_cc = np.linspace(0.0, X1, 400)
    y_cc = 8.0 * x_cc / (18.0 - x_cc)

    # Indifference curves through E (for Pareto-improving lens)
    x_grid = np.linspace(0.3, 9.7, 600)
    icA_E = (uA_E / (x_grid ** aA)) ** (1.0 / (1.0 - aA))
    icB_E = X2 - (uB_E / ((X1 - x_grid) ** aB)) ** (1.0 / (1.0 - aB))

    # Shade Pareto-improving lens (where icB_E > icA_E and inside [0, X2])
    lens_mask = (icB_E >= icA_E) & (icA_E >= 0) & (icB_E <= X2)
    ax.fill_between(x_grid[lens_mask], icA_E[lens_mask], icB_E[lens_mask],
                    color=AMBER, alpha=0.16, zorder=1)

    # Plot endowment ICs (dashed slate)
    mA_E = (icA_E >= 0.0) & (icA_E <= X2)
    mB_E = (icB_E >= 0.0) & (icB_E <= X2)
    ax.plot(x_grid[mA_E], icA_E[mA_E], color=SLATE, ls="--", lw=1.4, zorder=2)
    ax.plot(x_grid[mB_E], icB_E[mB_E], color=SLATE, ls="--", lw=1.4, zorder=2)

    # Plot equilibrium ICs through E*
    icA_S = (uA_S / (x_grid ** aA)) ** (1.0 / (1.0 - aA))
    icB_S = X2 - (uB_S / ((X1 - x_grid) ** aB)) ** (1.0 / (1.0 - aB))
    mA_S = (icA_S >= 0.0) & (icA_S <= X2)
    mB_S = (icB_S >= 0.0) & (icB_S <= X2)
    ax.plot(x_grid[mA_S], icA_S[mA_S], color=NAVY, lw=2.0, zorder=3, label=r"$u_A^*$ (Agent $A$)")
    ax.plot(x_grid[mB_S], icB_S[mB_S], color=RUST, lw=2.0, zorder=3, label=r"$u_B^*$ (Agent $B$)")

    # Contract curve
    ax.plot(x_cc, y_cc, color=NAVY, lw=2.4, ls="-", alpha=0.85, zorder=4,
            label=r"Contract curve ($MRS^A = MRS^B$)")

    # Budget line through E and E*: x2 = 10 - x1 (slope = -p1/p2)
    x_bl = np.linspace(0.0, 10.0, 200)
    ax.plot(x_bl, 10.0 - x_bl, color=GREEN, lw=2.2, zorder=4,
            label=r"Budget line (slope $= -p_1/p_2$)")

    # Points E and E*
    ax.scatter([e1], [e2], color=AMBER, edgecolor="white", s=90, lw=1.6, zorder=6)
    ax.scatter([eq1], [eq2], color=GREEN, edgecolor="white", s=95, lw=1.6, zorder=6)

    # Clean annotations
    ax.annotate(r"$E$", xy=(e1, e2), xytext=(e1 + 0.16, e2 + 0.22),
                fontsize=11.0, fontweight="bold", color=AMBER,
                bbox=dict(boxstyle="round,pad=0.15", fc=BG, ec="none", alpha=0.85))
    ax.annotate(r"$E^*$", xy=(eq1, eq2), xytext=(eq1, eq2 + 0.40),
                ha="center", va="bottom",
                fontsize=11.0, fontweight="bold", color=GREEN,
                bbox=dict(boxstyle="round,pad=0.15", fc=BG, ec="none", alpha=0.85))

    # Label endowment ICs accurately: lower dashed = u_A(E), upper dashed = u_B(E)
    ax.text(5.15, 7.35, r"$u_B(E)$", fontsize=9.2, color=SLATE)
    ax.text(3.45, 2.35, r"$u_A(E)$", fontsize=9.2, color=SLATE)

    # Direct labels for equilibrium ICs, contract curve, and budget line (no legend box)
    ax.text(8.15, 2.55, r"$u_A^*$", fontsize=10.0, fontweight="bold", color=NAVY)
    ax.text(1.05, 6.72, r"$u_B^*$", fontsize=10.0, fontweight="bold", color=RUST)
    ax.text(8.05, 8.15, "Contract\ncurve", fontsize=9.0, fontweight="bold",
            color=NAVY, ha="center")
    ax.text(7.75, 1.30, r"slope $= -p_1/p_2$", fontsize=9.2, fontweight="bold",
            color=GREEN, rotation=-32, ha="center",
            bbox=dict(boxstyle="round,pad=0.15", fc=BG, ec="none", alpha=0.82))

    # Box borders and dual axes
    ax.set_xlim(0, X1)
    ax.set_ylim(0, X2)
    ax.set_xticks(np.arange(0, 11, 2))
    ax.set_yticks(np.arange(0, 11, 2))
    ax.set_xlabel(r"Agent $A$'s Good 1 ($x_1^A$)", labelpad=6)
    ax.set_ylabel(r"Agent $A$'s Good 2 ($x_2^A$)", labelpad=6)
    ax.grid(True, color=GRID, lw=0.65, alpha=0.85)

    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color(NAVY)
        s.set_linewidth(1.2)

    ax_top = ax.twiny()
    ax_top.set_xlim(X1, 0)
    ax_top.set_xticks(np.arange(0, 11, 2))
    ax_top.set_xlabel(r"Agent $B$'s Good 1 ($x_1^B$)", labelpad=7, color=NAVY)
    ax_top.tick_params(colors=SLATE, length=3.5)
    for s in ax_top.spines.values():
        s.set_color(NAVY)

    ax_right = ax.twinx()
    ax_right.set_ylim(X2, 0)
    ax_right.set_yticks(np.arange(0, 11, 2))
    ax_right.set_ylabel(r"Agent $B$'s Good 2 ($x_2^B$)", labelpad=8, color=NAVY)
    ax_right.tick_params(colors=SLATE, length=3.5)
    for s in ax_right.spines.values():
        s.set_color(NAVY)

    # Origin labels
    ax.text(-0.55, -0.65, r"$O_A$", fontsize=11, fontweight="bold", color=NAVY, ha="center")
    ax.text(10.55, 10.65, r"$O_B$", fontsize=11, fontweight="bold", color=NAVY, ha="center")

    out_path = os.path.join(OUT_DIR, "fig_exchange_vanilla.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 6: Deriving a Trader's Price-Offer Curve
# ===========================================================================
def make_fig_offer_curve():
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    fig.subplots_adjust(left=0.12, right=0.95, bottom=0.13, top=0.90)

    a = 0.6
    e1, e2 = 2.0, 8.0

    # Smooth offer curve: parametrized by p = p1/p2
    p_vals = np.geomspace(0.62, 12.0, 400)
    W_vals = p_vals * e1 + e2
    x1_oc = a * W_vals / p_vals
    x2_oc = (1.0 - a) * W_vals
    mask_oc = (x1_oc <= 9.8) & (x2_oc <= 9.8)

    # Three illustrative price lines pivoting through E=(2, 8)
    prices = [
        (2.50, r"$p_H$", AMBER, (3.12, 5.20), (-0.15, -0.55)),
        (1.25, r"$p_M$", GREEN, (5.04, 4.20), (0.15, -0.60)),
        (0.75, r"$p_L$", RUST,  (7.60, 3.80), (0.18, -0.55)),
    ]

    x_line = np.linspace(0.0, 10.0, 300)
    for p, plab, col, (x1_opt, x2_opt), (dx, dy) in prices:
        # Budget line: x2 = p*(e1 - x1) + e2
        y_bl = p * (e1 - x_line) + e2
        m_bl = (y_bl >= 0.0) & (y_bl <= 10.0)
        ax.plot(x_line[m_bl], y_bl[m_bl], color=col, ls="--", lw=1.5, alpha=0.85, zorder=2)

        # Short tangent indifference curve segment around optimum
        u_opt = (x1_opt ** a) * (x2_opt ** (1.0 - a))
        x_ic = np.linspace(max(0.8, x1_opt - 1.5), min(9.8, x1_opt + 1.7), 160)
        y_ic = (u_opt / (x_ic ** a)) ** (1.0 / (1.0 - a))
        m_ic = (y_ic >= 0.0) & (y_ic <= 10.0)
        ax.plot(x_ic[m_ic], y_ic[m_ic], color=col, lw=1.6, alpha=0.75, zorder=3)

        # Optimal bundle dot
        ax.scatter([x1_opt], [x2_opt], color=col, edgecolor="white", s=65, lw=1.3, zorder=6)
        ax.text(x1_opt + dx, x2_opt + dy, plab, fontsize=9.8, fontweight="bold",
                color=col, ha="center")

    # Offer curve (bold navy)
    ax.plot(x1_oc[mask_oc], x2_oc[mask_oc], color=NAVY, lw=2.8, zorder=5)
    ax.text(6.6, 5.25, "Agent $A$'s\nOffer Curve", fontsize=10.2, fontweight="bold",
            color=NAVY, ha="left",
            bbox=dict(boxstyle="round,pad=0.22", fc=BG, ec="none", alpha=0.85))

    # Endowment dot E
    ax.scatter([e1], [e2], color=NAVY, edgecolor="white", s=90, lw=1.6, zorder=7)
    ax.annotate(r"$E = (e_1, e_2)$", xy=(e1, e2), xytext=(e1 + 0.55, e2 + 0.60),
                fontsize=10.2, fontweight="bold", color=NAVY,
                bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.88))

    # Endowment IC (subtle dotted)
    u_E = (e1 ** a) * (e2 ** (1.0 - a))
    x_eic = np.linspace(1.1, 9.6, 300)
    y_eic = (u_E / (x_eic ** a)) ** (1.0 / (1.0 - a))
    m_eic = (y_eic >= 0.0) & (y_eic <= 10.0)
    ax.plot(x_eic[m_eic], y_eic[m_eic], color=SLATE, ls=":", lw=1.3, zorder=1)
    ax.text(8.5, 1.45, r"$u_A(E)$", fontsize=8.8, color=SLATE)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks(np.arange(0, 11, 2))
    ax.set_yticks(np.arange(0, 11, 2))
    ax.set_xlabel(r"Good 1 ($x_1^A$)")
    ax.set_ylabel(r"Good 2 ($x_2^A$)")
    ax.set_title("Constructing a Price-Offer Curve", pad=10)
    style_axes_clean(ax)
    ax.grid(True, color=GRID, lw=0.65, alpha=0.85)

    out_path = os.path.join(OUT_DIR, "fig_offer_curve.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 7: One-Farm Economy Planner Optimum (static snapshot for Slide 4)
# ===========================================================================
def make_fig_one_farm():
    fig, ax = plt.subplots(figsize=(5.4, 4.3))
    fig.subplots_adjust(left=0.14, right=0.95, bottom=0.15, top=0.90)

    T = 12.0
    ell = np.linspace(0.0, T, 400)
    c_ppf = 3.0 * np.sqrt(T - ell)

    # Frontier
    ax.plot(ell, c_ppf, color=NAVY, lw=2.6, zorder=4, label=r"$c = F(T - \ell)$")
    ax.fill_between(ell, 0, c_ppf, color=NAVY, alpha=0.05, zorder=1)

    # Tangent line at E* = (8, 6), slope = -3/4
    ell_t = np.linspace(1.5, 12.0, 200)
    c_t = 6.0 - 0.75 * (ell_t - 8.0)
    ax.plot(ell_t, c_t, color=AMBER, ls="--", lw=1.8, zorder=3, label=r"Slope $= -MP_L$")

    # Indifference curve U = ln(48) -> c = 48 / ell
    ell_ic = np.linspace(3.5, 12.0, 300)
    c_ic = 48.0 / ell_ic
    m_ic = c_ic <= 13.5
    ax.plot(ell_ic[m_ic], c_ic[m_ic], color=GREEN, lw=2.2, zorder=3, label=r"Indiff. curve $U^*$")

    # Optimum E* = (8, 6)
    ax.plot([8.0, 8.0], [0.0, 6.0], color=SLATE, ls=":", lw=1.2, zorder=2)
    ax.plot([0.0, 8.0], [6.0, 6.0], color=SLATE, ls=":", lw=1.2, zorder=2)
    ax.scatter([8.0], [6.0], color=GREEN, edgecolor="white", s=85, lw=1.6, zorder=6)
    ax.annotate(r"$E^* = (\ell^*, c^*)$", xy=(8.0, 6.0), xytext=(8.55, 6.85),
                fontsize=10.0, fontweight="bold", color=NAVY,
                bbox=dict(boxstyle="round,pad=0.18", fc=BG, ec="none", alpha=0.85))

    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 13.5)
    ax.set_xticks([0, 4, 8, 12])
    ax.set_xticklabels(["0", "4", r"$\ell^*$", r"$T$"])
    ax.set_yticks([0, 6, 12])
    ax.set_yticklabels(["0", r"$c^*$", "12"])
    ax.set_xlabel(r"Leisure $\ell$ (Labor $L = T - \ell$)")
    ax.set_ylabel(r"Grain $c$")
    ax.set_title(r"Planner Optimum: $MRS_{\ell,c} = MP_L$", pad=9)
    style_axes_clean(ax)
    ax.grid(True, color=GRID, lw=0.65, alpha=0.85)
    ax.legend(loc="upper right", frameon=True, facecolor=BG, edgecolor=GRID, fontsize=8.4)

    out_path = os.path.join(OUT_DIR, "fig_one_farm.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 8: Simple Concave PPF with Tangent Line at E (Slide 8)
# ===========================================================================
def make_fig_ppf_simple():
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    fig.subplots_adjust(left=0.14, right=0.95, bottom=0.14, top=0.90)

    x = np.linspace(0.0, 10.0, 400)
    y = np.sqrt(np.maximum(0.0, 100.0 - x ** 2))

    # PPF curve & fill
    ax.plot(x, y, color=NAVY, lw=2.8, zorder=4, label=r"PPF: $x^2 + y^2 = 100$")
    ax.fill_between(x, 0, y, color=NAVY, alpha=0.05, zorder=1)

    # Point E = (6, 8), slope = -6/8 = -3/4
    ex, ey = 6.0, 8.0
    slope = -ex / ey
    x_tan = np.linspace(1.5, 10.5, 200)
    y_tan = ey + slope * (x_tan - ex)
    m_tan = (y_tan >= 0.0) & (y_tan <= 12.0)
    ax.plot(x_tan[m_tan], y_tan[m_tan], color=AMBER, ls="--", lw=2.0, zorder=3,
            label=r"Slope $= -RPT = -x/y$")

    ax.plot([ex, ex], [0.0, ey], color=SLATE, ls=":", lw=1.2, zorder=2)
    ax.plot([0.0, ex], [ey, ey], color=SLATE, ls=":", lw=1.2, zorder=2)
    ax.scatter([ex], [ey], color=AMBER, edgecolor="white", s=90, lw=1.6, zorder=6)
    ax.annotate(r"$E = (6, 8)$", xy=(ex, ey), xytext=(ex + 0.55, ey + 0.55),
                fontsize=10.2, fontweight="bold", color=NAVY,
                bbox=dict(boxstyle="round,pad=0.18", fc=BG, ec="none", alpha=0.88))

    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 12.0)
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.set_xlabel(r"Good $x$")
    ax.set_ylabel(r"Good $y$")
    ax.set_title(r"Production Possibility Frontier", pad=9)
    style_axes_clean(ax)
    ax.grid(True, color=GRID, lw=0.65, alpha=0.85)
    ax.legend(loc="upper right", frameon=True, facecolor=BG, edgecolor=GRID, fontsize=8.4)

    out_path = os.path.join(OUT_DIR, "fig_ppf_simple.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 9: National Income (GDP) Line on the PPF
# ===========================================================================
def make_fig_gdp_line():
    fig, ax = plt.subplots(figsize=(5.5, 4.4))
    fig.subplots_adjust(left=0.14, right=0.95, bottom=0.14, top=0.90)

    x = np.linspace(0.0, 10.0, 400)
    y = np.sqrt(np.maximum(0.0, 100.0 - x ** 2))

    # PPF curve & fill
    ax.plot(x, y, color=NAVY, lw=2.8, zorder=4, label=r"PPF ($x^2 + y^2 = 100$)")
    ax.fill_between(x, 0, y, color=NAVY, alpha=0.05, zorder=1)

    # Relative price p = p_x / p_y = 3/4
    p = 0.75

    # Suboptimal production point P0 = (9.6, 2.8) -> Y0/py = 0.75*9.6 + 2.8 = 10.0
    p0x, p0y = 9.6, 2.8
    Y0 = p * p0x + p0y  # 10.0
    x_l0 = np.linspace(0.0, Y0 / p, 200)
    y_l0 = Y0 - p * x_l0
    ax.plot(x_l0, y_l0, color=SLATE, ls="--", lw=1.7, zorder=3,
            label=r"Isovalue at $P_0$: $p_x x + p_y y = Y_0$")

    # GDP-maximizing tangent point A = (6, 8) -> Y*/py = 0.75*6 + 8 = 12.5
    ax_pt, ay_pt = 6.0, 8.0
    Ys = p * ax_pt + ay_pt  # 12.5
    x_ls = np.linspace(0.0, Ys / p, 200)
    y_ls = Ys - p * x_ls
    ax.plot(x_ls, y_ls, color=AMBER, lw=2.3, zorder=5,
            label=r"Max GDP line: $p_x x + p_y y = Y^*$")

    # Points P0 and A
    ax.scatter([p0x], [p0y], color=RUST, edgecolor="white", s=75, lw=1.5, zorder=6)
    ax.annotate(r"$P_0$", xy=(p0x, p0y), xytext=(p0x + 0.55, p0y + 0.45),
                fontsize=10.0, fontweight="bold", color=RUST,
                bbox=dict(boxstyle="round,pad=0.14", fc=BG, ec="none", alpha=0.88))

    ax.scatter([ax_pt], [ay_pt], color=AMBER, edgecolor="white", s=95, lw=1.6, zorder=7)
    ax.annotate(r"$A$ ($RPT = p_x/p_y$)", xy=(ax_pt, ay_pt), xytext=(ax_pt + 0.75, ay_pt + 0.7),
                fontsize=9.6, fontweight="bold", color=NAVY,
                bbox=dict(boxstyle="round,pad=0.16", fc=BG, ec="none", alpha=0.90))

    # Parallel shift arrow from Y0 line to Y* line
    ax.annotate("", xy=(2.2, Ys - p * 2.2 - 0.15), xytext=(2.2, Y0 - p * 2.2 + 0.15),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.3",
                                color=GREEN, lw=1.8), zorder=6)
    ax.text(2.55, 0.5 * (Ys + Y0) - p * 2.2 + 0.1, r"higher GDP",
            fontsize=8.6, fontweight="bold", color=GREEN,
            bbox=dict(boxstyle="round,pad=0.12", fc=BG, ec="none", alpha=0.88), zorder=7)

    # Intercept annotations
    ax.scatter([0.0, Ys / p], [Ys, 0.0], color=AMBER, s=32, zorder=6)
    ax.text(0.35, Ys + 0.28, r"$Y^*/p_y$", fontsize=9.2, fontweight="bold", color=AMBER)
    ax.text(Ys / p + 0.15, 0.65, r"$Y^*/p_x$", fontsize=9.2, fontweight="bold", color=AMBER, ha="center")
    ax.text(0.35, Y0 - 0.95, r"$Y_0/p_y$", fontsize=8.8, color=SLATE,
            bbox=dict(boxstyle="round,pad=0.10", fc=BG, ec="none", alpha=0.85))

    ax.set_xlim(0, 17.5)
    ax.set_ylim(0, 14.0)
    ax.set_xticks([0, 5, 10, 15])
    ax.set_yticks([0, 5, 10])
    ax.set_xlabel(r"Good $x$")
    ax.set_ylabel(r"Good $y$")
    ax.set_title(r"Production as Endowment $\rightarrow$ National GDP Line", pad=9)
    style_axes_clean(ax)
    ax.grid(True, color=GRID, lw=0.65, alpha=0.85)
    ax.legend(loc="upper right", frameon=True, facecolor=BG, edgecolor=GRID, fontsize=8.0)

    out_path = os.path.join(OUT_DIR, "fig_gdp_line.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"Saved {out_path}")


# ===========================================================================
# FIGURE 10: Static Production Edgeworth Box (alpha=0.75, beta=0.25)
# ===========================================================================
def make_fig_prod_box_vanilla():
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    fig.subplots_adjust(left=0.12, right=0.88, bottom=0.12, top=0.88)

    L_bar, K_bar = 100.0, 100.0
    alpha, beta = 0.75, 0.25

    L_grid = np.linspace(0.5, 99.5, 500)
    # Contract curve: K_x = 900*L_x / (100 + 8*L_x)
    K_cc = (9.0 * K_bar * L_grid) / (L_bar + 8.0 * L_grid)

    # Diagonal
    ax.plot([0, L_bar], [0, K_bar], color=SLATE, ls=":", lw=1.1, alpha=0.6, zorder=1)
    # Contract curve
    ax.plot(L_grid, K_cc, color=AMBER, lw=2.5, zorder=4, label=r"Contract curve ($RTS_x = RTS_y$)")

    # Inefficient point Z = (60, 30) and lens
    zx, zy = 60.0, 30.0
    xZ = (zy ** alpha) * (zx ** (1.0 - alpha))
    yZ = ((K_bar - zy) ** beta) * ((L_bar - zx) ** (1.0 - beta))

    L_iso = np.linspace(2.0, 98.0, 500)
    Kx_xZ = (xZ / (L_iso ** (1.0 - alpha))) ** (1.0 / alpha)
    Kx_yZ = K_bar - (yZ / ((L_bar - L_iso) ** (1.0 - beta))) ** (1.0 / beta)

    # Shade efficiency lens where Kx_yZ >= Kx_xZ
    mask_lens = (Kx_yZ >= Kx_xZ) & (Kx_xZ >= 0) & (Kx_yZ <= K_bar)
    ax.fill_between(L_iso, Kx_xZ, Kx_yZ, where=mask_lens, color=GREEN, alpha=0.14, zorder=2)

    m_xZ = (Kx_xZ >= 0) & (Kx_xZ <= K_bar)
    m_yZ = (Kx_yZ >= 0) & (Kx_yZ <= K_bar)
    ax.plot(L_iso[m_xZ], Kx_xZ[m_xZ], color=NAVY, lw=1.6, alpha=0.85, zorder=3,
            label=r"Good $x$ isoquants ($\alpha=0.75$)")
    ax.plot(L_iso[m_yZ], Kx_yZ[m_yZ], color=GREEN, lw=1.6, alpha=0.85, zorder=3,
            label=r"Good $y$ isoquants ($\beta=0.25$)")

    # Efficient point E = (25, 75) where RTS_x = RTS_y = 1
    ex, ey = 25.0, 75.0
    xE = (ey ** alpha) * (ex ** (1.0 - alpha))
    yE = ((K_bar - ey) ** beta) * ((L_bar - ex) ** (1.0 - beta))
    Kx_xE = (xE / (L_iso ** (1.0 - alpha))) ** (1.0 / alpha)
    Kx_yE = K_bar - (yE / ((L_bar - L_iso) ** (1.0 - beta))) ** (1.0 / beta)
    m_xE = (Kx_xE >= 0) & (Kx_xE <= K_bar)
    m_yE = (Kx_yE >= 0) & (Kx_yE <= K_bar)
    ax.plot(L_iso[m_xE], Kx_xE[m_xE], color=NAVY, lw=1.8, zorder=3)
    ax.plot(L_iso[m_yE], Kx_yE[m_yE], color=GREEN, lw=1.8, zorder=3)

    # Common tangent at E (slope = -1 through (25, 75))
    L_tan = np.linspace(8.0, 42.0, 50)
    K_tan = ey - 1.0 * (L_tan - ex)
    ax.plot(L_tan, K_tan, color=RUST, ls="--", lw=1.7, zorder=4,
            label=r"Factor-price line ($-w/v$)")

    # Points Z and E
    ax.scatter([zx], [zy], color=RUST, edgecolor="white", s=70, lw=1.4, zorder=6)
    ax.annotate(r"$Z$ (inefficient)", xy=(zx, zy), xytext=(zx + 4, zy - 7),
                fontsize=9.2, fontweight="bold", color=RUST,
                bbox=dict(boxstyle="round,pad=0.14", fc=BG, ec="none", alpha=0.88))

    ax.scatter([ex], [ey], color=AMBER, edgecolor="white", s=90, lw=1.6, zorder=7)
    ax.annotate(r"$E$", xy=(ex, ey), xytext=(ex + 4.5, ey - 0.8),
                fontsize=10.5, fontweight="bold", color=NAVY,
                bbox=dict(boxstyle="round,pad=0.10", fc=BG, ec="none", alpha=0.85))

    # Box frame and top/right axes for O_y
    ax.set_xlim(0, L_bar)
    ax.set_ylim(0, K_bar)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel(r"Labor in $x$ ($L_x \rightarrow$)", fontsize=10.0, color=NAVY)
    ax.set_ylabel(r"Capital in $x$ ($K_x \uparrow$)", fontsize=10.0, color=NAVY)

    ax_top = ax.twiny()
    ax_top.set_xlim(L_bar, 0)
    ax_top.set_xticks([0, 25, 50, 75, 100])
    ax_top.set_xlabel(r"$\leftarrow L_y$ (Labor in $y$)", fontsize=10.0, color=GREEN, labelpad=6)
    ax_top.tick_params(colors=GREEN, length=3.5)

    ax_right = ax.twinx()
    ax_right.set_ylim(K_bar, 0)
    ax_right.set_yticks([0, 25, 50, 75, 100])
    ax_right.set_ylabel(r"$K_y \downarrow$ (Capital in $y$)", fontsize=10.0, color=GREEN, labelpad=8)
    ax_right.tick_params(colors=GREEN, length=3.5)

    # Origin labels
    ax.text(-2.5, -6.5, r"$O_x$", fontsize=11, fontweight="bold", color=NAVY, ha="right", clip_on=False)
    ax.text(L_bar + 2.5, K_bar + 4.5, r"$O_y$", fontsize=11, fontweight="bold", color=GREEN, ha="left", clip_on=False)

    ax.grid(True, color=GRID, lw=0.6, alpha=0.8)
    ax.legend(loc="lower right", frameon=True, facecolor=BG, edgecolor=GRID, fontsize=7.8)

    out_path = os.path.join(OUT_DIR, "fig_prod_box_vanilla.png")
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    make_fig_stolper_samuelson()
    make_fig_ana_ben_box()
    make_fig_exchange_vanilla()
    make_fig_offer_curve()
    make_fig_one_farm()
    make_fig_ppf_simple()
    make_fig_gdp_line()
    make_fig_prod_box_vanilla()
    make_fig_upf_swf()
    make_fig_nested_ppf_box()
    print("All 10 figures generated successfully.")
