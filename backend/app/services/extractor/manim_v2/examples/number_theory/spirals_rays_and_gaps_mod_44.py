from manim import *
import numpy as np


class SpiralsRaysAndGapsMod44(Scene):
    """Plot n at polar (sqrt(n), n radians) for n up to N_max.  Two phases:
    (1) all integers reveal 44 tight spirals; (2) primes only — retain only
    the rays corresponding to residues coprime to 44 (i.e. coprime to 4
    and 11).  The gap pattern emerges: primes live on phi(44) = 20 of the
    44 rays.  Show the coprime/coprime ray colors."""

    def construct(self):
        title = Tex(
            r"Prime spiral gaps: $\phi(44)=20$ rays survive",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def sieve(n):
            flag = [True] * (n + 1)
            flag[0] = flag[1] = False
            for i in range(2, int(n ** 0.5) + 1):
                if flag[i]:
                    for j in range(i * i, n + 1, i):
                        flag[j] = False
            return [i for i, f in enumerate(flag) if f]

        N = 2500
        primes = set(sieve(N))

        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        def polar_point(n, scale=0.08):
            r = np.sqrt(n) * scale
            return np.array([r * np.cos(n), r * np.sin(n), 0])

        all_dots = VGroup()
        prime_dots = VGroup()
        coprime_color_dots = VGroup()
        for n in range(2, N):
            p = polar_point(n)
            if np.linalg.norm(p[:2]) > 4:
                continue
            d_all = Dot(p, radius=0.02, color=BLUE, fill_opacity=0.7)
            all_dots.add(d_all)
            if n in primes:
                color = YELLOW
                r = gcd(n, 44)
                if r == 1:
                    prime_dots.add(Dot(p, radius=0.03,
                                       color=YELLOW, fill_opacity=0.9))
                else:
                    prime_dots.add(Dot(p, radius=0.03,
                                       color=RED, fill_opacity=0.9))

        all_dots.shift(LEFT * 3.2 + DOWN * 0.2)
        prime_dots.shift(RIGHT * 3.2 + DOWN * 0.2)

        left_cap = Tex(r"all integers $n \le 2500$",
                       font_size=22, color=BLUE).move_to([-3.2, 2.2, 0])
        right_cap = Tex(r"primes only", font_size=22,
                        color=YELLOW).move_to([3.2, 2.2, 0])
        self.play(FadeIn(left_cap), FadeIn(right_cap))

        self.play(LaggedStart(*[FadeIn(d) for d in all_dots],
                              lag_ratio=0.001, run_time=2.5))
        self.play(LaggedStart(*[FadeIn(d) for d in prime_dots],
                              lag_ratio=0.003, run_time=2.5))

        legend = VGroup(
            VGroup(Dot(radius=0.07, color=YELLOW),
                   Tex(r"prime with $\gcd(n,44)=1$", font_size=20)).arrange(
                RIGHT, buff=0.2),
            VGroup(Dot(radius=0.07, color=RED),
                   Tex(r"prime 2, 11 or their multiples", font_size=20)).arrange(
                RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(legend))

        fact = MathTex(
            r"44 \text{ spirals, but only } \phi(44)=20"
            r"\text{ rays can hold primes}",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(fact))
        self.wait(1.5)
