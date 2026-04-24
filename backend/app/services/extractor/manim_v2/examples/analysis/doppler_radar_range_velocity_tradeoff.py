from manim import *
import numpy as np


class DopplerRadarRangeVelocityTradeoff(Scene):
    """Doppler radar faces a fundamental uncertainty: short pulse -> good
    range resolution but bad velocity (few cycles to detect Doppler shift),
    long pulse -> accurate velocity but coarse range.  Show two cases
    side by side: SHORT (sigma = 0.3) and LONG (sigma = 1.5), with time
    pulse on top and frequency echo on bottom."""

    def construct(self):
        title = Tex(
            r"Radar tradeoff: range vs velocity resolution",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def make_case(center_x, sigma, color, label, range_word, vel_word):
            ax_t = Axes(
                x_range=[-3, 3, 1], y_range=[-1.1, 1.1, 0.5],
                x_length=5.2, y_length=2.0,
                tips=False,
                axis_config={"stroke_width": 1.2, "include_ticks": True},
            ).move_to([center_x, 1.3, 0])
            ax_f = Axes(
                x_range=[0, 10, 2], y_range=[0, 1.1, 0.5],
                x_length=5.2, y_length=2.0,
                tips=False,
                axis_config={"stroke_width": 1.2, "include_ticks": True},
            ).move_to([center_x, -1.6, 0])
            f0 = 4.0
            time_curve = ax_t.plot(
                lambda t: np.exp(-t ** 2 / (2 * sigma ** 2))
                * np.cos(2 * np.pi * f0 * t),
                x_range=[-3, 3, 0.01],
                color=color, stroke_width=2,
            )
            env = ax_t.plot(
                lambda t: np.exp(-t ** 2 / (2 * sigma ** 2)),
                x_range=[-3, 3, 0.02],
                color=color, stroke_width=1,
                stroke_opacity=0.5,
            )
            fwid = 1.0 / (2 * np.pi * sigma)
            spec = ax_f.plot(
                lambda f: np.exp(-(f - f0) ** 2 / (2 * fwid ** 2)),
                x_range=[0, 10, 0.02],
                color=color, stroke_width=2,
            )
            cap = Tex(label, font_size=26, color=color).move_to(
                [center_x, 2.6, 0]
            )
            time_lab = Tex(
                rf"\textbf{{{range_word}}}", font_size=22, color=color,
            ).next_to(ax_t, DOWN, buff=0.1).shift(LEFT * 1.8)
            vel_lab = Tex(
                rf"\textbf{{{vel_word}}}", font_size=22, color=color,
            ).next_to(ax_f, DOWN, buff=0.1).shift(LEFT * 1.8)
            return VGroup(ax_t, ax_f, time_curve, env, spec, cap,
                          time_lab, vel_lab)

        short_case = make_case(
            center_x=-3.3, sigma=0.3, color=BLUE,
            label="Short pulse",
            range_word="sharp range",
            vel_word="broad velocity",
        )
        long_case = make_case(
            center_x=3.3, sigma=1.5, color=RED,
            label="Long pulse",
            range_word="fuzzy range",
            vel_word="sharp velocity",
        )
        self.play(FadeIn(short_case))
        self.play(FadeIn(long_case))

        product_note = MathTex(
            r"\sigma_t \cdot \sigma_f \ge \tfrac{1}{4\pi}"
            r"\quad\Rightarrow\quad"
            r"\text{range-velocity tradeoff is unavoidable}",
            font_size=26, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(Write(product_note))
        self.wait(1.5)
