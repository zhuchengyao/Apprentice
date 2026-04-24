from manim import *
import numpy as np


class RecursiveZeroFindingByWinding(Scene):
    """2D zero-finding algorithm from 3Blue1Brown's winding-number video.
    Start with a large rectangle, compute its boundary winding number —
    that equals the number of zeros of p(z) inside.  Subdivide into 4
    quadrants, compute winding for each; recurse on the subrectangles
    with nonzero winding.  Show p(z) = (z-1)(z+0.5i) with 2 zeros."""

    def construct(self):
        title = Tex(
            r"Recursive zero-finding by subdivision + winding counts",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=6.5, y_length=6.5,
            background_line_style={"stroke_opacity": 0.25},
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        self.play(Create(plane))

        root1 = 1.0 + 0.0j
        root2 = 0.0 - 0.5j

        def p(z):
            return (z - root1) * (z - root2)

        dot1 = Dot(plane.c2p(root1.real, root1.imag),
                   radius=0.12, color=RED).set_z_index(6)
        dot2 = Dot(plane.c2p(root2.real, root2.imag),
                   radius=0.12, color=RED).set_z_index(6)

        def winding_number(rect):
            xmin, xmax, ymin, ymax = rect
            N = 60
            pts = []
            for i in range(N):
                pts.append(xmin + (xmax - xmin) * i / N + 1j * ymin)
            for i in range(N):
                pts.append(xmax + 1j * (ymin + (ymax - ymin) * i / N))
            for i in range(N):
                pts.append(
                    xmin + (xmax - xmin) * (1 - i / N) + 1j * ymax
                )
            for i in range(N):
                pts.append(
                    xmin + 1j * (ymin + (ymax - ymin) * (1 - i / N))
                )
            vals = [p(z) for z in pts]
            total = 0.0
            for k in range(len(vals)):
                a = vals[k]
                b = vals[(k + 1) % len(vals)]
                da = np.angle(b) - np.angle(a)
                while da > np.pi:
                    da -= 2 * np.pi
                while da < -np.pi:
                    da += 2 * np.pi
                total += da
            return int(round(total / (2 * np.pi)))

        def draw_rect(rect, color, stroke_w=3, fill=0.0):
            xmin, xmax, ymin, ymax = rect
            return Polygon(
                plane.c2p(xmin, ymin),
                plane.c2p(xmax, ymin),
                plane.c2p(xmax, ymax),
                plane.c2p(xmin, ymax),
                color=color, stroke_width=stroke_w,
                fill_opacity=fill, fill_color=color,
            )

        def subdivide(rect):
            xmin, xmax, ymin, ymax = rect
            xm = (xmin + xmax) / 2
            ym = (ymin + ymax) / 2
            return [
                (xmin, xm, ymin, ym),
                (xm, xmax, ymin, ym),
                (xm, xmax, ym, ymax),
                (xmin, xm, ym, ymax),
            ]

        initial = (-2.0, 2.0, -2.0, 2.0)
        log_lines = []
        log_group = VGroup()
        log_y_start = 2.2

        def log(text, color):
            line = Tex(text, font_size=22, color=color)
            line.move_to([3.6, log_y_start - len(log_lines) * 0.4, 0])
            log_lines.append(line)
            log_group.add(line)
            return line

        big_rect = draw_rect(initial, YELLOW, stroke_w=4)
        w0 = winding_number(initial)
        self.play(Create(big_rect))
        self.play(FadeIn(dot1), FadeIn(dot2))
        entry0 = log(rf"big box: winding = {w0}", YELLOW)
        self.play(FadeIn(entry0))
        self.wait(0.3)

        subs = subdivide(initial)
        sub_mobs = []
        for s in subs:
            w = winding_number(s)
            if w == 0:
                rect = draw_rect(s, GREY_B, stroke_w=2, fill=0.05)
            else:
                rect = draw_rect(s, GREEN, stroke_w=3, fill=0.15)
            sub_mobs.append((rect, w))
        self.play(FadeOut(big_rect))
        self.play(LaggedStart(*[Create(r) for r, _ in sub_mobs],
                              lag_ratio=0.2))

        for r, w in sub_mobs:
            color = GREEN if w != 0 else GREY_B
            cen = r.get_center()
            t = MathTex(rf"w={w}", font_size=24, color=color).move_to(cen)
            self.play(FadeIn(t), run_time=0.3)

        entry1 = log(r"subdivide: two boxes have $w=1$", GREEN)
        self.play(FadeIn(entry1))

        refined_subs = []
        for s, (_, w) in zip(subs, sub_mobs):
            if w != 0:
                for ss in subdivide(s):
                    ws = winding_number(ss)
                    col = GREEN if ws != 0 else GREY_C
                    refined_subs.append((ss, ws,
                                         draw_rect(ss, col, stroke_w=2,
                                                   fill=0.1 if ws else 0.03)))

        self.play(LaggedStart(*[Create(r) for _, _, r in refined_subs],
                              lag_ratio=0.15))

        entry2 = log(r"recurse: isolate tight boxes around zeros",
                     BLUE)
        self.play(FadeIn(entry2))

        entry3 = log(r"zeros found: $z_1=1$, $z_2=-\tfrac{i}{2}$",
                     YELLOW)
        self.play(FadeIn(entry3))
        self.wait(1.3)
