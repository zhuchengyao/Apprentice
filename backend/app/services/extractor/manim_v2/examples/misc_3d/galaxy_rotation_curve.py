from manim import *
import numpy as np


class GalaxyRotationCurveExample(Scene):
    """
    Galaxy rotation curve: predicted Keplerian v(r) ∝ 1/√r falls off,
    observed v(r) stays flat — evidence for dark matter.

    TWO_COLUMN:
      LEFT  — galaxy top-down view with concentric stars; ValueTracker
              t_tr rotates each star at a different angular speed
              ω(r) = v(r) / r.
      RIGHT — v(r) plot: BLUE Keplerian vs ORANGE observed flat line.
    """

    def construct(self):
        title = Tex(r"Galaxy rotation: flat curves imply dark matter",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        gal_center = np.array([-3, -0.3, 0])

        # 24 stars at various radii
        rng = np.random.default_rng(20)
        radii = [0.5, 0.8, 1.0, 1.3, 1.6, 2.0]
        stars = []
        for r in radii:
            for k in range(4):
                theta0 = rng.uniform(0, 2 * PI)
                stars.append((r, theta0))

        v_flat = 1.0  # flat rotation curve value

        t_tr = ValueTracker(0.0)

        def star_dots():
            t = t_tr.get_value()
            grp = VGroup()
            # Observed flat rotation: ω(r) = v_flat / r
            for (r, theta0) in stars:
                theta = theta0 + v_flat / r * t
                p = gal_center + np.array([r * np.cos(theta),
                                               r * np.sin(theta), 0])
                grp.add(Dot(p, color=YELLOW, radius=0.08))
            return grp

        self.add(always_redraw(star_dots))

        center_dot = Dot(gal_center, color=WHITE, radius=0.12)
        self.play(FadeIn(center_dot))

        # RIGHT: v(r) plot
        ax = Axes(x_range=[0, 3, 0.5], y_range=[0, 1.5, 0.5],
                   x_length=5, y_length=3.5, tips=False,
                   axis_config={"font_size": 14}
                   ).move_to([3, -0.5, 0])
        r_lbl = MathTex(r"r", font_size=20).next_to(ax, DOWN, buff=0.1)
        v_lbl = MathTex(r"v(r)", font_size=20).next_to(ax, LEFT, buff=0.1)

        # Keplerian: v = k/√r (with k chosen to pass through (1, 1))
        kep_curve = ax.plot(lambda r: 1 / np.sqrt(max(r, 0.05)),
                              x_range=[0.1, 3, 0.02],
                              color=BLUE, stroke_width=3)
        # Observed: flat
        flat_curve = ax.plot(lambda r: v_flat,
                               x_range=[0.2, 3, 0.02],
                               color=ORANGE, stroke_width=3)

        self.play(Create(ax), Write(r_lbl), Write(v_lbl),
                   Create(kep_curve), Create(flat_curve))

        kep_lbl = Tex(r"Keplerian $v \propto 1/\sqrt r$",
                       color=BLUE, font_size=18
                       ).next_to(ax.c2p(2.8, 0.6), UP, buff=0.1)
        flat_lbl = Tex(r"observed (flat)", color=ORANGE, font_size=18
                        ).next_to(ax.c2p(2.8, 1.0), UP, buff=0.1)
        self.play(Write(kep_lbl), Write(flat_lbl))

        info = VGroup(
            Tex(r"stars rotate with $\omega(r) = v_{\text{flat}} / r$",
                 color=YELLOW, font_size=18),
            Tex(r"flat curve $\Rightarrow$ extra mass (dark matter)",
                 color=GREEN, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        self.play(Write(info))

        self.play(t_tr.animate.set_value(30),
                   run_time=10, rate_func=linear)
        self.wait(0.4)
