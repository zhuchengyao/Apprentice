from manim import *
import numpy as np


class ClacksBlockCollisionSimulation(Scene):
    """Two blocks and a wall.  A heavy block M moving left strikes a light
    stationary block m, which bounces off the wall and back.  Collisions
    are perfectly elastic.  The total number of collisions follows the
    first digits of pi as M/m = 100^k.  Here M/m = 100 produces 31
    collisions.  Animate positions and tally a live Integer counter."""

    def construct(self):
        title = Tex(
            r"Elastic block collisions count $\pi$: $M/m = 100$ $\to$ 31 clacks",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        floor = Line([-6, -1.0, 0], [6, -1.0, 0], color=WHITE,
                     stroke_width=3)
        wall = Line([-5.5, -1.0, 0], [-5.5, 3.0, 0], color=WHITE,
                    stroke_width=3)
        hatch = VGroup(*[
            Line(
                [-5.5 - 0.25, -1.0 + 0.3 * i, 0],
                [-5.5, -1.0 + 0.3 * (i + 1), 0],
                color=GREY_B, stroke_width=1.5,
            )
            for i in range(10)
        ])
        self.play(Create(floor), Create(wall), Create(hatch))

        v_small_tr = ValueTracker(0.0)
        v_big_tr = ValueTracker(-1.0)
        x_small = ValueTracker(-2.0)
        x_big = ValueTracker(2.5)

        def small_block():
            return Square(
                side_length=0.7, color=BLUE, fill_opacity=0.55,
                stroke_width=2,
            ).move_to([x_small.get_value(), -0.65, 0])

        def big_block():
            return Square(
                side_length=1.4, color=RED, fill_opacity=0.55,
                stroke_width=2,
            ).move_to([x_big.get_value(), -0.3, 0])

        sb = always_redraw(small_block)
        bb = always_redraw(big_block)
        self.add(sb, bb)

        counter = Integer(0, font_size=36, color=YELLOW)
        counter_lab = VGroup(Tex("clacks:", font_size=26), counter).arrange(
            RIGHT, buff=0.2,
        ).to_corner(UR, buff=0.4).shift(DOWN * 0.3)
        self.add(counter_lab)

        M = 100.0
        m = 1.0

        def simulate():
            xs, xb = -2.0, 2.5
            vs, vb = 0.0, -1.0
            clacks = 0
            events = []
            t = 0.0
            while clacks < 40 and t < 200:
                dt_wall = (-5.5 + 0.35 - xs) / vs if vs < 0 else np.inf
                lhs = xs + 0.35
                rhs = xb - 0.7
                relative = vs - vb
                if relative > 0:
                    dt_coll = (rhs - lhs) / relative
                else:
                    dt_coll = np.inf
                dt = min(dt_wall, dt_coll)
                if dt == np.inf or dt < 0:
                    break
                xs += vs * dt
                xb += vb * dt
                t += dt
                if dt_wall < dt_coll:
                    vs = -vs
                    clacks += 1
                    events.append(("wall", xs, xb, vs, vb, t, clacks))
                else:
                    vs_new = ((m - M) * vs + 2 * M * vb) / (m + M)
                    vb_new = ((M - m) * vb + 2 * m * vs) / (M + m)
                    vs, vb = vs_new, vb_new
                    clacks += 1
                    events.append(
                        ("block", xs, xb, vs, vb, t, clacks)
                    )
                if abs(vs) < 1e-9 and vb >= 0 and vb < 1e-9:
                    break
                if vb > 0 and vs >= vb:
                    break
            return events

        events = simulate()
        shown = min(len(events), 12)
        total_clacks = len(events)

        for i in range(shown):
            ev = events[i]
            typ, xs, xb, vs, vb, _, cnt = ev
            scale = 3.0
            target_small = -2.0 + (xs + 2.0) * scale * 0
            self.play(
                x_small.animate.set_value(-5.5 + 0.35 + (xs - (-5.5 + 0.35))),
                x_big.animate.set_value(xb),
                run_time=0.4,
            )
            counter.set_value(cnt)
            if typ == "wall":
                flash = Flash(
                    [-5.5 + 0.2, -0.65, 0], color=YELLOW,
                    flash_radius=0.35, run_time=0.25,
                )
            else:
                flash = Flash(
                    [(xs + xb) / 2, -0.4, 0], color=YELLOW,
                    flash_radius=0.35, run_time=0.25,
                )
            self.play(flash, run_time=0.25)

        counter.set_value(total_clacks)

        note = Tex(
            rf"Total collisions = {total_clacks} $\approx$ first digits of $\pi$",
            font_size=26, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note))

        formula = MathTex(
            r"\text{clacks}(M/m = 100^k) = \lfloor \pi \cdot 10^k \rfloor",
            font_size=28, color=YELLOW,
        ).next_to(note, UP, buff=0.3)
        self.play(Write(formula))
        self.wait(1.3)
