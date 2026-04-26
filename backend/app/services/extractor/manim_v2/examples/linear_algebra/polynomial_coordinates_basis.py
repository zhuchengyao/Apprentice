from manim import *


class PolynomialCoordinatesBasisExample(Scene):
    """A polynomial as coordinates in the basis 1, x, x^2, ..."""

    def construct(self):
        title = Tex(r"Polynomials can be vectors too", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        basis = VGroup(
            MathTex(r"1", font_size=30, color=GREEN),
            MathTex(r"x", font_size=30, color=RED),
            MathTex(r"x^2", font_size=30, color=YELLOW),
            MathTex(r"x^3", font_size=30, color=MAROON_B),
            MathTex(r"\cdots", font_size=30, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        basis_title = Tex("basis", font_size=23, color=BLUE_B).next_to(basis, UP, buff=0.18)
        basis_group = VGroup(basis_title, basis).move_to(LEFT * 4.7 + DOWN * 0.15)

        poly = MathTex(r"p(x)=5+3x+x^2", font_size=34)
        poly.set_color_by_tex("5", GREEN)
        poly.set_color_by_tex("3x", RED)
        poly.set_color_by_tex("x^2", YELLOW)
        poly.move_to(LEFT * 1.15 + UP * 0.9)

        coords = Matrix([["5"], ["3"], ["1"], ["0"], [r"\vdots"]], element_alignment_corner=ORIGIN)
        coords.scale(0.78)
        for entry, color in zip(coords.get_entries(), [GREEN, RED, YELLOW, MAROON_B, GREY_B]):
            entry.set_color(color)
        coords.move_to(RIGHT * 2.8 + DOWN * 0.15)
        equals = MathTex(r"\longleftrightarrow", font_size=34).move_to(RIGHT * 0.75 + DOWN * 0.15)

        note = Tex("Coordinates depend on the chosen basis.", font_size=23, color=BLUE_B)
        note.move_to(DOWN * 2.65)
        note_box = SurroundingRectangle(note, color=GREY_B, buff=0.2)
        note_box.set_fill(BLACK, opacity=0.84)

        self.play(FadeIn(basis_group))
        self.play(Write(poly))
        self.play(Write(equals), Write(coords.get_brackets()))

        source_terms = VGroup(poly[0][5].copy(), poly[0][7].copy(), poly[0][9].copy())
        target_entries = VGroup(coords.get_entries()[0], coords.get_entries()[1], coords.get_entries()[2])
        self.play(TransformFromCopy(source_terms, target_entries), run_time=1.8)
        self.play(FadeIn(VGroup(coords.get_entries()[3], coords.get_entries()[4])))
        self.play(FadeIn(VGroup(note_box, note)))
        self.wait(0.8)
