from manim import *
import numpy as np


class BackpropGradientDescentExample(Scene):
    """
    Gradient descent on a 2D loss landscape L(w_1, w_2) — adapted
    from _2017/nn/part3. ValueTracker step_tr advances 60 precomputed
    GD iterations; contour plot + descending trail.

    TWO_COLUMN:
      LEFT  — contour plot of L(w_1, w_2) = (w_1 - 1.5)^2 +
              5(w_2 - 0.5)^2 + 2·sin(w_1)·cos(w_2); trajectory +
              current weight dot via always_redraw.
      RIGHT — live w_1, w_2, L, ||∇L||, learning rate η, step index.
    """

    def construct(self):
        title = Tex(r"Backprop $=$ gradient descent on the loss landscape",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 5, 1], y_range=[-2.5, 3, 1],
                             x_length=7, y_length=5,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-2.5, -0.3, 0])
        self.play(Create(plane))

        def L(w1, w2):
            return ((w1 - 1.5) ** 2 + 5 * (w2 - 0.5) ** 2
                    + 2 * np.sin(w1) * np.cos(w2))

        def grad_L(w1, w2):
            return np.array([
                2 * (w1 - 1.5) + 2 * np.cos(w1) * np.cos(w2),
                10 * (w2 - 0.5) - 2 * np.sin(w1) * np.sin(w2)])

        # Level-set contour rings (approximate)
        contours = VGroup()
        for level in [1, 3, 6, 10, 15]:
            pts = []
            for a in np.linspace(0, 2 * PI, 120):
                # find r such that L(w_min + r*cos a, w_min + r*sin a) ≈ level
                r = 0.05
                for _ in range(12):
                    w1 = 1.5 + r * np.cos(a)
                    w2 = 0.5 + r * np.sin(a)
                    val = L(w1, w2)
                    r += 0.1 * (level - val) / (val + 0.2)
                    r = max(r, 0.01)
                pts.append(plane.c2p(1.5 + r * np.cos(a), 0.5 + r * np.sin(a)))
            m = VMobject(color=BLUE_D, stroke_width=1.5, stroke_opacity=0.55)
            m.set_points_as_corners(pts + [pts[0]])
            contours.add(m)
        self.play(Create(contours), run_time=2)

        # Minimum marker
        min_dot = Dot(plane.c2p(1.5, 0.5), color=GREEN, radius=0.1)
        min_lbl = Tex(r"min", color=GREEN, font_size=18
                       ).next_to(min_dot, UR, buff=0.05)
        self.play(FadeIn(min_dot), Write(min_lbl))

        # Precompute GD trajectory
        eta = 0.08
        n_steps = 60
        w = np.array([-2.0, 2.2])
        traj = [w.copy()]
        for _ in range(n_steps):
            g = grad_L(w[0], w[1])
            w = w - eta * g
            traj.append(w.copy())

        step_tr = ValueTracker(0)

        def trail():
            s = int(round(step_tr.get_value()))
            s = max(1, min(s, n_steps))
            pts = [plane.c2p(*traj[k]) for k in range(s + 1)]
            m = VMobject(color=YELLOW, stroke_width=3)
            m.set_points_as_corners(pts)
            return m

        def dot_cur():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n_steps))
            return Dot(plane.c2p(*traj[s]), color=YELLOW, radius=0.1)

        self.add(always_redraw(trail), always_redraw(dot_cur))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n_steps))
            w1, w2 = traj[s]
            loss = L(w1, w2)
            g = grad_L(w1, w2)
            gnorm = float(np.linalg.norm(g))
            return VGroup(
                MathTex(rf"\text{{step}} = {s}/{n_steps}",
                         color=WHITE, font_size=22),
                MathTex(rf"w_1 = {w1:+.3f}", color=YELLOW, font_size=22),
                MathTex(rf"w_2 = {w2:+.3f}", color=YELLOW, font_size=22),
                MathTex(rf"L = {loss:.3f}", color=BLUE, font_size=22),
                MathTex(rf"\|\nabla L\| = {gnorm:.3f}",
                         color=RED, font_size=22),
                MathTex(rf"\eta = {eta:.2f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        self.play(step_tr.animate.set_value(n_steps),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
