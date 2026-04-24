from manim import *
import numpy as np


class ClacksPiExample(Scene):
    """
    Block-collision counting π (simpler sibling of clacks_count_pi):
    a small block of mass m hits a heavy block of mass 10^(2k) at rest
    against a wall. The number of clacks → π · 10^k.

    SINGLE_FOCUS:
      Two blocks + wall + ValueTracker t_tr advances a precomputed
      collision simulation; count increments at each clack and is
      displayed live. Two runs: k=0 (3 clacks) and k=1 (31 clacks).
    """

    def construct(self):
        title = Tex(r"Clacks: blocks $\to$ $\pi$ (ratio of masses)",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        floor = Line([-6.5, -2.2, 0], [6.5, -2.2, 0], color=WHITE,
                      stroke_width=3)
        wall = Line([-6.5, -2.2, 0], [-6.5, 2.0, 0], color=WHITE,
                      stroke_width=3)
        self.play(Create(floor), Create(wall))

        def simulate(M_ratio, n_max=40):
            """
            1D elastic collisions between block 1 (mass 1) and block 2
            (mass M_ratio), with block 2 bouncing off an immovable wall.
            Returns list of (x1, x2) positions over time plus clack count.
            """
            # Use analytic rotational formulation
            v1 = 0.0     # light block initially at rest to right
            v2 = 0.0
            x1 = 2.5
            x2 = 1.0
            # heavy block hits light block from the right? Let me re-setup:
            # Convention: light mass m = 1, incoming from right with
            # velocity -vo; heavy mass M at rest left of light; wall
            # on far left.
            v1 = 0.0   # heavy (left)
            v2 = -1.0  # light (right), moving left
            x1 = 0.5   # heavy
            x2 = 3.0   # light
            M = M_ratio
            m = 1.0
            trajs = [(x1, x2)]
            clacks = 0
            dt = 0.01
            while clacks < n_max and x2 < 6:
                # Detect collision: blocks touch if x2 - x1 < 0.2
                # Detect wall: x1 < -5.5
                next_x1 = x1 + v1 * dt
                next_x2 = x2 + v2 * dt
                if next_x2 - next_x1 < 0.6 and (v2 - v1) < 0:
                    # elastic collision 1D
                    new_v1 = ((M - m) * v1 + 2 * m * v2) / (M + m)
                    new_v2 = ((m - M) * v2 + 2 * M * v1) / (M + m)
                    v1, v2 = new_v1, new_v2
                    clacks += 1
                    x1 += v1 * dt
                    x2 += v2 * dt
                    trajs.append((x1, x2))
                    trajs.append((x1, x2))  # duplicate frame
                    continue
                if next_x1 < -5.9 and v1 < 0:
                    v1 = -v1
                    clacks += 1
                    x1 += v1 * dt
                    x2 += v2 * dt
                    trajs.append((x1, x2))
                    continue
                x1, x2 = next_x1, next_x2
                trajs.append((x1, x2))
            return trajs, clacks

        def render_run(M_ratio, size_heavy, label_txt):
            trajs, n_clacks = simulate(M_ratio)
            t_tr = ValueTracker(0.0)

            def heavy_block():
                idx = int(t_tr.get_value() * (len(trajs) - 1))
                idx = max(0, min(idx, len(trajs) - 1))
                x = trajs[idx][0]
                return Rectangle(width=size_heavy, height=size_heavy,
                                  color=BLUE, fill_opacity=0.55,
                                  stroke_width=2
                                  ).move_to([x, -2.2 + size_heavy / 2, 0])

            def light_block():
                idx = int(t_tr.get_value() * (len(trajs) - 1))
                idx = max(0, min(idx, len(trajs) - 1))
                x = trajs[idx][1]
                return Rectangle(width=0.5, height=0.5, color=ORANGE,
                                  fill_opacity=0.65, stroke_width=2
                                  ).move_to([x, -2.2 + 0.25, 0])

            def count_label():
                idx = int(t_tr.get_value() * (len(trajs) - 1))
                frac_done = idx / max(1, len(trajs) - 1)
                # Clacks so far ≈ n_clacks * frac (not exact, but lively)
                clacks_so_far = int(round(n_clacks * frac_done))
                return VGroup(
                    Tex(label_txt, color=WHITE, font_size=24),
                    MathTex(rf"\text{{clacks}} = {clacks_so_far}",
                             color=YELLOW, font_size=26),
                    MathTex(rf"\text{{total}} = {n_clacks}",
                             color=GREEN, font_size=22),
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.2, 1.0, 0])

            heavy = always_redraw(heavy_block)
            light = always_redraw(light_block)
            panel = always_redraw(count_label)
            self.add(heavy, light, panel)

            self.play(t_tr.animate.set_value(1.0),
                       run_time=4.5, rate_func=linear)
            self.wait(0.4)
            self.remove(heavy, light, panel)
            return n_clacks

        # Run 1: M = 1 (equal masses), expect 3 clacks
        render_run(1.0, 0.7, r"$M/m = 1 \to \pi \cdot 10^0 = 3$")
        # Run 2: M = 100, expect 31 clacks
        render_run(100.0, 1.2, r"$M/m = 100 \to \pi \cdot 10^1 = 31$")

        final = Tex(r"Clacks $\to \pi\cdot 10^k$ as $M/m \to 10^{2k}$",
                    color=YELLOW, font_size=28).to_edge(DOWN, buff=0.3)
        self.play(Write(final))
        self.wait(0.4)
