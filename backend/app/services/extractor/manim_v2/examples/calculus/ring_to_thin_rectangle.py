from manim import *
import numpy as np


class RingToThinRectangleExample(Scene):
    """
    Unroll a thin ring (radius R, thickness dr) from a disk into a
    rectangle of width 2πR and height dr, area 2πR·dr.

    SINGLE_FOCUS: ValueTracker s_tr morphs the YELLOW ring from its
    circular shape to a flat strip, keeping area constant.
    """

    def construct(self):
        title = Tex(r"Unroll ring $(R, dr) \to$ rectangle $(2\pi R) \times dr$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 1.8
        dr = 0.25

        disk_center = LEFT * 3.5 + DOWN * 0.3
        strip_y = DOWN * 0.5  # final strip placement

        disk = Circle(radius=R, color=BLUE, stroke_width=2,
                       fill_color=BLUE, fill_opacity=0.3).move_to(disk_center)
        self.add(disk)

        s_tr = ValueTracker(0.0)

        def ring_or_strip():
            s = s_tr.get_value()
            n_pts = 100
            # Outer boundary: at s=0 it's an arc around disk_center of radius R+dr;
            # at s=1 it's the top edge of a rectangle.
            pts_top = []
            pts_bot = []
            for t in np.linspace(0, 1, n_pts):
                # circle coord
                theta = 2 * PI * t - PI
                outer_circle_pt = disk_center + (R + dr) * np.array([np.cos(theta), np.sin(theta), 0])
                inner_circle_pt = disk_center + R * np.array([np.cos(theta), np.sin(theta), 0])
                # strip coord: x goes from -π R to π R along horizontal line at given y
                strip_x = PI * R * (2 * t - 1)
                strip_top = np.array([strip_x, strip_y[1] + dr, 0])
                strip_bot = np.array([strip_x, strip_y[1], 0])
                pts_top.append((1 - s) * outer_circle_pt + s * strip_top)
                pts_bot.append((1 - s) * inner_circle_pt + s * strip_bot)
            return Polygon(*pts_top, *reversed(pts_bot),
                            color=YELLOW, stroke_width=2,
                            fill_color=YELLOW, fill_opacity=0.75)

        self.add(always_redraw(ring_or_strip))

        # Labels
        self.add(Tex(r"$R$", color=RED, font_size=22).move_to(disk_center + UP * 0.3))
        self.add(Tex(r"ring of width $dr$", color=YELLOW, font_size=20).move_to(
            disk_center + UP * 2.3))

        # After unroll, dimensions
        strip_center = np.array([0, strip_y[1] + dr / 2, 0])

        def dim_labels():
            s = s_tr.get_value()
            if s < 0.8: return VGroup()
            alpha = (s - 0.8) * 5
            alpha = min(1.0, alpha)
            return VGroup(
                Tex(r"$2\pi R$", color=GREEN, font_size=24,
                     fill_opacity=alpha).move_to(
                    np.array([0, strip_y[1] - 0.4, 0])),
                Tex(r"$dr$", color=YELLOW, font_size=20,
                     fill_opacity=alpha).move_to(
                    np.array([PI * R + 0.3, strip_y[1] + dr / 2, 0])),
            )
        self.add(always_redraw(dim_labels))

        self.play(s_tr.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.5)

        # Area stamp
        stamp = Tex(r"area $= 2\pi R \cdot dr$",
                     color=GREEN, font_size=28).to_edge(DOWN, buff=0.5)
        self.play(Write(stamp))
        self.wait(1.0)
