from manim import *
import numpy as np


class VAELatentSpaceExample(Scene):
    """
    Variational autoencoder: encoder maps input to a distribution
    over latent space (μ(x), σ(x)); decoder samples z ~ N(μ, σ²)
    and reconstructs. KL loss pushes q(z|x) toward N(0, I).

    TWO_COLUMN:
      LEFT  — 2D latent space with 5 input samples mapped to
              overlapping Gaussian "blobs" (ellipses). ValueTracker
              kl_weight_tr tightens them toward N(0, I).
      RIGHT — current (μ, σ) values for one class.
    """

    def construct(self):
        title = Tex(r"VAE latent space: encoder outputs $\mathcal N(\mu, \sigma^2)$ blobs",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=8, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        # 5 classes with initial (μ_x, μ_y, σ_x, σ_y)
        initial_clusters = [
            (-2.5, 1.5, 0.6, 0.4),  # class 0
            (2.2, 1.8, 0.5, 0.6),   # class 1
            (-1.8, -1.5, 0.7, 0.5),
            (2.5, -1.2, 0.4, 0.7),
            (0.0, 0.5, 0.3, 0.3),
        ]
        colors = [BLUE, GREEN, ORANGE, PURPLE, PINK]

        kl_weight_tr = ValueTracker(0.0)

        def blobs():
            s = kl_weight_tr.get_value()
            grp = VGroup()
            # At s=0: original clusters; at s=1: all → N(0, I)
            for (mu_x, mu_y, sig_x, sig_y), col in zip(initial_clusters, colors):
                cur_mx = (1 - s) * mu_x + s * 0
                cur_my = (1 - s) * mu_y + s * 0
                cur_sx = (1 - s) * sig_x + s * 1.0
                cur_sy = (1 - s) * sig_y + s * 1.0
                # 1-σ ellipse
                w = plane.c2p(cur_sx, 0)[0] - plane.c2p(0, 0)[0]
                h = plane.c2p(0, cur_sy)[1] - plane.c2p(0, 0)[1]
                e = Ellipse(width=2 * w, height=2 * h, color=col,
                              fill_opacity=0.35, stroke_width=2
                              ).move_to(plane.c2p(cur_mx, cur_my))
                grp.add(e)
                grp.add(Dot(plane.c2p(cur_mx, cur_my), color=col, radius=0.08))
            return grp

        self.add(always_redraw(blobs))

        # N(0, I) reference (unit circle at origin)
        ref_circle = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
                              color=WHITE, stroke_width=2,
                              stroke_opacity=0.6, fill_opacity=0
                              ).move_to(plane.c2p(0, 0))
        ref_lbl = MathTex(r"\mathcal N(0, I)", color=WHITE, font_size=18
                             ).next_to(ref_circle, UP, buff=0.15)
        self.play(Create(ref_circle), Write(ref_lbl))

        def info():
            s = kl_weight_tr.get_value()
            return VGroup(
                MathTex(rf"\lambda_{{\text{{KL}}}} = {s:.2f}",
                         color=YELLOW, font_size=24),
                Tex(r"encoder: $q(z|x) = \mathcal N(\mu(x), \sigma(x))$",
                     color=BLUE, font_size=18),
                Tex(r"KL loss: $D_{KL}(q || \mathcal N(0, I))$",
                     color=GREEN, font_size=18),
                Tex(r"high $\lambda_{KL}$: blobs $\to \mathcal N(0, I)$",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(kl_weight_tr.animate.set_value(1.0),
                   run_time=5, rate_func=smooth)
        self.wait(0.6)
        self.play(kl_weight_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
