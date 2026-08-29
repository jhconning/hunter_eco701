"""S5 — tangent slope & MRTS (~2 min).

Opens on the same isoquant map the 3D scene flattened into (matched geometry,
so the cut is invisible). Total differentiation -> MRTS definition card ->
Cobb-Douglas closed form -> live tangent sliding along the q̄=4 isoquant with
a falling MRTS readout: diminishing MRTS / convexity.
"""
from manim import *
import theme as T
import params as P

ISO = list(T.CD_COLOR_MAP.keys())
QB = 4.0


def K4(L):
    return P.K_of_L(L, QB)


def dK4(L):
    return P.dK_dL(L, QB)


class MRTS(T.PacedScene):
    def construct(self):
        # ---- rebuild the flattened map with matched geometry ---------------
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
        self.add(axes, xlab, ylab, curves, labels)   # seamless continuation

        # focus on the q̄ = 4 curve (set_stroke, NOT set_opacity — the latter
        # adds a fill to the open plot curves)
        self.wait(0.5)
        self.play(*[c.animate.set_stroke(opacity=0.18) for c in curves[:3]],
                  *[l.animate.set_opacity(0.25) for l in labels[:3]],
                  run_time=1.0)

        # ---- derivation: total differentiation along the isoquant ----------
        d_title = Text("stay on the curve…", font_size=26, color=GREY_A)
        d1 = T.colorize(MathTex(r"F(K, L) = \bar{q}", font_size=38,
                                substrings_to_isolate=ISO))
        d2 = T.colorize(MathTex(r"F_{K} \, dK + F_{L} \, dL = 0", font_size=38,
                                substrings_to_isolate=ISO))
        d3 = T.colorize(MathTex(
            r"\frac{dK}{dL} = -\,\frac{F_{L}}{F_{K}}", font_size=38,
            substrings_to_isolate=ISO))
        deriv = VGroup(d_title, d1, d2, d3).arrange(DOWN, buff=0.42)
        deriv.move_to(np.array([4.55, 1.9, 0]))

        self.play(FadeIn(d_title), Write(d1), run_time=1.3)
        self.wait(1.2)
        self.play(Write(d2), run_time=1.3)
        self.wait(1.4)
        self.play(Write(d3), run_time=1.2)
        self.wait(1.6)

        card = T.definition_card(
            "Marginal rate of technical substitution",
            r"\text{MRTS}_{L,K} \;=\; -\,\frac{dK}{dL}\Big|_{\bar{q}}"
            r" \;=\; \frac{F_{L}}{F_{K}}",
            "capital you can give up per extra unit of labor",
            formula_size=38)
        if card.width > 5.3:
            card.scale_to_fit_width(5.3)
        card.move_to(np.array([4.15, 2.0, 0]))
        card.shift(LEFT * max(0.0, card.get_right()[0] - 6.9))
        self.play(FadeOut(deriv, shift=UP * 0.3),
                  FadeIn(card, shift=UP * 0.3), run_time=1.2)
        self.wait(2.2)

        # ---- Cobb-Douglas closed form --------------------------------------
        cf1 = VGroup(
            T.colorize(MathTex(
                r"F_{K} = \alpha A K^{\alpha-1} L^{\beta} = \alpha\,\frac{q}{K}",
                font_size=30, substrings_to_isolate=ISO)),
            T.colorize(MathTex(
                r"F_{L} = \beta A K^{\alpha} L^{\beta-1} = \beta\,\frac{q}{L}",
                font_size=30, substrings_to_isolate=ISO)),
        ).arrange(RIGHT, buff=0.55)
        if cf1.width > 5.6:
            cf1.scale_to_fit_width(5.6)
        cf2 = T.colorize(MathTex(
            r"\text{MRTS} = \frac{\beta}{\alpha}\cdot\frac{K}{L}"
            r"\;\;\overset{\alpha=\beta}{=}\;\;\frac{K}{L}",
            font_size=38, substrings_to_isolate=ISO))
        cf = VGroup(cf1, cf2).arrange(DOWN, buff=0.4).next_to(
            card, DOWN, buff=0.5)
        self.play(Write(cf1), run_time=1.4)
        self.wait(1.4)
        self.play(Write(cf2), run_time=1.2)
        box = SurroundingRectangle(cf2, color=T.Q_COL, buff=0.15,
                                   corner_radius=0.08)
        self.play(Create(box), run_time=0.7)
        self.wait(1.8)

        # ---- the set-piece: slide along the isoquant ------------------------
        tr = ValueTracker(2.0)
        dot = T.moving_dot(axes, K4, tr, color=WHITE, radius=0.07)
        tan = T.moving_tangent(axes, K4, dK4, tr, half_len=1.3, color=WHITE,
                               stroke_width=3.0)
        readout = T.live_readout(
            r"\text{MRTS} = \frac{K}{L} =",
            lambda: P.MRTS(K4(tr.get_value()), tr.get_value()),
            color=T.Q_COL, font_size=40)
        rbox = RoundedRectangle(corner_radius=0.12,
                                width=readout.width + 0.55,
                                height=readout.height + 0.45,
                                stroke_color=GREY_D, stroke_width=1.2,
                                fill_color=T.CARD_FILL, fill_opacity=0.9)
        rgrp = VGroup(rbox, readout)
        rbox.move_to(readout.get_center())
        rgrp.move_to(np.array([5.15, -3.15, 0]))  # below the L axis label

        self.play(FadeIn(dot), FadeIn(tan), FadeIn(rgrp), run_time=1.0)
        self.wait(0.7)
        self.play(tr.animate.set_value(8.0), run_time=6.5,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.6)
        self.play(tr.animate.set_value(5.2), run_time=2.0,
                  rate_func=rate_functions.ease_in_out_sine)

        dim = Text("diminishing MRTS — isoquants are convex to the origin",
                   font_size=26, color=T.Q_COL).to_edge(UP, buff=0.35)
        twin = Text("(Nicholson & Snyder call it RTS · the consumer twin is MRS)",
                    font_size=20, color=GREY_B).next_to(dim, DOWN, buff=0.18)
        self.play(Write(dim), run_time=1.2)
        self.play(FadeIn(twin), run_time=0.8)
        self.wait(2.4)

        # ---- restore the family for the homotheticity scene ----------------
        self.play(FadeOut(dot), FadeOut(tan), FadeOut(rgrp), FadeOut(card),
                  FadeOut(cf), FadeOut(box), FadeOut(dim), FadeOut(twin),
                  *[c.animate.set_stroke(opacity=1.0) for c in curves[:3]],
                  *[l.animate.set_opacity(1.0) for l in labels[:3]],
                  run_time=1.2)
        self.wait(0.5)
