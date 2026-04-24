from manim import *
import numpy as np


class DragonCurveExample(Scene):
    """
    Heighway dragon curve: built by iterating "fold paper in half"
    rule. After n iterations, path has 2^n segments.

    Use L-system: axiom FX, rules X → X+YF+, Y → -FX-Y.
    F = move forward, +/- = turn 90° right/left.

    SINGLE_FOCUS: ValueTracker level_tr steps 1..12; always_redraw
    generates dragon curve at that depth via turtle graphics.
    """

    def construct(self):
        title = Tex(r"Heighway dragon curve (L-system)",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def generate(n):
            s = "FX"
            for _ in range(n):
                s2 = ""
                for ch in s:
                    if ch == "X":
                        s2 += "X+YF+"
                    elif ch == "Y":
                        s2 += "-FX-Y"
                    else:
                        s2 += ch
                s = s2
            return s

        def turtle_draw(s, step):
            x, y = 0.0, 0.0
            angle = 0.0
            pts = [(x, y)]
            for ch in s:
                if ch == "F":
                    x += step * np.cos(angle)
                    y += step * np.sin(angle)
                    pts.append((x, y))
                elif ch == "+":
                    angle -= PI / 2
                elif ch == "-":
                    angle += PI / 2
            return pts

        level_tr = ValueTracker(1.0)

        def dragon():
            L = int(round(level_tr.get_value()))
            L = max(1, min(12, L))
            s = generate(L)
            step = 6.0 / (2 ** (L / 2 + 1))  # rough scale to fit
            pts = turtle_draw(s, step)
            # Center
            xs_all = [p[0] for p in pts]
            ys_all = [p[1] for p in pts]
            cx = (min(xs_all) + max(xs_all)) / 2
            cy = (min(ys_all) + max(ys_all)) / 2
            pts_np = [np.array([p[0] - cx, p[1] - cy, 0]) for p in pts]
            if len(pts_np) < 2:
                return VMobject()
            # color by position along curve
            lines = VGroup()
            for i in range(len(pts_np) - 1):
                t = i / max(1, len(pts_np) - 1)
                col = interpolate_color(BLUE, RED, t)
                lines.add(Line(pts_np[i], pts_np[i + 1],
                                color=col, stroke_width=1.5))
            return lines

        self.add(always_redraw(dragon))

        # Info
        def L_now():
            return max(1, min(12, int(round(level_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"level $=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"segments $=2^L=$", font_size=22),
                   DecimalNumber(2, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"dim $=2$ (space-filling)",
                color=GREEN, font_size=20),
            Tex(r"rule: $X\to X+YF+$, $Y\to -FX-Y$",
                color=GREY_B, font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(L_now()))
        info[1][1].add_updater(lambda m: m.set_value(2 ** L_now()))
        self.add(info)

        for L in range(2, 13):
            self.play(level_tr.animate.set_value(float(L)),
                      run_time=0.7, rate_func=smooth)
            self.wait(0.2)
        self.wait(0.5)
