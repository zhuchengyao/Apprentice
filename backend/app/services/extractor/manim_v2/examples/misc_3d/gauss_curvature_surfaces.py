from manim import *
import numpy as np


class GaussCurvatureSurfacesExample(ThreeDScene):
    """
    Compare Gauss curvature K of 3 surfaces:
    K > 0 (sphere): K = 1/R²
    K = 0 (cylinder): K = 0
    K < 0 (saddle z = xy): K = -1/(1 + x² + y²)²

    ThreeDScene with 3 mini-surfaces; ValueTracker s_tr morphs between
    them. Color-coded by sign.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
                          x_length=4.5, y_length=4.5, z_length=4.0)
        self.add(axes)

        s_tr = ValueTracker(0.0)  # 0 → sphere, 1 → cylinder, 2 → saddle

        def pt_on_surface(u, v):
            s = s_tr.get_value()
            # Sphere point
            sph = np.array([np.sin(u) * np.cos(v),
                             np.sin(u) * np.sin(v),
                             np.cos(u)])
            # Cylinder
            cyl = np.array([np.cos(v), np.sin(v),
                             2 * (u / PI - 0.5)])
            # Saddle z = xy scaled
            x = 1.5 * (v / PI - 1)
            y = 1.5 * (u / PI - 0.5)
            sad = np.array([x, y, x * y])

            if s <= 1:
                return (1 - s) * sph + s * cyl
            else:
                alpha = s - 1
                return (1 - alpha) * cyl + alpha * sad

        def surface():
            s = s_tr.get_value()
            if s < 0.5:
                cols = [BLUE, TEAL]  # positive K
            elif s < 1.5:
                cols = [GREEN, YELLOW]  # zero K
            else:
                cols = [ORANGE, RED]  # negative K
            return Surface(
                lambda u, v: pt_on_surface(u, v),
                u_range=[0.1, PI - 0.1], v_range=[0, TAU],
                resolution=(28, 32),
                fill_opacity=0.6,
            ).set_color_by_gradient(*cols)

        self.add(always_redraw(surface))

        # Dynamic K label
        def K_desc():
            s = s_tr.get_value()
            if s < 0.5: return r"sphere: $K=1/R^2>0$"
            if s < 1.5: return r"cylinder: $K=0$"
            return r"saddle: $K=-1/(1+x^2+y^2)^2<0$"

        title = Tex(r"Gauss curvature $K$", font_size=26)
        info = VGroup(
            VGroup(Tex(r"morph $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"sphere: $K>0$", color=BLUE, font_size=22),
            Tex(r"cylinder: $K=0$", color=GREEN, font_size=22),
            Tex(r"saddle: $K<0$", color=ORANGE, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))

        desc_tex = Tex(K_desc(), color=YELLOW, font_size=24)
        self.add_fixed_in_frame_mobjects(desc_tex)
        desc_tex.to_edge(DOWN, buff=0.3)
        def update_desc(mob, dt):
            new = Tex(K_desc(), color=YELLOW, font_size=24).move_to(desc_tex)
            desc_tex.become(new)
            return desc_tex
        desc_tex.add_updater(update_desc)

        self.play(s_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(2.0), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(0.0), run_time=3, rate_func=smooth)
        self.stop_ambient_camera_rotation()
