from manim import *
import numpy as np


class BranchCutSqrtExample(Scene):
    """
    Branch cut of √z at the negative real axis. Approaching from
    above gives +i√|z|, from below gives -i√|z|. Define arg z ∈
    (-π, π].

    TWO_COLUMN: LEFT ComplexPlane with probe dot moving on a circle
    |z|=1 avoiding branch cut. RIGHT plots √z image plane. When probe
    crosses the branch cut, image jumps.
    """

    def construct(self):
        title = Tex(r"Branch cut of $\sqrt{z}$: discontinuity across $(-\infty,0]$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-1.8, 1.8, 1], y_range=[-1.8, 1.8, 1],
                            x_length=4.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.2)
        right = ComplexPlane(x_range=[-1.8, 1.8, 1], y_range=[-1.8, 1.8, 1],
                             x_length=4.5, y_length=4.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(RIGHT * 2.5)
        self.play(Create(left), Create(right))

        # Branch cut line
        cut = Line(left.n2p(-1.8, 0), left.n2p(0, 0),
                    color=RED, stroke_width=4)
        self.add(cut)
        cut_lbl = Tex(r"branch cut", color=RED, font_size=20).next_to(
            left.n2p(-0.9, 0), DOWN, buff=0.15)
        self.add(cut_lbl)

        theta_tr = ValueTracker(0.0)

        def z_pt():
            # angle in (-π, π] avoiding ±π exactly
            t = theta_tr.get_value()
            return np.exp(1j * t)

        def sqrt_z(z):
            # Use principal branch
            r = abs(z)
            theta = np.angle(z)  # in (-π, π]
            return np.sqrt(r) * np.exp(1j * theta / 2)

        def z_dot():
            z = z_pt()
            return Dot(left.n2p(complex(z.real, z.imag)),
                        color=YELLOW, radius=0.1)

        def w_dot():
            w = sqrt_z(z_pt())
            return Dot(right.n2p(complex(w.real, w.imag)),
                        color=GREEN, radius=0.1)

        def z_trail():
            t = theta_tr.get_value()
            ts = np.linspace(0, t, 120) if t > 0.01 else np.linspace(t, 0, 120)
            pts_z = [left.n2p(complex(np.cos(tk), np.sin(tk))) for tk in ts]
            return VMobject().set_points_as_corners(pts_z).set_color(YELLOW)\
                .set_stroke(width=2.5, opacity=0.7)

        def w_trail():
            t = theta_tr.get_value()
            if abs(t) < 0.01:
                return VMobject()
            ts = np.linspace(0, t, 200) if t > 0 else np.linspace(t, 0, 200)
            pts_w = []
            for tk in ts:
                z = np.exp(1j * tk)
                w = sqrt_z(z)
                pts_w.append(right.n2p(complex(w.real, w.imag)))
            return VMobject().set_points_as_corners(pts_w).set_color(GREEN)\
                .set_stroke(width=2.5, opacity=0.7)

        self.add(always_redraw(z_dot), always_redraw(w_dot),
                 always_redraw(z_trail), always_redraw(w_trail))

        info = VGroup(
            VGroup(Tex(r"$\arg z=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\sqrt z=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN),
                   Tex(r"$+$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN),
                   Tex(r"$i$", font_size=22),
                   ).arrange(RIGHT, buff=0.08),
            Tex(r"crossing cut: image jumps", color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(np.angle(z_pt())))
        info[1][1].add_updater(lambda m: m.set_value(sqrt_z(z_pt()).real))
        info[1][3].add_updater(lambda m: m.set_value(sqrt_z(z_pt()).imag))
        self.add(info)

        self.play(theta_tr.animate.set_value(PI - 0.02),
                  run_time=3, rate_func=smooth)
        self.wait(0.6)
        # Jump: approach -π from below (going negative)
        theta_tr.set_value(-PI + 0.02)
        self.wait(0.3)
        self.play(theta_tr.animate.set_value(0.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.8)
