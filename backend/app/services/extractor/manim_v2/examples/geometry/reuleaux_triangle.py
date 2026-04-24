from manim import *
import numpy as np


class ReuleauxTriangleExample(Scene):
    """
    Reuleaux triangle: curve of constant width, constructed from an
    equilateral triangle by replacing each side with a circular arc
    centered at the opposite vertex. Width = side length regardless
    of orientation.

    SINGLE_FOCUS:
      Reuleaux triangle between two parallel lines. ValueTracker
      theta_tr rotates it; always_redraw vertical calipers with
      constant width = 2 despite rotation.
    """

    def construct(self):
        title = Tex(r"Reuleaux triangle: constant width regardless of orientation",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        s = 2.0  # side length

        # Equilateral triangle vertices at angle θ
        theta_tr = ValueTracker(0.0)

        def triangle_verts():
            t = theta_tr.get_value()
            # Center at origin
            verts = []
            for i in range(3):
                ang = t + 2 * PI * i / 3 + PI / 2
                r = s / np.sqrt(3)  # circumradius
                verts.append(np.array([r * np.cos(ang), r * np.sin(ang), 0]))
            return verts

        def reuleaux_curve():
            verts = triangle_verts()
            # For each pair (V_i, V_{i+1}), arc centered at V_{i+2} of radius s
            pts = []
            for i in range(3):
                V_i = verts[i]
                V_j = verts[(i + 1) % 3]
                V_center = verts[(i + 2) % 3]
                # Angle range from V_i to V_j as seen from V_center
                ang_start = np.arctan2((V_i - V_center)[1], (V_i - V_center)[0])
                ang_end = np.arctan2((V_j - V_center)[1], (V_j - V_center)[0])
                # Shorter arc (60°)
                diff = ang_end - ang_start
                if diff > PI:
                    diff -= 2 * PI
                elif diff < -PI:
                    diff += 2 * PI
                for theta_arc in np.linspace(0, diff, 20):
                    ang = ang_start + theta_arc
                    pts.append(V_center + s * np.array([np.cos(ang),
                                                             np.sin(ang), 0]))
            m = VMobject(color=YELLOW, fill_opacity=0.4, stroke_width=3)
            m.set_points_as_corners(pts + [pts[0]])
            return m

        self.add(always_redraw(reuleaux_curve))

        # Calipers: two parallel horizontal lines at y = ±s/2
        caliper_top = Line([-4, s, 0], [4, s, 0], color=RED, stroke_width=3)
        caliper_bot = Line([-4, -s + 2 * (s / np.sqrt(3)) - s, 0],
                             [4, -s + 2 * (s / np.sqrt(3)) - s, 0],
                             color=RED, stroke_width=3)
        # Actually: Reuleaux has width s, so calipers at y = y_top and y_top - s
        # y_top depends on orientation... Let's dynamically draw calipers.

        def calipers():
            verts = triangle_verts()
            # Find bounding y values
            all_pts = []
            for i in range(3):
                V_i = verts[i]
                V_j = verts[(i + 1) % 3]
                V_center = verts[(i + 2) % 3]
                ang_start = np.arctan2((V_i - V_center)[1], (V_i - V_center)[0])
                ang_end = np.arctan2((V_j - V_center)[1], (V_j - V_center)[0])
                diff = ang_end - ang_start
                if diff > PI:
                    diff -= 2 * PI
                elif diff < -PI:
                    diff += 2 * PI
                for theta_arc in np.linspace(0, diff, 30):
                    ang = ang_start + theta_arc
                    all_pts.append(V_center + s * np.array([np.cos(ang),
                                                                 np.sin(ang), 0]))
            ys = [p[1] for p in all_pts]
            y_max = max(ys)
            y_min = min(ys)
            width = y_max - y_min
            c_top = Line([-4, y_max, 0], [4, y_max, 0],
                           color=RED, stroke_width=3)
            c_bot = Line([-4, y_min, 0], [4, y_min, 0],
                           color=RED, stroke_width=3)
            w_lbl = MathTex(rf"width = {width:.3f}",
                              color=RED, font_size=22
                              ).move_to([3, (y_max + y_min) / 2, 0])
            return VGroup(c_top, c_bot, w_lbl)

        self.add(always_redraw(calipers))

        info = VGroup(
            MathTex(r"\text{side} = 2", color=YELLOW, font_size=22),
            Tex(r"3 arcs, each radius 2, 60$^\circ$ arc",
                 color=YELLOW, font_size=20),
            Tex(r"width $= 2$ for any rotation",
                 color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        self.play(Write(info))

        self.play(theta_tr.animate.set_value(PI),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
