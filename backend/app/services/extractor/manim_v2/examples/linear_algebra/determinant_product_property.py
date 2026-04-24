from manim import *
import numpy as np


class DeterminantProductPropertyExample(Scene):
    """
    det(M_1 M_2) = det(M_1) · det(M_2). Intuition: applying M_2 first
    scales areas by det(M_2); then M_1 further scales by det(M_1);
    net scaling is the product.

    SINGLE_FOCUS: unit square scales by det(M_2) after M_2, then by
    det(M_1) after M_1. Live area label multiplies accordingly.
    """

    def construct(self):
        title = Tex(r"$\det(M_1 M_2)=\det(M_1)\det(M_2)$ via successive area scaling",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        M2 = np.array([[2.0, 0.5], [0.5, 1.5]])
        M1 = np.array([[1.0, -1.0], [1.0, 2.0]])
        det_M1 = float(np.linalg.det(M1))
        det_M2 = float(np.linalg.det(M2))
        det_prod = float(np.linalg.det(M1 @ M2))

        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return (1 - s) * np.eye(2) + s * M2
            alpha = s - 1
            return (1 - alpha) * M2 + alpha * (M1 @ M2)

        def square():
            M = M_of()
            pts = [plane.c2p(*(M @ p)) for p in
                    [np.zeros(2), np.array([1, 0]),
                     np.array([1, 1]), np.array([0, 1])]]
            d = float(np.linalg.det(M))
            col = GREEN if d > 0.05 else (RED if d < -0.05 else GREY_D)
            return Polygon(*pts, color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.4)

        self.add(always_redraw(square))

        # Dynamic area label
        def area_lbl():
            M = M_of()
            d = abs(float(np.linalg.det(M)))
            center = M @ np.array([0.5, 0.5])
            s = stage_tr.get_value()
            if s < 0.05:
                txt = r"$1$"
            elif s < 1.05:
                txt = rf"${d:.2f}$"
            else:
                txt = rf"${d:.2f}$"
            return Tex(txt, color=YELLOW, font_size=22).move_to(plane.c2p(*center))

        self.add(always_redraw(area_lbl))

        # Stage caption
        def stage_str():
            s = stage_tr.get_value()
            if s < 0.05: return r"unit square, area $1$"
            if s < 1.05: return rf"after $M_2$: area $\to \det(M_2)={det_M2:.2f}$"
            return rf"after $M_1 M_2$: area $\to \det(M_1)\det(M_2)={det_prod:.2f}$"

        stage_tex = Tex(stage_str(), color=YELLOW, font_size=24).to_edge(DOWN, buff=0.3)
        self.add(stage_tex)
        def update_stage(mob, dt):
            new = Tex(stage_str(), color=YELLOW, font_size=24).move_to(stage_tex)
            stage_tex.become(new)
            return stage_tex
        stage_tex.add_updater(update_stage)

        info = VGroup(
            Tex(rf"$\det(M_2)={det_M2:.3f}$", color=BLUE, font_size=22),
            Tex(rf"$\det(M_1)={det_M1:.3f}$", color=ORANGE, font_size=22),
            Tex(rf"product $={det_M1 * det_M2:.3f}$",
                color=YELLOW, font_size=22),
            Tex(rf"$\det(M_1 M_2)={det_prod:.3f}$",
                color=GREEN, font_size=22),
            Tex(r"$\Rightarrow$ equal",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.add(info)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(1.0)
