from manim import *
import numpy as np


class DoublePendulumExample(Scene):
    def construct(self):
        title = Text("Double pendulum: chaotic motion", font_size=28).to_edge(UP)
        self.play(Write(title))

        g = 9.8
        L1 = L2 = 1.5
        m1 = m2 = 1.0
        dt = 0.02
        steps_per_frame = 2

        # Initial angles (near-vertical upside-down)
        state = [np.array([2.5, 0.0, 2.2, 0.0]),
                 np.array([2.502, 0.0, 2.2, 0.0])]  # two nearly-identical initial conditions
        colors = [BLUE, RED]

        def deriv(s):
            th1, w1, th2, w2 = s
            d = th2 - th1
            denom1 = (2 * m1 + m2 - m2 * np.cos(2 * d))
            a1 = (-g * (2 * m1 + m2) * np.sin(th1)
                  - m2 * g * np.sin(th1 - 2 * th2)
                  - 2 * np.sin(d) * m2 * (w2**2 * L2 + w1**2 * L1 * np.cos(d))) / (L1 * denom1)
            a2 = (2 * np.sin(d) * (w1**2 * L1 * (m1 + m2)
                  + g * (m1 + m2) * np.cos(th1)
                  + w2**2 * L2 * m2 * np.cos(d))) / (L2 * denom1)
            return np.array([w1, a1, w2, a2])

        origin = np.array([0, 0.8, 0])
        pivot = Dot(origin, color=WHITE, radius=0.06)
        self.add(pivot)

        rods1 = VGroup()
        rods2 = VGroup()
        bobs = VGroup()
        for c in colors:
            r1 = Line(origin, origin + DOWN * L1, color=c, stroke_width=3)
            r2 = Line(r1.get_end(), r1.get_end() + DOWN * L2, color=c, stroke_width=3)
            bob = Dot(r2.get_end(), color=c, radius=0.1)
            rods1.add(r1); rods2.add(r2); bobs.add(bob)
        self.add(rods1, rods2, bobs)

        traces = [VMobject(color=c, stroke_width=2) for c in colors]
        for t in traces:
            t.set_points_as_corners([origin])
        self.add(*traces)

        def update_system(mobj, dt_frame):
            for _ in range(steps_per_frame):
                for i in range(2):
                    k1 = deriv(state[i])
                    k2 = deriv(state[i] + k1 * dt / 2)
                    k3 = deriv(state[i] + k2 * dt / 2)
                    k4 = deriv(state[i] + k3 * dt)
                    state[i] = state[i] + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

            for i in range(2):
                th1, _, th2, _ = state[i]
                p1 = origin + np.array([L1 * np.sin(th1), -L1 * np.cos(th1), 0])
                p2 = p1 + np.array([L2 * np.sin(th2), -L2 * np.cos(th2), 0])
                rods1[i].put_start_and_end_on(origin, p1)
                rods2[i].put_start_and_end_on(p1, p2)
                bobs[i].move_to(p2)
                pts = list(traces[i].get_anchors()) + [p2]
                if len(pts) > 200:
                    pts = pts[-200:]
                traces[i].set_points_as_corners(pts)

        dummy = Mobject()
        dummy.add_updater(update_system)
        self.add(dummy)
        self.wait(6)
        dummy.clear_updaters()

        caption = Text("Two near-identical starts diverge (sensitive dependence)",
                       font_size=22, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
