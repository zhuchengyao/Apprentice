from manim import *
import numpy as np


class CayleyHamiltonExample(Scene):
    """
    Cayley-Hamilton: every square matrix satisfies its characteristic
    polynomial. For A = [[a, b], [c, d]], p(λ) = λ² - tr(A)λ + det(A),
    so A² - tr(A)A + det(A)I = 0.

    SINGLE_FOCUS:
      Specific A = [[2, 1], [1, 3]]; compute A², tr(A)A, det(A)I;
      sum should equal 0 matrix. ValueTracker step_tr reveals each
      term, final sum highlighted.
    """

    def construct(self):
        title = Tex(r"Cayley-Hamilton: $A$ satisfies its char.\ poly.",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([[2, 1], [1, 3]], dtype=float)
        A_sq = A @ A
        tr_A = float(np.trace(A))
        det_A = float(np.linalg.det(A))
        trA_A = tr_A * A
        detA_I = det_A * np.eye(2)
        total = A_sq - trA_A + detA_I

        cell = 0.7

        def matrix_grid(M, origin, color, label):
            grp = VGroup()
            lbl = MathTex(label, color=color, font_size=22
                            ).move_to(origin + np.array([0, cell * 1.5, 0]))
            grp.add(lbl)
            for r in range(2):
                for c in range(2):
                    sq = Square(side_length=cell * 0.9, color=color,
                                  fill_opacity=0.35, stroke_width=1.5)
                    sq.move_to(origin + np.array([c * cell - cell * 0.5,
                                                       -r * cell + cell * 0.5, 0]))
                    grp.add(sq)
                    v = M[r, c]
                    grp.add(MathTex(rf"{v:+.1f}" if v != 0 else "0",
                                      color=WHITE, font_size=18
                                      ).move_to(sq.get_center()))
            return grp

        step_tr = ValueTracker(0)

        def scene_content():
            s = int(round(step_tr.get_value()))
            grp = VGroup()
            origins = [
                np.array([-5, 1.5, 0]),
                np.array([-2.5, 1.5, 0]),
                np.array([0.5, 1.5, 0]),
                np.array([3.5, 1.5, 0]),
            ]
            items = [
                (A, BLUE, r"A"),
                (A_sq, ORANGE, r"A^2"),
                (-trA_A, RED, r"-\text{tr}(A) A"),
                (detA_I, GREEN, r"\det(A) I"),
            ]
            for i in range(s):
                grp.add(matrix_grid(items[i][0], origins[i],
                                       items[i][1], items[i][2]))
            # Plus signs
            if s >= 2:
                grp.add(MathTex(r"=", color=WHITE, font_size=26
                                  ).move_to((origins[0] + origins[1]) / 2 + np.array([0, -0.3, 0])))
            if s >= 3:
                grp.add(MathTex(r"+", color=WHITE, font_size=26
                                  ).move_to((origins[1] + origins[2]) / 2 + np.array([0, -0.3, 0])))
            if s >= 4:
                grp.add(MathTex(r"+", color=WHITE, font_size=26
                                  ).move_to((origins[2] + origins[3]) / 2 + np.array([0, -0.3, 0])))
            if s >= 5:
                # Final sum = 0 matrix, shown below
                grp.add(matrix_grid(A_sq - trA_A + detA_I,
                                       np.array([0, -2, 0]), YELLOW,
                                       r"A^2 - \text{tr}(A) A + \det(A) I"))
            return grp

        self.add(always_redraw(scene_content))

        def info():
            s = int(round(step_tr.get_value()))
            return VGroup(
                MathTex(rf"\text{{step}} = {s}/5",
                         color=WHITE, font_size=22),
                MathTex(rf"\text{{tr}}(A) = {tr_A}",
                         color=RED, font_size=20),
                MathTex(rf"\det(A) = {det_A:.0f}",
                         color=GREEN, font_size=20),
                MathTex(r"p(\lambda) = \lambda^2 - 5\lambda + 5",
                         color=WHITE, font_size=18),
                MathTex(r"p(A) = 0\ \checkmark",
                         color=YELLOW if s >= 5 else GREY_B, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for s in range(1, 6):
            self.play(step_tr.animate.set_value(s),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.8)
        self.wait(0.5)
