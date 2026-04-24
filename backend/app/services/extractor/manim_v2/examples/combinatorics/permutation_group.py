from manim import *
import numpy as np


class PermutationGroupExample(Scene):
    """
    S_3: the 6 permutations of an equilateral triangle's vertices
    as a product of a 3-cycle and a reflection.

    SINGLE_FOCUS:
      Triangle with vertices labeled 1, 2, 3 (color-coded).
      Rotate the triangle by 120°, 240°, 360° to cycle vertices;
      then Transform-flip for reflections; ValueTracker step_tr
      sequences through all 6 elements of S_3.
    """

    def construct(self):
        title = Tex(r"Symmetric group $S_3$: 6 permutations of a triangle",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Triangle
        scale = 1.5
        tri_pts = [scale * np.array([np.cos(PI / 2 + k * 2 * PI / 3),
                                        np.sin(PI / 2 + k * 2 * PI / 3), 0])
                   for k in range(3)]
        tri = Polygon(*tri_pts, color=WHITE, stroke_width=3)
        tri_center = ORIGIN
        tri.move_to(tri_center + DOWN * 0.5)

        colors = [BLUE, RED, GREEN]
        dots = VGroup()
        labels = VGroup()
        for i, p in enumerate(tri_pts):
            d = Dot(p + DOWN * 0.5, color=colors[i], radius=0.15)
            dots.add(d)
            lbl = MathTex(str(i + 1), color=colors[i],
                           font_size=28).next_to(d, direction=p / np.linalg.norm(p), buff=0.2)
            labels.add(lbl)

        self.play(Create(tri), FadeIn(dots), Write(labels))

        ident_lbl = MathTex(r"e = (1)(2)(3)", color=YELLOW, font_size=26
                             ).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        cur_lbl = ident_lbl
        self.play(Write(cur_lbl))
        self.wait(0.5)

        permutations = [
            (r"r = (1\,2\,3)", "rot", 2 * PI / 3),
            (r"r^2 = (1\,3\,2)", "rot", 4 * PI / 3),
            (r"e = (1)(2)(3)", "rot", 2 * PI),
            (r"s = (2\,3)", "flip_x", None),
            (r"rs = (1\,2)", "flip_rot", 2 * PI / 3),
            (r"r^2 s = (1\,3)", "flip_rot2", 4 * PI / 3),
        ]

        # Keep a "live" group of tri + dots + labels to apply Rotate to
        tri_grp = VGroup(tri, dots, labels)

        for (label_text, op, angle) in permutations:
            new_lbl = MathTex(label_text, color=YELLOW, font_size=26
                                ).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
            if op == "rot":
                # rotate from initial (already at previous state); easier to re-rotate a constant angle delta
                pass
            # We rebuild tri_grp from scratch to avoid compounding rotations
            def rebuild(theta, flip=False):
                grp = VGroup()
                t = Polygon(*tri_pts, color=WHITE, stroke_width=3)
                t.move_to(DOWN * 0.5)
                new_dots = VGroup()
                new_labels = VGroup()
                for i, p in enumerate(tri_pts):
                    d = Dot(p + DOWN * 0.5, color=colors[i], radius=0.15)
                    new_dots.add(d)
                    lbl = MathTex(str(i + 1), color=colors[i],
                                    font_size=28).next_to(
                                        d, direction=p / np.linalg.norm(p), buff=0.2)
                    new_labels.add(lbl)
                grp.add(t, new_dots, new_labels)
                grp.rotate(theta, about_point=DOWN * 0.5)
                if flip:
                    grp.apply_function(
                        lambda pt: np.array([-pt[0], pt[1] - 1, 0])
                        if False else np.array([pt[0] - (pt[0]) * 2, pt[1], 0])
                    )
                return grp

            if op == "rot":
                new_grp = rebuild(angle)
                self.play(Transform(tri_grp, new_grp),
                           Transform(cur_lbl, new_lbl),
                           run_time=1.3)
            elif op == "flip_x":
                # reflect across vertical axis
                new_grp = VGroup()
                t = Polygon(*tri_pts, color=WHITE, stroke_width=3)
                t.move_to(DOWN * 0.5)
                nd = VGroup()
                nl = VGroup()
                # swap dots 2, 3 (indices 1, 2)
                for i, p in enumerate(tri_pts):
                    mapped = {0: 0, 1: 2, 2: 1}[i]
                    d = Dot(tri_pts[mapped] + DOWN * 0.5,
                             color=colors[i], radius=0.15)
                    nd.add(d)
                    lbl = MathTex(str(i + 1), color=colors[i],
                                    font_size=28).next_to(
                                        d, direction=tri_pts[mapped] / np.linalg.norm(tri_pts[mapped]),
                                        buff=0.2)
                    nl.add(lbl)
                new_grp.add(t, nd, nl)
                self.play(Transform(tri_grp, new_grp),
                           Transform(cur_lbl, new_lbl),
                           run_time=1.2)
            elif op in ("flip_rot", "flip_rot2"):
                # flip then rotate
                # swap dots 2, 3 first then rotate by angle
                new_grp = VGroup()
                t = Polygon(*tri_pts, color=WHITE, stroke_width=3)
                t.move_to(DOWN * 0.5)
                nd = VGroup()
                nl = VGroup()
                swap = {0: 0, 1: 2, 2: 1}
                for i, p in enumerate(tri_pts):
                    mapped = swap[i]
                    d = Dot(tri_pts[mapped] + DOWN * 0.5,
                             color=colors[i], radius=0.15)
                    nd.add(d)
                    lbl = MathTex(str(i + 1), color=colors[i],
                                    font_size=28).next_to(
                                        d, direction=tri_pts[mapped] / np.linalg.norm(tri_pts[mapped]),
                                        buff=0.2)
                    nl.add(lbl)
                new_grp.add(t, nd, nl)
                new_grp.rotate(angle, about_point=DOWN * 0.5)
                self.play(Transform(tri_grp, new_grp),
                           Transform(cur_lbl, new_lbl),
                           run_time=1.2)
            self.wait(0.5)

        size_note = MathTex(r"|S_3| = 3! = 6",
                              color=GREEN, font_size=28
                              ).to_edge(DOWN, buff=0.5)
        self.play(Write(size_note))
        self.wait(0.5)
