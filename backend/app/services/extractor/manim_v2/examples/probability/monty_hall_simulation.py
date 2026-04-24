from manim import *
import numpy as np


class MontyHallSimulationExample(Scene):
    """
    Monty Hall problem: 3 doors, 1 car, 2 goats. Contestant picks a
    door, host reveals a goat behind another door, then contestant
    can switch. Switch wins 2/3; stay wins 1/3.

    SINGLE_FOCUS:
      ValueTracker trial_tr runs 200 simulations for both "stay" and
      "switch" strategies. Two running-average bars converge to 1/3
      and 2/3.
    """

    def construct(self):
        title = Tex(r"Monty Hall: switch wins 2/3, stay wins 1/3",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 3 door diagrams
        doors = VGroup()
        for i in range(3):
            d = Rectangle(width=1.2, height=1.8,
                            color=WHITE, fill_opacity=0.15,
                            stroke_width=2)
            d.move_to([-4.5 + i * 1.8, 2, 0])
            num = MathTex(str(i + 1), font_size=30,
                            color=WHITE).move_to(d.get_center())
            doors.add(VGroup(d, num))
        self.play(FadeIn(doors))

        # Precompute 200 trials
        N = 200
        rng = np.random.default_rng(13)
        car_doors = rng.integers(0, 3, size=N)
        picks = rng.integers(0, 3, size=N)

        stay_wins = []
        switch_wins = []
        for i in range(N):
            car = car_doors[i]
            pick = picks[i]
            stay_wins.append(int(pick == car))
            # Host opens a goat door not equal to pick
            available = [d for d in range(3) if d != pick and d != car]
            if not available:  # pick == car
                # Host reveals one of the other two
                available = [d for d in range(3) if d != pick]
            # Switch door: the one not picked and not revealed
            switch_door = [d for d in range(3) if d != pick and d != available[0]][0]
            switch_wins.append(int(switch_door == car))

        cum_stay = np.cumsum(stay_wins)
        cum_switch = np.cumsum(switch_wins)

        # Axes
        ax = Axes(x_range=[0, N, 40], y_range=[0, 1, 0.25],
                   x_length=9, y_length=3.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([0, -1.5, 0])
        xlbl = Tex("trials", font_size=18).next_to(ax, DOWN, buff=0.1)
        ylbl = Tex("win rate", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        # Theoretical reference lines
        stay_ref = DashedLine(ax.c2p(0, 1/3), ax.c2p(N, 1/3),
                                color=RED, stroke_width=2)
        switch_ref = DashedLine(ax.c2p(0, 2/3), ax.c2p(N, 2/3),
                                  color=GREEN, stroke_width=2)
        self.play(Create(stay_ref), Create(switch_ref))

        trial_tr = ValueTracker(0)

        def stay_curve():
            k = int(round(trial_tr.get_value()))
            k = max(1, min(k, N))
            pts = [ax.c2p(i + 1, cum_stay[i] / (i + 1))
                   for i in range(k)]
            m = VMobject(color=RED, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def switch_curve():
            k = int(round(trial_tr.get_value()))
            k = max(1, min(k, N))
            pts = [ax.c2p(i + 1, cum_switch[i] / (i + 1))
                   for i in range(k)]
            m = VMobject(color=GREEN, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(stay_curve), always_redraw(switch_curve))

        def info():
            k = int(round(trial_tr.get_value()))
            k = max(1, min(k, N))
            stay_p = cum_stay[k - 1] / k
            switch_p = cum_switch[k - 1] / k
            return VGroup(
                MathTex(rf"\text{{trials}} = {k}",
                         color=WHITE, font_size=22),
                MathTex(rf"\hat p_{{\text{{stay}}}} = {stay_p:.3f}",
                         color=RED, font_size=22),
                MathTex(rf"\hat p_{{\text{{switch}}}} = {switch_p:.3f}",
                         color=GREEN, font_size=22),
                MathTex(r"1/3 \text{ vs } 2/3",
                         color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(trial_tr.animate.set_value(N),
                   run_time=9, rate_func=linear)
        self.wait(0.5)
