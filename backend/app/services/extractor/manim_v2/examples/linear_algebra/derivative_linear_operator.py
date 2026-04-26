from manim import *


class DerivativeLinearOperatorExample(Scene):
    """The derivative operator preserves sums: D(f+g)=Df+Dg."""

    def graph_label(
        self,
        axes: Axes,
        x: float,
        y: float,
        tex: str,
        color: ManimColor,
        direction: np.ndarray = UP,
    ) -> MathTex:
        label = MathTex(tex, color=color, font_size=25)
        label.set_stroke(BLACK, width=5, background=True)
        label.next_to(axes.c2p(x, y), direction, buff=0.06)
        return label

    def construct(self):
        title = Tex(r"The derivative is a linear operator", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-3, 7, 1],
            x_length=5.8,
            y_length=4.8,
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.1 + DOWN * 0.25)

        def f(x: float) -> float:
            return 0.45 * x**3 - 0.8 * x

        def g(x: float) -> float:
            return 0.55 * x**2 - 0.8

        def fp(x: float) -> float:
            return 1.35 * x**2 - 0.8

        def gp(x: float) -> float:
            return 1.1 * x

        def sum_fg(x: float) -> float:
            return f(x) + g(x)

        def sum_deriv(x: float) -> float:
            return fp(x) + gp(x)

        f_graph = axes.plot(f, x_range=[-2, 2], color=YELLOW)
        g_graph = axes.plot(g, x_range=[-2, 2], color=MAROON_B)
        sum_graph = axes.plot(sum_fg, x_range=[-2, 2], color=PINK)
        route_one_result = axes.plot(sum_deriv, x_range=[-2, 2], color=GREY_A, stroke_width=6)
        route_one_result.set_fill(opacity=0)
        route_one_result.set_stroke(GREY_A, width=6, opacity=0.32)
        route_two_f = axes.plot(f, x_range=[-2, 2], color=YELLOW, stroke_width=4)
        route_two_g = axes.plot(g, x_range=[-2, 2], color=MAROON_B, stroke_width=4)
        fp_graph = axes.plot(fp, x_range=[-2, 2], color=YELLOW, stroke_width=4)
        gp_graph = axes.plot(gp, x_range=[-2, 2], color=MAROON_B, stroke_width=4)
        route_two_result = axes.plot(sum_deriv, x_range=[-2, 2], color=GREEN_B, stroke_width=4)

        f_label = self.graph_label(axes, -1.55, f(-1.55), "f", YELLOW, DOWN)
        g_label = self.graph_label(axes, 1.25, g(1.25), "g", MAROON_B, DOWN)
        sum_label = self.graph_label(axes, 0.95, sum_fg(0.95), "f+g", PINK, UP)
        route_one_label = self.graph_label(axes, 1.18, sum_deriv(1.18), "D(f+g)", GREY_A, UP)
        route_two_f_label = self.graph_label(axes, -1.55, f(-1.55), "f", YELLOW, DOWN)
        route_two_g_label = self.graph_label(axes, 1.25, g(1.25), "g", MAROON_B, DOWN)
        fp_label = self.graph_label(axes, -1.25, fp(-1.25), "Df", YELLOW, UP)
        gp_label = self.graph_label(axes, -1.55, gp(-1.55), "Dg", MAROON_B, DOWN)
        final_label = self.graph_label(axes, 1.2, sum_deriv(1.2), "Df+Dg", GREEN_B, DOWN)

        route_one = MathTex(
            r"1.\quad f+g\xrightarrow{D}D(f+g)",
            font_size=26,
            color=PINK,
        )
        route_two = MathTex(
            r"2.\quad f\xrightarrow{D}Df,\quad g\xrightarrow{D}Dg",
            font_size=26,
            color=BLUE_B,
        )
        formula = MathTex(r"D(f+g)=Df+Dg", font_size=31)
        formula.set_color_by_tex("f", YELLOW)
        formula.set_color_by_tex("g", MAROON_B)
        note = Tex("Add first or differentiate first: the final curve matches.", font_size=22, color=GREY_A)
        panel = VGroup(route_one, route_two, formula, note).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.move_to(RIGHT * 3.08 + UP * 0.78)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(axes))
        self.play(FadeIn(panel_box), FadeIn(route_one))

        self.play(Create(f_graph), FadeIn(f_label), Create(g_graph), FadeIn(g_label))
        self.play(Create(sum_graph), FadeIn(sum_label), run_time=1.5)
        self.play(
            Transform(sum_graph, route_one_result),
            Transform(sum_label, route_one_label),
            FadeOut(f_graph),
            FadeOut(g_graph),
            FadeOut(f_label),
            FadeOut(g_label),
            run_time=1.7,
        )
        self.play(sum_graph.animate.set_fill(opacity=0).set_stroke(opacity=0.25), FadeOut(sum_label))

        self.play(FadeIn(route_two))
        self.play(Create(route_two_f), FadeIn(route_two_f_label), Create(route_two_g), FadeIn(route_two_g_label), run_time=1.4)
        self.play(
            Transform(route_two_f, fp_graph),
            Transform(route_two_f_label, fp_label),
            Transform(route_two_g, gp_graph),
            Transform(route_two_g_label, gp_label),
            run_time=1.6,
        )

        final_sweep = route_two_result.copy()
        final_sweep.pointwise_become_partial(route_two_result, 0, 0)
        final_label.set_opacity(0)
        self.add(final_sweep, final_label)

        def reveal_sum(mob: VMobject, alpha: float) -> None:
            mob.pointwise_become_partial(route_two_result, 0, alpha)

        def erase_df(mob: VMobject, alpha: float) -> None:
            mob.pointwise_become_partial(fp_graph, alpha, 1)

        def erase_dg(mob: VMobject, alpha: float) -> None:
            mob.pointwise_become_partial(gp_graph, alpha, 1)

        def reveal_final_label(mob: Mobject, alpha: float) -> None:
            mob.set_opacity(max(0, min(1, (alpha - 0.72) / 0.28)))

        self.play(
            UpdateFromAlphaFunc(final_sweep, reveal_sum),
            UpdateFromAlphaFunc(route_two_f, erase_df),
            UpdateFromAlphaFunc(route_two_g, erase_dg),
            FadeOut(route_two_f_label),
            FadeOut(route_two_g_label),
            UpdateFromAlphaFunc(final_label, reveal_final_label),
            run_time=1.8,
            rate_func=linear,
        )
        self.remove(route_two_f, route_two_g)
        route_two_result = final_sweep
        self.play(Write(formula), Write(note))
        self.play(Circumscribe(VGroup(sum_graph, route_two_result), color=YELLOW))
        self.wait(0.8)
