from manim import *
import numpy as np


class HiddenMarkovModelExample(Scene):
    """
    Hidden Markov Model: hidden state X_t follows Markov chain;
    observation Y_t depends on X_t. Visualize a sequence of hidden
    states and their noisy observations.

    TWO_COLUMN:
      LEFT  — top row of squares (hidden states H/L), bottom row of
              observations (R/G/B). ValueTracker t_tr reveals them
              one step at a time; always_redraw.
      RIGHT — transition matrix + emission probabilities.
    """

    def construct(self):
        title = Tex(r"Hidden Markov Model: hidden states $X_t$, observations $Y_t$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Simulate HMM: 2 hidden states (High, Low), 3 emissions (R, G, B)
        rng = np.random.default_rng(9)
        N = 15
        # Transitions: 0.8 stay, 0.2 switch
        P_trans = np.array([[0.8, 0.2], [0.3, 0.7]])
        # Emission: state 0 (H) emits (R=0.6, G=0.3, B=0.1);
        #           state 1 (L) emits (R=0.1, G=0.3, B=0.6)
        P_emit = np.array([[0.6, 0.3, 0.1],
                            [0.1, 0.3, 0.6]])

        hidden = [0]  # start at H
        for _ in range(N - 1):
            h = hidden[-1]
            nh = int(rng.choice([0, 1], p=P_trans[h]))
            hidden.append(nh)
        obs = []
        for h in hidden:
            o = int(rng.choice([0, 1, 2], p=P_emit[h]))
            obs.append(o)

        hidden_labels = ["H", "L"]
        obs_labels = ["R", "G", "B"]
        hidden_colors = [BLUE, ORANGE]
        obs_colors = [RED, GREEN, BLUE]

        cell = 0.55
        x_start = -4.5
        hidden_y = 1.2
        obs_y = -0.3

        # Row outlines
        row_hidden = VGroup()
        row_obs = VGroup()
        for i in range(N):
            sq_h = Rectangle(width=cell * 0.9, height=cell * 0.9,
                              color=WHITE, fill_opacity=0.05,
                              stroke_width=1.5)
            sq_h.move_to([x_start + i * cell, hidden_y, 0])
            row_hidden.add(sq_h)
            sq_o = Rectangle(width=cell * 0.9, height=cell * 0.9,
                              color=WHITE, fill_opacity=0.05,
                              stroke_width=1.5)
            sq_o.move_to([x_start + i * cell, obs_y, 0])
            row_obs.add(sq_o)

        h_lbl = MathTex(r"X_t", color=WHITE, font_size=22
                          ).move_to([x_start - 0.7, hidden_y, 0])
        o_lbl = MathTex(r"Y_t", color=WHITE, font_size=22
                          ).move_to([x_start - 0.7, obs_y, 0])
        self.play(FadeIn(row_hidden), FadeIn(row_obs),
                   Write(h_lbl), Write(o_lbl))

        t_tr = ValueTracker(0)

        def filled_cells():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, N))
            grp = VGroup()
            for i in range(t):
                # Hidden
                h = hidden[i]
                col_h = hidden_colors[h]
                sq_h = Rectangle(width=cell * 0.9, height=cell * 0.9,
                                   color=col_h, fill_opacity=0.8,
                                   stroke_width=1.5)
                sq_h.move_to([x_start + i * cell, hidden_y, 0])
                grp.add(sq_h)
                grp.add(Tex(hidden_labels[h], font_size=14, color=WHITE
                              ).move_to(sq_h.get_center()))
                # Obs
                o = obs[i]
                col_o = obs_colors[o]
                sq_o = Rectangle(width=cell * 0.9, height=cell * 0.9,
                                   color=col_o, fill_opacity=0.8,
                                   stroke_width=1.5)
                sq_o.move_to([x_start + i * cell, obs_y, 0])
                grp.add(sq_o)
                grp.add(Tex(obs_labels[o], font_size=14, color=WHITE
                              ).move_to(sq_o.get_center()))
                # Arrow from hidden to obs
                grp.add(Arrow(
                    [x_start + i * cell, hidden_y - cell * 0.5, 0],
                    [x_start + i * cell, obs_y + cell * 0.5, 0],
                    color=GREY_B, stroke_width=1.5,
                    buff=0.05,
                    max_tip_length_to_length_ratio=0.2))
            return grp

        self.add(always_redraw(filled_cells))

        # Right: transition matrix + emission
        trans_lbl = MathTex(r"P(X_{t+1}|X_t) = \begin{pmatrix} 0.8 & 0.2 \\ 0.3 & 0.7 \end{pmatrix}",
                              color=BLUE, font_size=20
                              ).move_to([3.5, 2.0, 0])
        emit_lbl = MathTex(r"P(Y|X) = \begin{pmatrix} 0.6 & 0.3 & 0.1 \\ 0.1 & 0.3 & 0.6 \end{pmatrix}",
                             color=GREEN, font_size=20
                             ).move_to([3.5, 0.8, 0])
        self.play(Write(trans_lbl), Write(emit_lbl))

        def info():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, N))
            return VGroup(
                MathTex(rf"t = {t}/{N}", color=WHITE, font_size=22),
                Tex(r"BLUE: H, ORANGE: L", color=YELLOW, font_size=18),
                Tex(r"RGB: emissions", color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, -2.3, 0])

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(N),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
