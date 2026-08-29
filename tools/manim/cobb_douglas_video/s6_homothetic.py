"""S6 — the homotheticity payoff (~90 s).

Full isoquant family; a ray K = mL from the origin crosses every isoquant
with the SAME slope (parallel tangent stubs). One-line proof: MRTS depends
only on K/L. Sweep the ray. Payoff: expansion paths are straight lines;
tease the Lagrange episode.
"""
import numpy as np
from manim import *
import theme as T
import params as P

ISO = list(T.CD_COLOR_MAP.keys())


class Homothetic(T.PacedScene):
    def construct(self):
        # ---- matched isoquant map (same geometry as S5 end state) ----------
        axes = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2],
                    x_length=5.6, y_length=5.6,
                    axis_config={"color": GREY_B, "include_ticks": True,
                                 "tip_width": 0.14, "tip_height": 0.14})
        axes.shift(np.array([-2.81, -2.76, 0]) - axes.c2p(0, 0))
        xlab = MathTex("L", font_size=30, color=T.L_COL).move_to(
            axes.c2p(10.55, 0.8, 0))
        ylab = MathTex("K", font_size=30, color=T.K_COL).move_to(
            axes.c2p(-0.8, 10.7, 0))
        curves, labels = VGroup(), VGroup()
        ladder = [(1.15, 2.2), (2.05, 3.2), (3.0, 4.2), (4.1, 5.2)]
        for qb, col, (lx, ky) in zip([1.0, 2.0, 3.0, 4.0], T.ISO_COLS, ladder):
            lmin = max(P.DOM_MIN, qb**2 / P.DOM_MAX)
            curves.add(axes.plot(lambda x, q=qb: P.K_of_L(x, q),
                                 x_range=[lmin, P.DOM_MAX], color=col,
                                 stroke_width=4.5))
            labels.add(MathTex(rf"\bar q = {qb:.0f}", font_size=24,
                               color=col).move_to(axes.c2p(lx, ky)))
        self.add(axes, xlab, ylab, curves, labels)
        self.wait(0.5)

        # ---- the ray and its parallel tangent stubs -------------------------
        mtr = ValueTracker(1.5)

        def ray_line():
            m = mtr.get_value()
            L_end = min(9.6, 9.6 / m)
            return Line(axes.c2p(0, 0), axes.c2p(L_end, m * L_end),
                        color=GREY_A, stroke_width=2.5)

        def stub_group():
            m = mtr.get_value()
            g = VGroup()
            h = 0.55
            for qb in P.QBARS:
                L0 = qb / np.sqrt(m)
                K0 = m * L0
                if not (P.DOM_MIN + 0.1 <= L0 <= 9.4 and K0 <= 9.4):
                    continue
                g.add(Line(axes.c2p(L0 - h, K0 + m * h),
                           axes.c2p(L0 + h, K0 - m * h),
                           color=T.TAN_COL, stroke_width=3.5))
                g.add(Dot(axes.c2p(L0, K0), radius=0.05, color=WHITE))
            return g

        ray = always_redraw(ray_line)
        raylab = MathTex(r"K = m\,L", font_size=30, color=GREY_A)
        raylab.add_updater(lambda l: l.move_to(
            ray_line().point_from_proportion(0.9) + np.array([-0.75, 0.3, 0])))

        self.play(Create(ray), FadeIn(raylab), run_time=1.6)
        self.wait(0.6)
        stubs = always_redraw(stub_group)
        self.play(FadeIn(stubs), run_time=1.2)
        self.wait(0.8)

        par = Text("same slope at every crossing", font_size=26,
                   color=T.Q_COL).to_edge(UP, buff=0.35)
        self.play(Write(par), run_time=1.2)
        self.wait(1.2)

        # ---- why: MRTS depends only on the ratio K/L ------------------------
        w1 = T.colorize(MathTex(
            r"\text{MRTS} = \frac{\beta}{\alpha}\cdot\frac{K}{L}",
            font_size=36, substrings_to_isolate=ISO))
        w2 = Text("…depends only on the ratio K/L", font_size=24,
                  color=GREY_A)
        # plain white on purpose: substring isolation garbles glyph baselines
        # in long \text{...} lines
        w3 = MathTex(
            r"F \text{ homog.\ of degree } r"
            r"\;\Rightarrow\; F_{K},\,F_{L} \text{ homog.\ of degree } r-1"
            r"\;\Rightarrow\; \text{MRTS}(tK,\,tL) = \text{MRTS}(K,\,L)",
            font_size=26, color=GREY_A)
        why = VGroup(w1, w2).arrange(DOWN, buff=0.3)
        why.move_to(np.array([4.5, 1.7, 0]))
        w3.move_to(np.array([0.0, -3.35, 0]))
        if w3.width > 13.0:
            w3.scale_to_fit_width(13.0)

        self.play(Write(w1), run_time=1.2)
        self.play(FadeIn(w2), run_time=0.8)
        self.wait(1.6)
        self.play(Write(w3), run_time=1.8)
        self.wait(2.2)

        card = T.definition_card(
            "Homothetic technology",
            r"\text{MRTS}(tK,\, tL) = \text{MRTS}(K,\, L)\;\;\;\forall\, t>0",
            "slopes constant along every ray from the origin",
            formula_size=34)
        card.scale(0.72).move_to(np.array([4.62, -0.5, 0]))
        card.shift(LEFT * max(0.0, card.get_right()[0] - 6.95))
        mono = Text("(any monotone transform of a homogeneous F is homothetic)",
                    font_size=18, color=GREY_B).next_to(card, DOWN, buff=0.22)
        mono.shift(LEFT * max(0.0, mono.get_right()[0] - 7.0))
        self.play(FadeIn(card, shift=UP * 0.25), run_time=1.0)
        self.play(FadeIn(mono), run_time=0.7)
        self.wait(2.0)

        # ---- sweep the ray: the property holds for every mix ----------------
        self.play(mtr.animate.set_value(0.5), run_time=3.2,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)
        self.play(mtr.animate.set_value(2.4), run_time=3.2,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)
        self.play(mtr.animate.set_value(1.0), run_time=1.8,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.8)

        payoff = Text(
            "scaling the firm up or down never changes the optimal input mix:",
            font_size=24, color=T.Q_COL)
        payoff2 = Text("expansion paths are straight rays", font_size=24,
                       color=T.Q_COL)
        pay = VGroup(payoff, payoff2).arrange(DOWN, buff=0.15)
        pay.move_to(np.array([0.0, -3.35, 0]))
        self.play(FadeOut(w3), FadeIn(pay), run_time=1.1)
        self.wait(2.4)

        tease = Text("next: add input prices → cost minimization & Lagrange",
                     font_size=24, color=GREY_A).move_to(pay.get_center())
        self.play(FadeOut(pay), FadeIn(tease), run_time=1.0)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in [axes, xlab, ylab, curves, labels,
                                         ray, raylab, stubs, par, why, card,
                                         mono, tease]], run_time=1.0)
        self.wait(0.3)
