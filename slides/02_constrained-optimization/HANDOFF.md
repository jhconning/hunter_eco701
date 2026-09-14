# Topic 2: Constrained Optimization — Handoff Document

**Course:** ECO 701: Microeconomic Theory (MA Level)  
**Instructor:** Jonathan Conning (Hunter College, CUNY)  
**Topic Folder:** `Y:\Hunter\eco701\slides\02_constrained-optimization\`  
**Target File:** `slides/02_constrained-optimization/deck.qmd` (to be created from `deck.md`)  
**Companion Notebooks:**
- [`Y:\Hunter\eco701\notebooks\topic02_constrained_optimization_numerical.ipynb`](../../notebooks/topic02_constrained_optimization_numerical.ipynb)
- [`Y:\Hunter\eco701\notebooks\topic02_constrained_optimization_figures.ipynb`](../../notebooks/topic02_constrained_optimization_figures.ipynb)

---

## 1. Pedagogical Arc & Continuity of Themes

### How Topic 2 Picks Up from Topic 1
Topic 1 (*Definitions and Key Tools*) established the course's overarching thesis:
> **model the rules $\to$ find the equilibrium $\to$ evaluate efficiency & distribution $\to$ redesign the rules**

Topic 1 introduced strategic interactions, games, institutions (rules of the game), and continuous optimization under the hood through the lake fishery. In that model, Alfredo chose hours freely: $\max_{e_A} u_A(e_A, e_B)$ without a budget, quota, or hour ceiling. That was **unconstrained optimization**.

Topic 1 closed with the **Bridge Slide (Slide 39)**:
> *"Where is the hill flat?"* vs. *"How high can you climb before hitting the fence?"*
> Real economic choices are rarely unconstrained. Consumers maximize utility subject to a **budget constraint**; firms minimize costs subject to a **production target**; relief agencies allocate supplies subject to **transport capacity**.

**Topic 2 builds the core mathematical engine for choice under scarcity:**
1. **Unconstrained multivariable optimization:** Gradient vectors ($\nabla f = 0$), contour lines, and implicit differentiation ($dy/dx = -f_x / f_y$).
2. **Constrained optimization via three pedagogical angles:**
   - **Direct Substitution:** Eliminating a variable (algebraic, but clumsy for general forms).
   - **Tangency / Arbitrage:** Equalizing marginal bang-per-buck: $\frac{f_x}{P_x} = \frac{f_y}{P_y} \iff MRS = MRT$.
   - **The Method of Lagrange:** Converting a constrained problem into an unconstrained artificial function $\mathcal{L}(x, y, \lambda) = f(x, y) - \lambda [g(x, y) - c]$.
3. **The Economic Meaning of the Multiplier ($\lambda$):**
   - $\lambda$ is not just an algebraic trick; it is the **shadow price** of the constraint:
     $$\lambda^* = \frac{\partial f(x^*, y^*)}{\partial c}$$
   - The marginal valuation of relaxing scarcity by one unit (the Envelope Theorem in miniature).
4. **Inequality Constraints & Kuhn–Tucker (KKT):**
   - Recognizing when the fence binds vs. when it is slack (complementary slackness: $\lambda \ge 0, \; g(x, y) \le c, \; \lambda [c - g(x, y)] = 0$).
   - Corner solutions where tangency fails.
5. **Multi-Constraint Optimization (The Earthquake Relief Problem / PS1 Q3):**
   - Relief agency choosing food $x$ and tents $y$ subject to *both* a financial budget constraint ($P_x x + P_y y \le I$) *and* a transport capacity constraint ($w_x x + w_y y \le T$).
   - Systematic case analysis ($2^K$ candidate regimes) and solving numerically in Python via `scipy.optimize`.

---

## 2. Where This Fits in the Semester Curriculum
- **Topic 1:** Foundations — institutions, game theory, Pareto criterion, unconstrained baseline.
- **Topic 2 (Current Task):** The Machinery of Constrained Optimization — Lagrange, Kuhn–Tucker, shadow prices, multi-constraint problems.
- **Topic 3:** Duality, Expenditure Minimization, and the Envelope Theorem.
- **Topics 4–6:** Consumer Theory, Choice under Risk & Time, Household Production (direct application of Lagrange/KKT).
- **Topic 7:** General Equilibrium (integrating all optimizing consumers and firms into markets; proving when Smith's invisible hand holds).

---

## 3. Current State of the Topic 2 Directory

### Assets in `slides/02_constrained-optimization/`:
- [`deck.md`](file:///y:/Hunter/eco701/slides/02_constrained-optimization/deck.md): Legacy Marp markdown file (571 lines, 60 slides). Fully transcribed from legacy PowerPoint `E701_F18 _slidesI.pptx` (slides 43–102).
- [`new_ideas.md`](file:///y:/Hunter/eco701/slides/02_constrained-optimization/new_ideas.md): Backlog of potential additions (Python solver slide, 3 hand cases vs. 1 `scipy` call, rotatable 3D Plotly view, corner solution graphic).
- [`source.yml`](file:///y:/Hunter/eco701/slides/02_constrained-optimization/source.yml): Metadata and conversion history from the legacy slides.
- `media/`: Contains legacy Mathcad equation crops and charts.
- `figs/`: Contains modern Python-generated figures for the Earthquake relief problem, tangency checks, and 3D surfaces.
- **Numerical Companion Notebook:**
  - [`notebooks/topic02_constrained_optimization_numerical.ipynb`](file:///y:/Hunter/eco701/notebooks/topic02_constrained_optimization_numerical.ipynb): Contains fully verified symbolic and numerical solutions (`scipy.optimize.minimize` SLSQP) for the single-constraint consumer problem, corner solutions (quasi-linear utility), and the multi-constraint Earthquake relief problem.

---

## 4. Planned Conversion Steps to Quarto Reveal.js (`deck.qmd`)

1. **Create `deck.qmd` with Unified Header:**
   ```yaml
   ---
   title: "Microeconomic Theory"
   subtitle: "Topic 2: Constrained Optimization"
   author: "Jonathan Conning"
   description: "ECO 701 Topic 2: Constrained Optimization"
   deploy: true
   institute: "Hunter College, Dept. of Economics"
   format:
     revealjs:
       theme: [default, ../_shared/eco701-revealjs.scss]
       slide-number: true
       footer: "Eco 701 - Micro Theory"
       html-math-method: katex
       chalkboard: true
       width: 1280
       height: 720
   jupyter: ecopy
   execute:
     echo: false
     warning: false
     freeze: auto
   ---
   ```

2. **Structure the Deck into 3 Cohesive Parts:**
   - **Opening:** Direct callback to Topic 1's bridge (*"From the Hill to the Fence"*).
   - **Part I: Mathematical Preliminaries (Slides ~1–20):** Single-variable FOC/SOC review $\to$ Multivariable surfaces $\to$ Contour plots $\to$ Partial derivatives $\to$ Implicit function theorem & slope of level curves ($dy/dx = -f_x / f_y$).
   - **Part II: Constrained Optimization & Lagrange (Slides ~21–45):** The consumer problem $\to$ Substitution method $\to$ Tangency condition ($MRS = MRT$) $\to$ Method of Lagrange $\to$ Interpretation of $\lambda$ as shadow price $\to$ PPF application $\to$ Corner solutions $\to$ Kuhn–Tucker conditions and complementary slackness.
   - **Part III: Applications & Multi-Constraint Problems (Slides ~46–60):** The Earthquake Relief problem (budget $I$ and transport $T$) $\to$ Systematic case checking $\to$ Solving with Python (`scipy.optimize`) vs. by hand $\to$ Envelope theorem sensitivity check.

3. **Key Modernization Opportunities:**
   - Replace legacy Mathcad screenshot crops in `media/` with clean KaTeX equations and crisp Python-generated graphs from `figs/`.
   - Add the short comparative slide: *"Why Economists Still Solve This by Hand"* (3 hand-checked cases vs. 1 `scipy` call, and how this scales).
   - Ensure clean Reveal.js column layouts (`:::: {.columns}`) and avoid vertical text collisions.

---

## 5. Build, Verification & Workflow Protocol

### Quarto Build:
```bash
quarto render slides/02_constrained-optimization/deck.qmd
```

### Visual Margin & Overflow Verification:
```bash
mamba run -n ecopy python tools/verify_deck.py --topic 02_constrained-optimization --keep-pdf
```
*(Inspect generated PNG rasters in `_verify/02_constrained-optimization/` to guarantee zero text overflow or footer collisions).*

### Strict Global Agent Rules Reminder:
- **Paths:** Always use `Y:\` drive mapping (`Y:\Hunter\eco701\...`), NEVER machine-specific `C:\Users` paths.
- **Language Style:** Keep prose simple, direct, economical, and natural; avoid grandiose or AI-sounding buzzwords.
- **Logging:** Update `Y:\B\notable\Main notes\gemini\master_worklog.md` with a detailed entry at the end of any turn performing significant work.
