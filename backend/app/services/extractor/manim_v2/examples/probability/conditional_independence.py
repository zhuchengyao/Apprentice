from manim import *
import numpy as np


class ConditionalIndependenceExample(Scene):
    """
    Conditional independence: X⊥Y|Z means P(X, Y|Z) = P(X|Z) P(Y|Z).
    Example: naive Bayes. Without conditioning on Z (disease),
    two symptoms X, Y appear correlated; conditioned on Z they're
    independent.

    TWO_COLUMN: LEFT heatmap of joint (X, Y) distribution marginalizing
    over Z. RIGHT shows P(X, Y|Z=1) and P(X, Y|Z=0) — products of
    marginals. ValueTracker s_tr toggles marginal vs conditional.
    """

    def construct(self):
        title = Tex(r"$X\perp Y\mid Z$: conditional independence",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Joint P(X, Y, Z) for binary variables
        # P(Z=1) = 0.4
        # P(X=1|Z=1)=0.8, P(X=1|Z=0)=0.2
        # P(Y=1|Z=1)=0.7, P(Y=1|Z=0)=0.1
        pZ = np.array([0.6, 0.4])  # [Z=0, Z=1]
        pX_Z = [[0.8, 0.2], [0.2, 0.8]]  # pX_Z[Z][X]: P(X|Z=z)
        pY_Z = [[0.9, 0.1], [0.3, 0.7]]

        def joint(z, x, y):
            return pZ[z] * pX_Z[z][x] * pY_Z[z][y]

        # Marginal P(X, Y) = sum over Z
        def P_marg(x, y):
            return joint(0, x, y) + joint(1, x, y)

        # P(X, Y | Z=z) = P(X|Z) · P(Y|Z)
        def P_cond(x, y, z):
            return pX_Z[z][x] * pY_Z[z][y]

        s_tr = ValueTracker(0.0)  # 0 = marginal, 1 = cond on Z=1, 2 = cond on Z=0

        def prob(x, y):
            s = s_tr.get_value()
            if s <= 1:
                # interpolate marginal to cond Z=1
                return (1 - s) * P_marg(x, y) + s * P_cond(x, y, 1)
            else:
                # interpolate cond Z=1 to cond Z=0
                alpha = s - 1
                return (1 - alpha) * P_cond(x, y, 1) + alpha * P_cond(x, y, 0)

        # 2×2 heatmap
        cell_size = 1.4
        origin = np.array([-1.2, -0.3, 0])

        def heatmap():
            grp = VGroup()
            for x in range(2):
                for y in range(2):
                    p = prob(x, y)
                    col = interpolate_color(GREY_D, YELLOW, min(1, p * 2))
                    rect = Square(side_length=cell_size,
                                   color=col,
                                   stroke_width=2,
                                   fill_color=col,
                                   fill_opacity=0.9).move_to(
                        origin + RIGHT * (y - 0.5) * cell_size
                                 + UP * (0.5 - x) * cell_size)
                    lbl = Tex(f"{p:.3f}", font_size=24).move_to(
                        origin + RIGHT * (y - 0.5) * cell_size
                                 + UP * (0.5 - x) * cell_size)
                    grp.add(rect, lbl)
            return grp

        self.add(always_redraw(heatmap))

        # Header labels
        self.add(Tex(r"$Y=0$", font_size=22).move_to(
            origin + LEFT * 0.5 * cell_size + UP * 1.1 * cell_size))
        self.add(Tex(r"$Y=1$", font_size=22).move_to(
            origin + RIGHT * 0.5 * cell_size + UP * 1.1 * cell_size))
        self.add(Tex(r"$X=0$", font_size=22).move_to(
            origin + LEFT * 1.15 * cell_size + UP * 0.5 * cell_size))
        self.add(Tex(r"$X=1$", font_size=22).move_to(
            origin + LEFT * 1.15 * cell_size + DOWN * 0.5 * cell_size))

        # Regime label
        def regime_str():
            s = s_tr.get_value()
            if s < 0.1:
                return r"$P(X,Y)$ (marginal)"
            if s < 1.05:
                return r"interpolating $\to P(X,Y|Z{=}1)$"
            if s < 1.15:
                return r"$P(X,Y|Z{=}1)$"
            if s < 1.95:
                return r"interpolating $\to P(X,Y|Z{=}0)$"
            return r"$P(X,Y|Z{=}0)$"

        regime_tex = Tex(regime_str(), color=YELLOW, font_size=26).to_edge(UP, buff=0.9)
        self.add(regime_tex)
        def update_regime(mob, dt):
            new = Tex(regime_str(), color=YELLOW, font_size=26).move_to(regime_tex)
            regime_tex.become(new)
            return regime_tex
        regime_tex.add_updater(update_regime)

        # Right side panel showing products
        def independence_check():
            # For conditional: check P(X=1, Y=1) vs P(X=1)·P(Y=1)
            s = s_tr.get_value()
            if s < 0.5:
                p_xy = P_marg(1, 1)
                p_x = P_marg(1, 0) + P_marg(1, 1)
                p_y = P_marg(0, 1) + P_marg(1, 1)
                return p_xy, p_x * p_y
            elif s < 1.5:
                p_xy = P_cond(1, 1, 1)
                p_x = pX_Z[1][1]
                p_y = pY_Z[1][1]
                return p_xy, p_x * p_y
            else:
                p_xy = P_cond(1, 1, 0)
                p_x = pX_Z[0][1]
                p_y = pY_Z[0][1]
                return p_xy, p_x * p_y

        info = VGroup(
            Tex(r"check $P(X{=}1, Y{=}1)\stackrel{?}{=}P(X{=}1)P(Y{=}1)$",
                font_size=20),
            VGroup(Tex(r"joint $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"product $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"marginal: joint $\neq$ product",
                color=RED, font_size=20),
            Tex(r"conditional: joint $=$ product",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(independence_check()[0]))
        info[2][1].add_updater(lambda m: m.set_value(independence_check()[1]))
        self.add(info)

        self.play(s_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(2.0), run_time=3, rate_func=smooth)
        self.wait(0.8)
