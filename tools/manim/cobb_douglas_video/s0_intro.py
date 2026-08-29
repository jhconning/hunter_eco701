"""S0 — branding cold open (~13 s). Reusable pattern for the whole series."""
from manim import *
import theme as T


class Intro(T.PacedScene):
    episode_line = "Producer Theory I · The Cobb-Douglas Production Function"

    def construct(self):
        grp, series, sub, flourish, episode = T.branding_card(self.episode_line)

        self.play(Write(series), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)
        self.wait(0.3)
        ax, curves = flourish
        self.play(Create(ax), run_time=0.8)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3),
                  run_time=2.0)
        self.play(FadeIn(episode, shift=UP * 0.2), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(grp), run_time=0.8)
        self.wait(0.3)
