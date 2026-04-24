from manim import *
import numpy as np


class LogRiemannSurfaceExample(Scene):
    """
    Riemann surface for log z: infinitely many sheets, each
    corresponding to adding 2πi to the value. Principal branch is
    the slice arg(z) ∈ (-π, π].

    COMPARISON:
      LEFT z-plane with variable θ (going past π); RIGHT w-plane
      where w = log|z| + iθ (continuous θ, no wrap-around). After
      θ > π, w enters "sheet 2".
    """

    def construct(self):
        title = Tex(r"log $z$: infinitely many sheets",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                              x_length=5, y_length=5,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, -0.3, 0])
        right = ComplexPlane(x_range=[-1, 1.5, 0.5], y_range=[-7, 7, 2],
                               x_length=5, y_length=5.5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        z_lbl = MathTex(r"z", color=BLUE, font_size=22
                         ).next_to(left, UP, buff=0.1)
        w_lbl = MathTex(r"w = \log z", color=YELLOW, font_size=22
                          ).next_to(right, UP, buff=0.1)
        self.play(Write(z_lbl), Write(w_lbl))

        # Sheet boundary lines
        for k in [-2, -1, 0, 1, 2]:
            y_sheet = k * 2 * PI
            if abs(y_sheet) < 6.5:
                line = DashedLine(right.c2p(-1, y_sheet),
                                    right.c2p(1.5, y_sheet),
                                    color=GREY_B, stroke_width=1.5,
                                    stroke_opacity=0.4)
                self.add(line)

        r_tr = ValueTracker(1.0)  # modulus
        theta_tr = ValueTracker(0.0)  # unwrapped angle

        def z_dot():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            return Dot(left.c2p(r * np.cos(t), r * np.sin(t)),
                        color=BLUE, radius=0.12)

        def w_dot():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            # w = log(r) + i * t (unwrapped)
            return Dot(right.c2p(np.log(r), t),
                        color=YELLOW, radius=0.12)

        def w_trail():
            t_cur = theta_tr.get_value()
            r = r_tr.get_value()
            pts = []
            n = max(20, int(60 * abs(t_cur) / (2 * PI)))
            for ti in np.linspace(0, t_cur, n):
                pts.append(right.c2p(np.log(r), ti))
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(z_dot), always_redraw(w_dot),
                  always_redraw(w_trail))

        def info():
            t = theta_tr.get_value()
            r = r_tr.get_value()
            sheet = int(t // (2 * PI))
            sheet_names = {-1: "sheet -1", 0: "sheet 0 (principal)",
                            1: "sheet 1", 2: "sheet 2"}
            return VGroup(
                MathTex(rf"|z| = {r:.2f}", color=BLUE, font_size=20),
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=BLUE, font_size=20),
                MathTex(rf"\log z = {np.log(r):.2f} + {t:.2f}i",
                         color=YELLOW, font_size=20),
                Tex(sheet_names.get(sheet, f"sheet {sheet}"),
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        # Wind around 2x at fixed r=1
        self.play(theta_tr.animate.set_value(4 * PI),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
