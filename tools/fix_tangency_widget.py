import json

nb_path = "notebooks/topic02_constrained_optimization_numerical.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

cell9_src = """def plot_tangency(p1_val, p2_val, I_val, ax=None, xlim=(0, 100), ylim=(0, 70)):
    c1_star = I_val / (2 * p1_val)
    c2_star = I_val / (2 * p2_val)
    u_star = c1_star * c2_star

    show = ax is None
    if ax is None:
        fig, ax = plt.subplots(figsize=(6.5, 5.4))

    # Grid for indifference curves spanning the fixed xlim window
    x_max = xlim[1] if xlim else max(I_val / p1_val * 1.05, 80)
    x = np.linspace(0.5, x_max, 400)
    for u_level, color in zip([0.5 * u_star, u_star, 1.5 * u_star], ["#9fb0d9", NAVY, "#9fb0d9"]):
        y = u_level / x
        ax.plot(x, y, color=color, lw=2 if color == NAVY else 1.3)

    x_budget_max = min(I_val / p1_val, x_max)
    x_budget = np.linspace(0, x_budget_max, 200)
    y_budget = (I_val - p1_val * x_budget) / p2_val
    ax.plot(x_budget, y_budget, color=AMBER, lw=2.2, label="Budget line")

    ax.plot(c1_star, c2_star, "o", color=AMBER, ms=9, zorder=5)
    ax.annotate(f"$E=({c1_star:.1f}, {c2_star:.1f})$", (c1_star, c2_star),
                textcoords="offset points", xytext=(10, 10), fontweight="bold")

    if xlim is not None:
        ax.set_xlim(*xlim)
    else:
        ax.set_xlim(0, I_val / p1_val * 1.05)
        
    if ylim is not None:
        ax.set_ylim(*ylim)
    else:
        ax.set_ylim(0, I_val / p2_val * 1.6)

    ax.set_xlabel("$c_1$")
    ax.set_ylabel("$c_2$")
    ax.set_title(fr"$p_1={p1_val:g},\ p_2={p2_val:g},\ I={I_val:g}$")
    ax.grid(True, alpha=0.3)
    if show:
        plt.show()
        return fig

fig = plot_tangency(p1_val, p2_val, I_val)
savefig(fig, "tangency-scipy-check.png")
"""

cell11_src = """import ipywidgets as widgets

def _interactive_tangency(p1=2.0, p2=3.0, I=120.0):
    fig, ax = plt.subplots(figsize=(6.5, 5.4))
    plot_tangency(p1, p2, I, ax=ax, xlim=(0, 100), ylim=(0, 70))
    plt.show()

widgets.interact(
    _interactive_tangency,
    p1=widgets.FloatSlider(value=2.0, min=1.0, max=5.0, step=0.25, description="$p_1$"),
    p2=widgets.FloatSlider(value=3.0, min=1.0, max=5.0, step=0.25, description="$p_2$"),
    I=widgets.FloatSlider(value=120.0, min=60.0, max=180.0, step=10.0, description="$I$"),
);
"""

nb["cells"][9]["source"] = [line + "\n" for line in cell9_src.splitlines()]
nb["cells"][11]["source"] = [line + "\n" for line in cell11_src.splitlines()]

# Ensure tags are set
for idx in [9, 11]:
    if "metadata" not in nb["cells"][idx]:
        nb["cells"][idx]["metadata"] = {}
    if "tags" not in nb["cells"][idx]["metadata"]:
        nb["cells"][idx]["metadata"]["tags"] = []
    if "hide-input" not in nb["cells"][idx]["metadata"]["tags"]:
        nb["cells"][idx]["metadata"]["tags"].append("hide-input")

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Successfully updated cells 9 and 11 in topic02_constrained_optimization_numerical.ipynb")
