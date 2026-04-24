from manim import *
import numpy as np


class BayesTheoremExample(Scene):
    """
    Bayes' theorem visualized as a 2×2 contingency table whose
    cell areas update as ValueTrackers move the prior P(H) and
    likelihoods P(E|H), P(E|¬H).

    SINGLE_FOCUS:
      Unit square split horizontally by P(H), then each column split
      vertically by P(E|H) for the left column and P(E|¬H) for the
      right. Top-left = TP (true positives), top-right = FP,
      bottom-left = FN, bottom-right = TN. Posterior P(H|E) = TP / (TP + FP).
    """

    def construct(self):
        title = Tex(r"Bayes: $P(H \mid E) = \dfrac{P(E\mid H)\,P(H)}{P(E)}$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Trackers
        prior = ValueTracker(0.30)
        like_h = ValueTracker(0.80)   # P(E | H)
        like_nh = ValueTracker(0.20)  # P(E | ¬H)

        # Unit square dimensions
        sq_w, sq_h = 4.5, 4.0
        anchor = np.array([-3.0, -0.6, 0])  # bottom-left of square

        # Outer frame
        frame = Rectangle(width=sq_w, height=sq_h, color=GREY_B,
                          stroke_width=2)
        frame.move_to(anchor + np.array([sq_w / 2, sq_h / 2, 0]))
        self.play(Create(frame))

        # 4 always_redraw cells
        def cell_TP():
            p = prior.get_value()
            l = like_h.get_value()
            w = sq_w * p
            h = sq_h * l
            rect = Rectangle(width=w, height=h, color=YELLOW, stroke_width=1,
                             fill_color=YELLOW, fill_opacity=0.7)
            rect.move_to(anchor + np.array([w / 2, sq_h - h / 2, 0]))
            return rect

        def cell_FN():
            p = prior.get_value()
            l = like_h.get_value()
            w = sq_w * p
            h = sq_h * (1 - l)
            rect = Rectangle(width=w, height=h, color=RED_E, stroke_width=1,
                             fill_color=RED_E, fill_opacity=0.5)
            rect.move_to(anchor + np.array([w / 2, h / 2, 0]))
            return rect

        def cell_FP():
            p = prior.get_value()
            l = like_nh.get_value()
            w = sq_w * (1 - p)
            h = sq_h * l
            rect = Rectangle(width=w, height=h, color=ORANGE, stroke_width=1,
                             fill_color=ORANGE, fill_opacity=0.6)
            rect.move_to(anchor + np.array([sq_w * p + w / 2, sq_h - h / 2, 0]))
            return rect

        def cell_TN():
            p = prior.get_value()
            l = like_nh.get_value()
            w = sq_w * (1 - p)
            h = sq_h * (1 - l)
            rect = Rectangle(width=w, height=h, color=BLUE_E, stroke_width=1,
                             fill_color=BLUE_E, fill_opacity=0.4)
            rect.move_to(anchor + np.array([sq_w * p + w / 2, h / 2, 0]))
            return rect

        self.add(always_redraw(cell_TP), always_redraw(cell_FN),
                 always_redraw(cell_FP), always_redraw(cell_TN))

        # Axis labels
        h_lbl = Tex(r"$H$", color=YELLOW, font_size=22).next_to(
            anchor + np.array([sq_w * 0.15, sq_h + 0.1, 0]), UP, buff=0.05)
        nh_lbl = Tex(r"$\neg H$", color=BLUE, font_size=22).next_to(
            anchor + np.array([sq_w * 0.7, sq_h + 0.1, 0]), UP, buff=0.05)
        e_lbl = Tex(r"$E$", color=GREEN, font_size=22).next_to(
            anchor + np.array([-0.2, sq_h * 0.8, 0]), LEFT, buff=0.05)
        ne_lbl = Tex(r"$\neg E$", color=RED, font_size=22).next_to(
            anchor + np.array([-0.2, sq_h * 0.2, 0]), LEFT, buff=0.05)
        self.play(Write(h_lbl), Write(nh_lbl), Write(e_lbl), Write(ne_lbl))

        # RIGHT COLUMN
        rcol_x = +4.4

        def info_panel():
            p = prior.get_value()
            lh = like_h.get_value()
            lnh = like_nh.get_value()
            tp = p * lh
            fp = (1 - p) * lnh
            P_E = tp + fp
            posterior = tp / P_E if P_E > 0 else 0
            return VGroup(
                MathTex(rf"P(H) = {p:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"P(E|H) = {lh:.2f}", color=GREEN, font_size=22),
                MathTex(rf"P(E|\neg H) = {lnh:.2f}", color=ORANGE, font_size=22),
                MathTex(rf"P(E) = {P_E:.4f}", color=WHITE, font_size=22),
                MathTex(rf"P(H|E) = {posterior:.3f}",
                        color=YELLOW, font_size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        # Sweep parameters
        for p_v, lh_v, lnh_v in [(0.30, 0.80, 0.20),
                                 (0.05, 0.99, 0.05),    # rare disease, accurate test
                                 (0.50, 0.70, 0.30),
                                 (0.05, 0.95, 0.20),
                                 (0.30, 0.80, 0.20)]:
            self.play(prior.animate.set_value(p_v),
                      like_h.animate.set_value(lh_v),
                      like_nh.animate.set_value(lnh_v),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
