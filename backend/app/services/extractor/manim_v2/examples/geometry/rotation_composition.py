from manim import *
import numpy as np


class RotationCompositionExample(Scene):
    """
    Composition of 2D rotations about different centers is either a
    rotation about a third center (if total angle ≠ 0 mod 2π) or
    a translation (if total angle = 0).

    SINGLE_FOCUS: triangle gets rotated about C_1 by α then about
    C_2 by β. Composition = rotation about C_3 by α+β. Show the
    intermediate.
    """

    def construct(self):
        title = Tex(r"Composition of two rotations = rotation about a new center",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=6,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        C1 = np.array([-2.0, 1.0, 0])
        C2 = np.array([2.0, -0.5, 0])
        alpha = PI / 3
        beta = PI / 2

        # Triangle initial
        tri_pts = [np.array([-3.3, -0.3, 0]), np.array([-2.5, -0.5, 0]),
                   np.array([-2.9, 0.5, 0])]

        def rotate_pts(pts, center, angle):
            c, s = np.cos(angle), np.sin(angle)
            R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
            return [center + R @ (p - center) for p in pts]

        t_tr = ValueTracker(0.0)  # [0, 1]: rotate about C_1, [1, 2]: rotate about C_2

        def current_tri():
            t = t_tr.get_value()
            if t <= 1:
                angle = alpha * t
                pts = rotate_pts(tri_pts, C1, angle)
                col = GREEN
            else:
                intermediate = rotate_pts(tri_pts, C1, alpha)
                angle = beta * (t - 1)
                pts = rotate_pts(intermediate, C2, angle)
                col = ORANGE if t < 1.999 else RED
            return Polygon(*pts, color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.25)

        self.add(always_redraw(current_tri))

        # Show initial + final
        init_tri = Polygon(*tri_pts, color=BLUE, stroke_width=2,
                            fill_opacity=0.15).set_stroke(color=BLUE, opacity=0.5)
        self.add(init_tri)

        # Centers
        C1_dot = Dot(C1, color=GREEN, radius=0.12)
        C2_dot = Dot(C2, color=ORANGE, radius=0.12)
        self.add(C1_dot, C2_dot)
        self.add(Tex(r"$C_1, \alpha=\pi/3$", color=GREEN, font_size=20).next_to(C1_dot, UL, buff=0.1))
        self.add(Tex(r"$C_2, \beta=\pi/2$", color=ORANGE, font_size=20).next_to(C2_dot, DR, buff=0.1))

        # Compute composite rotation center via formula
        # For R_2 ∘ R_1 with angles α, β about C_1, C_2:
        # New center C = (R_{α+β} - I)^(-1) · (R_α · (-C_1) + (R_β - I)·something)
        # Simpler: apply to a test point, solve fixed point
        def apply(p):
            p1 = rotate_pts([p], C1, alpha)[0]
            p2 = rotate_pts([p1], C2, beta)[0]
            return p2

        # Fixed point: p_* = apply(p_*)
        # Solve (I - R_total) p = apply(origin) numerically
        # Actually easier: iterate map until fixed.
        p = np.zeros(3)
        for _ in range(50):
            p = 0.5 * (p + apply(p))
        C3 = p
        C3_dot = Dot(C3, color=RED, radius=0.12)
        self.add(C3_dot)
        self.add(Tex(r"$C_3, \alpha+\beta=5\pi/6$", color=RED, font_size=20).next_to(C3_dot, UR, buff=0.1))

        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            Tex(r"stage 1 ($t\in[0,1]$): rotate about $C_1$",
                color=GREEN, font_size=18),
            Tex(r"stage 2 ($t\in[1,2]$): rotate about $C_2$",
                color=ORANGE, font_size=18),
            Tex(r"$=$ single rotation by $\alpha+\beta$ about $C_3$",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        self.add(info)

        self.play(t_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.4)
        self.play(t_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(0.8)
