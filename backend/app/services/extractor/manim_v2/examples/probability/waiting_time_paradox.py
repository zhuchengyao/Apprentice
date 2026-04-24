from manim import *
import numpy as np


class WaitingTimeParadoxExample(Scene):
    """
    Bus waiting paradox: if buses arrive per Poisson process with
    rate λ, average inter-arrival = 1/λ. A passenger arriving at
    random time waits average 1/λ (not 1/(2λ) as naive reasoning
    suggests) — size-biased sampling visits longer intervals
    proportionally more often.

    TWO_COLUMN: LEFT timeline with Poisson-arrival bus dots +
    ValueTracker pass_tr randomly placed passenger marker; highlighted
    interval (containing passenger). RIGHT histograms of interval
    lengths (vs size-biased).
    """

    def construct(self):
        title = Tex(r"Waiting time paradox: $E[\text{wait}]=1/\lambda$ (not $1/(2\lambda)$)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        np.random.seed(2)
        lam = 1.0  # rate 1 per unit
        T = 12.0
        # Generate Poisson arrivals
        arrivals = []
        t = 0
        while t < T:
            t += np.random.exponential(1 / lam)
            if t < T:
                arrivals.append(t)
        arrivals = [0.0] + arrivals + [T]

        line = NumberLine(x_range=[0, T, 2], length=11,
                          include_numbers=True,
                          font_size=18).shift(DOWN * 0.3)
        self.play(Create(line))

        # Bus arrival dots
        for t in arrivals[1:-1]:
            self.add(Dot(line.n2p(t), color=BLUE, radius=0.08))
        self.add(Tex(r"buses (blue dots)", color=BLUE, font_size=20).to_corner(UR, buff=0.3))

        # Passenger marker
        pass_tr = ValueTracker(0.0)

        def passenger_pos():
            return pass_tr.get_value()

        def passenger_dot():
            t = passenger_pos()
            return Dot(line.n2p(t), color=RED, radius=0.11)

        def pass_label():
            t = passenger_pos()
            return Tex(r"you", color=RED, font_size=18).next_to(
                line.n2p(t), UP, buff=0.05)

        def interval_highlight():
            t = passenger_pos()
            # find surrounding arrivals
            idx = np.searchsorted(arrivals, t)
            a, b = arrivals[max(0, idx - 1)], arrivals[min(len(arrivals) - 1, idx)]
            return Line(line.n2p(a), line.n2p(b),
                         color=YELLOW, stroke_width=6)

        def wait_segment():
            t = passenger_pos()
            idx = np.searchsorted(arrivals, t)
            b = arrivals[min(len(arrivals) - 1, idx)]
            return Line(line.n2p(t) + UP * 0.3,
                         line.n2p(b) + UP * 0.3,
                         color=ORANGE, stroke_width=4)

        self.add(always_redraw(interval_highlight),
                 always_redraw(wait_segment),
                 always_redraw(passenger_dot),
                 always_redraw(pass_label))

        # Info
        def current_wait():
            t = passenger_pos()
            idx = np.searchsorted(arrivals, t)
            b = arrivals[min(len(arrivals) - 1, idx)]
            return float(b - t)

        def interval_len():
            t = passenger_pos()
            idx = np.searchsorted(arrivals, t)
            a = arrivals[max(0, idx - 1)]
            b = arrivals[min(len(arrivals) - 1, idx)]
            return float(b - a)

        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"interval length $=$", color=YELLOW, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"wait $=$", color=ORANGE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"uniform $t$ sees bigger intervals",
                color=YELLOW, font_size=20),
            Tex(r"$E[\text{wait}]=E[\text{len}]/2\cdot \text{size-bias}=1/\lambda$",
                color=GREEN, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=1.5).shift(LEFT * 3.5)

        info[0][1].add_updater(lambda m: m.set_value(passenger_pos()))
        info[1][1].add_updater(lambda m: m.set_value(interval_len()))
        info[2][1].add_updater(lambda m: m.set_value(current_wait()))
        self.add(info)

        self.play(pass_tr.animate.set_value(T - 0.2),
                  run_time=10, rate_func=linear)
        self.wait(0.8)
