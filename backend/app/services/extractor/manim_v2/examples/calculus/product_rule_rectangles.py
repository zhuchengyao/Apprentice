from manim import *
import numpy as np


class ProductRuleRectanglesExample(Scene):
    """
    Product rule from a growing rectangle.

    A ValueTracker t drives f(t) and g(t). The main blue rectangle
    grows smoothly, and at a chosen moment three strips appear: the
    green g·df strip on the right, yellow f·dg strip on top, and
    red df·dg corner. Watch the corner become vanishingly small
    compared to the two strips, motivating d(fg) ≈ g·df + f·dg.
    """

    def construct(self):
        title = Tex(r"Product rule: $d(fg) = g\,df + f\,dg$", font_size=34).to_edge(UP)
        self.play(Write(title))

        # The rectangle lives in the LEFT half of the frame.
        # All commentary/formula text is anchored to the RIGHT half to avoid overlap.
        right_anchor_x = 2.2

        t = ValueTracker(1.0)

        def f_of(tv): return 0.8 + 0.6 * tv
        def g_of(tv): return 0.5 + 0.5 * tv

        origin = np.array([-5.4, -2.2, 0])

        def main_rect():
            fv = f_of(t.get_value())
            gv = g_of(t.get_value())
            rect = Rectangle(width=fv, height=gv, color=BLUE,
                             fill_opacity=0.6, stroke_width=1)
            rect.move_to(origin + np.array([fv / 2, gv / 2, 0]))
            return rect

        def f_label():
            fv = f_of(t.get_value())
            return MathTex("f", color=BLUE, font_size=26).move_to(
                origin + np.array([fv / 2, -0.3, 0])
            )

        def g_label():
            gv = g_of(t.get_value())
            return MathTex("g", color=BLUE, font_size=26).move_to(
                origin + np.array([-0.3, gv / 2, 0])
            )

        # Right-side info panel shows the current f and g numerically
        def info_panel():
            fv = f_of(t.get_value())
            gv = g_of(t.get_value())
            return VGroup(
                MathTex(rf"f = {fv:.2f}", color=BLUE, font_size=26),
                MathTex(rf"g = {gv:.2f}", color=BLUE, font_size=26),
                MathTex(rf"f g = {fv * gv:.3f}", color=YELLOW, font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(
                [right_anchor_x, 1.0, 0]
            )

        self.add(always_redraw(main_rect),
                 always_redraw(f_label),
                 always_redraw(g_label),
                 always_redraw(info_panel))

        # Phase 1: grow the rectangle continuously so viewer sees fg climbing
        self.play(t.animate.set_value(2.5), run_time=3, rate_func=smooth)
        self.wait(0.4)

        # Phase 2: freeze state and break the next growth into strips.
        # Remove updaters so strips don't get wiped on every frame.
        f_now = f_of(t.get_value())
        g_now = g_of(t.get_value())
        self.clear()
        self.add(title)

        base_rect = Rectangle(width=f_now, height=g_now, color=BLUE,
                              fill_opacity=0.6, stroke_width=1)
        base_rect.move_to(origin + np.array([f_now / 2, g_now / 2, 0]))

        f_static = MathTex("f", color=BLUE, font_size=26).move_to(
            origin + np.array([f_now / 2, -0.3, 0]))
        g_static = MathTex("g", color=BLUE, font_size=26).move_to(
            origin + np.array([-0.3, g_now / 2, 0]))

        self.add(base_rect, f_static, g_static)

        df_val = 0.55
        dg_val = 0.4

        right_strip = Rectangle(width=df_val, height=g_now, color=GREEN,
                                fill_opacity=0.7, stroke_width=1)
        right_strip.move_to(origin + np.array([f_now + df_val / 2, g_now / 2, 0]))

        top_strip = Rectangle(width=f_now, height=dg_val, color=YELLOW,
                              fill_opacity=0.7, stroke_width=1)
        top_strip.move_to(origin + np.array([f_now / 2, g_now + dg_val / 2, 0]))

        corner = Rectangle(width=df_val, height=dg_val, color=RED,
                           fill_opacity=0.9, stroke_width=1)
        corner.move_to(origin + np.array([f_now + df_val / 2,
                                          g_now + dg_val / 2, 0]))

        df_brace = Brace(right_strip, DOWN, color=GREEN)
        df_lbl = MathTex("df", color=GREEN, font_size=22).next_to(df_brace, DOWN, buff=0.05)
        dg_brace = Brace(top_strip, LEFT, color=YELLOW)
        dg_lbl = MathTex("dg", color=YELLOW, font_size=22).next_to(dg_brace, LEFT, buff=0.05)

        # Strip area labels inside each strip
        right_area = MathTex(r"g\,df", color=GREEN, font_size=22).move_to(right_strip.get_center())
        top_area = MathTex(r"f\,dg", color=YELLOW, font_size=22).move_to(top_strip.get_center())
        corner_area = MathTex(r"df\,dg", color=RED, font_size=14).move_to(corner.get_center())

        # Right-side legend stacked vertically — NO overlap with rectangle area
        legend = VGroup(
            MathTex(r"g\,df", color=GREEN, font_size=28),
            MathTex(r"f\,dg", color=YELLOW, font_size=28),
            MathTex(r"df\,dg", color=RED, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(
            [right_anchor_x, 0.8, 0]
        )

        self.play(FadeIn(right_strip), Create(df_brace), Write(df_lbl),
                  Write(legend[0]))
        self.play(FadeIn(top_strip), Create(dg_brace), Write(dg_lbl),
                  Write(legend[1]))
        self.play(FadeIn(corner), Write(legend[2]))
        self.play(Write(right_area), Write(top_area), Write(corner_area))
        self.wait(0.4)

        # Phase 3: shrink df, dg by 5× — corner vanishes faster than the strips.
        shrink = 0.2
        small_right = Rectangle(width=df_val * shrink, height=g_now,
                                color=GREEN, fill_opacity=0.7, stroke_width=1)
        small_right.move_to(origin + np.array([f_now + df_val * shrink / 2,
                                               g_now / 2, 0]))
        small_top = Rectangle(width=f_now, height=dg_val * shrink,
                              color=YELLOW, fill_opacity=0.7, stroke_width=1)
        small_top.move_to(origin + np.array([f_now / 2,
                                             g_now + dg_val * shrink / 2, 0]))
        small_corner = Rectangle(width=df_val * shrink, height=dg_val * shrink,
                                 color=RED, fill_opacity=0.9, stroke_width=1)
        small_corner.move_to(origin + np.array([f_now + df_val * shrink / 2,
                                                g_now + dg_val * shrink / 2, 0]))

        self.play(
            Transform(right_strip, small_right),
            Transform(top_strip, small_top),
            Transform(corner, small_corner),
            FadeOut(right_area), FadeOut(top_area), FadeOut(corner_area),
            FadeOut(df_brace), FadeOut(df_lbl),
            FadeOut(dg_brace), FadeOut(dg_lbl),
            run_time=2.5,
        )

        # Highlight second-order corner in the legend area
        corner_note = Tex(r"$df\,dg \to 0$ faster (second order)",
                          font_size=26, color=RED).move_to(
            [right_anchor_x, -0.8, 0]
        )
        self.play(Write(corner_note))
        self.wait(0.4)

        # Final formula sits BELOW the legend, with clear vertical gap.
        # Use two lines to keep each line narrow.
        formula_line1 = MathTex(
            r"d(fg) = g\,df + f\,dg + df\,dg",
            font_size=26, color=YELLOW,
        ).move_to([right_anchor_x, -1.8, 0])
        formula_line2 = MathTex(
            r"\frac{d(fg)}{dt} = g\,f'(t) + f\,g'(t)",
            font_size=28, color=YELLOW,
        ).next_to(formula_line1, DOWN, buff=0.3)

        self.play(Write(formula_line1))
        self.play(Write(formula_line2))
        self.wait(1.2)
