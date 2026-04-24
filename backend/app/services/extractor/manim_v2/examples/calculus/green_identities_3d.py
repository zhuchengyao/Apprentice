from manim import *
import numpy as np


class GreenIdentities3DExample(Scene):
    """
    Green's identity: ∫_V (u ∇²v − v ∇²u) dV = ∮_∂V (u ∇v − v ∇u) · n dS.

    In 2D: ∬_D (u Δv − v Δu) dA = ∮_∂D (u ∂_n v − v ∂_n u) ds.

    Demonstrate with u = x, v = x² + y². Δu = 0, Δv = 4.
    LHS = ∬ -4x dA; on unit disk = 0 by symmetry. RHS also = 0.

    TWO_COLUMN: LEFT disk + vector field. RIGHT shows the integral
    equality both sides equal 0.
    """

    def construct(self):
        title = Tex(r"Green's 2nd identity: $\iint(u\Delta v-v\Delta u)\,dA=\oint(u\partial_n v-v\partial_n u)\,ds$",
                    font_size=20).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                            x_length=5.0, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.8 + DOWN * 0.2)
        self.play(Create(plane))

        # Unit disk
        disk = Circle(radius=plane.x_length / (plane.x_range[1] - plane.x_range[0]),
                      color=BLUE, stroke_width=3).move_to(plane.n2p(0))
        self.add(disk)

        # Show vector field u∇v - v∇u at grid points
        t_tr = ValueTracker(0.0)

        def uDv_mvDu_arrows():
            grp = VGroup()
            for x in np.linspace(-0.9, 0.9, 7):
                for y in np.linspace(-0.9, 0.9, 7):
                    if x * x + y * y > 0.95: continue
                    u_val = x
                    v_val = x * x + y * y
                    grad_u = np.array([1, 0])
                    grad_v = np.array([2 * x, 2 * y])
                    field = u_val * grad_v - v_val * grad_u
                    mag = np.linalg.norm(field)
                    if mag < 1e-3: continue
                    scale = 0.12 / max(mag, 0.4)
                    grp.add(Arrow(plane.n2p(complex(x, y)),
                                   plane.n2p(complex(x + field[0] * scale,
                                                      y + field[1] * scale)),
                                   color=YELLOW, buff=0, stroke_width=1.5,
                                   max_tip_length_to_length_ratio=0.3))
            return grp

        self.add(uDv_mvDu_arrows())

        # Right: integrals
        # LHS = ∬_D -4x dA = 0 by symmetry
        # RHS via explicit computation
        def LHS_numeric():
            xs = np.linspace(-1, 1, 50)
            ys = np.linspace(-1, 1, 50)
            total = 0.0
            dx = dy = xs[1] - xs[0]
            for x in xs:
                for y in ys:
                    if x * x + y * y <= 1:
                        total += -4 * x * dx * dy
            return total

        def RHS_numeric():
            ts = np.linspace(0, TAU, 200, endpoint=False)
            dt = TAU / 200
            total = 0.0
            for t in ts:
                x, y = np.cos(t), np.sin(t)
                n_out = np.array([x, y])
                u_val = x
                v_val = 1  # x² + y² = 1 on boundary
                grad_u = np.array([1, 0])
                grad_v = np.array([2 * x, 2 * y])
                integrand = u_val * np.dot(grad_v, n_out) - v_val * np.dot(grad_u, n_out)
                total += integrand * dt
            return total

        lhs = LHS_numeric()
        rhs = RHS_numeric()

        info = VGroup(
            Tex(r"$u=x$, $v=x^2+y^2$", font_size=22),
            Tex(r"$\Delta u=0$, $\Delta v=4$",
                color=YELLOW, font_size=22),
            VGroup(Tex(r"LHS $=\iint -4x\,dA=$", font_size=22),
                   DecimalNumber(lhs, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"RHS$=\oint\cdots ds=$", font_size=22),
                   DecimalNumber(rhs, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$=0$ by $x$-antisymmetry",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        self.add(info)

        # Animate an arrow along boundary showing line integrand
        theta_tr = ValueTracker(0.0)

        def boundary_probe():
            t = theta_tr.get_value()
            x, y = np.cos(t), np.sin(t)
            n_out = np.array([x, y])
            pos = plane.n2p(complex(x, y))
            normal_arrow = Arrow(pos, pos + np.array([n_out[0] * 0.3, n_out[1] * 0.3, 0]),
                                  color=RED, buff=0, stroke_width=2.5,
                                  max_tip_length_to_length_ratio=0.2)
            dot = Dot(pos, color=RED, radius=0.09)
            return VGroup(normal_arrow, dot)

        self.add(always_redraw(boundary_probe))

        self.play(theta_tr.animate.set_value(TAU),
                  run_time=5, rate_func=linear)
        self.wait(0.8)
