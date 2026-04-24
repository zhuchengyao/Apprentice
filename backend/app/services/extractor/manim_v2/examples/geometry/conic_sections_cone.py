from manim import *
import numpy as np


class ConicSectionsConeExample(ThreeDScene):
    """
    Conic sections: slicing a double cone with a plane gives an
    ellipse (small tilt), parabola (parallel to side), or hyperbola
    (steep tilt). Visualize with tiltable plane.

    3D scene:
      Double cone + plane at varying tilt angle; ValueTracker tilt_tr
      sweeps plane tilt from 0 (horizontal → circle) to steep.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=3)
        self.add(axes)

        # Double cone
        def cone_param(u, v):
            # u ∈ [-1, 1] = z; v ∈ [0, 2π]
            r = abs(u) * 1.5
            x = r * np.cos(v)
            y = r * np.sin(v)
            z = u * 2
            return axes.c2p(x, y, z)

        cone = Surface(cone_param, u_range=[-1, 1], v_range=[0, 2 * PI],
                         resolution=(15, 24),
                         fill_opacity=0.25,
                         checkerboard_colors=[GREY, GREY_B])
        self.add(cone)

        tilt_tr = ValueTracker(0.1)

        def cutting_plane():
            tilt = tilt_tr.get_value()
            # Plane: z = mx + h where m = tan(tilt)
            # Draw as a parallelogram
            def param(u, v):
                x = u * 2.5
                y = v * 2.5
                z = np.tan(tilt) * x + 0.3
                return axes.c2p(x, y, z)

            return Surface(param, u_range=[-1, 1], v_range=[-1, 1],
                             resolution=(5, 5),
                             fill_opacity=0.35,
                             checkerboard_colors=[YELLOW, YELLOW])

        self.add(always_redraw(cutting_plane))

        # Conic intersection curve: compute intersection of plane with cone
        def intersection_curve():
            tilt = tilt_tr.get_value()
            m = np.tan(tilt)
            h = 0.3
            # Cone: z² = r² · (2/1.5)² → use z² = (4/1.5²) r² → simplify, cone z² = 4 r² / 2.25
            # We have z = u*2 (u is z/2) and r = |u| * 1.5 → cone eqn: r² = (z/2)² · 1.5² = 2.25 z² / 4
            # → r² = (9/16) z²
            # Plug z = mx + h: r² = x² + y² = (9/16)(mx + h)²
            # Parametrize by x in a range, solve for y.
            pts = []
            for x in np.linspace(-2.5, 2.5, 100):
                z_val = m * x + h
                r2 = (9 / 16) * z_val ** 2
                y2 = r2 - x ** 2
                if y2 >= 0 and abs(z_val) < 2.0:
                    y = np.sqrt(y2)
                    pts.append(axes.c2p(x, y, z_val))
            for x in np.linspace(2.5, -2.5, 100):
                z_val = m * x + h
                r2 = (9 / 16) * z_val ** 2
                y2 = r2 - x ** 2
                if y2 >= 0 and abs(z_val) < 2.0:
                    y = -np.sqrt(y2)
                    pts.append(axes.c2p(x, y, z_val))
            m_curve = VMobject(color=RED, stroke_width=4)
            if len(pts) >= 3:
                m_curve.set_points_as_corners(pts)
            return m_curve

        self.add(always_redraw(intersection_curve))

        title = Tex(r"Conic sections: plane $\cap$ cone",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            tilt = tilt_tr.get_value()
            tilt_deg = np.degrees(tilt)
            # Slope vs cone angle (arctan(1.5/2) = 36.87°)
            cone_angle = np.degrees(np.arctan(1.5 / 2))
            if tilt_deg < cone_angle - 2:
                kind = "ellipse"
                col = GREEN
            elif abs(tilt_deg - cone_angle) < 2:
                kind = "parabola"
                col = YELLOW
            else:
                kind = "hyperbola"
                col = RED
            return VGroup(
                MathTex(rf"\text{{tilt}} = {tilt_deg:.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"\text{{cone half-angle}} = 36.87^\circ",
                         color=GREY_B, font_size=20),
                Tex(kind, color=col, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.12)
        for tv in [20, 35, 50, 70]:
            self.play(tilt_tr.animate.set_value(tv * DEGREES),
                       run_time=2, rate_func=smooth)
            new_pnl = panel()
            self.add_fixed_in_frame_mobjects(new_pnl)
            self.play(Transform(pnl, new_pnl), run_time=0.2)
            self.wait(0.4)
        self.stop_ambient_camera_rotation()
