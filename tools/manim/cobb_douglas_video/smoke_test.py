"""Toolchain smoke test: MathTex (latex->dvisvgm), Text (pango), 3D surface, encode."""
from manim import *
import theme as T
import params as P


class SmokeTest(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes(x_range=[0, 4, 1], y_range=[0, 4, 1], z_range=[0, 3, 1],
                          x_length=6, y_length=6, z_length=3)
        surf = Surface(
            lambda u, v: axes.c2p(u, v, P.F(v, u)),
            u_range=[P.DOM_MIN, 4], v_range=[P.DOM_MIN, 4],
            resolution=(16, 16), fill_opacity=0.7,
        )
        surf.set_fill_by_value(axes=axes, colorscale=[(BLUE_D, 0), (TEAL_C, 1), (YELLOW, 2)], axis=2)

        title = T.colorize(MathTex(r"q = A K^{\alpha} L^{\beta}",
                                   substrings_to_isolate=list(T.CD_COLOR_MAP.keys())))
        label = Text("smoke test — pango text", font_size=24, color=GREY_A)
        hud = VGroup(title, label).arrange(DOWN).to_corner(UL)
        self.add_fixed_in_frame_mobjects(hud)

        self.play(Create(axes), Write(hud), run_time=1.5)
        self.play(Create(surf), run_time=1.5)
        self.wait(0.5)
