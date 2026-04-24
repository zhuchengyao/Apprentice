from manim import *
import numpy as np


class LSystemPlantExample(Scene):
    """
    L-system plant: axiom X; rules X → F+[[X]-X]-F[-FX]+X, F → FF
    applied iteratively produces increasingly detailed branching
    plants.

    ValueTracker depth_tr steps 1..5; always_redraw generates the
    plant by interpreting the expanded string with turtle graphics.
    """

    def construct(self):
        title = Tex(r"L-system plant: $X\to F+[[X]-X]-F[-FX]+X$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def expand(axiom, rules, depth):
            s = axiom
            for _ in range(depth):
                s2 = ""
                for ch in s:
                    s2 += rules.get(ch, ch)
                s = s2
            return s

        rules = {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}

        def draw_lsystem(depth):
            s = expand("X", rules, depth)
            lines = []
            x, y = 0.0, -3.0
            angle = PI / 2  # pointing up
            step = 3.2 / (2 ** depth)
            da = 25 * DEGREES
            stack = []
            for ch in s:
                if ch == "F":
                    nx = x + step * np.cos(angle)
                    ny = y + step * np.sin(angle)
                    lines.append(((x, y), (nx, ny)))
                    x, y = nx, ny
                elif ch == "+":
                    angle += da
                elif ch == "-":
                    angle -= da
                elif ch == "[":
                    stack.append((x, y, angle))
                elif ch == "]":
                    x, y, angle = stack.pop()
            return lines

        depth_tr = ValueTracker(1.0)

        def plant():
            d = int(round(depth_tr.get_value()))
            d = max(1, min(5, d))
            lines = draw_lsystem(d)
            grp = VGroup()
            for (p1, p2) in lines:
                grp.add(Line(np.array([p1[0], p1[1], 0]),
                              np.array([p2[0], p2[1], 0]),
                              color=GREEN, stroke_width=1.5))
            return grp

        self.add(always_redraw(plant))

        # Info
        def d_now():
            return max(1, min(5, int(round(depth_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"depth $=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"rules:", font_size=20),
            Tex(r"$X \to F+[[X]-X]-F[-FX]+X$",
                font_size=18, color=GREEN),
            Tex(r"$F \to FF$", font_size=18, color=GREEN),
            Tex(r"turn angle $= 25^\circ$",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(d_now()))
        self.add(info)

        for d in range(2, 6):
            self.play(depth_tr.animate.set_value(float(d)),
                      run_time=1.3, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
