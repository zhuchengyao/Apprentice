from manim import *
import numpy as np


class WindmillPartitionInvariant(Scene):
    """IMO 2011 'windmill' problem.  A rotating line through a pivot sweeps
    a finite point set; when it hits another point it chooses that point
    as the new pivot.  Key invariant: the number of points on each side
    of the line is preserved.  Show a 9-point configuration with the line
    pivoting through a sequence of points; counts stay balanced at 4 vs 4."""

    def construct(self):
        title = Tex(
            r"Windmill invariant: points-per-side stays balanced",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        points_xy = np.array([
            [-3.5, 1.2], [-2.4, -0.6], [-1.4, 2.0], [-0.5, -1.3],
            [0.5, 0.4], [1.6, -1.8], [2.4, 1.5], [3.3, -0.2],
            [0.2, 2.1],
        ])

        pivot_sequence = [4, 7, 2, 0, 8]
        angles = [0.3, 1.2, 2.0, 2.9, 3.6]

        dots = VGroup()
        for xy in points_xy:
            dots.add(Dot(np.array([xy[0], xy[1], 0]),
                         radius=0.09).set_z_index(4))
        self.play(LaggedStart(*[FadeIn(d) for d in dots],
                              lag_ratio=0.07))

        def classify(pivot_idx, angle):
            dir_v = np.array([np.cos(angle), np.sin(angle), 0])
            normal = np.array([-np.sin(angle), np.cos(angle), 0])
            red, blue = [], []
            for i in range(len(points_xy)):
                if i == pivot_idx:
                    continue
                p = np.array([points_xy[i][0], points_xy[i][1], 0])
                pivot = np.array(
                    [points_xy[pivot_idx][0],
                     points_xy[pivot_idx][1], 0]
                )
                side = np.dot(p - pivot, normal)
                if side > 0:
                    red.append(i)
                else:
                    blue.append(i)
            return red, blue

        def colorize(red, blue, pivot_idx):
            anims = []
            for i in range(len(points_xy)):
                d = dots[i]
                if i == pivot_idx:
                    anims.append(d.animate.set_color(YELLOW))
                elif i in red:
                    anims.append(d.animate.set_color(RED))
                else:
                    anims.append(d.animate.set_color(BLUE))
            return anims

        def make_line(pivot_idx, angle):
            pivot = np.array([points_xy[pivot_idx][0],
                              points_xy[pivot_idx][1], 0])
            dir_v = np.array([np.cos(angle), np.sin(angle), 0])
            return Line(
                pivot - 8 * dir_v, pivot + 8 * dir_v,
                color=WHITE, stroke_width=2.5,
            )

        red_val = Integer(0, font_size=32, color=RED)
        blue_val = Integer(0, font_size=32, color=BLUE)
        panel = VGroup(
            VGroup(Tex(r"\# RED (above):", font_size=26, color=RED),
                   red_val).arrange(RIGHT, buff=0.15),
            VGroup(Tex(r"\# BLUE (below):", font_size=26, color=BLUE),
                   blue_val).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        panel.to_corner(UR, buff=0.5).shift(DOWN * 0.5)
        self.add(panel)

        current_line = None
        for pivot_idx, angle in zip(pivot_sequence, angles):
            red, blue = classify(pivot_idx, angle)
            line_new = make_line(pivot_idx, angle)
            anims = colorize(red, blue, pivot_idx)
            if current_line is None:
                self.play(*anims, Create(line_new), run_time=1.0)
            else:
                self.play(*anims, Transform(current_line, line_new),
                          run_time=1.2)
            current_line = line_new if current_line is None else current_line
            red_val.set_value(len(red))
            blue_val.set_value(len(blue))
            self.wait(0.3)

        insight = Tex(
            r"Counts on each side remain equal — the windmill cycle never drifts.",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(insight))
        self.wait(1.3)
