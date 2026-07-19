# New Ideas: Constrained Optimization

Expansion ideas for this topic, captured 2026-07-16 after finishing the
full slide conversion (all three sub-chunks) and the numerical companion
notebook ([`notebooks/topic02_constrained_optimization_numerical.ipynb`](../../notebooks/topic02_constrained_optimization_numerical.ipynb)).
Nothing here is committed to — this is a backlog to pull from, not a plan.

**2026-07-18: Part III ("Optimization Meets Strategy") is now DONE** — see
`source.yml` for the full note. It sits right after "The Art of the Solve"
and *before* the two Python-tools items below, per Jonathan's explicit
ordering call — so "near the end of the deck" in those two items now means
"after Part III," not immediately after "The Art of the Solve."

## New slides

- **"Solving It With Python"** — a short slide near the end of the deck
  showing the `scipy.optimize` pattern (objective, constraints, bounds,
  `SLSQP`) as the modern counterpart to the legacy Mathcad screenshot on
  "Checking the Answer Symbolically." Could either replace that screenshot
  outright or sit right after it as an explicit old-tool/new-tool contrast.
  Could also show `scipy.optimize` cross-checking the new Cournot example
  (Worked Example 6 in the numerical notebook doesn't currently do this —
  only the symbolic route was used there, unlike Worked Examples 1-4).
- **"Why Economists Still Solve This by Hand"** — a slide built around the
  notebook's own punchline: 3 hand-checked cases vs. 1 `scipy` call for a
  2-constraint problem, and why that ratio flips once you have more than a
  couple of constraints. Natural bridge from Part III into the Python-tools
  material above.
- **A visual for "Example: A Corner Solution"** (current slide 84-equivalent
  has no image) — cheap to add now since the notebook already has a working,
  verified corner example (quasi-linear utility, $u=c_1+\sqrt{c_2}$) with a
  real graph.
- **Beyond Cobb-Douglas** — a short slide showing the *same* symbolic solver
  (`lagrangian_solve` in the notebook) applied to a CES or other functional
  form, to make explicit that nothing in the method was Cobb-Douglas-specific.
  Sets up demand theory in later topics.

## New visualizations

- **Interactive shadow-price demo for the Earthquake problem** — the notebook
  currently only shows the envelope-theorem check as static before/after
  numbers ($I=100$ vs. $I=101$). An `ipywidgets` version with live sliders
  for $I$ and $T$, updating both the graph and a numeric readout of
  $U^*,\lambda,\mu$, would make the "shadow price" idea tangible in class
  the same way the existing tangency-point slider already does for the
  single-constraint case.
- **Income-expansion path** for the Cobb-Douglas running example — plot how
  $(c_1^*,c_2^*)$ moves as $I$ rises. Genuinely new content (not a
  replication of anything already in the deck); a natural lead-in to
  Engel curves whenever that's covered.
- **Rotatable 3-D view (plotly)** of the objective surface with the
  constraint curve traced on it and the tangency point marked — lets
  students see "tangent to a level curve" as a literal 3-D tangency rather
  than only the 2-D contour-map version. Good candidate for live lecture use
  (plotly survives HTML export, unlike `ipywidgets`).

## Problem set ideas

- **Asymmetric Cournot** — give the two firms different marginal costs
  $c_1\neq c_2$ and ask students to `nash_solve` the resulting system by
  hand (or reuse the notebook's helper) - the closed-form answer no longer
  collapses to a single symmetric $q^*$, a genuine step beyond the deck's
  worked (symmetric) case.
- **A contest/rent-seeking game** — continuous effort $e_i$, win probability
  $e_i/(e_1+e_2)$, a prize $V$: `nash_solve` applies unmodified, but the
  reaction functions are no longer linear - a good test of whether students
  actually understood the method or just pattern-matched linear algebra.
  Ties to the wrap-up slide's explicit promise of "problem sets" for
  variants beyond the fisherman/Cournot pair.
- **Third constraint on Earthquake Relief** (e.g., a food-spoilage/capacity
  limit) — pushes the case-count to $2^3=8$, past what's comfortable by
  hand, motivating `scipy.optimize` directly rather than just asserting
  "computers help once problems get bigger."
- **Sensitivity-analysis exercise** — hand students the notebook's
  `solve_for_T` pattern, ask them to sweep $T$ from 60 to 100 and plot
  $dU^*/dT$, then explain in words why it's zero over part of the range and
  positive over the rest. Turns the envelope-theorem section into a graded
  question instead of a passive demo.
- **"Build your own case-solver"** — give students `lagrangian_solve` and
  ask them to apply it to a new problem, e.g. cost minimization subject to
  an output target (the dual of the utility-maximization problem this topic
  covers). Tests whether they understand the tool is general-purpose, not
  wired to the earthquake example specifically.

## Where these came from

Every idea above is scoped to something that already exists in `deck.md` or
the numerical notebook — none of it requires new source material from the
legacy PowerPoint. See `HANDOFF.md`'s "Code-generated figures" section for
the notebook's own status, and `source.yml` for the conversion history.
