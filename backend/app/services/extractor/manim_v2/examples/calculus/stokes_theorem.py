from manim import *
import numpy as np


class StokesTheoremExample(ThreeDScene):
    """
    Stokes' theorem visualized in 3D:
    ∮_∂S F·dr = ∬_S (∇×F)·n dA

    F(x,y,z) = (-y, x, 0) (rigid rotation), on the upper hemisphere of
    the unit sphere. ∇×F = (0, 0, 2). Boundary is the unit circle z=0.

    ValueTracker phi_tr sweeps boundary param; always_redraw segment of
    tangent probe + highlighted arc track progress. Second phase: 48
    surface normals appear with ∇×F·n glyph coloring.
    """

    def construct(self):
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                          z_range=[-1, 2, 1], x_length=5, y_length=5, z_length=3.5)
        self.set_camera_orientation(phi=65 * DEGREES, theta=40 * DEGREES)

        hemi = Surface(
            lambda u, v: np.array([np.sin(u) * np.cos(v),
                                    np.sin(u) * np.sin(v),
                                    np.cos(u)]),
            u_range=[0.01, PI / 2], v_range=[0, TAU],
            resolution=(16, 28), fill_opacity=0.35,
        ).set_color(BLUE)
        self.add(axes, hemi)

        boundary = ParametricFunction(
            lambda t: np.array([np.cos(t), np.sin(t), 0.0]),
            t_range=[0, TAU], color=YELLOW, stroke_width=4,
        )
        self.play(Create(boundary), run_time=1.5)

        phi_tr = ValueTracker(0.0)

        def traced_arc():
            phi = phi_tr.get_value()
            return ParametricFunction(
                lambda t: np.array([np.cos(t), np.sin(t), 0.0]),
                t_range=[0, max(phi, 1e-3)], color=ORANGE, stroke_width=8,
            )

        def tangent_probe():
            phi = phi_tr.get_value()
            p = np.array([np.cos(phi), np.sin(phi), 0.0])
            F = np.array([-np.sin(phi), np.cos(phi), 0.0])
            return Arrow3D(start=p, end=p + 0.5 * F, color=GREEN, thickness=0.02)

        self.add(always_redraw(traced_arc), always_redraw(tangent_probe))

        title = Tex(r"Stokes: $\oint_{\partial S} \mathbf{F}\cdot d\mathbf{r} = \iint_S (\nabla\times \mathbf{F})\cdot \mathbf{n}\, dA$",
                    font_size=26).to_corner(UL)
        sideinfo = VGroup(
            Tex(r"$\mathbf{F}=(-y,x,0)$", font_size=22),
            Tex(r"$\nabla\times \mathbf{F}=(0,0,2)$", font_size=22),
            Tex(r"LHS $= 2\pi$", color=YELLOW, font_size=22),
            Tex(r"RHS $= 2\cdot \pi(1)^2 = 2\pi$", color=ORANGE, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR)
        self.add_fixed_in_frame_mobjects(title, sideinfo)

        self.begin_ambient_camera_rotation(rate=0.05)
        self.play(phi_tr.animate.set_value(TAU), run_time=5, rate_func=linear)
        self.wait(0.5)

        # Phase 2: surface normals with curl dot product
        normals = VGroup()
        for u in np.linspace(0.25, PI / 2 - 0.15, 5):
            for v in np.linspace(0, TAU, 12, endpoint=False):
                p = np.array([np.sin(u) * np.cos(v),
                               np.sin(u) * np.sin(v),
                               np.cos(u)])
                nvec = p  # outward unit normal on unit sphere
                # curl · n = 2 * n_z = 2 cos u
                val = 2 * np.cos(u)
                col = interpolate_color(BLUE, RED, np.clip(val / 2, 0, 1))
                arrow = Arrow3D(start=p, end=p + 0.35 * nvec,
                                 color=col, thickness=0.015)
                normals.add(arrow)

        self.play(Create(normals, lag_ratio=0.02), run_time=3)
        self.wait(1.5)
        self.stop_ambient_camera_rotation()
