"""S7 — recap + outro branding (~25 s)."""
from manim import *
import theme as T

ISO = list(T.CD_COLOR_MAP.keys())


class Outro(T.PacedScene):
    def construct(self):
        title = Text("What we built", weight=BOLD, font_size=36,
                     color=T.Q_COL).to_edge(UP, buff=0.5)

        rows_spec = [
            (r"q = A\, K^{\alpha} L^{\beta}",
             "the Cobb-Douglas production function"),
            (r"F(tK,\, tL) = t^{\alpha+\beta} F(K, L)",
             "homogeneous of degree α + β  →  returns to scale"),
            (r"\{\,(K, L) : F(K, L) = \bar{q}\,\}",
             "isoquants: horizontal slices of the surface"),
            (r"\text{MRTS} = \frac{F_{L}}{F_{K}} = \frac{\beta}{\alpha}\cdot\frac{K}{L}",
             "the slope of an isoquant, and it diminishes"),
            (r"\text{MRTS}(tK,\, tL) = \text{MRTS}(K,\, L)",
             "homothetic: same slope along every ray"),
        ]
        rows = VGroup()
        for tex, desc in rows_spec:
            f = T.colorize(MathTex(tex, font_size=32,
                                   substrings_to_isolate=ISO))
            d = Text(desc, font_size=22, color=GREY_A)
            rows.add(VGroup(f, d))
        for r in rows:
            r.arrange(RIGHT, buff=0.6)
        # align: formulas right-aligned, descriptions left-aligned
        rows.arrange(DOWN, buff=0.42)
        for r in rows:
            r[0].align_to(np.array([-0.4, 0, 0]), RIGHT)
            r[1].align_to(np.array([0.2, 0, 0]), LEFT)
        rows.next_to(title, DOWN, buff=0.55)

        self.play(Write(title), run_time=1.0)
        for r in rows:
            self.play(FadeIn(r[0], shift=RIGHT * 0.2), FadeIn(r[1]),
                      run_time=0.75)
            self.wait(0.35)
        self.wait(2.2)
        self.play(FadeOut(rows), FadeOut(title), run_time=0.9)

        # ---- closing branding card ------------------------------------------
        grp, series, sub, flourish, episode = T.branding_card(
            "Next episode · Constrained Optimization & the Method of Lagrange")
        self.play(FadeIn(VGroup(series, sub), shift=UP * 0.2), run_time=1.0)
        ax, curvs = flourish
        self.play(Create(ax), LaggedStart(*[Create(c) for c in curvs],
                                          lag_ratio=0.25), run_time=1.6)
        self.play(FadeIn(episode, shift=UP * 0.2), run_time=0.9)
        self.wait(2.5)
        self.play(FadeOut(grp), run_time=1.0)
        self.wait(0.4)
