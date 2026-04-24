from manim import *


class GaussRowReductionExample(Scene):
    def construct(self):
        title = Text("Gaussian elimination: row-reduce to echelon form", font_size=26).to_edge(UP)
        self.play(Write(title))

        def mat(entries, highlight=None):
            m = Matrix(entries, h_buff=1.2)
            if highlight is not None:
                for (r, c) in highlight:
                    m.get_entries()[r * len(entries[0]) + c].set_color(YELLOW)
            return m

        m0 = mat([["2", "1", "-1", " 8"],
                  ["-3", "-1", "2", "-11"],
                  ["-2", "1", "2", "-3"]])
        self.play(Write(m0))

        step1 = MathTex(r"R_2 \leftarrow R_2 + \tfrac{3}{2}R_1,\;\; R_3 \leftarrow R_3 + R_1",
                        font_size=28, color=BLUE).next_to(m0, DOWN, buff=0.3)
        self.play(Write(step1))

        m1 = mat([["2", "1", "-1", "8"],
                  ["0", "0.5", "0.5", "1"],
                  ["0", "2", "1", "5"]], highlight=[(1, 0), (2, 0)])
        self.play(Transform(m0, m1), FadeOut(step1))

        step2 = MathTex(r"R_3 \leftarrow R_3 - 4R_2",
                        font_size=28, color=BLUE).next_to(m0, DOWN, buff=0.3)
        self.play(Write(step2))

        m2 = mat([["2", "1", "-1", "8"],
                  ["0", "0.5", "0.5", "1"],
                  ["0", "0", "-1", "1"]], highlight=[(2, 1)])
        self.play(Transform(m0, m2), FadeOut(step2))

        caption = MathTex(r"\Rightarrow z = -1,\; y = 3,\; x = 2",
                          font_size=30, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
