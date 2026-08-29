# ECO 701 manim videos (3Blue1Brown style)

## Role & working mode

You are acting as an expert Manim (Community Edition) developer and math/economics communicator, building animated video in the visual style of 3Blue1Brown (Grant Sanderson) to accompany the lectures for my ECO 701, Masters graduate microeconomics course. These videos are not to be toy demos, they must get the economics exactly right.

The task right now is to build a first video.

Work in two passes:
1. **Plan first.** Write a scene-by-scene storyboard (what's on screen, what narration/on-screen text accompanies it, rough duration, key animations/camera moves) covering the content outline below. Resolve the "Open decisions" section — either pick a sensible default and state your choice, or ask me directly if it materially changes the approach. Share the plan before writing substantial code.
2. **Then build incrementally.** Implement one scene/beat at a time, render each in low quality (`-pql`) to check it before moving to the next, rather than writing everything blind. Verify the environment works (see Setup) with a trivial smoke-test scene before touching the real content.

## Audience & purpose

This is for a producer-theory unit in Econ 701, a Masters graduate microeconomics course (reference text: Nicholson & Snyder, *Microeconomic Theory*). The audience already knows multivariable calculus, but needs some extra hand holding on partial derivatives, implicit differentiation, and the analogous consumer-theory concepts (indifference curves, MRS) — so move briskly but provide intuition as you go and use precise notation rather than re-deriving basic calculus. Do carefully define each new *economic* object (isoquant, MRTS, homotheticity) the first time it appears. This supplements lecture, so it should stand alone but doesn't need to be exhaustive — a focused, precise, visually-driven explainer, roughly 7–11 minutes.

## Content outline (required — cover all six in this order)

Look at Slides E701_F18 _slidesI.pdf and in particular slides 43-79. on understanding production function visualization, isoquants and level curves, and concepts like the marginal rate of technical substitution.

You do not need to follow the slides exactly, I point to them mainly to make clear what topics students will need to master. 

After you are done with the simple examples, of univariate optimization, use a single running numerical example throughout so the video feels like one coherent story rather than five disconnected clips: **A = 1, α = β = 0.5**, i.e. q = √(KL) (constant returns to scale). Keep K, L on a domain like [0.3, 9] (stay away from the axes — Cobb-Douglas isoquants are asymptotic there and K=0 or L=0 causes rendering/derivative issues at the boundary).

**1. The mathematical expression.**
Introduce q = F(K,L) = A·K^α·L^β. Name each symbol: q output, A total factor productivity, K capital, L labor, α, β the output elasticities of capital and labor (α, β > 0). Show that F(tK, tL) = t^(α+β)·F(K,L) — Cobb-Douglas is homogeneous of degree (α+β) — and name the three cases: α+β=1 constant returns to scale, α+β<1 decreasing, α+β>1 increasing. This sets up the homotheticity payoff at the end, so don't skip it even though the request starts with "the expression" — it's one short beat, not a full digression. Then specialize to the running example (α=β=0.5) for everything that follows.

**2. The 3D surface, rotating.**
Build 3D axes with **L on the x-axis, K on the y-axis, q on the z-axis** (lock this axis convention for the whole video — see the isoquant beat for why). Plot the surface z = F(x,y) over the domain. Orbit the camera around it (ambient rotation or a few deliberate `move_camera` moves) to reveal that it's increasing in both directions, passes through the origin, and is concave — curving over, not a flat plane or a cone. If it fits naturally, slice the surface with a fixed-L or fixed-K vertical plane to show a single cross-section curve and call out that it's concave (diminishing marginal product of one input holding the other fixed) — this is optional polish, not required.

**3. Isoquants, visually.**
This is the conceptual hinge of the video, and the best opportunity for a genuinely 3b1b-style moment: don't just cut to a 2D contour plot — *derive* the isoquant from the surface on screen. Animate a translucent horizontal plane at height z=q̄ rising through the surface; highlight the curve where it intersects the surface; then project that curve straight down onto the base (K,L) plane. Repeat for 2–4 output levels to build up a family of isoquants. Then move the camera to a straight-overhead view (roughly `phi=0`; verify exact angles empirically) so the 3D scene *becomes* the familiar 2D isoquant map — a continuous camera move, not a hard cut. Define isoquant on screen: the set of all (K,L) producing the same output q̄. Name-check the analogy to indifference curves for students coming from consumer theory.

**4. Tangent slope and MRTS.**
Zoom into a single isoquant. Place a point on it and draw its tangent line. State the definition precisely:
MRTS_LK = −dK/dL |_q̄ = F_L / F_K
(the amount of capital you can give up per extra unit of labor while holding output constant — always reported as a positive number, mirroring MRS in consumer theory). Derive/display the closed form for the running example:
F_K = αAK^(α−1)L^β, F_L = βAK^αL^(β−1), so MRTS_LK = (β/α)·(K/L).
Animate a `ValueTracker`-driven point sliding along the isoquant with the tangent line updating live (`always_redraw`), plus a live numeric readout of the current MRTS value next to it. Let students see the slope flatten as the point slides toward more L / less K — diminishing MRTS, i.e. the isoquant is convex to the origin.

Illustrative pattern for the live tangent (adapt, don't copy verbatim — get the math right for whatever function/parameters you land on):
```python
L_tracker = ValueTracker(1.0)

def K_of_L(L, q=4.0, alpha=0.5, beta=0.5, A=1.0):
    return (q / (A * L**beta)) ** (1/alpha)

dot = always_redraw(lambda: Dot(
    axes.c2p(L_tracker.get_value(), K_of_L(L_tracker.get_value())), color=YELLOW
))

def tangent_line():
    L0 = L_tracker.get_value()
    K0 = K_of_L(L0)
    slope = -(beta / alpha) * (K0 / L0)          # dK/dL along this isoquant
    return Line(axes.c2p(L0 - 1, K0 - slope), axes.c2p(L0 + 1, K0 + slope), color=RED)

tangent = always_redraw(tangent_line)
self.add(dot, tangent)
self.play(L_tracker.animate.set_value(4.0), run_time=4)
```



**Template for future videos**

This is a concept video. If it works well we will do several more to follow the course.  It would be nice to have some video branding in the form of introductory slides that make clear this is for 'Eco 701: Microeconomic Theory' at Hunter College, CUNY

The next video after this first one will focus on Constrained Optimization and the Method of Lagrange.