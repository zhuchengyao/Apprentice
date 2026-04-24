from manim import *
import numpy as np


class TensorRankSlicingExample(Scene):
    """
    3-tensor T ∈ ℝ^{4×3×2} as a stack of 2 matrices (mode-3 slices).
    Rank-1 factorization T = u ⊗ v ⊗ w decomposes into outer product.

    SINGLE_FOCUS: 4×3 cell grid repeated for 2 slices; cells colored
    by value. ValueTracker s_tr rotates from general tensor to
    rank-1 approximation via best-rank-1 power method.
    """

    def construct(self):
        title = Tex(r"3-tensor $T_{ijk}$: rank-1 approximation $u\otimes v\otimes w$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Fixed random tensor + best rank-1 decomposition
        np.random.seed(2)
        I, J, K = 4, 3, 2
        T_full = np.random.randn(I, J, K) * 0.5 + 1.0

        # Find best rank-1 via power method on each mode
        u = np.random.randn(I); u /= np.linalg.norm(u)
        v = np.random.randn(J); v /= np.linalg.norm(v)
        w = np.random.randn(K); w /= np.linalg.norm(w)
        for _ in range(40):
            u_new = np.einsum("ijk,j,k->i", T_full, v, w)
            u = u_new / np.linalg.norm(u_new)
            v_new = np.einsum("ijk,i,k->j", T_full, u, w)
            v = v_new / np.linalg.norm(v_new)
            w_new = np.einsum("ijk,i,j->k", T_full, u, v)
            sigma = np.linalg.norm(w_new)
            w = w_new / sigma
        T_rank1 = sigma * np.einsum("i,j,k->ijk", u, v, w)

        s_tr = ValueTracker(0.0)

        def current():
            s = s_tr.get_value()
            return (1 - s) * T_full + s * T_rank1

        cell_s = 0.5

        def slice_display(k, origin):
            T = current()
            grp = VGroup()
            for i in range(I):
                for j in range(J):
                    v_val = T[i, j, k]
                    col_base = BLUE if v_val >= 0 else RED
                    col = interpolate_color(GREY_D, col_base, min(1, abs(v_val) / 2.5))
                    rect = Square(side_length=cell_s * 0.9,
                                   color=col, stroke_width=0.8,
                                   fill_color=col, fill_opacity=0.85).move_to(
                        origin + RIGHT * j * cell_s - DOWN * i * cell_s)
                    lbl = Tex(f"{v_val:+.2f}", font_size=14).move_to(
                        origin + RIGHT * j * cell_s - DOWN * i * cell_s)
                    grp.add(rect, lbl)
            return grp

        origin_k0 = np.array([-4.0, 0.5, 0])
        origin_k1 = np.array([-0.3, 0.5, 0])

        def slices():
            return VGroup(slice_display(0, origin_k0),
                           slice_display(1, origin_k1))

        self.add(always_redraw(slices))

        # Slice labels
        self.add(Tex(r"$k=0$ slice", font_size=22, color=YELLOW).move_to(
            origin_k0 + DOWN * 2.0 + RIGHT * cell_s))
        self.add(Tex(r"$k=1$ slice", font_size=22, color=YELLOW).move_to(
            origin_k1 + DOWN * 2.0 + RIGHT * cell_s))

        # Factor vectors shown
        def factors_display():
            grp = VGroup()
            # u (4 entries)
            origin_u = np.array([3.5, 1.8, 0])
            for i in range(I):
                col = interpolate_color(GREY_D, GREEN, min(1, abs(u[i]) * 1.5))
                rect = Square(side_length=0.4, color=col,
                               stroke_width=0.8,
                               fill_color=col, fill_opacity=0.85).move_to(
                    origin_u + DOWN * i * 0.5)
                lbl = Tex(f"{u[i]:+.2f}", font_size=12).move_to(rect)
                grp.add(rect, lbl)
            # v (3 entries)
            origin_v = np.array([4.5, 1.8, 0])
            for j in range(J):
                col = interpolate_color(GREY_D, ORANGE, min(1, abs(v[j]) * 1.5))
                rect = Square(side_length=0.4, color=col,
                               stroke_width=0.8,
                               fill_color=col, fill_opacity=0.85).move_to(
                    origin_v + DOWN * j * 0.5)
                lbl = Tex(f"{v[j]:+.2f}", font_size=12).move_to(rect)
                grp.add(rect, lbl)
            # w (2 entries)
            origin_w = np.array([5.5, 1.8, 0])
            for k in range(K):
                col = interpolate_color(GREY_D, PURPLE, min(1, abs(w[k]) * 1.5))
                rect = Square(side_length=0.4, color=col,
                               stroke_width=0.8,
                               fill_color=col, fill_opacity=0.85).move_to(
                    origin_w + DOWN * k * 0.5)
                lbl = Tex(f"{w[k]:+.2f}", font_size=12).move_to(rect)
                grp.add(rect, lbl)
            return grp

        self.add(factors_display())
        self.add(Tex(r"$u$", color=GREEN, font_size=20).move_to([3.5, 2.3, 0]))
        self.add(Tex(r"$v$", color=ORANGE, font_size=20).move_to([4.5, 2.3, 0]))
        self.add(Tex(r"$w$", color=PURPLE, font_size=20).move_to([5.5, 2.3, 0]))

        info = VGroup(
            VGroup(Tex(r"morph $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(rf"$\sigma={sigma:.3f}$", color=BLUE, font_size=20),
            VGroup(Tex(r"$\|T-\hat T\|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3).shift(LEFT * 2)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(T_full - current()))))
        self.add(info)

        self.play(s_tr.animate.set_value(1.0),
                  run_time=4, rate_func=smooth)
        self.wait(0.6)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=2.5, rate_func=smooth)
        self.wait(0.5)
