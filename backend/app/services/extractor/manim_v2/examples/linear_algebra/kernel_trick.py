from manim import *
import numpy as np


class KernelTrickExample(Scene):
    """
    Kernel trick: non-linearly separable data in ℝ² becomes linearly
    separable after a feature map φ: (x, y) → (x², y², √2 xy) in ℝ³.

    Data: concentric rings — inner class (BLUE) with r < 1, outer
    class (RED) with r > 1.5. After φ, the data separates by a
    plane: z = x² + y² = constant.

    TWO_COLUMN: LEFT axes with 2D dots; ValueTracker s_tr morphs
    them via always_redraw to 3D projection (axonometric) on RIGHT,
    and a separating plane z=1.25 appears.
    """

    def construct(self):
        title = Tex(r"Kernel trick: $\phi(x,y)=(x^2,y^2,\sqrt{2}\,xy)$ makes rings separable",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        np.random.seed(3)
        inner = []
        for _ in range(40):
            theta = np.random.uniform(0, TAU)
            r = np.random.uniform(0.3, 0.8)
            inner.append((r * np.cos(theta), r * np.sin(theta)))
        outer = []
        for _ in range(40):
            theta = np.random.uniform(0, TAU)
            r = np.random.uniform(1.5, 2.0)
            outer.append((r * np.cos(theta), r * np.sin(theta)))

        left_plane = NumberPlane(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
                                  x_length=4.8, y_length=4.8,
                                  background_line_style={"stroke_opacity": 0.3}
                                  ).shift(LEFT * 3.3)
        self.play(Create(left_plane))

        right_axes = ThreeDAxes(x_range=[0, 5, 1], y_range=[0, 5, 1], z_range=[-5, 5, 1],
                                x_length=4.0, y_length=4.0, z_length=4.0)
        # axonometric projection
        def proj(v):
            x, y, z = v
            P = np.array([x - 0.4 * y, z - 0.4 * y + 1.0, 0.0])
            return P * 0.42 + RIGHT * 2.5 + DOWN * 0.2

        # Draw right axes as arrows
        right_arrows = VGroup(
            Arrow(proj([0, 0, 0]), proj([5, 0, 0]), color=BLUE,
                   buff=0, stroke_width=2),
            Arrow(proj([0, 0, 0]), proj([0, 5, 0]), color=GREEN,
                   buff=0, stroke_width=2),
            Arrow(proj([0, 0, 0]), proj([0, 0, 5]), color=ORANGE,
                   buff=0, stroke_width=2),
            Tex(r"$x^2$", font_size=22, color=BLUE).move_to(proj([5.4, 0, 0])),
            Tex(r"$y^2$", font_size=22, color=GREEN).move_to(proj([0, 5.4, 0])),
            Tex(r"$\sqrt{2}xy$", font_size=22, color=ORANGE).move_to(proj([0, 0, 5.4])),
        )
        self.play(FadeIn(right_arrows))

        s_tr = ValueTracker(0.0)

        def data_dots():
            s = s_tr.get_value()
            grp = VGroup()
            for (x, y), col, r_class in \
                [(p, BLUE, "inner") for p in inner] + [(p, RED, "outer") for p in outer]:
                # left 2D position
                left_pos = left_plane.c2p(x, y)
                # right 3D → projected
                phi = np.array([x * x, y * y, np.sqrt(2) * x * y])
                right_pos = proj(phi)
                pos = (1 - s) * left_pos + s * right_pos
                grp.add(Dot(pos, color=col, radius=0.06))
            return grp

        self.add(always_redraw(data_dots))

        # Separating plane z = 1.25 in the 3D axonometric
        def sep_plane():
            s = s_tr.get_value()
            if s < 0.5:
                return VGroup()
            # approximate plane z = 1.25 as a parallelogram spanning
            # x² in [0, 5], y² in [0, 5]
            corners = [proj([0, 0, 1.25]),
                        proj([5, 0, 1.25]),
                        proj([5, 5, 1.25]),
                        proj([0, 5, 1.25])]
            return Polygon(*corners, color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.3 * (s - 0.5) * 2)

        self.add(always_redraw(sep_plane))

        # Info
        info = VGroup(
            Tex(r"inner ring: $r<0.8$", color=BLUE, font_size=20),
            Tex(r"outer ring: $r>1.5$", color=RED, font_size=20),
            Tex(r"linearly non-separable in $\mathbb{R}^2$",
                color=GREY_B, font_size=20),
            Tex(r"in $\phi$-space: $z=r^2$", font_size=22),
            VGroup(Tex(r"morph $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"separating plane $z=1.25$",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3).shift(LEFT * 0.5)
        info[4][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        self.add(info)

        self.play(s_tr.animate.set_value(1.0),
                  run_time=4, rate_func=smooth)
        self.wait(0.8)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=2, rate_func=smooth)
        self.play(s_tr.animate.set_value(1.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.8)
