from manim import *
import hashlib
import numpy as np


class BitcoinMiningNonceLottery(Scene):
    """A Bitcoin miner tries nonces until SHA-256(header || nonce) starts
    with enough leading zeros.  Simulate the hunt by scanning nonce =
    0, 1, ... and looking for 3 leading zero hex chars.  Every failed hash
    flashes RED, the winning one turns GREEN.  Each nonce pays a constant
    computation yet only 1/16^k land a block — the lottery picture."""

    def construct(self):
        title = Tex(
            r"Bitcoin mining: nonce lottery for leading-zero hashes",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        header = "block_header_"
        target_prefix = "000"

        header_tex = Tex(
            rf"header: \texttt{{{header}}} + nonce",
            font_size=26, color=BLUE,
        ).move_to(UP * 2.2)
        target_tex = Tex(
            rf"target: hash starts with \texttt{{{target_prefix}}}",
            font_size=26, color=YELLOW,
        ).move_to(UP * 1.5)
        self.play(Write(header_tex), Write(target_tex))

        nonce_val = Integer(0, font_size=30, color=WHITE)
        nonce_row = VGroup(
            Tex("nonce:", font_size=26), nonce_val,
        ).arrange(RIGHT, buff=0.15)
        nonce_row.to_edge(LEFT, buff=1.0).shift(UP * 0.3)
        self.add(nonce_row)

        hash_text = Tex("", font_size=24).move_to([0.5, 0.3, 0])
        status = Tex("", font_size=26).move_to([0.5, -0.45, 0])
        self.add(hash_text, status)

        failed_count = Integer(0, font_size=30, color=RED)
        failed_row = VGroup(
            Tex("failed attempts:", font_size=26, color=RED),
            failed_count,
        ).arrange(RIGHT, buff=0.15)
        failed_row.to_corner(DR, buff=0.4).shift(UP * 0.1)
        self.add(failed_row)

        rng = np.random.default_rng(7)
        start_nonce = int(rng.integers(0, 1000000))
        n = start_nonce
        attempts = 0
        winner = None
        winner_hash = None
        max_attempts = 120
        while attempts < max_attempts:
            msg = f"{header}{n}".encode()
            h = hashlib.sha256(msg).hexdigest()
            attempts += 1
            if h.startswith(target_prefix):
                winner = n
                winner_hash = h
                break
            n += 1

        n = start_nonce
        for i in range(min(attempts, 12)):
            msg = f"{header}{n}".encode()
            h = hashlib.sha256(msg).hexdigest()
            new_hash = Tex(
                rf"SHA256 = \texttt{{{h[:24]}}}\ldots",
                font_size=22, color=RED,
            ).move_to(hash_text)
            new_status = Tex(
                rf"prefix \texttt{{{h[:3]}}} $\ne$ \texttt{{{target_prefix}}}",
                font_size=24, color=RED,
            ).move_to(status)
            nonce_val.set_value(n)
            failed_count.set_value(i + 1)
            self.play(
                Transform(hash_text, new_hash),
                Transform(status, new_status),
                run_time=0.25,
            )
            n += 1

        if winner is not None:
            msg = f"{header}{winner}".encode()
            h = hashlib.sha256(msg).hexdigest()
            new_hash = Tex(
                rf"SHA256 = \texttt{{{h[:24]}}}\ldots",
                font_size=24, color=GREEN,
            ).move_to(hash_text)
            new_status = Tex(
                rf"prefix \texttt{{{h[:3]}}} = \texttt{{{target_prefix}}}\ \checkmark",
                font_size=28, color=GREEN,
            ).move_to(status)
            nonce_val.set_value(winner)
            failed_count.set_value(attempts - 1)
            self.play(
                Transform(hash_text, new_hash),
                Transform(status, new_status),
                run_time=0.8,
            )
            box = SurroundingRectangle(
                VGroup(hash_text, status), color=GREEN,
                buff=0.2, stroke_width=3,
            )
            self.play(Create(box))

        summary = Tex(
            r"Expected tries $\approx 16^k$ for $k$ leading zeros "
            r"— pure computational lottery.",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(summary))
        self.wait(1.5)
