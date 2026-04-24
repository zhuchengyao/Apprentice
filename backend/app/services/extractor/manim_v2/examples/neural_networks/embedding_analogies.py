from manim import *
import numpy as np


class EmbeddingAnalogiesExample(Scene):
    """
    Word2Vec-style analogy: vec(king) - vec(man) + vec(woman) ≈
    vec(queen). Adapted from _2024/transformers/embedding.

    SINGLE_FOCUS:
      2D embedding plane with 6 word vectors (king, man, queen, woman,
      prince, princess). ValueTracker step_tr animates the analogy:
      start at KING, subtract MAN (yellow arrow), add WOMAN (green
      arrow), land near QUEEN. Parallel for PRINCE → PRINCESS.
    """

    def construct(self):
        title = Tex(r"Embedding analogy: $\vec{\text{king}} - \vec{\text{man}} + \vec{\text{woman}} \approx \vec{\text{queen}}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=9, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-0.5, -0.3, 0])
        self.play(Create(plane))

        # Embeddings placed so the analogy works exactly
        emb = {
            "king":     np.array([2.5, 1.5]),
            "man":      np.array([2.5, 0.0]),
            "queen":    np.array([-1.5, 1.5]),
            "woman":    np.array([-1.5, 0.0]),
            "prince":   np.array([2.5, -1.0]),
            "princess": np.array([-1.5, -1.0]),
        }

        colors = {"king": BLUE, "man": BLUE,
                  "queen": RED, "woman": RED,
                  "prince": GREEN, "princess": GREEN}

        dots = VGroup()
        labels = VGroup()
        for name, pos in emb.items():
            d = Dot(plane.c2p(*pos), color=colors[name], radius=0.1)
            l = Tex(name, color=colors[name], font_size=22
                     ).next_to(d, UR, buff=0.05)
            dots.add(d)
            labels.add(l)
        self.play(FadeIn(dots), Write(labels))

        # Parallel arrows: man→king, woman→queen should be parallel
        t_tr = ValueTracker(0.0)

        def gender_arrow():
            t = t_tr.get_value()
            start = plane.c2p(*emb["man"])
            end = plane.c2p(*emb["man"] + t * (emb["king"] - emb["man"]))
            return Arrow(start, end, color=BLUE, buff=0,
                          stroke_width=4,
                          max_tip_length_to_length_ratio=0.15)

        def analogy_arrow():
            t = t_tr.get_value()
            start = plane.c2p(*emb["woman"])
            end = plane.c2p(*emb["woman"] + t * (emb["queen"] - emb["woman"]))
            return Arrow(start, end, color=RED, buff=0,
                          stroke_width=4,
                          max_tip_length_to_length_ratio=0.15)

        def prince_arrow():
            t = t_tr.get_value()
            start = plane.c2p(*emb["prince"])
            end = plane.c2p(*emb["prince"] + t * (emb["king"] - emb["man"]))
            return Arrow(start, end, color=BLUE_D, buff=0,
                          stroke_width=3,
                          max_tip_length_to_length_ratio=0.15)

        self.add(always_redraw(gender_arrow),
                  always_redraw(analogy_arrow),
                  always_redraw(prince_arrow))

        self.play(t_tr.animate.set_value(1.0),
                   run_time=3, rate_func=smooth)

        note = Tex(r"male $\to$ female direction is consistent across rank",
                    color=YELLOW, font_size=24).to_edge(DOWN, buff=0.4)
        self.play(Write(note))

        # Second phase: analogy arithmetic via moving dot
        moving_dot_tr = ValueTracker(0.0)

        def analogy_path():
            t = moving_dot_tr.get_value()
            # Path: king → king-man → king-man+woman (= queen)
            king = emb["king"]
            man = emb["man"]
            woman = emb["woman"]
            if t < 0.5:
                s = t / 0.5
                return plane.c2p(*(king - s * man))
            else:
                s = (t - 0.5) / 0.5
                return plane.c2p(*(king - man + s * woman))

        def moving_pt():
            return Dot(analogy_path(), color=YELLOW, radius=0.12)

        def moving_trail():
            t = moving_dot_tr.get_value()
            pts = []
            n = max(10, int(60 * t))
            for ti in np.linspace(0, t, n):
                mt = moving_dot_tr.get_value()
                moving_dot_tr.set_value(ti)
                pts.append(analogy_path())
            moving_dot_tr.set_value(mt)
            m = VMobject(color=YELLOW, stroke_width=2.5, stroke_opacity=0.7)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(moving_trail),
                  always_redraw(moving_pt))

        self.play(moving_dot_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.5)
