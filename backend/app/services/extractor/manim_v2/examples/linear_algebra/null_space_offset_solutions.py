from manim import *
import numpy as np


class NullSpaceOffsetSolutionsExample(Scene):
    """
    When Ax = v has a solution x_0 and A has nontrivial null space N,
    the full solution set is x_0 + N. Every x_0 + n (n ∈ N) also maps
    to v because A(x_0 + n) = Ax_0 + An = v + 0 = v.
    """

    def construct(self):
        title = Tex(r"Solution set $=\vec x_0 + N$ (particular + null space)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[1.0, -1.0], [-1.0, 1.0]])  # det = 0
        # Null space: direction (1, 1)
        # Ax = v where v = (2, -2) which is in col space (direction (1, -1))
        # Particular solution: try x_0 = (1, -1): A @ (1, -1) = (1+1, -1-1) = (2, -2). Good.
        x_0 = np.array([1.0, -1.0])

        # Draw particular solution x_0 as RED arrow
        x_arrow = Arrow(plane.c2p(0, 0), plane.c2p(x_0[0], x_0[1]),
                         color=RED, buff=0, stroke_width=5)
        x_lbl = Tex(r"$\vec x_0$ (particular)", color=RED,
                     font_size=22).next_to(x_arrow.get_end(), DR, buff=0.1)
        self.play(Create(x_arrow), Write(x_lbl))

        # Draw null space line through origin
        null_line = Line(plane.c2p(-3, -3), plane.c2p(3, 3),
                          color=YELLOW, stroke_width=3, stroke_opacity=0.6)
        null_lbl = Tex(r"null space", color=YELLOW,
                        font_size=22).next_to(plane.c2p(2.5, 2.5), UP, buff=0.1)
        self.play(Create(null_line), Write(null_lbl))
        self.wait(0.3)

        # Draw shifted null space line through x_0 — all solutions
        sol_line = Line(plane.c2p(x_0[0] - 3, x_0[1] - 3),
                         plane.c2p(x_0[0] + 3, x_0[1] + 3),
                         color=GREEN, stroke_width=4)
        sol_lbl = Tex(r"solution set $=\vec x_0+N$", color=GREEN,
                        font_size=22).next_to(plane.c2p(3, -0.5), RIGHT, buff=0.1)
        self.play(Create(sol_line), Write(sol_lbl))

        # Show several solutions as green dots on sol_line
        for a in np.linspace(-2, 2, 5):
            xi = x_0 + a * np.array([1, 1]) / np.sqrt(2) * 1.2
            self.add(Dot(plane.c2p(xi[0], xi[1]), color=GREEN, radius=0.08))

        self.wait(0.5)

        # Algebraic note
        info = VGroup(
            Tex(r"$A(\vec x_0+\vec n)=A\vec x_0+A\vec n$", font_size=22),
            Tex(r"$=\vec v+\vec 0=\vec v$", color=GREEN, font_size=22),
            Tex(r"$\Rightarrow$ all $\vec x_0+\vec n$ are solutions",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
