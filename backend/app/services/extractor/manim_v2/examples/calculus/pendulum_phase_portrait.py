from manim import *
import numpy as np


class PendulumPhasePortraitExample(Scene):
    """
    Nonlinear pendulum phase portrait (from _2019/diffyq/part1/phase_space):
    θ'' + sin θ = 0. Phase space (θ, θ') has closed orbits for
    low energy (oscillations), open orbits for high energy
    (rotations), separated by the separatrix through the unstable
    saddle at θ = π, θ' = 0.

    SINGLE_FOCUS:
      Phase plane with 8 precomputed orbit trajectories (oscillatory
      below, rotational above); ValueTracker t_tr advances a rider
      dot on one chosen orbit; orbit family drawn.
    """

    def construct(self):
        title = Tex(r"Pendulum phase space: $\ddot\theta + \sin\theta = 0$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2 * PI, 2 * PI, PI / 2],
                             y_range=[-3, 3, 1],
                             x_length=10, y_length=5,
                             background_line_style={"stroke_opacity": 0.2}
                             ).move_to([0, -0.4, 0])
        self.play(Create(plane))

        # Axis labels
        th_lbl = MathTex(r"\theta", font_size=22).next_to(plane, DOWN, buff=0.1)
        dth_lbl = MathTex(r"\dot\theta", font_size=22).next_to(plane, LEFT, buff=0.1)
        self.play(Write(th_lbl), Write(dth_lbl))

        # Integrate orbits via RK4-ish Euler for plotting
        def integrate(th0, dth0, T=20.0, dt=0.02):
            pts = [(th0, dth0)]
            th, dth = th0, dth0
            for _ in range(int(T / dt)):
                # f = (dth, -sin th)
                k1 = (dth, -np.sin(th))
                k2 = (dth + 0.5 * dt * k1[1],
                       -np.sin(th + 0.5 * dt * k1[0]))
                th += dt * k2[0]
                dth += dt * k2[1]
                pts.append((th, dth))
                if abs(th) > 3 * PI or abs(dth) > 3.5:
                    break
            return pts

        # Draw family of orbits
        orbit_family = VGroup()
        seeds = [
            (0.5, 0, BLUE),
            (1.5, 0, BLUE),
            (2.5, 0, BLUE),
            (0, 2.5, YELLOW),    # rotating
            (0, -2.5, YELLOW),
            (PI - 0.01, 0, RED),  # near separatrix
            (0, 2.0, PURPLE),    # just above
            (0, 1.5, GREEN),
        ]
        for (th0, dth0, col) in seeds:
            pts = integrate(th0, dth0, T=14.0)
            v = VMobject(color=col, stroke_width=2)
            v.set_points_as_corners(
                [plane.c2p(th, dth) for (th, dth) in pts
                 if abs(th) <= 2 * PI and abs(dth) <= 3])
            orbit_family.add(v)
        self.play(Create(orbit_family), run_time=2.5)

        # Separatrix: sharp drawn
        sep_pts_upper = integrate(-PI + 0.001, 0, T=20.0)
        sep_pts_lower = integrate(-PI + 0.001, 0.0001, T=20.0)
        # Separatrix energy E = 1 - cos π = 2 ⇒ dth = ±√(2(1 - cos θ + 2 - 2))
        sep_curve = VMobject(color=WHITE, stroke_width=3)
        sep_pts = []
        for th in np.linspace(-PI, PI, 120):
            val = 2 * (1 - np.cos(th) - 1 + 1)  # = 2 + 2 cos th? Let me fix
            # Correct: E = 1/2 dth² + (1 - cos θ). Separatrix E = 2 ⇒ dth² = 2 + 2 cos θ
            d2 = 2 + 2 * np.cos(th)
            if d2 < 0:
                continue
            dth = np.sqrt(d2)
            sep_pts.append(plane.c2p(th, dth))
        sep_pts += [plane.c2p(th, -np.sqrt(2 + 2 * np.cos(th)))
                     for th in np.linspace(PI, -PI, 120)
                     if 2 + 2 * np.cos(th) >= 0]
        sep_curve.set_points_as_corners(sep_pts + [sep_pts[0]])
        sep_curve.set_color(RED).set_stroke(width=3)
        self.play(Create(sep_curve), run_time=2)

        # Rider on small-oscillation orbit
        rider_orbit = integrate(1.5, 0, T=14.0)
        t_tr = ValueTracker(0.0)

        def rider():
            t = t_tr.get_value()
            idx = int(t * (len(rider_orbit) - 1))
            idx = max(0, min(idx, len(rider_orbit) - 1))
            th, dth = rider_orbit[idx]
            return Dot(plane.c2p(th, dth), color=ORANGE, radius=0.1)

        self.add(always_redraw(rider))

        info = VGroup(
            Tex(r"closed loops: oscillation", color=BLUE, font_size=22),
            Tex(r"open curves: rotation", color=YELLOW, font_size=22),
            Tex(r"separatrix (red): $E = 2$", color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        self.play(Write(info))

        self.play(t_tr.animate.set_value(1.0),
                   run_time=5, rate_func=linear)
        self.wait(0.4)
