from manim import *
import numpy as np


class IsoperimetricInequalityExample(Scene):
    """
    Isoperimetric inequality: among all closed curves with given
    perimeter L, the circle maximizes enclosed area.
    A ≤ L²/(4π), equality iff circle.

    SINGLE_FOCUS:
      Several shapes of equal perimeter (L = 2π ≈ 6.28): circle
      (A=π), square (A=(L/4)²), equilateral triangle, ellipse.
      ValueTracker step_tr cycles through them showing area ratios.
    """

    def construct(self):
        title = Tex(r"Isoperimetric: $A \le L^2/(4\pi)$, $=$ iff circle",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        L = 2 * PI

        # Shapes with perimeter L
        shapes_data = [
            ("circle", 1.0, "lambda t: (cos t, sin t)"),  # r=1, circ=2π, A=π
            ("square", L / 4, None),
            ("equilat_tri", L / 3, None),
            ("ellipse (a=1.5)", None, None),  # area specially
            ("star", None, None),  # arbitrary decorative low-area
        ]

        def make_shape(idx):
            if idx == 0:  # circle
                return Circle(radius=1.0, color=BLUE, stroke_width=3,
                                fill_opacity=0.3)
            elif idx == 1:  # square
                s = L / 4
                return Square(side_length=s, color=GREEN,
                                stroke_width=3, fill_opacity=0.3)
            elif idx == 2:  # equilateral triangle
                s = L / 3
                h = s * np.sqrt(3) / 2
                return Polygon([-s / 2, -h / 3, 0],
                                 [s / 2, -h / 3, 0],
                                 [0, 2 * h / 3, 0],
                                 color=ORANGE, stroke_width=3,
                                 fill_opacity=0.3)
            elif idx == 3:  # ellipse with a=1.5 and equal perimeter ≈ 2π
                # Ramanujan: P ≈ π(3(a+b) - √((3a+b)(a+3b)))
                # For a=1.5, solve for b
                from scipy.optimize import brentq
                def perim_diff(b):
                    a = 1.5
                    return PI * (3 * (a + b) - np.sqrt((3 * a + b) * (a + 3 * b))) - L
                b_val = brentq(perim_diff, 0.3, 1.0)
                pts = []
                for t in np.linspace(0, 2 * PI, 80):
                    pts.append(np.array([1.5 * np.cos(t),
                                             b_val * np.sin(t), 0]))
                m = VMobject(color=RED, stroke_width=3, fill_opacity=0.3)
                m.set_points_as_corners(pts + [pts[0]])
                return m
            else:  # star (arbitrary, low area)
                pts = []
                for k in range(10):
                    r = 1.3 if k % 2 == 0 else 0.4
                    ang = PI / 2 + k * PI / 5
                    pts.append(np.array([r * np.cos(ang),
                                             r * np.sin(ang), 0]))
                m = VMobject(color=PURPLE, stroke_width=3, fill_opacity=0.3)
                m.set_points_as_corners(pts + [pts[0]])
                return m

        step_tr = ValueTracker(0)

        def shape_obj():
            idx = int(round(step_tr.get_value())) % 5
            s = make_shape(idx)
            s.move_to([-3, -0.3, 0])
            return s

        self.add(always_redraw(shape_obj))

        # Theoretical max area
        max_area = L ** 2 / (4 * PI)

        def info():
            idx = int(round(step_tr.get_value())) % 5
            names = ["circle", "square", "equilateral △",
                      "ellipse a=1.5", "star"]
            # Compute area for each
            if idx == 0:
                A = PI * 1 ** 2
                formula = r"A = \pi r^2 = \pi"
            elif idx == 1:
                s = L / 4
                A = s ** 2
                formula = rf"A = s^2 = {A:.3f}"
            elif idx == 2:
                s = L / 3
                A = s ** 2 * np.sqrt(3) / 4
                formula = rf"A = \tfrac{{\sqrt 3}}{{4}} s^2 = {A:.3f}"
            elif idx == 3:
                # A = π a b; use b ≈ 0.655 for matching
                from scipy.optimize import brentq
                def perim_diff(b):
                    a = 1.5
                    return PI * (3 * (a + b) - np.sqrt((3 * a + b) * (a + 3 * b))) - L
                b_val = brentq(perim_diff, 0.3, 1.0)
                A = PI * 1.5 * b_val
                formula = rf"A = \pi a b \approx {A:.3f}"
            else:
                # Star: estimate via shoelace on 10 points
                pts = []
                for k in range(10):
                    r = 1.3 if k % 2 == 0 else 0.4
                    ang = PI / 2 + k * PI / 5
                    pts.append((r * np.cos(ang), r * np.sin(ang)))
                A = 0.0
                for i in range(10):
                    x1, y1 = pts[i]
                    x2, y2 = pts[(i + 1) % 10]
                    A += x1 * y2 - x2 * y1
                A = abs(A) / 2
                formula = rf"A \approx {A:.3f}"
            ratio = A / max_area
            return VGroup(
                Tex(names[idx], color=YELLOW, font_size=24),
                MathTex(formula, color=BLUE, font_size=20),
                MathTex(rf"\text{{area}}/\text{{max}} = {ratio:.3f}",
                         color=GREEN if ratio > 0.99 else ORANGE, font_size=20),
                MathTex(rf"\max = L^2/(4\pi) = \pi = {max_area:.3f}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for i in range(1, 5):
            self.play(step_tr.animate.set_value(i),
                       run_time=1.3, rate_func=smooth)
            self.wait(1.0)
        self.wait(0.5)
