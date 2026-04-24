from manim import *
import numpy as np


class GaltonWatsonExtinctionExample(Scene):
    """
    Galton-Watson branching process: each individual has offspring
    ~ Poisson(λ). Mean = λ. Extinction probability q solves
        q = φ(q) = e^(λ(q-1)).
    For λ=0.8, q=1 (certain extinction). For λ=1.5, q≈0.417.

    TWO_COLUMN: LEFT shows 4 simulated trees growing over generations
    for λ=1.5; ValueTracker gen_tr reveals generations. RIGHT plots
    φ(q)=e^(λ(q-1)) vs q intersecting y=q at extinction probability;
    live λ_tr between 0.8 and 1.5.
    """

    def construct(self):
        title = Tex(r"Galton-Watson: extinction probability $q=e^{\lambda(q-1)}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Right panel: q-fixed-point diagram
        right_axes = Axes(x_range=[0, 1.1, 0.2], y_range=[0, 1.1, 0.2],
                          x_length=4.0, y_length=4.0,
                          axis_config={"include_numbers": True,
                                       "font_size": 16}
                          ).shift(RIGHT * 3.0 + DOWN * 0.3)
        self.play(Create(right_axes))

        lambda_tr = ValueTracker(1.5)

        def phi_curve():
            lam = lambda_tr.get_value()
            return right_axes.plot(lambda q: float(np.exp(lam * (q - 1))),
                                    x_range=[0, 1], color=BLUE, stroke_width=3)

        def diag():
            return right_axes.plot(lambda q: q, x_range=[0, 1],
                                    color=GREY_B, stroke_width=2)

        def fixed_points():
            lam = lambda_tr.get_value()
            # Solve q = e^(lam*(q-1)) numerically
            if lam <= 1:
                return VGroup(Dot(right_axes.c2p(1, 1), color=RED, radius=0.1))
            qs = np.linspace(0, 0.99, 200)
            vals = np.exp(lam * (qs - 1)) - qs
            sign = np.sign(vals)
            idx = np.where(np.diff(sign) != 0)[0]
            grp = VGroup()
            for i in idx:
                grp.add(Dot(right_axes.c2p(qs[i], qs[i]),
                             color=RED, radius=0.1))
            grp.add(Dot(right_axes.c2p(1, 1),
                         color=ORANGE, radius=0.08))
            return grp

        self.add(always_redraw(phi_curve), diag(), always_redraw(fixed_points))

        # LEFT: tree visualization
        np.random.seed(2)
        # Precompute one tree for lambda=1.5
        def simulate_tree(lam, max_gen=6):
            # List of generations: each is list of parents-children tuples
            gens = [[(0, 0)]]  # first individual at x=0
            for g in range(max_gen):
                prev = gens[-1]
                new = []
                for i, (px, _) in enumerate(prev):
                    k = np.random.poisson(lam)
                    xs = np.linspace(px - k * 0.25, px + k * 0.25, k) if k > 0 else []
                    for x in xs:
                        new.append((x, px))
                gens.append(new)
                if len(new) == 0:
                    break
            return gens

        tree = simulate_tree(1.5)

        left_origin = np.array([-4.5, 1.5, 0])
        h_step = 0.6

        def tree_draw():
            g = int(round(gen_tr.get_value()))
            g = max(0, min(len(tree) - 1, g))
            grp = VGroup()
            for gi in range(g + 1):
                for (x, px) in tree[gi]:
                    pos = left_origin + RIGHT * x * 0.7 + DOWN * gi * h_step
                    grp.add(Dot(pos, color=GREEN, radius=0.08))
                    if gi > 0:
                        parent_pos = left_origin + RIGHT * px * 0.7 + DOWN * (gi - 1) * h_step
                        grp.add(Line(parent_pos, pos, color=TEAL,
                                      stroke_width=1.5))
            return grp

        gen_tr = ValueTracker(0.0)
        self.add(always_redraw(tree_draw))

        # Info
        def fp_val():
            lam = lambda_tr.get_value()
            if lam <= 1:
                return 1.0
            q = 0.001
            for _ in range(200):
                q = np.exp(lam * (q - 1))
            return float(q)

        info = VGroup(
            VGroup(Tex(r"$\lambda=$", font_size=22),
                   DecimalNumber(1.5, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$q=$", font_size=22),
                   DecimalNumber(0.417, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"$\lambda<1$: extinct a.s.", color=ORANGE, font_size=20),
            Tex(r"$\lambda>1$: survives with prob $1-q$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(lambda_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(fp_val()))
        self.add(info)

        # Animate tree growing
        for g in range(len(tree)):
            self.play(gen_tr.animate.set_value(float(g)),
                      run_time=0.7, rate_func=smooth)
            self.wait(0.15)

        # Morph lambda down to show extinction
        self.play(lambda_tr.animate.set_value(0.8),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(lambda_tr.animate.set_value(1.5),
                  run_time=2, rate_func=smooth)
        self.wait(0.5)
