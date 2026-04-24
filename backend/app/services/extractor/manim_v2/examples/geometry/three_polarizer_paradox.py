from manim import *
import numpy as np


class ThreePolarizerParadox(Scene):
    """Two crossed polarizers (vertical then horizontal) transmit 0% of
    unpolarized light.  But slipping a 45° polarizer BETWEEN them lets 1/8
    of the original intensity through — more light from MORE filters!
    Quantitative derivation via Malus I = I_0 * cos^2(theta) twice:
    1/2 (unpolarized -> V)  * cos^2(45 deg) * cos^2(45 deg) = 1/8."""

    def construct(self):
        title = Tex(
            r"Three polarizers paradox",
            font_size=32,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def make_polarizer(x, angle_deg, color):
            box = Circle(radius=0.6, color=color, stroke_width=3,
                         fill_opacity=0.12)
            axis = Line(
                box.get_center() + rotate_vector(RIGHT * 0.55,
                                                 angle_deg * DEGREES),
                box.get_center() + rotate_vector(LEFT * 0.55,
                                                 angle_deg * DEGREES),
                color=color, stroke_width=5,
            )
            lab = MathTex(f"{angle_deg}^\\circ", font_size=22,
                          color=color).next_to(box, DOWN, buff=0.12)
            grp = VGroup(box, axis, lab).shift(RIGHT * x)
            return grp

        def draw_case(title_text, pol_specs, intensity_labels,
                      final_fraction_tex, final_color):
            caption = Tex(title_text, font_size=26, color=YELLOW).move_to(
                UP * 1.8
            )
            self.play(FadeIn(caption))

            pols = VGroup(*[
                make_polarizer(x, ang, col)
                for (x, ang, col) in pol_specs
            ])
            pols.shift(DOWN * 0.3)

            beam_y = pols[0][0].get_center()[1]
            start_x = -6
            end_x = 6

            xs = [p[0].get_center()[0] for p in pols]
            segment_xs = [start_x] + xs + [end_x]
            seg_lines = VGroup()
            prev_color = WHITE
            for i in range(len(segment_xs) - 1):
                a = segment_xs[i] + (0.6 if i > 0 else 0)
                b = segment_xs[i + 1] - (0.6 if i < len(segment_xs) - 2 else 0)
                color_ = intensity_labels[i][1]
                line = Line(
                    [a, beam_y, 0], [b, beam_y, 0],
                    color=color_, stroke_width=2 + 6 * intensity_labels[i][2],
                )
                seg_lines.add(line)

            intens_labs = VGroup()
            for i, (txt, col, _) in enumerate(intensity_labels):
                mid_x = (segment_xs[i] + segment_xs[i + 1]) / 2
                t = MathTex(txt, font_size=22, color=col).move_to(
                    [mid_x, beam_y + 0.7, 0]
                )
                intens_labs.add(t)

            self.play(LaggedStart(*[FadeIn(p) for p in pols],
                                  lag_ratio=0.2))
            self.play(Create(seg_lines, run_time=2))
            self.play(LaggedStart(*[Write(t) for t in intens_labs],
                                  lag_ratio=0.15))

            final_box = MathTex(
                final_fraction_tex, font_size=32, color=final_color,
            )
            final_box.to_edge(DOWN, buff=0.35)
            final_rect = SurroundingRectangle(final_box, color=final_color,
                                              buff=0.15, stroke_width=3)
            self.play(Write(final_box), Create(final_rect))
            self.wait(1.0)

            group = VGroup(caption, pols, seg_lines, intens_labs,
                           final_box, final_rect)
            self.play(FadeOut(group))

        draw_case(
            "Case 1: V filter then H filter",
            [(-2.0, 90, BLUE), (2.0, 0, GREEN)],
            [
                (r"I_0", WHITE, 1.0),
                (r"\tfrac{1}{2}\,I_0", BLUE, 0.5),
                (r"0", RED, 0.0),
            ],
            r"I_{\text{final}} = \tfrac{1}{2}\,I_0 \cdot \cos^2 90^\circ = 0",
            RED,
        )

        draw_case(
            r"Case 2: V, then $45^\circ$, then H",
            [(-3.0, 90, BLUE), (0.0, 45, PURPLE), (3.0, 0, GREEN)],
            [
                (r"I_0", WHITE, 1.0),
                (r"\tfrac{1}{2}\,I_0", BLUE, 0.5),
                (r"\tfrac{1}{4}\,I_0", PURPLE, 0.25),
                (r"\tfrac{1}{8}\,I_0", YELLOW, 0.125),
            ],
            r"I_{\text{final}} = \tfrac{1}{2}I_0 \cdot \cos^2 45^\circ \cdot \cos^2 45^\circ = \tfrac{1}{8}\,I_0",
            YELLOW,
        )

        note = Tex(
            r"Adding a filter INCREASES transmission — quantum measurement at work.",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note))
        self.wait(1.5)
