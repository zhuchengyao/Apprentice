from manim import *
import numpy as np


class SteveLibrarianBayesExample(Scene):
    """
    Base-rate fallacy: as base-rate ratio shifts, the posterior P(librarian|description)
    moves dramatically. ValueTracker base_pct shifts how many of the 200
    people are librarians; matching dots recolored YELLOW; live posterior updates.

    SINGLE_FOCUS:
      Two grids of dots: top row = librarians, bottom row = farmers.
      ValueTracker base_pct slides the librarian count from 1 to 100
      (out of 200 total). 40% of librarians and 10% of farmers match
      Steve's description (recolored YELLOW). Live posterior updates.
    """

    def construct(self):
        title = Tex(r"Base-rate fallacy: $P(\text{librarian} \mid \text{Steve-like})$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        TOTAL = 200

        base_tr = ValueTracker(10)  # number of librarians out of TOTAL

        # Layout
        anchor = np.array([-5.5, -1.5, 0])
        spacing = 0.32

        def population_dots():
            n_lib = max(0, min(TOTAL, int(round(base_tr.get_value()))))
            n_farm = TOTAL - n_lib
            grp = VGroup()
            # Top row: librarians colored BLUE; YELLOW for the 40% who match
            n_lib_match = int(round(0.4 * n_lib))
            cols = 25
            for i in range(n_lib):
                row = i // cols
                col = i % cols
                pos = anchor + np.array([col * spacing, +1.0 + row * spacing, 0])
                color = YELLOW if i < n_lib_match else BLUE
                grp.add(Dot(pos, color=color, radius=0.10))
            # Bottom rows: farmers GREEN_E; YELLOW for the 10% who match
            n_farm_match = int(round(0.1 * n_farm))
            for i in range(n_farm):
                row = i // cols
                col = i % cols
                pos = anchor + np.array([col * spacing, -1.0 - row * spacing, 0])
                color = YELLOW if i < n_farm_match else GREEN_E
                grp.add(Dot(pos, color=color, radius=0.07))
            return grp

        self.add(always_redraw(population_dots))

        # Labels
        lib_lbl = Tex(r"librarians", color=BLUE, font_size=22).move_to(
            anchor + np.array([-1.5, +1.0, 0]))
        farm_lbl = Tex(r"farmers", color=GREEN, font_size=22).move_to(
            anchor + np.array([-1.5, -1.4, 0]))
        self.play(Write(lib_lbl), Write(farm_lbl))

        # RIGHT COLUMN
        rcol_x = +5.0

        def info_panel():
            n_lib = max(0, min(TOTAL, int(round(base_tr.get_value()))))
            n_farm = TOTAL - n_lib
            n_lib_match = int(round(0.4 * n_lib))
            n_farm_match = int(round(0.1 * n_farm))
            total_match = n_lib_match + n_farm_match
            posterior = n_lib_match / total_match if total_match > 0 else 0
            return VGroup(
                MathTex(rf"\text{{librarians}} = {n_lib}",
                        color=BLUE, font_size=22),
                MathTex(rf"\text{{farmers}} = {n_farm}",
                        color=GREEN, font_size=22),
                MathTex(rf"\text{{Steve-like lib.}} = {n_lib_match}",
                        color=YELLOW, font_size=20),
                MathTex(rf"\text{{Steve-like farm.}} = {n_farm_match}",
                        color=YELLOW, font_size=20),
                MathTex(rf"P(\text{{lib}} \mid \text{{Steve}}) = {posterior:.3f}",
                        color=ORANGE, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        # Sweep base rate from 10 to 100 to 1
        for tgt in [50, 100, 5, 1, 30]:
            self.play(base_tr.animate.set_value(tgt),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)

        principle = Tex(r"Posterior depends on base rate as much as on the description",
                        color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(Write(principle))
        self.wait(1.0)
