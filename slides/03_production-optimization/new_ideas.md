# New Ideas: Production Optimization

Expansion ideas for this topic, captured 2026-07-16 right after finishing
the full slide conversion. Nothing here is committed to — this is a
backlog to pull from, not a plan.

## New slides

- **A genuine short-run/long-run numeric example** — the deck's
  "Short-Run and Long-Run Costs" slide is qualitative only (an envelope of
  $SC(k_i)$ curves). A Cobb-Douglas worked example (fix $k$ at a few
  levels, solve short-run cost at each, show the long-run curve as their
  lower envelope) would make the envelope relationship concrete the same
  way the Cobb-Douglas cost function already does for the unconstrained
  cost-minimization slides.
- **A returns-to-scale spectrum slide** — CRS and DRS are each given their
  own worked example, but increasing returns to scale (IRS, $\alpha+\beta>1$)
  is never shown. Adding a third $\alpha+\beta>1$ example alongside the
  existing CRS/DRS ones would complete the picture and set up a natural
  "which case is realistic when" discussion.
- **Bridge slide to Topic 2** — this topic's Method-of-Lagrange
  cost-minimization derivation (isocost tangency, the multiplier as
  marginal cost) is structurally identical to Topic 2's utility
  maximization. An explicit "you've seen this exact math before" slide
  early in Part I could reinforce the general-purpose nature of the method
  rather than leaving the parallel implicit.

## New visualizations

- **Interactive isoquant/isocost tangency demo** — same pattern as Topic 2's
  tangency-point slider (`ipywidgets`), but for $(K,L)$ with sliders for
  $w$, $r$, and the technology's $\alpha,\beta$. Directly reusable code
  from a hypothetical Topic 3 numerical notebook (none exists yet — see
  below).
- **Animated short-run-to-long-run envelope** — step through $SC(k_1)$,
  $SC(k_2)$, $SC(k_3),\dots$ and watch the long-run $C$ curve emerge as
  their lower envelope. Would make "Short-Run and Long-Run Costs" (currently
  a single static image) much more legible.
- **Side-by-side CRS/DRS/IRS cost-curve comparison** — one figure, three
  curves, shared axes — cheaper to build than three separate static PNGs
  and more useful for cross-comparison than the deck's current one-curve-
  per-slide treatment.

## Problem set ideas

- **Given a Cobb-Douglas technology and specific factor prices, derive the
  full cost function and classify its returns to scale** — direct
  application of the closed-form derivation this topic builds up to.
- **A profit-maximization problem with a non-linear (not just linear)
  inverse demand curve** — the deck's own worked example uses linear
  demand throughout; asking students to redo the AR/MR derivation for,
  say, constant-elasticity demand tests whether they understand the
  *method* (AR = price by definition, MR from differentiating revenue)
  rather than having memorized the linear-demand formulas.
- **A short-run vs. long-run decision problem**: given a fixed capital
  level and a demand shock, ask students to compute the short-run optimal
  labor choice, then compare to the long-run optimum once capital can
  adjust — motivated directly by the "Short-Run Total Costs" slide.

## Notebook idea (doesn't exist yet for this topic)

Topic 2 has a companion notebook
(`notebooks/topic02_constrained_optimization_numerical.ipynb`) that solves
its examples symbolically (`sympy`) and numerically (`scipy.optimize`).
Topic 3 has no equivalent yet — a natural extension would reuse the same
`lagrangian_solve` helper for the cost-minimization problem here (it's the
identical mathematical structure with $K,L$ in place of $c_1,c_2$), then
add the profit-maximization FOC/SOC checks and the returns-to-scale
examples as new sections.

## Where these came from

Every idea above is scoped to something that already exists in `deck.md`
— none of it requires new source material from the legacy PowerPoint. See
`source.yml` for the conversion history and gotchas specific to this
topic (native-diagram capture, the variable title-height crop issue).

## Parked for Topic 4 (cut from the Topic 3 deck 2026-10-05)

The consumer/producer duality map was removed from Topic 3 because its
consumer column (expenditure function, Hicksian and Marshallian demand) is
not taught until Topic 4. It belongs at the end of Topic 4, when both
columns are known. Caution before reusing: cost minimization is the true
twin of expenditure minimization, but profit maximization has no budget
constraint and is not the twin of utility maximization, so the
"Primal/Dual" row labels overstate the symmetry. Original slide:

```markdown
## The Duality Map {.compact}

| | **Consumer** | **Producer** |
|---|---|---|
| Primal | $\max u(x)$ s.t. $p\cdot x = m$ | $\max pq - C(q)$ |
| Dual | $\min p\cdot x$ s.t. $u(x) = \bar u$ | $\min wL + rK$ s.t. $F(K,L) = q$ |
| Value function | $V(p,m)$, $E(p,\bar u)$ | $\pi(p,w,r)$, $C(w,r,q)$ |
| Quantity-fixed demand | Hicksian $x^h(p,\bar u)$ | conditional $L^*(w,r,q)$ |
| Free demand | Marshallian $x(p,m)$ | unconditional $L(p,w,r)$ |
| Envelope result | $\partial E/\partial p_i = x_i^h$ | $\partial C/\partial w = L^*, \; \partial \pi^*/\partial p = q^*$ |

::: {.fragment}
Two problems, one skeleton. Learn the skeleton and each new application costs you an afternoon, not a semester.
:::
```

Also cut and available if wanted: a full Hotelling's lemma slide (now one
bullet on the Shephard slide) and "Why Duality Earns Its Keep" (only the
estimation point survives, in the Shephard callout).
