from manim import *
import numpy as np


class RamseyNumberR33Example(Scene):
    """
    Ramsey number R(3, 3) = 6: any 2-coloring of edges of K_6 contains
    a monochromatic triangle. K_5 with proper 2-coloring can avoid
    monochromatic triangles; K_6 cannot.

    COMPARISON:
      LEFT K_5 with 2-coloring that has no monochromatic triangle;
      RIGHT K_6 with 2-coloring; ValueTracker step_tr progressively
      reveals edges and highlights the found monochromatic triangle.
    """

    def construct(self):
        title = Tex(r"Ramsey: $R(3, 3) = 6$; $K_5$ can avoid, $K_6$ cannot",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n5 = 5
        center_L = np.array([-3.5, -0.5, 0])
        R5 = 1.7
        pos_L = [center_L + R5 * np.array([np.cos(2 * PI * k / n5 + PI / 2),
                                               np.sin(2 * PI * k / n5 + PI / 2), 0])
                 for k in range(n5)]
        edges_L = []
        for i in range(n5):
            edges_L.append(((i, (i + 1) % n5), RED))  # pentagon
            edges_L.append(((i, (i + 2) % n5), BLUE))  # star

        dots_K5 = VGroup(*[Dot(p, color=YELLOW, radius=0.1) for p in pos_L])
        self.play(FadeIn(dots_K5))

        n6 = 6
        center_R = np.array([3.5, -0.5, 0])
        R6 = 1.7
        pos_R = [center_R + R6 * np.array([np.cos(2 * PI * k / n6 + PI / 2),
                                               np.sin(2 * PI * k / n6 + PI / 2), 0])
                 for k in range(n6)]

        rng = np.random.default_rng(7)
        edges_list = [(i, j) for i in range(n6) for j in range(i + 1, n6)]
        edge_colors = rng.choice([RED, BLUE], size=len(edges_list))
        dots_K6 = VGroup(*[Dot(p, color=YELLOW, radius=0.1) for p in pos_R])
        self.play(FadeIn(dots_K6))

        K5_lbl = Tex(r"$K_5$: no mono triangle",
                      color=GREEN, font_size=20
                      ).move_to(center_L + np.array([0, 2.5, 0]))
        K6_lbl = Tex(r"$K_6$: mono triangle forced",
                      color=RED, font_size=20
                      ).move_to(center_R + np.array([0, 2.5, 0]))
        self.play(Write(K5_lbl), Write(K6_lbl))

        # Find monochromatic triangle in K_6
        def find_mono_triangle(colors):
            from itertools import combinations
            for (a, b, c) in combinations(range(n6), 3):
                c_ab = colors[edges_list.index((min(a, b), max(a, b)))]
                c_bc = colors[edges_list.index((min(b, c), max(b, c)))]
                c_ca = colors[edges_list.index((min(c, a), max(c, a)))]
                if c_ab == c_bc == c_ca:
                    return (a, b, c), c_ab
            return None, None

        tri_verts, tri_color = find_mono_triangle(list(edge_colors))

        step_tr = ValueTracker(0)

        def edges_K5():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(edges_L)))
            grp = VGroup()
            for i in range(s):
                (u, v), col = edges_L[i]
                grp.add(Line(pos_L[u], pos_L[v],
                               color=col, stroke_width=2.5))
            return grp

        def edges_K6_grp():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(edges_list)))
            grp = VGroup()
            for i in range(s):
                u, v = edges_list[i]
                grp.add(Line(pos_R[u], pos_R[v],
                               color=edge_colors[i], stroke_width=2.5))
            return grp

        def mono_triangle_highlight():
            s = int(round(step_tr.get_value()))
            if s < max(len(edges_L), len(edges_list)) or tri_verts is None:
                return VGroup()
            a, b, c = tri_verts
            return Polygon(pos_R[a], pos_R[b], pos_R[c],
                             color=YELLOW, fill_opacity=0.4,
                             stroke_width=4)

        self.add(always_redraw(edges_K5),
                  always_redraw(edges_K6_grp),
                  always_redraw(mono_triangle_highlight))

        total_steps = max(len(edges_L), len(edges_list))

        def info():
            s = int(round(step_tr.get_value()))
            return VGroup(
                MathTex(rf"\text{{edges drawn}} = {s}/{total_steps}",
                         color=WHITE, font_size=20),
                Tex(r"K_5: pentagon RED + star BLUE",
                     color=GREEN, font_size=18),
                Tex(r"K_6: random coloring has forced mono triangle",
                     color=RED if s >= total_steps else GREY_B, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(step_tr.animate.set_value(total_steps),
                   run_time=6, rate_func=linear)
        self.wait(0.8)
