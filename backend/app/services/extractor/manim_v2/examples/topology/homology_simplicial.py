from manim import *
import numpy as np


class HomologySimplicialExample(Scene):
    """
    Simplicial homology on a triangulated annulus:
    χ = V − E + F = 0 for annulus (ring). H_0 = ℤ (one component),
    H_1 = ℤ (one loop around hole), H_2 = 0.

    SINGLE_FOCUS: annulus triangulated with ring of 8 outer + 8 inner
    vertices. Count vertices, edges, faces; compute χ = 0 matching
    β_0 − β_1 + β_2 = 1 − 1 + 0.
    """

    def construct(self):
        title = Tex(r"Simplicial homology of annulus: $\chi=V-E+F=\beta_0-\beta_1=0$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Triangulate annulus: 8 outer + 8 inner vertices
        n = 8
        R_out, R_in = 2.5, 1.2
        outer = [R_out * np.array([np.cos(2 * PI * i / n), np.sin(2 * PI * i / n), 0])
                 for i in range(n)]
        inner = [R_in * np.array([np.cos(2 * PI * i / n + PI / n), np.sin(2 * PI * i / n + PI / n), 0])
                 for i in range(n)]

        # Vertices
        outer_dots = VGroup(*[Dot(p, color=BLUE, radius=0.08) for p in outer])
        inner_dots = VGroup(*[Dot(p, color=GREEN, radius=0.08) for p in inner])
        self.play(FadeIn(outer_dots), FadeIn(inner_dots))

        # Edges and faces
        edges = []
        faces = []
        for i in range(n):
            # outer ring
            edges.append((outer[i], outer[(i + 1) % n]))
            # inner ring
            edges.append((inner[i], inner[(i + 1) % n]))
            # cross edges
            edges.append((outer[i], inner[i]))
            edges.append((outer[(i + 1) % n], inner[i]))
            # 2 triangles per segment
            faces.append((outer[i], outer[(i + 1) % n], inner[i]))
            faces.append((outer[(i + 1) % n], inner[(i + 1) % n], inner[i]))

        V = 2 * n
        E = len(edges)
        F = len(faces)

        step_tr = ValueTracker(0.0)

        def edges_revealed():
            s = step_tr.get_value()
            n_reveal = int(s * E)
            grp = VGroup()
            for k in range(min(n_reveal, E)):
                p1, p2 = edges[k]
                grp.add(Line(p1, p2, color=GREY_B, stroke_width=1.5))
            return grp

        def faces_revealed():
            s = step_tr.get_value()
            if s < 1.1:
                return VGroup()
            alpha = min(1.0, (s - 1.1) / 1.0)
            n_reveal = int(alpha * F)
            grp = VGroup()
            for k in range(min(n_reveal, F)):
                p1, p2, p3 = faces[k]
                col = interpolate_color(YELLOW, ORANGE, k / F)
                grp.add(Polygon(p1, p2, p3, color=col,
                                 stroke_width=1,
                                 fill_color=col, fill_opacity=0.35))
            return grp

        self.add(always_redraw(faces_revealed))
        self.add(always_redraw(edges_revealed))

        info = VGroup(
            VGroup(Tex(r"$V=$", color=BLUE, font_size=22),
                   DecimalNumber(2 * n, num_decimal_places=0,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$E=$", color=GREY_B, font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(GREY_B)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$F=$", color=YELLOW, font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$V-E+F=$", color=GREEN, font_size=22),
                   DecimalNumber(2 * n, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"annulus: $\beta_0=1$, $\beta_1=1$",
                color=YELLOW, font_size=20),
            Tex(r"$\chi=\beta_0-\beta_1=0$",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DL, buff=0.3)

        def E_now():
            s = step_tr.get_value()
            return min(E, int(s * E))

        def F_now():
            s = step_tr.get_value()
            if s < 1.1:
                return 0
            alpha = min(1.0, (s - 1.1) / 1.0)
            return int(alpha * F)

        info[1][1].add_updater(lambda m: m.set_value(E_now()))
        info[2][1].add_updater(lambda m: m.set_value(F_now()))
        info[3][1].add_updater(lambda m: m.set_value(2 * n - E_now() + F_now()))
        self.add(info)

        self.play(step_tr.animate.set_value(1.0),
                  run_time=4, rate_func=linear)
        self.wait(0.3)
        self.play(step_tr.animate.set_value(2.1),
                  run_time=3, rate_func=linear)
        self.wait(0.8)
