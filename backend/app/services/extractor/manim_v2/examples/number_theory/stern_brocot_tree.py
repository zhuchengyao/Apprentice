from manim import *
import numpy as np


class SternBrocotTreeExample(Scene):
    """
    Stern-Brocot tree: every positive rational appears exactly once
    in lowest form. Built from 0/1 and 1/0; each interior level
    inserts mediants (a+c)/(b+d) between consecutive (a/b, c/d).

    SINGLE_FOCUS: 5 levels of the tree displayed. ValueTracker
    level_tr reveals levels 1..5; always_redraw draws the mediant
    fractions at correct positions.
    """

    def construct(self):
        title = Tex(r"Stern-Brocot: mediant $(a+c)/(b+d)$ hits every $\mathbb{Q}^+_{>0}$ once",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Build tree levels via BFS; start boundary 0/1, 1/0
        # Generate up to level 5
        levels = [[(0, 1), (1, 0)]]
        for _ in range(5):
            prev = levels[-1]
            new_level = [prev[0]]
            for i in range(len(prev) - 1):
                a, b = prev[i]
                c, d = prev[i + 1]
                new_level.append((a + c, b + d))
                new_level.append(prev[i + 1])
            levels.append(new_level)

        level_tr = ValueTracker(1.0)

        def layer_y(L):
            return 2.5 - L * 0.9

        def fraction_dots():
            L = int(round(level_tr.get_value()))
            L = max(0, min(5, L))
            grp = VGroup()
            for ell in range(L + 1):
                layer = levels[ell]
                n_pts = len(layer)
                xs = np.linspace(-5.5, 5.5, n_pts)
                for k, (a, b) in enumerate(layer):
                    if (a, b) in [(0, 1), (1, 0)]:
                        col = RED
                    elif ell == L:
                        col = YELLOW
                    else:
                        col = interpolate_color(BLUE, TEAL, ell / 5)
                    lbl = rf"$\tfrac{{{a}}}{{{b}}}$" if (a, b) != (1, 0) \
                           else r"$\infty$"
                    t = Tex(lbl, color=col, font_size=22).move_to(
                        [xs[k], layer_y(ell), 0])
                    grp.add(t)
                    if (a, b) not in [(0, 1), (1, 0)]:
                        # Find parents
                        if ell > 0:
                            prev_layer = levels[ell - 1]
                            prev_xs = np.linspace(-5.5, 5.5, len(prev_layer))
                            # parents are (a-c, b-d) and (c, d) approximately;
                            # use mediant formula — parents are the two neighbors in prev
                            # that averaged to give this frac
                            for i in range(len(prev_layer) - 1):
                                aa, bb = prev_layer[i]
                                cc, dd = prev_layer[i + 1]
                                if aa + cc == a and bb + dd == b:
                                    p1 = np.array([prev_xs[i], layer_y(ell - 1), 0])
                                    p2 = np.array([prev_xs[i + 1], layer_y(ell - 1), 0])
                                    mid = np.array([xs[k], layer_y(ell), 0])
                                    grp.add(Line(p1, mid, color=GREY_D,
                                                  stroke_width=1, stroke_opacity=0.5))
                                    grp.add(Line(p2, mid, color=GREY_D,
                                                  stroke_width=1, stroke_opacity=0.5))
                                    break
            return grp

        self.add(always_redraw(fraction_dots))

        # Info
        def L_now():
            return max(0, min(5, int(round(level_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"level $L=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"total fracs $=2^L+1$:", font_size=22),
                   DecimalNumber(3, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            Tex(r"every $p/q$ in lowest form exactly once",
                color=GREEN, font_size=20),
            Tex(r"$\gcd(p,q)=1$ everywhere",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(L_now()))
        info[1][1].add_updater(lambda m: m.set_value(2 ** L_now() + 1))
        self.add(info)

        for L in range(2, 6):
            self.play(level_tr.animate.set_value(float(L)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
