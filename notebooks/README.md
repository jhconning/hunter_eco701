# Computational Notebooks

Companion Jupyter notebooks for **ECO 701 (Microeconomic Theory)**.

These notebooks accompany the lecture slides, providing analytical derivations, interactive simulations, and figure-generation scripts used to produce both static and interactive diagrams for class and to explore key theoretical topics more deeply. 

Many of these notebooks and interactive visualizations were improved with AI pair-programming assistance (using **Google Antigravity** and **Claude Code**).

See also my [teaching notebooks](https://jhconning.github.io/Econ-Teach/) on micro theory, trade, and other topics.

---

## Running the Notebooks

* **Interactive Web View:** Browse static and interactive figures directly within the course site navigation on the left.
* **Google Colab:** Click the **"Open in Colab"** badge at the top of any course notebook to run, modify, and experiment with the code in your browser with zero local installation.
* **Local Python Environment:** Clone the [course repository](https://github.com/jhconning/hunter_eco701) and run notebooks locally inside an `ecopy` conda/mamba environment (`numpy`, `scipy`, `sympy`, `matplotlib`, `plotly`, `pandas`).

---

## Course Notebooks

| Topic & Notebook | Description | Links |
| :--- | :--- | :--- |
| **Topic 1: Model Figures** | Continuous Fisherman's Dilemma, private best-response curves, Pigouvian tax internalizers, payoff surfaces, and the linear Utility Possibility Frontier (UPF). | [View Notebook](topic01_definitions_key_tools_figures.ipynb) |
| **Topic 1: Schelling Segregation** | Thomas Schelling's (1971) spatial agent-based simulation demonstrating micro-motives, tolerance thresholds, and macro-segregation tipping dynamics. | [View Notebook](topic01_schelling_segregation.ipynb) |
| **Topic 2: Optimization Geometry** | 3D objective surfaces, level curves, tangent planes, isoquants, gradient vectors, and the geometry of Lagrange multipliers. | [View Notebook](topic02_constrained_optimization_figures.ipynb) |
| **Topic 2: Optimization Solvers** | Analytical derivations and numerical solvers with SymPy and SciPy: equality and inequality (KKT) constraints, shadow prices, and bordered Hessians. | [View Notebook](topic02_constrained_optimization_numerical.ipynb) |
| **Applications: Farm-Household Model** | Autarkic (Chayanovian) household vs. separable market model: profit maximization, labor market regimes, and the separation property. | [View Notebook](farm_household.ipynb) |

---

## Complementary Micro Theory Notebooks (Econ-Teach)

The following companion notebooks from the [Econ-Teach](https://jhconning.github.io/Econ-Teach/) project provide further interactive visualizations and mathematical derivations:

| Notebook | Topic & Coverage | External Link |
| :--- | :--- | :--- |
| **Constrained Optimization** | Lagrangian methods, first- and second-order conditions, envelope theorems, and duality in consumer and producer theory. | [Econ-Teach: Constrained Optimization](https://jhconning.github.io/Econ-Teach/notebooks/micro/01_Constrained_Optimization.html) |
| **CES Functions** | Constant Elasticity of Substitution (CES) utility and production functions, substitution elasticities ($\sigma$), isoquants, and expenditure functions. | [Econ-Teach: CES Functions](https://jhconning.github.io/Econ-Teach/notebooks/micro/ces.html) |
| **Edgeworth Box Economy** | Pure exchange general equilibrium, contract curves, offer curves, competitive price vectors, and the First and Second Welfare Theorems. | [Econ-Teach: Edgeworth Box](https://jhconning.github.io/Econ-Teach/notebooks/trade/Edgeworth.html) |
