from manim import *
import numpy as np


class InversionInCircleExample(Scene):
    """
    Inversion in a circle of radius R centered at O: z ↦ R²·z/|z|².
    Points inside go outside and vice versa; the circle itself is
    fixed pointwise.

    SINGLE_FOCUS:
      Reference circle + ValueTracker z_ang_tr moves a source point
      around various radii; always_redraw image + arc connecting them.
    """

    def construct(self):
        title = Tex(r"Inversion in circle: $z \mapsto R^2 z / |z|^2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=9, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([0, -0.3, 0])
        self.play(Create(plane))

        R = 1.5
        ref_circ = Circle(radius=plane.c2p(R, 0)[0] - plane.c2p(0, 0)[0],
                            color=YELLOW, stroke_width=3
                            ).move_to(plane.c2p(0, 0))
        R_lbl = MathTex(rf"R = {R}", color=YELLOW, font_size=22
                          ).move_to(plane.c2p(1.1, -0.8))
        self.play(Create(ref_circ), Write(R_lbl))

        z_ang_tr = ValueTracker(0.0)
        r_state = [0.7]  # start inside

        def source_pt():
            ang = z_ang_tr.get_value()
            r = r_state[0]
            return plane.c2p(r * np.cos(ang), r * np.sin(ang))

        def image_pt():
            ang = z_ang_tr.get_value()
            r = r_state[0]
            r_img = R * R / max(r, 1e-4)
            return plane.c2p(r_img * np.cos(ang), r_img * np.sin(ang))

        def source_dot():
            return Dot(source_pt(), color=BLUE, radius=0.11)

        def image_dot():
            return Dot(image_pt(), color=RED, radius=0.11)

        def radial():
            ang = z_ang_tr.get_value()
            end = plane.c2p(3.5 * np.cos(ang), 3.5 * np.sin(ang))
            start = plane.c2p(-3.5 * np.cos(ang), -3.5 * np.sin(ang))
            return DashedLine(start, end, color=GREY_B, stroke_width=1.5)

        self.add(always_redraw(radial),
                  always_redraw(source_dot),
                  always_redraw(image_dot))

        src_lbl = MathTex(r"z", color=BLUE, font_size=22
                            ).next_to(plane.c2p(0.7, 0), DOWN, buff=0.05)
        img_lbl = MathTex(r"z^*", color=RED, font_size=22
                            ).next_to(plane.c2p(3.2, 0), DOWN, buff=0.05)
        self.play(Write(src_lbl), Write(img_lbl))

        def info():
            ang = z_ang_tr.get_value()
            r = r_state[0]
            r_img = R * R / max(r, 1e-4)
            return VGroup(
                MathTex(rf"|z| = {r:.2f}", color=BLUE, font_size=22),
                MathTex(rf"|z^*| = R^2 / |z| = {r_img:.2f}",
                         color=RED, font_size=22),
                MathTex(rf"|z| \cdot |z^*| = {r * r_img:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"R^2 = {R * R}",
                         color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        # Sweep angle for r=0.7 (inside)
        self.play(z_ang_tr.animate.set_value(2 * PI),
                   run_time=4, rate_func=linear)
        self.wait(0.3)
        # Now move r to outside
        r_state[0] = 2.2
        self.play(z_ang_tr.animate.set_value(4 * PI),
                   run_time=4, rate_func=linear)
        self.wait(0.4)
