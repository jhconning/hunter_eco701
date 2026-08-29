"""S1 — univariate warm-up (~70 s).

Profit example straight from the lecture slides (MC1): pi(q) = 10q - 10 - q^2.
FOC as a flat tangent at the top; minimum counterexample; SOC.
"""
from manim import *
import theme as T


def PI(q):
    return 10 * q - 10 - q * q


def DPI(q):
    return 10 - 2 * q


def G(x):  # counterexample: same FOC, but a minimum
    return x * x - 10 * x + 20


def DG(x):
    return 2 * x - 10


class Warmup1D(T.PacedScene):
    def construct(self):
        title = Text("Warm-up: choosing one number", weight=BOLD,
                     font_size=34).to_edge(UP, buff=0.4)

        axes = Axes(
            x_range=[0, 10.5, 2], y_range=[-12, 22, 10],
            x_length=6.4, y_length=4.6,
            axis_config={"color": GREY_C, "include_numbers": False,
                         "tip_width": 0.18, "tip_height": 0.18},
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        xlab = MathTex("q", font_size=34, color=T.Q_COL).next_to(
            axes.x_axis.get_end(), DR, buff=0.15)
        ylab = MathTex(r"\pi", font_size=34).next_to(
            axes.y_axis.get_end(), UL, buff=0.15)

        curve = axes.plot(PI, x_range=[0.15, 9.85], color=T.Q_COL,
                          stroke_width=4)
        formula = MathTex(r"\pi(q) = 10\,q - 10 - q^2",
                          font_size=40).to_corner(UR, buff=0.6).shift(
                              DOWN * 0.85)  # clear of the scene title

        self.play(Write(title), run_time=1.2)
        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=1.4)
        self.play(Create(curve), Write(formula), run_time=1.8)
        self.wait(1.0)
        self.play(FadeOut(title), run_time=0.5)

        # live tangent riding the profit hill
        tr = ValueTracker(1.2)
        dot = T.moving_dot(axes, PI, tr)
        tan = T.moving_tangent(axes, PI, DPI, tr, half_len=1.1)
        readout = T.live_readout(r"\text{slope} = \pi'(q) =",
                                 lambda: DPI(tr.get_value()), color=T.TAN_COL)
        readout.next_to(formula, DOWN, buff=0.4).align_to(formula, RIGHT)

        self.play(FadeIn(dot), FadeIn(tan), FadeIn(readout), run_time=0.9)
        self.wait(0.6)
        self.play(tr.animate.set_value(5.0), run_time=5.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(Flash(axes.c2p(5, PI(5)), color=T.Q_COL, flash_radius=0.5),
                  run_time=0.8)

        vline = DashedLine(axes.c2p(5, 0), axes.c2p(5, PI(5)), color=GREY_B)
        qstar = MathTex("q^* = 5", font_size=34).next_to(axes.c2p(5, 0), DOWN,
                                                         buff=0.2)
        self.play(Create(vline), Write(qstar), run_time=1.2)

        foc = T.definition_card("First-order condition",
                                r"\pi'(q^*) = 0",
                                "necessary at an interior maximum")
        foc.scale(0.85).to_corner(DR, buff=0.45)
        self.play(FadeIn(foc, shift=UP * 0.25), run_time=1.0)
        self.wait(2.6)

        # counterexample: same flat tangent, a minimum
        inset = Axes(
            x_range=[0, 10.5, 5], y_range=[-8, 24, 10],
            x_length=3.0, y_length=2.1,
            axis_config={"color": GREY_D, "include_ticks": False,
                         "tip_width": 0.12, "tip_height": 0.12},
        ).next_to(formula, DOWN, buff=0.85).align_to(formula, RIGHT)
        gcurve = inset.plot(G, x_range=[0.4, 9.6], color=BLUE_C,
                            stroke_width=3)
        gdot = Dot(inset.c2p(5, G(5)), color=BLUE_C, radius=0.05)
        gtan = Line(inset.c2p(3.4, G(5)), inset.c2p(6.6, G(5)),
                    color=T.TAN_COL, stroke_width=3)
        gcap = Text("same condition — a minimum", font_size=18,
                    color=GREY_A).next_to(inset, DOWN, buff=0.15)
        self.play(FadeOut(readout), Create(inset), Create(gcurve),
                  run_time=1.4)
        self.play(FadeIn(gdot), Create(gtan), FadeIn(gcap), run_time=1.0)
        self.wait(2.0)

        soc = T.definition_card("Second-order condition",
                                r"\pi''(q^*) < 0",
                                "curvature separates tops from bottoms")
        soc.scale(0.85).to_corner(DR, buff=0.45)
        self.play(FadeOut(foc, shift=DOWN * 0.2),
                  FadeIn(soc, shift=UP * 0.2), run_time=1.1)
        self.wait(2.4)

        # bridge to two inputs
        bridge = Text("But firms choose bundles: capital K and labor L",
                      font_size=28, color=T.Q_COL).to_edge(DOWN, buff=0.5)
        keep = VGroup(axes, xlab, ylab, curve, vline, qstar, formula, inset,
                      gcurve, gdot, gtan, gcap, soc)
        self.play(Write(bridge), run_time=1.4)
        self.wait(2.0)
        self.play(FadeOut(keep), FadeOut(bridge), FadeOut(dot), FadeOut(tan),
                  run_time=1.0)
        self.wait(0.3)
