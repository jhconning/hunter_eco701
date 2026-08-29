"""Shared design system for the Eco 701 video series (import in every scene file).

Conventions (locked across videos):
  labor L = blue, capital K = green, output q = yellow, tangents = red,
  alpha = teal, beta = light purple, A (TFP) = grey.
Axis convention: L on x, K on y, q on z — everywhere.
"""
from manim import *

# ---------------------------------------------------------------- palette --
BG = "#171717"
L_COL = BLUE_C          # labor
K_COL = GREEN_C         # capital
Q_COL = YELLOW          # output / emphasis
TAN_COL = RED_C         # tangent lines
ALPHA_COL = TEAL_C
BETA_COL = "#c791e0"    # soft purple (manim PURPLE is too dark on BG)
A_COL = GREY_B
CARD_FILL = "#222222"
CARD_EDGE = GREY_B

# isoquant family colors, low output -> high output (warm ramp)
ISO_COLS = [YELLOW_A, GOLD_B, ORANGE, RED_B]

config.background_color = BG

# Map symbol substrings -> colors for MathTex(..., substrings_to_isolate=...) use
CD_COLOR_MAP = {
    "q": Q_COL, "A": A_COL, "K": K_COL, "L": L_COL,
    r"\alpha": ALPHA_COL, r"\beta": BETA_COL,
}


def colorize(mtex: MathTex) -> MathTex:
    """Apply the standard symbol colors to a MathTex built with isolated substrings.

    WARNING: substrings_to_isolate=list(CD_COLOR_MAP) splits on bare 'q', 'A',
    'K', 'L' — which corrupts any LaTeX command containing those letters.
    In isolated strings NEVER use: \\quad, \\qquad, \\sqrt (contain 'q'),
    \\Leftrightarrow/\\Longrightarrow (contain 'L'), or \\text{...} holding
    those capitals. Use \\;\\; for spacing and ^{1/2} instead of \\sqrt, or
    leave the formula un-colorized. Accents/scripts on colored letters need
    braces: \\bar{q} and F_{K}, never \\bar q or F_K (isolation inserts
    \\special before the letter, which the accent/script grabs instead).
    """
    mtex.set_color_by_tex_to_color_map(CD_COLOR_MAP)
    return mtex


# ----------------------------------------------------------------- pacing --
# Animations are authored at "reading speed"; narration needs longer holds.
# PACE multiplies wait() durations only — play() run_times are untouched.
PACE = 4.0


class PacedScene(Scene):
    def wait(self, duration=1.0, **kwargs):
        return super().wait(duration * PACE, **kwargs)


class PacedThreeDScene(ThreeDScene):
    def wait(self, duration=1.0, **kwargs):
        return super().wait(duration * PACE, **kwargs)


# ------------------------------------------------------------------ cards --
def definition_card(title: str, formula: str, plain: str, formula_size=44) -> VGroup:
    """Consistent 'definition card': title, one formula, one plain-English line."""
    tt = Text(title, weight=BOLD, font_size=28, color=Q_COL)
    ff = colorize(MathTex(formula, font_size=formula_size,
                          substrings_to_isolate=list(CD_COLOR_MAP.keys())))
    pp = Text(plain, font_size=20, color=GREY_A)
    content = VGroup(tt, ff, pp).arrange(DOWN, buff=0.28)
    box = RoundedRectangle(
        corner_radius=0.15,
        width=content.width + 0.7, height=content.height + 0.55,
        stroke_color=CARD_EDGE, stroke_width=1.5,
        fill_color=CARD_FILL, fill_opacity=0.9,
    )
    content.move_to(box.get_center())
    return VGroup(box, content)


# ------------------------------------------------- live tangent machinery --
def moving_dot(axes, f, tracker, color=Q_COL, radius=0.07):
    return always_redraw(
        lambda: Dot(axes.c2p(tracker.get_value(), f(tracker.get_value())),
                    color=color, radius=radius)
    )


def moving_tangent(axes, f, fprime, tracker, half_len=1.2, color=TAN_COL,
                   stroke_width=3.5):
    """Tangent segment through (x, f(x)) with slope f'(x), updating with tracker."""
    def build():
        x0 = tracker.get_value()
        y0, m = f(x0), fprime(x0)
        return Line(axes.c2p(x0 - half_len, y0 - m * half_len),
                    axes.c2p(x0 + half_len, y0 + m * half_len),
                    color=color, stroke_width=stroke_width)
    return always_redraw(build)


def live_readout(label_tex: str, value_fn, color=WHITE, num_decimal_places=2,
                 font_size=36):
    """'label = 1.23' group whose number tracks value_fn()."""
    label = MathTex(label_tex, font_size=font_size)
    num = DecimalNumber(value_fn(), num_decimal_places=num_decimal_places,
                        font_size=font_size, color=color)
    num.next_to(label, RIGHT, buff=0.15)
    num.add_updater(lambda m: m.set_value(value_fn()))
    return VGroup(label, num)


def example_badge() -> VGroup:
    """Small persistent 'running example' chip, bottom-left."""
    txt = MathTex(r"\text{running example:}\;\; q=\sqrt{K L}\;\;(A{=}1,\ \alpha{=}\beta{=}\tfrac12)",
                  font_size=26, color=GREY_A)
    box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.4,
                           height=txt.height + 0.3, stroke_color=GREY_D,
                           stroke_width=1.2, fill_color=CARD_FILL,
                           fill_opacity=0.85)
    txt.move_to(box.get_center())
    return VGroup(box, txt).to_corner(DL, buff=0.35)


# --------------------------------------------------------------- branding --
SERIES_TITLE = "ECO 701 · Microeconomic Theory"
SERIES_SUB = "Hunter College · CUNY"


def _iso_flourish(color=Q_COL):
    """Small decorative isoquant sweep used on the branding cards."""
    ax = Axes(x_range=[0.25, 4, 1], y_range=[0.25, 4, 1],
              x_length=3.0, y_length=2.2,
              axis_config={"include_ticks": False, "stroke_width": 2,
                           "color": GREY_C, "tip_width": 0.15,
                           "tip_height": 0.15})
    curves = VGroup(*[
        ax.plot(lambda x, q=q: q / x, x_range=[q / 3.8, 3.8], color=c,
                stroke_width=3)
        for q, c in zip([0.9, 1.8, 3.2], [BLUE_D, TEAL_C, YELLOW])
    ])
    return VGroup(ax, curves)


def branding_card(episode_line: str):
    series = Text(SERIES_TITLE, weight=BOLD, font_size=44)
    sub = Text(SERIES_SUB, font_size=26, color=GREY_A)
    episode = Text(episode_line, font_size=30, color=Q_COL)
    flourish = _iso_flourish()
    top = VGroup(series, sub).arrange(DOWN, buff=0.25)
    grp = VGroup(top, flourish, episode).arrange(DOWN, buff=0.55)
    return grp, series, sub, flourish, episode
