from manim import *
import numpy as np


class GaltonBoardExample(Scene):
    """
    Galton board (bean machine): N balls fall through a triangular
    peg array; each peg deflects left/right with prob 1/2; bin counts
    converge to a binomial distribution → Gaussian (CLT).

    Adapted from _2023/clt/galton_board.

    SINGLE_FOCUS:
      Triangular peg array with 10 rows; ValueTracker ball_idx_tr
      sends 200 balls through sequentially (precomputed paths);
      always_redraw bin histogram grows; overlay shows binomial
      reference + σ scaling.
    """

    def construct(self):
        title = Tex(r"Galton board $\to$ binomial $\to$ Gaussian",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N_rows = 10
        peg_y_top = 2.0
        peg_spacing = 0.4
        bin_y = -2.6

        # Pegs
        pegs = VGroup()
        for r in range(N_rows):
            for c in range(r + 1):
                x = (c - r / 2) * peg_spacing
                y = peg_y_top - r * peg_spacing
                pegs.add(Dot([x, y, 0], color=GREY_B, radius=0.04))
        self.play(FadeIn(pegs))

        # Bins (N_rows + 1 bins)
        bin_count = N_rows + 1
        bin_xs = [(c - N_rows / 2) * peg_spacing for c in range(bin_count)]

        # Precompute N balls
        rng = np.random.default_rng(12)
        N_balls = 200
        # Each ball: list of (L or R) deflections
        all_paths = []
        final_bins = []
        for _ in range(N_balls):
            path = rng.choice([-0.5, 0.5], size=N_rows)
            # Final x coord
            x_pos = 0.0
            x_trail = [0.0]
            for dx in path:
                x_pos += dx * peg_spacing
                x_trail.append(x_pos)
            final_bin = int(round(x_pos / peg_spacing + N_rows / 2))
            final_bin = max(0, min(final_bin, N_rows))
            all_paths.append(x_trail)
            final_bins.append(final_bin)

        ball_idx_tr = ValueTracker(0)

        def histogram():
            n = int(round(ball_idx_tr.get_value()))
            n = max(0, min(n, N_balls))
            counts = [sum(1 for k in range(n) if final_bins[k] == i)
                      for i in range(bin_count)]
            grp = VGroup()
            for i, c in enumerate(counts):
                if c == 0:
                    continue
                h = c * 0.04
                bar = Rectangle(width=peg_spacing * 0.85, height=h,
                                 color=BLUE, fill_opacity=0.7,
                                 stroke_width=1
                                 ).move_to([bin_xs[i], bin_y + h / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(histogram))

        # Binomial overlay: p=0.5, n=10; mean = 0, sigma = √n/2
        def binomial_overlay():
            n = int(round(ball_idx_tr.get_value()))
            n = max(1, min(n, N_balls))
            from math import comb
            pts = []
            for i in range(bin_count):
                prob = comb(N_rows, i) * 0.5 ** N_rows
                expected_count = prob * n
                pts.append([bin_xs[i], bin_y + expected_count * 0.04, 0])
            m = VMobject(color=YELLOW, stroke_width=3)
            m.set_points_smoothly(pts)
            return m

        self.add(always_redraw(binomial_overlay))

        def info():
            n = int(round(ball_idx_tr.get_value()))
            n = max(0, min(n, N_balls))
            if n > 0:
                mean = np.mean(final_bins[:n]) - N_rows / 2
                sd = np.std(final_bins[:n])
            else:
                mean = 0.0
                sd = 0.0
            return VGroup(
                MathTex(rf"N = {n}", color=WHITE, font_size=22),
                MathTex(rf"\overline{{x}} = {mean:+.2f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\sigma = {sd:.2f}", color=RED, font_size=22),
                MathTex(rf"\text{{expected }}\sigma = \sqrt{{n/4}} = {np.sqrt(N_rows / 4):.2f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(ball_idx_tr.animate.set_value(N_balls),
                   run_time=10, rate_func=linear)
        self.wait(0.5)
