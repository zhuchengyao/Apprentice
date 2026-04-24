from manim import *
import numpy as np


class HopfFibrationExample(ThreeDScene):
    """
    Hopf fibration S³ → S²: fibers are great circles of S³ whose
    stereographic projection are linked circles in ℝ³ (except for
    the fiber over the north pole which is a straight line).

    Each fiber corresponds to a point (a, b, c) on S². Parametrize
    fiber over (a, b, c) with t ∈ [0, 2π]:
      (z_1, z_2) = ( cos(t)(√((1+c)/2)), (e^{iξ} sin(t)/√(1-c²))(a+ib) )
    where ξ = t; take real 4D vector (x, y, z, w) then stereographic
    project to ℝ³.

    Draw 8 fibers at varying latitudes. ValueTracker t_tr animates
    color-coded dots along each fiber.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
                          x_length=4.0, y_length=4.0, z_length=4.0)
        self.add(axes)

        # Stereographic from S³ to R³ (north pole = w axis)
        def stereo(x, y, z, w):
            if abs(1 - w) < 1e-6:
                return np.array([1e9, 0, 0])
            k = 1 / (1 - w)
            return np.array([x * k, y * k, z * k])

        def fiber_point(a, b, c, t):
            # parametrize: choose z1 = sqrt((1+c)/2) e^{i t}, z2 depends on phase
            # Using standard Hopf map: p(z1, z2) = (2 z1 conj(z2),
            # |z1|^2 - |z2|^2).
            # Pick z1 = e^{it} cos(β), z2 = e^{iφ} sin(β) with cos 2β = c.
            # then a + i b = 2 e^{i(t - φ)} sin β cos β
            # choose φ = 0 so e^{it} = (a + i b)/|a+ib| * 1 or adjust.
            # Simpler: use explicit parametrization of fiber over (a, b, c)
            # as (z1, z2) = e^{it} · (z1_0, z2_0) where (z1_0, z2_0) is a fixed
            # lift of (a, b, c).
            if abs(c - 1) < 1e-9:
                z1_0 = 1.0 + 0j
                z2_0 = 0.0 + 0j
            elif abs(c + 1) < 1e-9:
                z1_0 = 0.0 + 0j
                z2_0 = 1.0 + 0j
            else:
                r = np.sqrt((1 + c) / 2)
                rr = np.sqrt((1 - c) / 2)
                z1_0 = r + 0j
                z2_0 = (a + 1j * b) / np.sqrt(a * a + b * b + 1e-18) * rr
            z1 = np.exp(1j * t) * z1_0
            z2 = np.exp(1j * t) * z2_0
            x, y = z1.real, z1.imag
            z, w = z2.real, z2.imag
            return stereo(x, y, z, w)

        # 8 fibers spread across S²
        fibers_s2 = [
            (0.0, 0.0, 0.95),
            (0.6, 0.0, 0.5),
            (0.0, 0.6, 0.5),
            (-0.6, 0.0, 0.5),
            (0.0, -0.6, 0.5),
            (0.85, 0.0, 0.0),
            (0.0, 0.85, 0.0),
            (0.0, 0.0, -0.7),
        ]
        colors = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK]

        fiber_curves = VGroup()
        for (a, b, c), col in zip(fibers_s2, colors):
            pts = []
            for t in np.linspace(0, TAU, 80):
                p = fiber_point(a, b, c, t)
                if np.linalg.norm(p) < 6:
                    pts.append(p)
            if len(pts) >= 2:
                fiber_curves.add(
                    VMobject().set_points_smoothly(pts + [pts[0]])
                    .set_color(col).set_stroke(width=3)
                )
        self.play(Create(fiber_curves, lag_ratio=0.1), run_time=3)

        t_tr = ValueTracker(0.0)

        def dots():
            t = t_tr.get_value()
            grp = VGroup()
            for (a, b, c), col in zip(fibers_s2, colors):
                p = fiber_point(a, b, c, t)
                if np.linalg.norm(p) < 6:
                    grp.add(Dot3D(point=p, color=col, radius=0.12))
            return grp

        self.add(always_redraw(dots))

        title = Tex(r"Hopf fibration $S^3\to S^2$: stereographic image of fibers",
                    font_size=22)
        panel = Tex(r"Every pair of fibers is linked (Hopf link)",
                    color=YELLOW, font_size=22)
        self.add_fixed_in_frame_mobjects(title, panel)
        title.to_edge(UP, buff=0.3)
        panel.to_edge(DOWN, buff=0.3)

        self.play(t_tr.animate.set_value(TAU),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
        self.stop_ambient_camera_rotation()
