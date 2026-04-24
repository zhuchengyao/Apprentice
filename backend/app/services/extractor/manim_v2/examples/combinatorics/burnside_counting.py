from manim import *
import numpy as np


class BurnsideCountingExample(Scene):
    """
    Burnside's lemma (from _2025/guest_videos/burnside):
      # orbits = (1/|G|) Σ_{g ∈ G} |Fix(g)|

    Example: how many distinct 6-bead necklaces in k=3 colors under
    the cyclic group C_6 of rotations? |G|=6; fix counts are
    k^gcd(6, i) summed over i=0..5.

    SINGLE_FOCUS:
      Circle with 6 beads; ValueTracker rot_tr rotates them through
      6 group elements; always_redraw rebuilds 6 example necklaces
      colored by 3 colors; live Fix count per rotation + orbit
      count = (1/6) Σ.
    """

    def construct(self):
        title = Tex(r"Burnside: orbits $= \tfrac{1}{|G|}\sum_g |\text{Fix}(g)|$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        from math import gcd

        n = 6
        k = 3  # 3 colors
        R = 1.4
        center = np.array([-3.2, -0.3, 0])

        # Draw circle
        circ = Circle(radius=R, color=WHITE, stroke_width=2
                       ).move_to(center)
        self.play(Create(circ))

        # Specific 6-bead necklace: colors c_i
        rng = np.random.default_rng(6)
        colors_palette = [RED, BLUE, YELLOW]
        beads_colors = [0, 1, 2, 0, 1, 2]  # periodic under rotation 3

        def beads_at(shift):
            grp = VGroup()
            for i in range(n):
                angle = 2 * PI * i / n + PI / 2
                p = center + R * np.array([np.cos(angle), np.sin(angle), 0])
                c = beads_colors[(i - shift) % n]
                grp.add(Dot(p, color=colors_palette[c], radius=0.22))
            return grp

        rot_tr = ValueTracker(0)

        def beads():
            s = int(round(rot_tr.get_value())) % n
            return beads_at(s)

        self.add(always_redraw(beads))

        # Fix count formula for C_n: |Fix(g^i)| = k^gcd(n, i)
        fix_counts = [k ** gcd(n, i) for i in range(n)]
        total_orbits = sum(fix_counts) // n

        # Table
        table_rows = VGroup()
        table_rows.add(MathTex(r"i \quad\ \gcd(n, i)\quad |\text{Fix}(g^i)| = k^{\gcd}",
                                 color=WHITE, font_size=22))
        for i in range(n):
            g = gcd(n, i)
            fx = k ** g
            col = YELLOW if i == 0 else WHITE
            table_rows.add(MathTex(rf"{i}\quad\quad {g} \quad\quad {fx}",
                                     color=col, font_size=22))
        table_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16
                            ).move_to([3.2, 0.5, 0])

        self.play(Write(table_rows))

        def active_row_highlight():
            i = int(round(rot_tr.get_value())) % n
            # return a yellow box around row i+1 (0 is header)
            row = table_rows[i + 1]
            return Rectangle(
                width=row.width + 0.3, height=row.height + 0.12,
                color=YELLOW, fill_opacity=0.2, stroke_width=2
            ).move_to(row.get_center())

        self.add(always_redraw(active_row_highlight))

        summary = VGroup(
            MathTex(rf"\sum |\text{{Fix}}(g^i)| = {sum(fix_counts)}",
                     color=GREEN, font_size=22),
            MathTex(rf"\text{{orbits}} = {sum(fix_counts)}/{n} = {total_orbits}",
                     color=GREEN, font_size=24),
            Tex(r"distinct necklaces", color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18
                    ).to_edge(DOWN, buff=0.3)
        self.play(Write(summary))

        # Rotate through each group element
        for i in range(1, n + 1):
            self.play(rot_tr.animate.set_value(i),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
