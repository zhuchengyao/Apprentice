from manim import *
import numpy as np


class GaussianIntegerLatticeRingCount(Scene):
    """Gaussian integers on the complex plane. ValueTracker r2_tr steps through
    r^2 = 1, 2, 4, 5, 8, 9, 10, 13, 16, 17, 18, 20, 25. For each r^2 a YELLOW
    circle of radius sqrt(r^2) is drawn and every lattice point (a, b) with
    a^2 + b^2 = r^2 is highlighted RED.  Right panel shows the integer count
    of such points — the classic 4 * (d_1(n) - d_3(n)) formula counts them.
    """

    def construct(self):
        title = Tex(
            r"Lattice points on circles: $a^2 + b^2 = r^2$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-6, 6, 1],
            x_length=6.8, y_length=6.8,
            background_line_style={"stroke_opacity": 0.25},
        ).shift(LEFT * 2.2 + DOWN * 0.15)
        origin = plane.c2p(0, 0)
        unit = plane.c2p(1, 0)[0] - origin[0]
        self.play(Create(plane))

        lattice_pts = {}
        dots = VGroup()
        for a in range(-5, 6):
            for b in range(-5, 6):
                if a * a + b * b > 25:
                    continue
                d = Dot(plane.c2p(a, b), radius=0.055, color=BLUE)
                lattice_pts[(a, b)] = d
                dots.add(d)
        self.play(LaggedStart(*[FadeIn(d) for d in dots],
                              lag_ratio=0.005, run_time=1.5))

        r2_tr = ValueTracker(1.0)

        def get_ring():
            r2 = r2_tr.get_value()
            r = np.sqrt(max(r2, 1e-3))
            return Circle(radius=r * unit, color=YELLOW,
                          stroke_width=3).move_to(origin)

        highlighted = VGroup()

        def highlight_for(r2_val):
            nonlocal highlighted
            hits = []
            tol = 1e-6
            for (a, b), d in lattice_pts.items():
                if abs(a * a + b * b - r2_val) < tol:
                    ring_dot = Dot(
                        plane.c2p(a, b), radius=0.09, color=RED,
                    ).set_z_index(4)
                    hits.append(ring_dot)
            return VGroup(*hits)

        ring = always_redraw(get_ring)
        self.add(ring)

        panel = VGroup()
        r2_label = VGroup(
            MathTex(r"r^2 =", font_size=30),
            Integer(1, font_size=30),
        ).arrange(RIGHT, buff=0.12)
        count_label = VGroup(
            Tex("count:", font_size=28),
            Integer(0, font_size=30, color=YELLOW),
        ).arrange(RIGHT, buff=0.12)
        panel = VGroup(r2_label, count_label).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3,
        )
        panel.to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        self.add(panel)

        sequence = [1, 2, 4, 5, 8, 9, 10, 13, 16, 17, 18, 20, 25]
        for r2 in sequence:
            self.play(r2_tr.animate.set_value(r2), run_time=0.5)
            new_highlights = highlight_for(r2)
            r2_label[1].set_value(r2)
            count_label[1].set_value(len(new_highlights))
            self.play(FadeOut(highlighted), FadeIn(new_highlights),
                      run_time=0.4)
            highlighted = new_highlights
            self.wait(0.35)

        self.wait(1.2)
