from manim import *
import hashlib


class Sha256AvalancheProperty(Scene):
    """SHA-256's 'avalanche' property: flipping a single bit in the input
    flips roughly half the bits in the output, and the two output digests
    look completely unrelated.  Hash two nearly identical strings and
    highlight the bits that differ."""

    def construct(self):
        title = Tex(
            r"SHA-256 avalanche: 1-bit input change $\to$ 50\% output bits flip",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        s1 = "hello world"
        s2 = "hello worle"
        h1 = hashlib.sha256(s1.encode()).hexdigest()
        h2 = hashlib.sha256(s2.encode()).hexdigest()

        msg_a = Tex(rf"input A: \texttt{{{s1}}}",
                    font_size=28, color=BLUE).move_to(UP * 2.2)
        msg_b = Tex(rf"input B: \texttt{{{s2}}}",
                    font_size=28, color=GREEN).move_to(UP * 1.5)
        self.play(Write(msg_a), Write(msg_b))

        note = Tex(
            r"(only the last character differs)",
            font_size=22, color=GREY_B,
        ).move_to(UP * 0.9)
        self.play(FadeIn(note))

        def render_hex(hex_str, color, base_color=WHITE):
            chars = VGroup(*[
                Tex(ch, font_size=22, color=base_color)
                for ch in hex_str
            ]).arrange(RIGHT, buff=0.05)
            return chars

        hex_a = render_hex(h1, BLUE)
        hex_a_lab = Tex(r"SHA256(A)=", font_size=24,
                        color=BLUE).next_to(hex_a, LEFT, buff=0.15)
        row_a = VGroup(hex_a_lab, hex_a)
        row_a.move_to([0, -0.2, 0])

        hex_b = render_hex(h2, GREEN)
        hex_b_lab = Tex(r"SHA256(B)=", font_size=24,
                        color=GREEN).next_to(hex_b, LEFT, buff=0.15)
        row_b = VGroup(hex_b_lab, hex_b)
        row_b.move_to([0, -1.0, 0])

        self.play(FadeIn(row_a))
        self.play(FadeIn(row_b))
        self.wait(0.5)

        diff_count = 0
        anims = []
        for i, (c1, c2) in enumerate(zip(h1, h2)):
            if c1 != c2:
                diff_count += 1
                anims.append(hex_a[i].animate.set_color(RED))
                anims.append(hex_b[i].animate.set_color(RED))

        self.play(LaggedStart(*anims, lag_ratio=0.02, run_time=1.8))

        stats = VGroup(
            MathTex(
                rf"{diff_count} / 64\ \text{{hex chars differ}}",
                font_size=28, color=RED,
            ),
            MathTex(
                r"\approx \tfrac{1}{2}\ \text{of 256 output bits flip}",
                font_size=28, color=YELLOW,
            ),
            Tex(
                r"one-way function: outputs look random, no back-calculation",
                font_size=22, color=YELLOW,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        stats.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(stats[0]))
        self.play(FadeIn(stats[1]))
        self.play(FadeIn(stats[2]))
        self.wait(1.5)
