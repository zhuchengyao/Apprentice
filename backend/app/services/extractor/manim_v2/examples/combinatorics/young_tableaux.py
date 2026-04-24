from manim import *
import numpy as np


class YoungTableauxExample(Scene):
    """
    Standard Young tableaux of shape λ = (3, 2, 1) (Ferrers diagram
    with row lengths 3, 2, 1). Count = 16 via hook-length formula.

    SINGLE_FOCUS:
      Show the Young diagram, then the hook lengths, then apply
      hook-length formula. ValueTracker step_tr reveals stages.
    """

    def construct(self):
        title = Tex(r"Standard Young tableaux: hook-length formula",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        shape = [3, 2, 1]
        cell = 0.85
        origin = np.array([-2.0, 1.0, 0])

        def cell_center(i, j):
            return origin + np.array([j * cell, -i * cell, 0])

        # Hook lengths for shape (3, 2, 1):
        #   row 0 (3 cells): 5, 3, 1
        #   row 1 (2 cells): 3, 1
        #   row 2 (1 cell):  1
        hooks = {
            (0, 0): 5, (0, 1): 3, (0, 2): 1,
            (1, 0): 3, (1, 1): 1,
            (2, 0): 1,
        }

        # Step 1: draw empty Young diagram
        empty_diagram = VGroup()
        for i, row_len in enumerate(shape):
            for j in range(row_len):
                sq = Square(side_length=cell * 0.95,
                              color=WHITE, stroke_width=2,
                              fill_opacity=0.1)
                sq.move_to(cell_center(i, j))
                empty_diagram.add(sq)
        self.play(FadeIn(empty_diagram))

        step_tr = ValueTracker(0)

        # Stage labels
        stage_labels = [
            r"Young diagram $\lambda = (3, 2, 1)$",
            r"hook lengths $h_{ij}$",
            r"$f^\lambda = \dfrac{n!}{\prod h_{ij}}$",
            r"$= \dfrac{6!}{5 \cdot 3 \cdot 1 \cdot 3 \cdot 1 \cdot 1} = \dfrac{720}{45} = 16$",
        ]

        def stage_text():
            s = int(round(step_tr.get_value())) % len(stage_labels)
            return MathTex(stage_labels[s],
                             color=YELLOW, font_size=24
                             ).to_edge(DOWN, buff=0.6)

        self.add(always_redraw(stage_text))

        def hook_numbers():
            s = int(round(step_tr.get_value()))
            if s < 1:
                return VGroup()
            grp = VGroup()
            for (i, j), h in hooks.items():
                grp.add(MathTex(rf"{h}", color=BLUE, font_size=30
                                  ).move_to(cell_center(i, j)))
            return grp

        self.add(always_redraw(hook_numbers))

        def hook_shape_example():
            s = int(round(step_tr.get_value()))
            if s < 1:
                return VGroup()
            # Highlight the hook of cell (0, 0): the cell itself +
            # cells to the right in row 0 + cells below in column 0
            cells = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]
            grp = VGroup()
            for (i, j) in cells:
                sq = Square(side_length=cell * 0.95,
                              color=ORANGE, fill_opacity=0.25,
                              stroke_width=2)
                sq.move_to(cell_center(i, j))
                grp.add(sq)
            return grp

        self.add(always_redraw(hook_shape_example))

        for s in range(1, 4):
            self.play(step_tr.animate.set_value(s),
                       run_time=1.0)
            self.wait(1.2)
        self.wait(0.5)
