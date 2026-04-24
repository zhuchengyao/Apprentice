from manim import *
import numpy as np


class BanachFixedPointContractionExample(Scene):
    """
    Banach fixed-point: for contraction T: [a, b]→[a, b] with
    |T(x)−T(y)| ≤ L|x−y| (L<1), iterates x_{k+1}=T(x_k) converge
    to the unique fixed point.

    Example T(x) = cos(x) on [0, 1]. T is a contraction with
    L = sin(1) ≈ 0.841. Fixed point x* ≈ 0.7391.

    TWO_COLUMN: LEFT plot of T and y=x; cobweb diagram via ValueTracker
    k_tr reveals iterates. RIGHT shows |x_k - x*| shrinking like L^k.
    """

    def construct(self):
        title = Tex(r"Banach fixed-point: $T(x)=\cos x$ on $[0,1]$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1.1, 0.2], y_range=[0, 1.1, 0.2],
                    x_length=5.5, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        T_curve = axes.plot(lambda x: np.cos(x),
                             x_range=[0, 1], color=BLUE, stroke_width=3)
        y_x = axes.plot(lambda x: x, x_range=[0, 1],
                         color=GREY_B, stroke_width=2)
        self.play(Create(T_curve), Create(y_x))

        # Compute iterates
        x_star = 0.7390851332151607  # Dottie number
        x0 = 0.2
        iters = [x0]
        for _ in range(15):
            iters.append(np.cos(iters[-1]))

        k_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(15, int(round(k_tr.get_value()))))

        def cobweb():
            k = k_now()
            grp = VGroup()
            for i in range(k):
                # vertical from (x_i, x_i) to (x_i, T(x_i))
                grp.add(Line(axes.c2p(iters[i], iters[i]),
                              axes.c2p(iters[i], iters[i + 1]),
                              color=YELLOW, stroke_width=2))
                # horizontal from (x_i, T(x_i)) to (T(x_i), T(x_i))
                grp.add(Line(axes.c2p(iters[i], iters[i + 1]),
                              axes.c2p(iters[i + 1], iters[i + 1]),
                              color=YELLOW, stroke_width=2))
            # current point
            grp.add(Dot(axes.c2p(iters[k], iters[k]),
                         color=RED, radius=0.12))
            return grp

        self.add(always_redraw(cobweb))

        # Fixed point marker
        self.add(Dot(axes.c2p(x_star, x_star), color=GREEN, radius=0.1))
        self.add(Tex(r"$x^*\approx 0.739$", color=GREEN,
                     font_size=20).next_to(axes.c2p(x_star, x_star), UR, buff=0.1))

        # Right: error plot
        err_axes = Axes(x_range=[0, 15, 5], y_range=[-7, 0, 1],
                        x_length=4.5, y_length=3.5,
                        axis_config={"include_numbers": True,
                                     "font_size": 16}
                        ).shift(RIGHT * 3.0 + DOWN * 0.6)
        self.add(err_axes)
        self.add(Tex(r"$\log_{10}|x_k-x^*|$ vs $k$",
                     font_size=20).next_to(err_axes, UP, buff=0.15))

        def err_trail():
            k = k_now()
            pts = []
            for i in range(k + 1):
                e = max(1e-7, abs(iters[i] - x_star))
                pts.append(err_axes.c2p(i, np.log10(e)))
            if len(pts) < 2:
                return VMobject()
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=3)

        def ref_line():
            # log L^k = k log L
            L = np.sin(1)
            return err_axes.plot(lambda k: np.log10(max(1e-7, abs(iters[0] - x_star))) + k * np.log10(L),
                                  x_range=[0, 15], color=GREY_B,
                                  stroke_width=1.5, stroke_opacity=0.6)

        self.add(always_redraw(err_trail), ref_line())

        # Info
        info = VGroup(
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$x_k=$", font_size=22),
                   DecimalNumber(0.2, num_decimal_places=5,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(rf"$L=\sin(1)\approx {np.sin(1):.4f}$",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=1.3).shift(RIGHT * 3.0)
        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(iters[k_now()]))
        self.add(info)

        self.play(k_tr.animate.set_value(15.0),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
