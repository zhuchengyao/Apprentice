from manim import *
import numpy as np


class TetrahedronCircumsphereExample(ThreeDScene):
    """
    Every tetrahedron has a unique circumsphere passing through all
    4 vertices. Compute via solving |P − v_i|² = R² for i=1..4.

    ValueTracker s_tr morphs the tetrahedron through 3 configurations;
    always_redraw recomputes circumsphere.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=40 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
                          x_length=4.0, y_length=4.0, z_length=4.0)
        self.add(axes)

        configs = [
            [np.array([-1.0, -1.0, -0.8]),
             np.array([1.5, -1.0, -0.8]),
             np.array([0.0, 1.5, -0.8]),
             np.array([0.0, 0.0, 1.6])],
            [np.array([-1.5, -1.5, -0.5]),
             np.array([1.5, -1.5, -0.5]),
             np.array([0.0, 1.8, 0.2]),
             np.array([0.0, 0.2, 2.0])],
            [np.array([-0.8, -0.8, -1.0]),
             np.array([1.2, -0.8, -1.0]),
             np.array([0.0, 1.0, -0.8]),
             np.array([-0.2, 0.3, 1.2])],
        ]

        s_tr = ValueTracker(0.0)

        def verts():
            s = s_tr.get_value()
            k = int(s)
            frac = s - k
            k_next = min(len(configs) - 1, k + 1)
            return [(1 - frac) * configs[k][i] + frac * configs[k_next][i]
                    for i in range(4)]

        def circumsphere_params(v):
            # solve for center C, radius R:
            # |C-v_0|² = |C-v_1|² ⇒ 2(v_1-v_0)·C = |v_1|²-|v_0|²
            rows = []
            rhs = []
            for i in range(1, 4):
                rows.append(2 * (v[i] - v[0]))
                rhs.append(np.dot(v[i], v[i]) - np.dot(v[0], v[0]))
            A = np.array(rows)
            b = np.array(rhs)
            try:
                C = np.linalg.solve(A, b)
            except np.linalg.LinAlgError:
                C = np.mean(v, axis=0)
            R = np.linalg.norm(C - v[0])
            return C, R

        def draw_tet():
            v = verts()
            edges = VGroup(
                *[Line(v[i], v[j], color=BLUE, stroke_width=3)
                  for i in range(4) for j in range(i + 1, 4)]
            )
            dots = VGroup(*[Dot3D(point=p, color=BLUE, radius=0.08) for p in v])
            C, R = circumsphere_params(v)
            sphere = Sphere(radius=R, resolution=(18, 28),
                             fill_opacity=0.2).set_color(YELLOW).move_to(C)
            center_dot = Dot3D(point=C, color=RED, radius=0.08)
            return VGroup(sphere, edges, dots, center_dot)

        self.add(always_redraw(draw_tet))

        title = Tex(r"Circumsphere of a tetrahedron", font_size=24)
        info = VGroup(
            Tex(r"BLUE: tetrahedron", color=BLUE, font_size=20),
            Tex(r"YELLOW: circumsphere",
                color=YELLOW, font_size=20),
            Tex(r"RED: circumcenter",
                color=RED, font_size=20),
            Tex(r"solves $|C-v_i|^2=R^2\ \forall i$",
                color=GREEN, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)

        for k in range(1, len(configs)):
            self.play(s_tr.animate.set_value(float(k)),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
