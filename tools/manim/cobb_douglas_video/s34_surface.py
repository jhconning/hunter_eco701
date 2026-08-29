"""S3+S4 — one continuous ThreeDScene (~2.5 min).

Surface reveal + orbit -> fixed-K slice (partial derivative / MP_L) ->
horizontal planes slice out isoquants, projected to the floor ->
camera flattens overhead: the surface BECOMES the 2D isoquant map.
Axis convention (locked): L on x, K on y, q on z.
"""
from manim import *
import theme as T
import params as P

RES = (36, 36)


class SurfaceToIsoquants(T.PacedThreeDScene):
    def construct(self):
        # ------------------------------------------------ axes and surface --
        axes = ThreeDAxes(
            x_range=[0, 10, 2], y_range=[0, 10, 2], z_range=[0, 10, 2],
            x_length=7.0, y_length=7.0, z_length=3.8,
            axis_config={"color": GREY_B, "include_ticks": True,
                         "tip_width": 0.18, "tip_height": 0.18},
        )
        # L/K labels lie flat in the floor plane (they read perfectly once the
        # camera flattens overhead); q stands upright in the x-z plane.
        xlab = MathTex("L", font_size=44, color=T.L_COL).move_to(
            axes.c2p(10.55, 0.8, 0))
        ylab = MathTex("K", font_size=44, color=T.K_COL).move_to(
            axes.c2p(-0.8, 10.7, 0))
        zlab = MathTex("q", font_size=44, color=T.Q_COL).rotate(
            90 * DEGREES, axis=RIGHT).move_to(axes.c2p(0, -0.8, 9.2))
        # upright K for the 3D phase (the flat one hides behind the surface
        # until the camera goes overhead)
        kup = MathTex("K", font_size=44, color=T.K_COL).rotate(
            90 * DEGREES, axis=RIGHT).move_to(axes.c2p(-0.7, 10.2, 0.9))

        def srf_point(u, v):  # u = L, v = K
            return axes.c2p(u, v, P.F(v, u))

        surf = Surface(srf_point, u_range=[P.DOM_MIN, P.DOM_MAX],
                       v_range=[P.DOM_MIN, P.DOM_MAX], resolution=RES,
                       fill_opacity=0.75, stroke_width=0.4)
        surf.set_fill_by_value(axes=axes, axis=2,
                               colorscale=[(BLUE_D, 0), (TEAL_C, 4.5),
                                           (YELLOW, 9)])

        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES,
                                    zoom=0.9)

        hud_eq = T.colorize(MathTex(r"q = F(K, L) = K^{1/2} L^{1/2}",
                                    font_size=38,
                                    substrings_to_isolate=list(T.CD_COLOR_MAP)))
        hud_eq.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(hud_eq)
        hud_eq.set_opacity(0)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), FadeIn(zlab),
                  FadeIn(kup), run_time=2.0)
        self.play(hud_eq.animate.set_opacity(1), run_time=0.8)
        self.play(Create(surf), run_time=3.2)

        # orbit while the two structural call-outs appear
        note1 = Text("increasing in both inputs", font_size=26,
                     color=GREY_A).to_corner(UR, buff=0.5)
        note2 = Text("concave — it curves over as it grows", font_size=26,
                     color=GREY_A).to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(note1)
        note1.set_opacity(0)
        # slow rate: with PACE-stretched waits the orbit runs ~23 s; keep the
        # total drift ≈ -20 degrees so theta stays in the good viewing band
        self.begin_ambient_camera_rotation(rate=-0.016)
        self.play(note1.animate.set_opacity(1), run_time=0.8)
        self.wait(3.2)
        self.add_fixed_in_frame_mobjects(note2)
        note2.set_opacity(0)
        self.play(note1.animate.set_opacity(0),
                  note2.animate.set_opacity(1), run_time=0.9)
        self.wait(3.2)
        self.stop_ambient_camera_rotation()
        self.play(note2.animate.set_opacity(0), run_time=0.6)

        # ------------------------------- fixed-K slice: partial derivative --
        # face the K=4 plane (its normal is +y) more frontally
        self.move_camera(phi=66 * DEGREES, theta=-78 * DEGREES, run_time=2.0)
        K0 = 4.0
        slice_plane = Surface(
            lambda u, v: axes.c2p(u, K0, v),
            u_range=[P.DOM_MIN, P.DOM_MAX], v_range=[0, 6.8],
            resolution=(1, 1), fill_opacity=0.18, stroke_width=0,
            fill_color=GREY_B)
        slice_curve = ParametricFunction(
            lambda t: axes.c2p(t, K0, P.F(K0, t)),
            t_range=[P.DOM_MIN, P.DOM_MAX], color=WHITE, stroke_width=5)

        note3 = VGroup(
            Text("hold K = 4 fixed → one-variable curve", font_size=26,
                 color=GREY_A),
            T.colorize(MathTex(
                r"\frac{\partial q}{\partial L} = \text{marginal product of labor}"
                r"\;\;(\text{diminishing})",
                font_size=32, substrings_to_isolate=[r"q", r"L"])),
        ).arrange(DOWN, buff=0.25).to_corner(UR, buff=0.4)
        self.add_fixed_in_frame_mobjects(note3)
        note3.set_opacity(0)

        self.play(FadeIn(slice_plane), run_time=1.2)
        self.play(Create(slice_curve), note3.animate.set_opacity(1),
                  run_time=1.6)

        ltr = ValueTracker(1.5)

        def slice_tangent():
            L0 = ltr.get_value()
            m = 0.5 * P.F(K0, L0) / L0          # dq/dL for q = 2 sqrt(L)
            return Line(axes.c2p(L0 - 1.1, K0, P.F(K0, L0) - 1.1 * m),
                        axes.c2p(L0 + 1.1, K0, P.F(K0, L0) + 1.1 * m),
                        color=T.TAN_COL, stroke_width=4.5)

        tan3d = always_redraw(slice_tangent)
        dot3d = always_redraw(lambda: Dot3D(
            axes.c2p(ltr.get_value(), K0, P.F(K0, ltr.get_value())),
            color=T.TAN_COL, radius=0.06))
        self.play(FadeIn(tan3d), FadeIn(dot3d), run_time=0.8)
        self.play(ltr.animate.set_value(7.5), run_time=4.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.8)
        self.play(FadeOut(tan3d), FadeOut(dot3d), FadeOut(slice_plane),
                  FadeOut(slice_curve), note3.animate.set_opacity(0),
                  run_time=1.1)

        # --------------------------------- isoquants: slice, glow, project --
        def iso_curve(qbar, z=None, **kw):
            z = qbar if z is None else z
            lmin = max(P.DOM_MIN, qbar**2 / P.DOM_MAX)
            return ParametricFunction(
                lambda t: axes.c2p(t, P.K_of_L(t, qbar), z),
                t_range=[lmin, P.DOM_MAX], **kw)

        def h_plane(qbar):
            return Surface(lambda u, v: axes.c2p(u, v, qbar),
                           u_range=[P.DOM_MIN, P.DOM_MAX],
                           v_range=[P.DOM_MIN, P.DOM_MAX],
                           resolution=(1, 1), fill_opacity=0.22,
                           stroke_width=0, fill_color=T.Q_COL)

        note4 = Text("slice horizontally at a fixed output level",
                     font_size=26, color=GREY_A).to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(note4)
        note4.set_opacity(0)

        # symmetric view; theta lands at -90 so the later flatten is a pure
        # phi move with no azimuth swing
        self.move_camera(phi=58 * DEGREES, theta=-90 * DEGREES, run_time=2.0)

        floor_isos = VGroup()

        # detailed first pass at qbar = 2
        qb = 2.0
        plane = h_plane(qb)
        dz = axes.c2p(0, 0, qb) - axes.c2p(0, 0, 0)
        plane.shift(-dz)                     # start on the floor
        self.play(FadeIn(plane), note4.animate.set_opacity(1), run_time=0.9)
        self.play(plane.animate.shift(dz), run_time=2.2)

        lift = iso_curve(qb, color=WHITE, stroke_width=5.5)
        self.play(Create(lift), run_time=1.8)
        self.wait(0.6)

        floor = iso_curve(qb, z=0, color=T.ISO_COLS[1], stroke_width=4.5)
        guides = VGroup(*[
            DashedLine(axes.c2p(l, P.K_of_L(l, qb), qb),
                       axes.c2p(l, P.K_of_L(l, qb), 0),
                       color=GREY_C, stroke_width=2)
            for l in [0.7, 2.0, 4.5, 8.0]])
        self.play(Create(guides), run_time=0.9)
        self.play(TransformFromCopy(lift, floor), run_time=1.8)
        self.play(FadeOut(guides), FadeOut(plane), note4.animate.set_opacity(0),
                  lift.animate.set_stroke(width=2.0, opacity=0.65),
                  run_time=0.9)
        floor_isos.add(floor)

        # rapid passes: qbar = 1, 3, 4
        for i, qb in enumerate([1.0, 3.0, 4.0]):
            plane = h_plane(qb)
            dz = axes.c2p(0, 0, qb) - axes.c2p(0, 0, 0)
            plane.shift(-dz)
            self.play(FadeIn(plane), run_time=0.4)
            self.play(plane.animate.shift(dz), run_time=1.0)
            lift = iso_curve(qb, color=WHITE, stroke_width=5.0)
            self.play(Create(lift), run_time=0.9)
            floor = iso_curve(qb, z=0,
                              color=T.ISO_COLS[0 if qb == 1 else i + 1],
                              stroke_width=4.5)
            self.play(TransformFromCopy(lift, floor), FadeOut(plane),
                      lift.animate.set_stroke(width=2.0, opacity=0.65),
                      run_time=1.1)
            floor_isos.add(floor)
        self.wait(0.8)

        # ----------------------------------- the flatten: 3D -> 2D overhead --
        note5 = Text("now look straight down…", font_size=28,
                     color=T.Q_COL).to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(note5)
        note5.set_opacity(0)
        self.play(note5.animate.set_opacity(1), run_time=0.8)

        self.move_camera(phi=32 * DEGREES, theta=-90 * DEGREES, run_time=2.5)
        self.play(surf.animate.set_opacity(0.28),
                  *[l.animate.set_stroke(opacity=0.3) for l in
                    [m for m in self.mobjects if isinstance(m, ParametricFunction)
                     and m not in floor_isos]],
                  run_time=1.0)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.8,
                         run_time=3.5)
        self.play(FadeOut(surf), FadeOut(zlab), FadeOut(kup),
                  FadeOut(axes.z_axis), FadeOut(hud_eq),
                  note5.animate.set_opacity(0),
                  *[FadeOut(m) for m in self.mobjects
                    if isinstance(m, ParametricFunction) and m not in floor_isos],
                  run_time=1.4)

        # level labels lying in the floor plane (read correctly from overhead)
        # labels sit on a diagonal ladder in the gaps between the curves
        lvl_labels = VGroup()
        for qb, col, (lx, ky) in zip(
                [1, 2, 3, 4],
                [T.ISO_COLS[0], T.ISO_COLS[1], T.ISO_COLS[2], T.ISO_COLS[3]],
                [(1.15, 2.2), (2.05, 3.2), (3.0, 4.2), (4.1, 5.2)]):
            lab = MathTex(rf"\bar q = {qb}", font_size=34, color=col)
            lab.move_to(axes.c2p(lx, ky, 0))
            lvl_labels.add(lab)
        self.play(LaggedStart(*[FadeIn(l) for l in lvl_labels],
                              lag_ratio=0.2), run_time=1.4)

        card = T.definition_card(
            "Isoquant",
            r"\{\,(K, L) \;:\; F(K, L) = \bar{q}\,\}",
            "all input mixes that produce the same output")
        card.scale(0.8)
        self.add_fixed_in_frame_mobjects(card)
        card.to_corner(DR, buff=0.4).set_opacity(0)
        self.play(card.animate.set_opacity(1), run_time=1.0)
        self.wait(2.2)

        twin = Text(
            "consumer-theory twin: indifference curves (fix utility, not output)",
            font_size=24, color=GREY_A)
        alias = Text("math name: level curves / contour lines", font_size=24,
                     color=GREY_C)
        notes = VGroup(twin, alias).arrange(DOWN, buff=0.18,
                                            aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(notes)
        notes.to_corner(UR, buff=0.45).set_opacity(0)
        self.play(notes.animate.set_opacity(1), run_time=0.9)
        self.wait(2.6)

        self.play(*[FadeOut(m) for m in [notes, card]], run_time=0.8)
        self.wait(0.5)
