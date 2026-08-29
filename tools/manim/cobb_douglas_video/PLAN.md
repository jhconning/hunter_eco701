# PLAN — Eco 701 Video 1: The Cobb-Douglas Production Function

3Blue1Brown-style Manim (Community Edition) explainer for the producer-theory unit of
Eco 701 (Masters micro, Hunter College CUNY; reference text Nicholson & Snyder).
Target length **≈ 9½ min** (within the 7–11 min brief). Running example throughout:
**A = 1, α = β = 0.5, q = √(KL)**, domain **K, L ∈ [0.3, 9]**.

Source brief: `Y:\Hunter\eco701\tools\manim\manim_prompt1.md`
Slide anchor: `Y:\Hunter\eco701\archive\past_semesters\eco701_F18\slides\pdf\E701_F18 _slidesI.pdf`, slides 43–79.

> **This file is the design history.** For the day-to-day guide — code map,
> render commands, and the layout-editing workflow — see `README.md`.

---

## 1. Interpretation of the brief & resolved decisions

The prompt says "cover all six in this order" but lists four numbered beats (it references
"Setup" and "Open decisions" sections trimmed from an earlier draft). Reconstruction, grounded
in the F18 slides and the prompt's own text:

| # | Beat | Grounding |
|---|------|-----------|
| 1 | Univariate optimization warm-up | "After you are done with the simple examples of univariate optimization…"; slides 43–47 (FOC, necessary vs. sufficient, SOC, inflection) |
| 2 | The mathematical expression + homogeneity | prompt beat 1 |
| 3 | The 3D surface, rotating | prompt beat 2; slide 49–50 plots exactly f(x,y)=√(xy) |
| 4 | Isoquants derived from the surface | prompt beat 3; slides 56–58 (contour lines) |
| 5 | Tangent slope & MRTS, diminishing MRTS | prompt beat 4; slides 56–59 (total differentiation → slope = −F_L/F_K) |
| 6 | Homotheticity payoff | "sets up the homotheticity payoff at the end"; legacy `homothetic.tex` |

**Other decisions (defaults chosen; flag if wrong):**

- **Scene architecture:** separate Scene classes per beat, rendered individually and stitched
  at the end — *except* beats 3+4, which must be **one continuous `ThreeDScene`** (the
  surface→isoquant-map camera flatten is the centerpiece and cannot be cut). Per-beat scenes
  give fast `-pql` iteration; cuts land only at natural beat boundaries.
- **Narration:** the video is paced for a recorded voiceover (script per beat below, for
  Jonathan to record or TTS later); on-screen text carries only definitions, labels, and
  formulas, 3b1b-style. No burned-in captions of the narration.
- **Isoquant family levels:** q̄ ∈ {1, 2, 3, 4} (all interior to the domain: K = q̄²/L stays
  inside [0.3, 9] over a wide L-range for each level).
- **Final render:** 1080p30 (`-qh`); dev renders 480p15 (`-pql`). Upgrade to 60fps only if
  render time is acceptable at the end.
- **Terminology:** MRTS_{L,K} = −dK/dL|_q̄ = F_L/F_K, reported positive, per the prompt;
  name-check once that Nicholson & Snyder call this simply *RTS*.
- **Axis convention (locked):** L on x, K on y, q on z, everywhere — so the flattened 3D view
  *is* the standard 2D isoquant diagram with L horizontal and K vertical.

## 2. Environment — verified state & setup steps

Verified 2026-07-12 on this machine:

- `ecopy` env (Python 3.13.13) has **no manim**; conda-forge has manim ≤ 0.20.1.
- `mamba` is not on the non-interactive PATH — call it as
  `& "$env:USERPROFILE\miniforge3\condabin\mamba.bat" run -n ecopy …`.
- LaTeX: **TinyTeX** at `%APPDATA%\TinyTeX` (latex.exe on PATH) but **`dvisvgm` is missing**
  — Manim's `MathTex` pipeline is latex → dvi → dvisvgm → svg, so this blocks all math text.
- No ffmpeg CLI (fine: manim ≥ 0.19 encodes via bundled PyAV; ffmpeg only wanted for stitching).

**Setup (step 0 of implementation):**

1. `mamba install -n ecopy -c conda-forge manim ffmpeg` — if the solver fights the large
   geospatial env, fall back to a dedicated env `manim701` (same command with `-n manim701 python=3.12`).
2. `tlmgr install dvisvgm standalone preview doublestroke ms setspace rsfs relsize ragged2e fundus-calligra microtype semantic-markup wasysym physics jknapltx wasy cm-super babel-english gnu-freefont mathastext cbfonts-fd` (Manim's documented LaTeX dependency list; TinyTeX's tlmgr handles these).
3. **Smoke test** (`smoke_test.py`): one scene with `MathTex(r"q = A K^\alpha L^\beta")` and a
   small `Surface` on `ThreeDAxes`, rendered `-pql`. This exercises LaTeX/dvisvgm, Cairo,
   and the 3D pipeline in one shot before any real content.

## 3. Project layout

```
Y:\Hunter\eco701\tools\manim\cobb_douglas_video\      (as built: flat layout —
  PLAN.md                  ← this file            simplest for manim CLI+imports)
  params.py                # A, ALPHA, BETA, domain, QBARS + closed forms
  theme.py                 # palette, colorize(), definition_card(), tangent
                           # machinery, PACE + PacedScene, branding_card()
  s0_intro.py Intro        s1_warmup.py Warmup1D    s2_expression.py Expression
  s34_surface.py SurfaceToIsoquants (ThreeDScene, beats 3+4)
  s5_mrts.py MRTS          s6_homothetic.py Homothetic   s7_outro.py Outro
  smoke_test.py            # toolchain check (MathTex + 3D + encode)
  math_check.py            # sympy gate: every on-screen formula (19 checks)
  qa_frames.py             # dump every Nth mp4 frame to PNG via PyAV, for visual QA
  stitch.py                # ffmpeg concat of the per-scene mp4s in episode order
  render.ps1               # .\render.ps1 [-Final] → render all + stitch
  NARRATION.md             # recording script with approx. timestamps
  renders\                 # stitched deliverables
```

## 4. Design system

- Background: near-black dark gray (≈ `#171717`), 3b1b-style.
- **Color code (constant across this and future videos):** L / labor = manim `BLUE`,
  K / capital = `GREEN`, output q / surface = `YELLOW` accents on a blue→teal surface
  gradient, isoquants = warm gradient by level (e.g. `YELLOW_A`→`ORANGE`), tangent lines =
  `RED`, definitions boxed in soft white, α β = `TEAL`/`PURPLE`, A = `GREY_B`.
- Every economic definition appears in a consistent "definition card" (rounded rect, title,
  one formula, one plain-English line) — isoquant, MRTS, homothetic each get one.
- Branding: cold-open card "**ECO 701 · Microeconomic Theory** — Hunter College, CUNY",
  episode line "Producer Theory I: The Cobb-Douglas Production Function", small animated
  isoquant-flourish logo; same card template closes the video and trails "Next: Constrained
  Optimization & the Method of Lagrange."

## 5. Storyboard (scene by scene)

Durations are targets; narration is a draft script to be recorded (or replaced) by Jonathan.

### S0 · Branding intro — ~0:15
- **Screen:** dark card; series title writes on; episode subtitle fades in; a single isoquant
  curve sweeps as a logo flourish.
- **Tech:** `Write`, `FadeIn`, `Create` on a `ParametricFunction`.

### S1 · Warm-up: one choice variable — ~1:15
- **Screen:** 2D axes; π(q) = 10q − 10 − q² (the exact MC1 example from lecture slides).
  A tangent line rides the curve; its slope value ticks down to 0 at the top (q* = 5).
  FOC card: π′(q) = 0 — *necessary*. Flash counterexample f(x) = x² − 10x + 20 (same FOC,
  a minimum) → sufficiency needs π″ < 0. (Optional 3-sec flash: −x³ inflection.)
- **Narration draft:** "Before firms, a warm-up you've seen: pick one number to maximize a
  function. Profit from selling q units at price 10 with cost 10 + q². At the top of the
  hill the tangent is flat — the first-order condition. But flat tangents also happen at
  valley bottoms, so we check curvature: the second-order condition. Economics is full of
  hills like this one. The trouble is, real firms don't choose one number — they choose
  bundles. Capital *and* labor. So we need functions of several variables, and that's where
  the pictures get interesting."
- **Tech:** `Axes`, `ValueTracker` + `always_redraw` tangent, `DecimalNumber` slope readout.
  (Same machinery is reused in S5 — build it once in `theme.py`.)

### S2 · The expression & homogeneity — ~1:30
- **Screen:** q = F(K, L) = A·K^α·L^β center-stage, each symbol color-pulsed and labeled on
  a legend (q output · A total factor productivity · K capital · L labor · α, β output
  elasticities, α, β > 0). Then the scaling computation animates line by line:
  F(tK, tL) = A(tK)^α(tL)^β = t^{α+β}·A K^α L^β = t^{α+β} F(K, L) — "homogeneous of degree
  α+β". Number line for α+β with the three named cases: <1 decreasing, =1 constant,
  >1 increasing returns to scale. Specialize: A=1, α=β=0.5 ⇒ **q = √(KL)**, CRS; numeric
  check (1,4)→2 doubles to (2,8)→4. This card stays as the running example badge.
- **Narration draft:** "Here is the workhorse: Cobb-Douglas. …name each piece… Scale both
  inputs by t and the exponents collect: output scales by t^{α+β} — the function is
  homogeneous of degree α plus β. That single number sorts technologies into decreasing,
  constant, and increasing returns to scale. File this away — it buys us something elegant
  at the end of the video. From here on, one running example: A = 1, α = β = ½ — output is
  the square root of K times L, constant returns."
- **Tech:** `MathTex` with `substrings_to_isolate`, `TransformMatchingTex` for the algebra,
  `NumberLine` with three labeled zones.

### S3 · The 3D surface — ~1:30 *(first half of `SurfaceToIsoquants`)*
- **Screen:** `ThreeDAxes` (L→x, K→y, q→z, ranges [0.3,9]², z [0,9] with compressed
  z-length so the surface reads wide, not tall). Surface z = √(xy) fades in with a
  blue→teal height gradient; slow orbit (`begin_ambient_camera_rotation`, then a couple of
  deliberate `move_camera` beats). Call-outs (fixed-in-frame): increasing in both inputs;
  concave — it curves over. Then a vertical plane K = 4 slices the surface; the intersection
  curve q = 2√L lifts out and gets a tangent whose slope shrinks as L grows — "hold K fixed
  and you're back in one variable: this slope *is* the partial derivative ∂q/∂L, the
  marginal product of labor, and it diminishes." (Ties S1's tangent machinery to partials —
  the hand-holding the audience needs.)
- **Narration draft:** "Two inputs means the graph lives in three dimensions: labor this
  way, capital that way, output straight up. Watch it grow in every direction — more of
  either input, more output — but watch it curve over as it grows: that bend is diminishing
  returns. Slice it at a fixed capital level and the cut edge is an ordinary one-variable
  curve — its slope is the partial derivative of output with respect to labor, the marginal
  product of labor."
- **Tech:** `Surface(resolution=(48,48))`, `add_fixed_in_frame_mobjects` for labels,
  `ParametricFunction` for the slice curve on the surface.

### S4 · Isoquants, derived on screen — ~2:15 *(second half of `SurfaceToIsoquants`; the hinge)*
- **Screen:** a translucent horizontal plane rises to height q̄ = 2; the intersection curve
  with the surface glows (parametric: K = q̄²/L at height q̄); the curve then **projects
  straight down** onto the floor (animated drop with dashed vertical guide lines). Repeat
  for q̄ = 1, 3, 4 — faster each time — building a family of floor curves colored by level.
  Camera then executes one continuous move to straight overhead (φ → 0, verified
  empirically so L reads rightward and K upward), the 3D axes crossfade into clean 2D
  axes at the identical screen position: the surface has *become* the isoquant map.
  Definition card: **Isoquant** = {(K, L) : F(K, L) = q̄} — all input mixes producing the
  same output. Name-check: "the producer twin of the indifference curve; in consumer theory
  the analogous curve fixes utility instead of output." Mathematicians' name: level curve /
  contour line.
- **Narration draft:** "Fix an output target — say two units — and slice the mountain
  horizontally. The cut is every input combination that hits exactly that target. Drop it
  to the floor and you have a curve economists call an isoquant — 'iso', same; 'quant',
  quantity. Do this at several heights and the floor collects a topographic map of the
  technology. Now look straight down: the 3D surface and the 2D map are the same object.
  Every contour map you've ever read is this move. If you've seen indifference curves in
  consumer theory, this is the same construction with output in place of utility."
- **Tech:** `Square`/`Surface` translucent plane at z = q̄ with `.animate.shift`,
  `ParametricFunction` intersection curves (exact closed form, no marching squares),
  `move_camera(phi=0°…)`, crossfade 3D→2D axes; keep floor curves as the objects that
  survive into the 2D world.

### S5 · Tangent slope & MRTS — ~2:15
- **Screen:** clean 2D isoquant map (matched to S4's final frame); zoom to the q̄ = 4 curve.
  Point on the curve, tangent line drawn. Derivation panel, mirroring the lecture's
  total-differentiation route (slides 56–58): along an isoquant F(K,L) = q̄, so
  F_K dK + F_L dL = 0 ⇒ dK/dL = −F_L/F_K. Definition card:
  **MRTS_{L,K} = −dK/dL|_{q̄} = F_L/F_K** — capital you can give up per extra unit of labor,
  holding output constant; reported positive (mirrors MRS; Nicholson calls it RTS). Closed
  form animates: F_K = αAK^{α−1}L^β, F_L = βAK^αL^{β−1} ⇒ MRTS = (β/α)(K/L), and with
  α = β = ½: **MRTS = K/L** (also shown in the tidy form F_K = αq/K, F_L = βq/L).
  Then the set-piece: `ValueTracker` slides the point from (L=2, K=8) to (L=8, K=2); tangent
  updates live; a readout shows MRTS falling 4.00 → 0.25. Caption: **diminishing MRTS** —
  the isoquant is convex to the origin: the more labor you already have, the less capital
  each extra worker replaces.
- **Narration draft:** "Zoom into one curve. Its slope at a point answers a trade question:
  if I hire a little more labor, how much capital can I release and still hit my target?
  Total-differentiate the isoquant condition… the slope is minus the ratio of marginal
  products. We report it as a positive number and call it the marginal rate of technical
  substitution. For Cobb-Douglas it collapses to something beautiful: beta over alpha,
  times K over L. Watch the readout as we slide along the curve — from four units of
  capital per worker down to a quarter. Substitution gets harder the further you push:
  isoquants bow toward the origin."
- **Tech:** reuse S1's tracker/tangent/readout machinery; `TransformMatchingTex` derivation;
  numbers formatted with `DecimalNumber(num_decimal_places=2)`.

### S6 · The homotheticity payoff — ~1:30
- **Screen:** full isoquant family; a ray K = mL shoots from the origin. At each crossing
  with an isoquant, a short tangent stub appears — all visibly **parallel**. Why: along the
  ray K/L is constant and MRTS = (β/α)(K/L) depends *only* on K/L. One-line general proof
  panel: F homogeneous of degree r ⇒ its partials are homogeneous of degree r−1 ⇒ their
  ratio is homogeneous of degree 0 ⇒ MRTS(tK, tL) = MRTS(K, L). Definition card:
  **Homothetic** technology — MRTS constant along rays from the origin (any monotone
  transformation of a homogeneous function). A `ValueTracker` sweeps the ray's slope m;
  the parallel stubs ride along. Payoff, stated over the picture: scaling a firm up doesn't
  change the trade-off between inputs — so optimal input *mixes* lie on straight rays, which
  is exactly what makes the cost-minimization problem of the next video so clean. Tease:
  "when a price line enters this picture, tangency picks the ray."
- **Narration draft:** "Remember homogeneity? Here's the payoff. Draw any ray from the
  origin — a fixed capital-labor ratio — and look at the slope where it crosses each
  isoquant. Identical. Every isoquant is a scaled copy of every other: the technology is
  homothetic, and this follows from homogeneity of any degree, not just constant returns.
  Economically: a bigger firm facing the same input prices has no reason to change its
  input mix — expansion happens along straight lines. Next time, we put prices on this
  map and let Lagrange find the tangency."
- **Tech:** `always_redraw` stubs anchored at ray–isoquant intersections (closed form:
  crossing of K = mL with K = q̄²/L is L = q̄/√m), slope-m `ValueTracker` sweep.

### S7 · Recap & outro — ~0:25
- **Screen:** five mini-panels line up: the formula, the surface, the slicing plane, the
  MRTS tangent, the parallel-slopes ray — one sentence each; branding card returns with
  "Next: Constrained Optimization & the Method of Lagrange."
- **Tech:** scale-down snapshots (re-instantiated small versions, not literal frame grabs).

**Total ≈ 9:25.**

## 6. Build workflow (incremental, per the brief)

1. **M0** Setup + smoke test (§2). Confirm MathTex + 3D render at `-pql`.
2. **M1** `params.py` + `theme.py` + S0 intro card.
3. **M2–M7** One beat at a time in storyboard order; after each: render `-pql`, dump frames
   via `qa_frames.py`, inspect (Claude reads the PNGs), fix, only then advance. The 3D beat
   S3/S4 gets extra checkpoints: (a) surface + orbit, (b) one plane-slice-project cycle,
   (c) full family + overhead flatten — each verified visually before the next is written.
4. **M8** Full `-pql` end-to-end stitch (`stitch.py`) for pacing review → final `-qh` render.
5. Math correctness gate before final render: every on-screen formula checked symbolically
   (sympy one-liners: partials, MRTS closed form, homogeneity identity, slice slopes).

## 7. Economics correctness checklist (gate for M8)

- [ ] Homogeneity identity displayed with correct degree α+β and the three RTS cases.
- [ ] Isoquant definition as a *set*: {(K,L) : F(K,L) = q̄}.
- [ ] MRTS sign convention: defined via −dK/dL, displayed and read out as positive.
- [ ] MRTS_{L,K} = F_L/F_K (not F_K/F_L — the classic slip with L on the horizontal axis).
- [ ] Diminishing MRTS attributed to convexity of isoquants — *not* conflated with
      diminishing marginal products (related but distinct; don't claim equivalence).
- [ ] Homothetic ≠ homogeneous: homothetic defined as monotone transform of homogeneous /
      MRTS depends only on K/L; homogeneous stated as a *sufficient* condition.
- [ ] Domain kept to [0.3, 9]²; no curve or surface evaluated at K=0 or L=0.
- [ ] Notation matches course: F_K, F_L subscripts for partials; q̄ for the fixed level.

## 8. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Conda solver conflict installing manim into big `ecopy` env | Fallback dedicated `manim701` env (py 3.12); all commands go through `mamba.bat run -n <env>` |
| TinyTeX missing manim's LaTeX packages beyond dvisvgm | Full `tlmgr install` list in §2; smoke test fails fast if anything's missing |
| Overhead camera (φ=0) axis orientation flips L/K on screen | Empirical labeled test frame before building S4; adjust θ or axis mapping until L→right, K→up |
| 3D `MathTex` labels billboard wrongly during orbit | HUD text via `add_fixed_in_frame_mobjects`; only axis labels live in 3D |
| Long 3D render times on final pass | Keep 1080p30; render scenes in parallel processes if needed; `-ql` for all pacing decisions |
| Google Drive sync churn on `media\` partial files | Acceptable at `-pql`; if it thrashes, point `--media_dir` at local scratch and copy finals back |
| Scene-boundary visual jumps | Cuts only at beat boundaries; S4→S5 matched-frame handoff (same axes geometry) verified by diffing last/first frames |

## 9. Explicitly deferred

- Voiceover recording/TTS and syncing (`manim-voiceover` could be added later; animations
  are paced generously so narration fits over them).
- Euler's theorem / cost-function derivation (in `legacy/homothetic.tex`) — next videos.
- Video 2: **Constrained Optimization & the Method of Lagrange** (slides 63–79 already
  reviewed: substitution method, tangency/arbitrage argument, Lagrange FOCs, λ as marginal
  utility of income, welfare-max-subject-to-PPF example) — reuse `theme.py` branding,
  the isoquant map, and the MRTS tangent machinery.

## 10. Assumptions to confirm (won't block starting)

1. The six-beat reconstruction in §1 — in particular opening with the univariate FOC/SOC
   warm-up (slides 43–47) and closing with homotheticity.
2. Voiceover-paced (silent) video rather than on-screen narration captions.
3. Installing manim + ffmpeg into `ecopy` (falling back to a fresh `manim701` env only if
   the solve conflicts).

---

## 11. As-built notes (2026-07-12)

**Status: built and rendered.** All seven scenes implemented, visually QA'd
frame-by-frame at 480p15, all 19 sympy checks green (`math_check.py`), final
1080p30 stitched episode in `renders\`. Per-scene durations at PACE=3.3 were
15/56/70/99/69/71/33 s (≈6:53 total); shipped PACE=4.0 → ≈7:50.

**Environment facts (deviations from §2):**
- manim 0.20.1 + ffmpeg installed into `ecopy` cleanly — no solver conflict,
  no `manim701` fallback needed. sympy added for `math_check.py`.
- TinyTeX's tlmgr repo had to be switched to an **https** mirror of the frozen
  TL2025 archive (`ftp://tug.org` downloads fail):
  `tlmgr option repository https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2025/tlnet-final`
- Renders were pointed at a **local media dir** for speed and to spare Drive
  sync the thousands of partial files (`render.ps1` does this and copies the
  stitched mp4 back). Rendering into the project `media\` on Y: also works —
  the one failure originally blamed on a Drive file lock turned out to be the
  LaTeX isolation bug below.

**Manim gotchas encountered (baked into `theme.colorize` docstring):**
- `substrings_to_isolate` on q/A/K/L corrupts any LaTeX command containing
  those letters: **never** use `\quad`, `\qquad`, `\sqrt` in colorized
  formulas; write accents/scripts with braces (`\bar{q}`, `F_{K}`).
- `set_opacity()` on `axes.plot()` curves adds an ugly fill — dim curves with
  `set_stroke(opacity=...)`.
- `checkerboard_colors=None` crashes `Surface` — omit the kwarg instead.
- Camera: L/K axis labels lie flat in the floor plane (they become the 2D
  map's labels after the flatten); an extra upright "K" is shown during the
  3D phase and faded out at the flatten. The flatten is a pure phi-move
  (theta parked at −90° beforehand).
- Pacing: `theme.PACE` multiplies `wait()` holds only (PacedScene /
  PacedThreeDScene); ambient-rotation rate was retuned for the stretched
  orbit (−0.016).

**Matched-cut geometry** (S34 → S5 → S6): 2D scenes rebuild the map with
`Axes(x_length=y_length=5.6)` shifted so the origin sits at (−2.81, −2.76) —
this reproduces the flattened 3D floor at zoom 0.8 exactly.

**Deferred / next steps:** voiceover recording over `NARRATION.md`;
episode 2 (Lagrange) reuses `theme.py` branding, the map builder, and the
tangent machinery.
