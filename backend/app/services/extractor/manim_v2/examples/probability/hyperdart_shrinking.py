from manim import *
import numpy as np


class HyperdartShrinkingExample(Scene):
    def construct(self):
        title = Text("Hyperdart: each hit shrinks the target", font_size=28).to_edge(UP)
        self.play(Write(title))

        np.random.seed(7)

        disc = Circle(radius=2.2, color=BLUE, fill_opacity=0.2)
        self.play(Create(disc))

        hits = VGroup()
        for _ in range(5):
            # Uniformly random point inside current disc
            r = disc.width / 2
            theta = np.random.uniform(0, TAU)
            u = np.random.uniform(0, 1)
            p = disc.get_center() + r * np.sqrt(u) * np.array([np.cos(theta), np.sin(theta), 0])
            hit = Dot(p, color=RED, radius=0.1)
            self.play(FadeIn(hit), run_time=0.4)
            hits.add(hit)

            # New radius = distance from center to hit
            new_r = np.linalg.norm(p - disc.get_center())
            new_disc = Circle(radius=new_r, color=YELLOW, fill_opacity=0.2).move_to(p)
            self.play(Transform(disc, new_disc), run_time=0.9)

        caption = MathTex(
            r"P(\text{game never ends}) = \tfrac{\pi}{4}",
            font_size=32, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
