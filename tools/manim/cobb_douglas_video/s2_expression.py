"""S2 — the Cobb-Douglas expression, symbol naming, homogeneity, RTS cases (~70 s)."""
from manim import *
import theme as T

ISO = list(T.CD_COLOR_MAP.keys())


class Expression(T.PacedScene):
    def construct(self):
        # ---- phase A: the expression, each symbol named -------------------
        eq = T.colorize(MathTex(r"q = A\, K^{\alpha} L^{\beta}",
                                font_size=64, substrings_to_isolate=ISO))
        eq.move_to(UP * 2.2)
        self.play(Write(eq), run_time=1.8)
        self.wait(0.5)

        legend_rows = [
            (r"q", "output", T.Q_COL),
            (r"A", "total factor productivity", T.A_COL),
            (r"K,\ L", "capital, labor", None),
            (r"\alpha,\ \beta", "output elasticities of K and L"
                                "   (both > 0)", None),
        ]
        legend = VGroup()
        for sym, desc, col in legend_rows:
            s = T.colorize(MathTex(sym, font_size=38,
                                   substrings_to_isolate=ISO))
            if col:
                s.set_color(col)
            d = Text(desc, font_size=24, color=GREY_A)
            row = VGroup(s, d).arrange(RIGHT, buff=0.45)
            legend.add(row)
        for row in legend:
            row[0].align_to(legend[0][0], RIGHT)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(
            eq, DOWN, buff=0.8)

        for (sym, _, _), row in zip(legend_rows, legend):
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.55)
        self.wait(1.2)

        # ---- phase B: scale both inputs by t ------------------------------
        self.play(FadeOut(legend), eq.animate.to_edge(UP, buff=0.5),
                  run_time=0.9)

        lines = VGroup(
            T.colorize(MathTex(r"F(tK,\, tL) = A\,(tK)^{\alpha}(tL)^{\beta}",
                               font_size=46, substrings_to_isolate=ISO)),
            T.colorize(MathTex(
                r"= t^{\alpha+\beta}\cdot A\, K^{\alpha} L^{\beta}",
                font_size=46, substrings_to_isolate=ISO)),
            T.colorize(MathTex(r"= t^{\alpha+\beta}\, F(K,\, L)",
                               font_size=46, substrings_to_isolate=ISO)),
        )
        lines.arrange(DOWN, buff=0.42)
        # nudge continuation lines right so they read as one derivation
        lines[1].align_to(lines[0], LEFT).shift(RIGHT * 2.1)
        lines[2].align_to(lines[0], LEFT).shift(RIGHT * 2.1)
        lines.move_to(UP * 0.9)

        self.play(Write(lines[0]), run_time=1.4)
        self.wait(0.8)
        self.play(Write(lines[1]), run_time=1.2)
        self.wait(0.6)
        self.play(Write(lines[2]), run_time=1.1)

        box = SurroundingRectangle(lines[2], color=T.Q_COL, buff=0.18,
                                   corner_radius=0.1)
        homog = Text("homogeneous of degree α + β", font_size=26,
                     color=T.Q_COL).next_to(box, DOWN, buff=0.3)
        self.play(Create(box), FadeIn(homog), run_time=1.0)
        self.wait(2.2)

        # ---- phase C: the three returns-to-scale cases ---------------------
        self.play(FadeOut(lines[0]), FadeOut(lines[1]),
                  VGroup(lines[2], box, homog).animate.scale(0.75).to_edge(
                      LEFT, buff=0.6).shift(UP * 1.6),
                  run_time=1.0)

        nl = NumberLine(x_range=[0.4, 1.6, 0.2], length=8.5,
                        include_numbers=False, color=GREY_B).move_to(
                            DOWN * 0.6)
        one_tick = MathTex(r"\alpha+\beta = 1", font_size=32).next_to(
            nl.n2p(1.0), DOWN, buff=0.35)
        marker = Triangle(color=T.Q_COL, fill_opacity=1).scale(0.12)
        marker.rotate(60 * DEGREES).next_to(nl.n2p(1.0), UP, buff=0.05)

        drs = VGroup(Text("decreasing", font_size=24, color=BLUE_C),
                     Text("returns to scale", font_size=18, color=GREY_A)
                     ).arrange(DOWN, buff=0.1).next_to(nl.n2p(0.62), UP,
                                                       buff=0.5)
        crs = VGroup(Text("constant", font_size=24, color=T.Q_COL),
                     Text("returns to scale", font_size=18, color=GREY_A)
                     ).arrange(DOWN, buff=0.1).next_to(nl.n2p(1.0), UP,
                                                       buff=0.85)
        irs = VGroup(Text("increasing", font_size=24, color=RED_C),
                     Text("returns to scale", font_size=18, color=GREY_A)
                     ).arrange(DOWN, buff=0.1).next_to(nl.n2p(1.38), UP,
                                                       buff=0.5)

        self.play(Create(nl), Write(one_tick), run_time=1.2)
        self.play(FadeIn(drs, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(crs, shift=UP * 0.15), FadeIn(marker), run_time=0.7)
        self.play(FadeIn(irs, shift=UP * 0.15), run_time=0.7)
        self.wait(2.4)

        # ---- phase D: specialize to the running example --------------------
        every = VGroup(nl, one_tick, drs, crs, irs, marker, lines[2], box,
                       homog)
        self.play(FadeOut(every), run_time=0.8)

        choose = T.colorize(MathTex(
            r"A = 1,\;\; \alpha = \beta = \tfrac{1}{2}", font_size=46,
            substrings_to_isolate=ISO)).move_to(UP * 1.3)
        sq_cd = T.colorize(MathTex(r"q = K^{1/2} L^{1/2}", font_size=60,
                                   substrings_to_isolate=ISO))
        sq_rt = MathTex(r"= \sqrt{K\,L}", font_size=60)  # plain: \sqrt can't be isolated
        sq = VGroup(sq_cd, sq_rt).arrange(RIGHT, buff=0.35)
        sq.next_to(choose, DOWN, buff=0.7)
        check = T.colorize(MathTex(
            r"F(1,4) = 2 \;\;\longrightarrow\;\; F(2,8) = 4",
            font_size=40, substrings_to_isolate=ISO)).next_to(
                sq, DOWN, buff=0.75)
        chk_cap = Text("double both inputs → double the output (CRS)",
                       font_size=24, color=GREY_A).next_to(check, DOWN,
                                                           buff=0.3)

        self.play(Write(choose), run_time=1.1)
        self.play(TransformFromCopy(eq, sq), run_time=1.4)
        self.wait(0.8)
        self.play(Write(check), run_time=1.1)
        self.play(FadeIn(chk_cap), run_time=0.8)
        self.wait(1.6)

        badge = T.example_badge()
        self.play(FadeIn(badge, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in [eq, choose, sq, check, chk_cap,
                                         badge]], run_time=1.0)
        self.wait(0.3)
