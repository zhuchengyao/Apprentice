from manim import *
import numpy as np


class ClacksCountPiExample(Scene):
    """
    Colliding-blocks count π via the phase-circle reflection picture.

    For mass ratio m_big/m_small = 100^n, the number of clacks equals
    ⌊π·10ⁿ⌋. Each clack rotates a state vector by 2θ where
    θ = arctan(√(m_small/m_big)).

    TWO_COLUMN:
      LEFT  — phase circle with the polygonal reflection path drawn
              progressively. ValueTracker step_idx advances; an
              always_redraw VGroup builds chord by chord; live count
              increments. Three runs at mass ratios 1, 100, 10000.
      RIGHT — live mass ratio, θ in degrees, expected count π·10ⁿ,
              actual count, formula.
    """

    def construct(self):
        title = Tex(r"Colliding blocks count $\pi$ via phase-circle reflections",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        circle = Circle(radius=2.2, color=BLUE,
                        stroke_width=2).move_to([-2.4, -0.4, 0])
        self.play(Create(circle))

        ratios = [1, 100, 10000]
        thetas = [np.arctan(1.0 / np.sqrt(r)) for r in ratios]

        # Run through three mass ratios; for each, animate clack-by-clack
        for idx, (ratio, theta) in enumerate(zip(ratios, thetas)):
            n_clacks = int(PI / (2 * theta))
            angle_step = 2 * theta

            step_tr = ValueTracker(0)

            def reflection_path():
                k_max = int(round(step_tr.get_value()))
                pts = []
                for k in range(k_max + 1):
                    ang = PI - k * angle_step
                    if ang < -0.1:
                        break
                    pts.append(circle.point_at_angle(ang))
                if len(pts) < 2:
                    return VMobject(color=BLACK, stroke_width=0)
                path = VMobject(color=ORANGE, stroke_width=3)
                path.set_points_as_corners(pts)
                return path

            # Right column readout
            rcol_x = +3.2

            def stats(ratio=ratio, theta=theta, n_clacks=n_clacks):
                def fn():
                    k = int(round(step_tr.get_value()))
                    return VGroup(
                        MathTex(rf"\text{{ratio}} = {ratio}", color=BLUE, font_size=22),
                        MathTex(rf"\theta = {np.degrees(theta):.4f}^\circ",
                                color=GREEN, font_size=22),
                        MathTex(rf"\text{{clacks so far}} = {k}",
                                color=YELLOW, font_size=24),
                        MathTex(rf"\lfloor \pi \cdot 10^{{{idx}}} \rfloor = {n_clacks}",
                                color=YELLOW, font_size=22),
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +1.0, 0])
                return fn

            path_redrawer = always_redraw(reflection_path)
            stats_redrawer = always_redraw(stats(ratio, theta, n_clacks))
            self.add(path_redrawer, stats_redrawer)

            # Animate stepping through clacks (clamp for large counts)
            visible_steps = min(n_clacks, 60)
            self.play(step_tr.animate.set_value(visible_steps),
                      run_time=2.5, rate_func=linear)
            self.wait(0.6)

            # Clean up before next iteration so always_redraw closures don't accumulate
            self.remove(path_redrawer, stats_redrawer)

            # Show final outline of complete path
            final_path = VMobject(color=ORANGE, stroke_width=2,
                                  stroke_opacity=0.5)
            full_pts = []
            for k in range(n_clacks + 1):
                ang = PI - k * angle_step
                if ang < -0.1:
                    break
                full_pts.append(circle.point_at_angle(ang))
            if len(full_pts) >= 2:
                final_path.set_points_as_corners(full_pts)
            self.add(final_path)
            self.wait(0.4)
            if idx < len(ratios) - 1:
                self.remove(final_path)

        formula = MathTex(r"\#\text{clacks}(100^n) = \lfloor \pi \cdot 10^n \rfloor",
                          color=YELLOW, font_size=28).to_edge(DOWN, buff=0.4)
        self.play(Write(formula))
        self.wait(1.0)
