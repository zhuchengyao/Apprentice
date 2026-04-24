from manim import *
import numpy as np


class SphereToCylinderAreaPreservation(ThreeDScene):
    """Why is the surface area of a sphere 4*pi*R^2?  Map the sphere
    radially outward to the enclosing cylinder.  A tiny square on the
    sphere becomes a rectangle on the cylinder — it widens by 1/cos(phi)
    AND shrinks vertically by cos(phi), so its area is preserved.  The
    cylinder unfolds to 2*pi*R x 2*R = 4*pi*R^2."""

    def construct(self):
        self.set_camera_orientation(phi=72 * DEGREES, theta=-45 * DEGREES)

        R = 1.8
        sphere = Sphere(
            radius=R, resolution=(30, 30),
            fill_opacity=0.55, stroke_width=0.3, stroke_color=BLUE,
            fill_color=BLUE_D,
        )
        cyl = ParametricSurface(
            lambda u, v: np.array([
                R * np.cos(u), R * np.sin(u), v,
            ]),
            u_range=[0, 2 * np.pi], v_range=[-R, R],
            resolution=(40, 20),
            fill_opacity=0.10, stroke_width=0.4, stroke_color=YELLOW,
            fill_color=YELLOW_E,
            checkerboard_colors=[YELLOW_E, YELLOW_D],
        )
        self.add(sphere, cyl)

        title = Tex(
            r"Sphere $\to$ cylinder: width stretches, height squishes, area preserved",
            font_size=26,
        )
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)

        phi_tr = 45 * DEGREES
        ring_pts = []
        for i in range(100):
            u = i / 99 * 2 * np.pi
            ring_pts.append(np.array([
                R * np.cos(phi_tr) * np.cos(u),
                R * np.cos(phi_tr) * np.sin(u),
                R * np.sin(phi_tr),
            ]))
        sphere_ring = VMobject(color=RED, stroke_width=3)
        sphere_ring.set_points_as_corners(ring_pts + [ring_pts[0]])

        cyl_pts = []
        for i in range(100):
            u = i / 99 * 2 * np.pi
            cyl_pts.append(np.array([
                R * np.cos(u), R * np.sin(u), R * np.sin(phi_tr),
            ]))
        cyl_ring = VMobject(color=GREEN, stroke_width=3)
        cyl_ring.set_points_as_corners(cyl_pts + [cyl_pts[0]])

        self.play(Create(sphere_ring), Create(cyl_ring))

        radial_arrows = VGroup()
        for theta_u in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            p_sph = np.array([
                R * np.cos(phi_tr) * np.cos(theta_u),
                R * np.cos(phi_tr) * np.sin(theta_u),
                R * np.sin(phi_tr),
            ])
            p_cyl = np.array([
                R * np.cos(theta_u), R * np.sin(theta_u),
                R * np.sin(phi_tr),
            ])
            radial_arrows.add(Arrow3D(
                start=p_sph, end=p_cyl,
                color=WHITE, thickness=0.008,
                height=0.08, base_radius=0.03,
            ))
        self.play(LaggedStart(*[Create(a) for a in radial_arrows],
                              lag_ratio=0.05))

        derivation = VGroup(
            MathTex(r"\text{tiny square on sphere at latitude } \phi",
                    font_size=22),
            MathTex(r"\Delta A = (R\,d\phi)(R\cos\phi\,d\theta)",
                    font_size=22, color=BLUE),
            MathTex(
                r"\text{image on cylinder: }"
                r"\Delta A' = \tfrac{R\,d\phi}{\cos\phi}"
                r"\cdot R\cos\phi\,d\theta = R^2\,d\phi\,d\theta = \Delta A",
                font_size=22, color=GREEN,
            ),
            MathTex(
                r"A_{\text{sphere}} = A_{\text{cylinder lateral}}"
                r" = 2\pi R \cdot 2R = 4\pi R^2",
                font_size=26, color=YELLOW,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        self.add_fixed_in_frame_mobjects(derivation)
        derivation.to_corner(DR, buff=0.3)
        self.play(FadeIn(derivation[0]))
        self.play(Write(derivation[1]))
        self.play(Write(derivation[2]))
        box = SurroundingRectangle(derivation[3], color=YELLOW,
                                   buff=0.15, stroke_width=3)
        self.add_fixed_in_frame_mobjects(box)
        self.play(Write(derivation[3]), Create(box))

        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(6)
        self.stop_ambient_camera_rotation()
        self.wait(1.0)
