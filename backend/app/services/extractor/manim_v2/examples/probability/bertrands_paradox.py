from manim import *
import numpy as np


class BertrandsParadoxExample(Scene):
    """
    Bertrand's paradox: "probability that a random chord is longer
    than √3 R" depends on sampling method — 1/3, 1/2, or 1/4.

    COMPARISON (3 panels):
      Each circle shows N=50 chords sampled by a different method;
      YELLOW for longer than √3 R, grey otherwise. ValueTracker n_tr
      grows the sample count; always_redraw live fraction label
      converges to the respective theoretical p.
    """

    def construct(self):
        title = Tex(r"Bertrand's paradox: 3 ways to sample a random chord",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 1.2
        centers = [np.array([-4.0, -0.5, 0]),
                    np.array([0.0, -0.5, 0]),
                    np.array([4.0, -0.5, 0])]
        method_names = [r"random endpoints",
                         r"random radial midpoint",
                         r"random interior midpoint"]
        method_p = [1 / 3, 1 / 2, 1 / 4]

        # Draw three reference circles
        circles = VGroup(*[Circle(radius=R, color=WHITE, stroke_width=2
                                    ).move_to(c)
                            for c in centers])
        self.play(Create(circles))

        # Precompute 50 chords per method via given seed
        rng = np.random.default_rng(4)
        thresh = np.sqrt(3) * R

        def sample_method_A():
            # two uniform endpoints on circle
            th1 = rng.uniform(0, 2 * PI)
            th2 = rng.uniform(0, 2 * PI)
            p1 = R * np.array([np.cos(th1), np.sin(th1), 0])
            p2 = R * np.array([np.cos(th2), np.sin(th2), 0])
            return p1, p2

        def sample_method_B():
            # uniform midpoint along a radius at uniform angle
            th = rng.uniform(0, 2 * PI)
            d = rng.uniform(0, R)
            # midpoint at d along radius at angle th; chord is perpendicular
            mid = d * np.array([np.cos(th), np.sin(th), 0])
            perp = np.array([-np.sin(th), np.cos(th), 0])
            half = np.sqrt(max(R ** 2 - d ** 2, 0))
            p1 = mid + half * perp
            p2 = mid - half * perp
            return p1, p2

        def sample_method_C():
            # uniform midpoint inside disk
            while True:
                x, y = rng.uniform(-R, R), rng.uniform(-R, R)
                if x * x + y * y <= R * R:
                    break
            mid = np.array([x, y, 0])
            d = np.linalg.norm(mid)
            if d < 1e-6:
                th = rng.uniform(0, 2 * PI)
                perp = np.array([np.cos(th), np.sin(th), 0])
                half = R
            else:
                perp = np.array([-y, x, 0]) / d
                half = np.sqrt(max(R ** 2 - d ** 2, 0))
            p1 = mid + half * perp
            p2 = mid - half * perp
            return p1, p2

        samplers = [sample_method_A, sample_method_B, sample_method_C]
        N_total = 50
        chord_data = []
        for s in samplers:
            ch = []
            for _ in range(N_total):
                p1, p2 = s()
                ch.append((p1, p2))
            chord_data.append(ch)

        n_tr = ValueTracker(0)

        def chords_for(method_idx):
            def f():
                n = int(round(n_tr.get_value()))
                n = max(0, min(n, N_total))
                grp = VGroup()
                for k in range(n):
                    p1, p2 = chord_data[method_idx][k]
                    length = np.linalg.norm(p1 - p2)
                    color = YELLOW if length > thresh else GREY_B
                    grp.add(Line(centers[method_idx] + p1,
                                    centers[method_idx] + p2,
                                    color=color, stroke_width=1.5,
                                    stroke_opacity=0.7))
                return grp
            return f

        for i in range(3):
            self.add(always_redraw(chords_for(i)))

        method_lbls = VGroup()
        for i in range(3):
            lbl = Tex(method_names[i], font_size=18).next_to(
                centers[i], UP, buff=R + 0.2)
            method_lbls.add(lbl)
        self.play(Write(method_lbls))

        def panel(i):
            def f():
                n = int(round(n_tr.get_value()))
                n = max(1, min(n, N_total))
                count = sum(
                    1 for k in range(n)
                    if np.linalg.norm(chord_data[i][k][0] - chord_data[i][k][1]) > thresh)
                frac = count / n
                return VGroup(
                    MathTex(rf"\hat p = {frac:.2f}",
                             color=YELLOW, font_size=22),
                    MathTex(rf"\to {method_p[i]:.3f}",
                             color=GREEN, font_size=20),
                ).arrange(DOWN, buff=0.1).next_to(centers[i],
                                                     DOWN, buff=R + 0.3)
            return f

        for i in range(3):
            self.add(always_redraw(panel(i)))

        self.play(n_tr.animate.set_value(N_total),
                   run_time=6, rate_func=linear)

        note = Tex(r"Same question, different answer: 1/3, 1/2, or 1/4",
                    color=RED, font_size=22).to_edge(DOWN, buff=0.25)
        self.play(Write(note))
        self.wait(0.5)
