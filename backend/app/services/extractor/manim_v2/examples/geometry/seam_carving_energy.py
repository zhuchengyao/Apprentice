from manim import *
import numpy as np


class SeamCarvingEnergyExample(Scene):
    """
    Seam carving (from _2020/18S191/seam_carving): content-aware
    image resizing finds the lowest-energy path from top to bottom
    and removes it, shrinking horizontally without distorting salient
    regions.

    SINGLE_FOCUS:
      10×14 energy grid (random with two high-energy "salient" spots).
      ValueTracker step_tr runs DP fill across rows; always_redraw
      cumulative-energy values; second phase traces the minimum
      seam top→bottom in RED.
    """

    def construct(self):
        title = Tex(r"Seam carving: DP finds lowest-energy path",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rows, cols = 8, 12
        rng = np.random.default_rng(5)
        energy = rng.integers(1, 5, (rows, cols)).astype(float)
        # Add high-energy "salient" blob
        for r in range(3, 6):
            for c in range(3, 6):
                energy[r, c] += 8

        # DP: cumulative energy from top
        dp = energy.copy()
        for r in range(1, rows):
            for c in range(cols):
                candidates = [dp[r - 1, c]]
                if c > 0:
                    candidates.append(dp[r - 1, c - 1])
                if c < cols - 1:
                    candidates.append(dp[r - 1, c + 1])
                dp[r, c] += min(candidates)

        cell = 0.55
        origin = np.array([-cell * (cols - 1) / 2, cell * (rows - 1) / 2 - 0.4, 0])

        def pos(r, c):
            return origin + np.array([c * cell, -r * cell, 0])

        # Draw grid base
        grid = VGroup()
        for r in range(rows):
            for c in range(cols):
                # Color by energy (darker = higher)
                e = energy[r, c]
                intensity = min(1.0, 0.15 + 0.1 * (e / energy.max()))
                sq = Square(side_length=cell * 0.95, color=WHITE,
                              fill_opacity=intensity, fill_color=WHITE,
                              stroke_width=0.8)
                sq.move_to(pos(r, c))
                grid.add(sq)
        self.play(FadeIn(grid), run_time=1.2)

        # Animate filling row by row
        step_tr = ValueTracker(0)

        def fill_cells():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, rows))
            grp = VGroup()
            for r in range(s):
                for c in range(cols):
                    v = dp[r, c]
                    # Color by dp value (low = cool, high = warm)
                    frac = (v - dp.min()) / (dp.max() - dp.min() + 1e-6)
                    color = interpolate_color(BLUE, RED, frac)
                    sq = Square(side_length=cell * 0.95,
                                  color=color, fill_opacity=0.55,
                                  stroke_width=1)
                    sq.move_to(pos(r, c))
                    grp.add(sq)
                    if rows <= 10:
                        lbl = MathTex(rf"{int(v)}",
                                        color=BLACK, font_size=14)
                        lbl.move_to(pos(r, c))
                        grp.add(lbl)
            return grp

        self.add(always_redraw(fill_cells))

        self.play(step_tr.animate.set_value(rows),
                   run_time=5, rate_func=linear)
        self.wait(0.5)

        # Phase 2: traceback minimum seam
        # Start from bottom row: find argmin
        seam = [int(np.argmin(dp[rows - 1]))]
        for r in range(rows - 1, 0, -1):
            c = seam[-1]
            candidates = [(dp[r - 1, c], c)]
            if c > 0:
                candidates.append((dp[r - 1, c - 1], c - 1))
            if c < cols - 1:
                candidates.append((dp[r - 1, c + 1], c + 1))
            seam.append(min(candidates)[1])
        seam.reverse()

        seam_tr = ValueTracker(0)

        def seam_path():
            k = int(round(seam_tr.get_value()))
            k = max(0, min(k, len(seam)))
            grp = VGroup()
            for i in range(k):
                r, c = i, seam[i]
                d = Dot(pos(r, c), color=RED, radius=0.13)
                grp.add(d)
            for i in range(1, k):
                c1 = seam[i - 1]
                c2 = seam[i]
                grp.add(Line(pos(i - 1, c1), pos(i, c2),
                               color=RED, stroke_width=4))
            return grp

        self.add(always_redraw(seam_path))

        seam_note = Tex(r"minimum-energy seam (traceback)",
                          color=RED, font_size=22
                          ).next_to(title, DOWN, buff=0.3)
        self.play(Write(seam_note))
        self.play(seam_tr.animate.set_value(len(seam)),
                   run_time=3, rate_func=linear)

        total = dp[rows - 1, seam[-1]]
        final_lbl = MathTex(rf"\text{{total energy}} = {int(total)}",
                              color=RED, font_size=24
                              ).to_edge(DOWN, buff=0.4)
        self.play(Write(final_lbl))
        self.wait(0.4)
