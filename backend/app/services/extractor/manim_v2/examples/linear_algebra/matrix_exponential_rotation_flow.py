from manim import *
import numpy as np


class MatrixExponentialRotationFlowExample(Scene):
    """The exponential of a rotation generator moves vectors continuously."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
        tip_length: float = 0.2,
        tip_width: float = 0.2,
    ) -> Line:
        arrow = Line(start, end, color=color, stroke_width=stroke_width)
        length = np.linalg.norm(end - start)
        if length > 0.08:
            arrow.add_tip(
                tip_length=min(tip_length, 0.45 * length),
                tip_width=min(tip_width, 0.45 * length),
            )
        return arrow

    def construct(self):
        time = ValueTracker(0.0)

        title = Tex(r"$e^{tJ}$ is the continuous flow of the linear system $\dot{x}=Jx$", font_size=28)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5.0,
            y_length=5.0,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.27, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.05 + DOWN * 0.2)
        origin = plane.c2p(0, 0)

        orbit = Circle(radius=np.linalg.norm(plane.c2p(1.5, 0) - origin), color=BLUE_B, stroke_width=3)
        orbit.move_to(origin)

        def point_coords() -> np.ndarray:
            t = time.get_value()
            return np.array([1.5 * np.cos(t), 1.5 * np.sin(t)])

        vector = always_redraw(
            lambda: self.fixed_tip_arrow(
                origin,
                plane.c2p(*point_coords()),
                YELLOW,
                stroke_width=8,
            )
        )
        dot = always_redraw(lambda: Dot(plane.c2p(*point_coords()), color=YELLOW, radius=0.08))
        tangent = always_redraw(
            lambda: self.fixed_tip_arrow(
                plane.c2p(*point_coords()),
                plane.c2p(*(point_coords() + 0.45 * np.array([-point_coords()[1], point_coords()[0]]))),
                ORANGE,
                stroke_width=5,
                tip_length=0.18,
                tip_width=0.18,
            )
        )

        t_number = DecimalNumber(time.get_value(), num_decimal_places=2, font_size=28, color=YELLOW)
        t_number.add_updater(lambda m: m.set_value(time.get_value()))
        live_t = VGroup(MathTex(r"t=", font_size=28, color=YELLOW), t_number).arrange(RIGHT, buff=0.08)
        panel = VGroup(
            MathTex(r"J=\begin{bmatrix}0&-1\\1&0\end{bmatrix}", font_size=31),
            MathTex(r"\frac{d}{dt}\vec{x}(t)=J\vec{x}(t)", font_size=31),
            MathTex(r"\vec{x}(t)=e^{tJ}\vec{x}(0)", font_size=31, color=YELLOW),
            live_t,
            Tex("The matrix exponential packages a continuous rotation.", font_size=22, color=BLUE_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.move_to(RIGHT * 3.05 + UP * 0.45)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(plane), Create(orbit))
        self.add(vector, dot, tangent)
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.play(time.animate.set_value(TAU), run_time=4.0, rate_func=linear)
        self.play(Circumscribe(panel[2], color=YELLOW))
        self.wait(0.8)
