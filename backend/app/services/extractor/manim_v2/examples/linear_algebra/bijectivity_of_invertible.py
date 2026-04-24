from manim import *
import numpy as np


class BijectivityOfInvertibleExample(Scene):
    """
    A is invertible ⟺ L(x) = Ax is bijective. Each vector in the plane
    lands on exactly one vector (injective), and every vector has
    been landed on (surjective).
    """

    def construct(self):
        title = Tex(r"Invertible $\Leftrightarrow$ bijective (one-to-one + onto)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[0.0, 2.0], [-1.0, 1.0]])  # det = 2, invertible

        # 5x5 grid of dots
        pts = []
        for x in range(-3, 4):
            for y in range(-2, 3):
                pts.append(np.array([x, y]))

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        def dots_mobject():
            M = M_of()
            grp = VGroup()
            for p in pts:
                p_new = M @ p
                col = interpolate_color(BLUE, RED, (p[0] + 3) / 6)
                grp.add(Dot(plane.c2p(p_new[0], p_new[1]),
                             color=col, radius=0.07))
            return grp

        self.add(always_redraw(dots_mobject))

        # Stage labels
        def stage_str():
            t = t_tr.get_value()
            if t < 0.02: return r"each lattice point = unique vector"
            if t < 0.98: return r"transforming..."
            return r"each lattice point still $\to$ unique vector (invertible)"

        stage_tex = Tex(stage_str(), color=YELLOW, font_size=22).to_edge(DOWN, buff=0.3)
        self.add(stage_tex)
        def update(mob, dt):
            new = Tex(stage_str(), color=YELLOW, font_size=22).move_to(stage_tex)
            stage_tex.become(new)
            return stage_tex
        stage_tex.add_updater(update)

        info = VGroup(
            Tex(r"injective: each $x$ maps to unique $Ax$", color=BLUE, font_size=20),
            Tex(r"surjective: every $y$ has preimage", color=RED, font_size=20),
            Tex(r"$\Rightarrow$ $A^{-1}$ exists", color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        self.add(info)

        self.play(t_tr.animate.set_value(1.0), run_time=3.5, rate_func=smooth)
        self.wait(0.8)
        self.play(t_tr.animate.set_value(0.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
