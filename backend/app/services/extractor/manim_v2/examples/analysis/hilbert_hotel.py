from manim import *
import numpy as np


class HilbertHotelExample(Scene):
    """
    Hilbert's infinite hotel (from _2022/infinity adaptation):
    ℕ has "room for one more" even when every room is occupied.

    SINGLE_FOCUS (two-phase):
      Phase 1 (∞ + 1): 12 rooms visible; ValueTracker shift_tr moves
      every guest from room n to room n+1 via always_redraw, opening
      room 1 for a new guest.
      Phase 2 (∞ + ∞): shift_tr2 sends guest at room n to room 2n,
      freeing all odd-numbered rooms for a countable busload.
    """

    def construct(self):
        title = Tex(r"Hilbert's hotel: $\aleph_0 + 1 = \aleph_0 + \aleph_0 = \aleph_0$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 12
        room_y = 0.7
        x0, x1 = -5.6, 5.6
        dx = (x1 - x0) / N

        rooms = VGroup()
        for i in range(N):
            r = Rectangle(width=dx - 0.08, height=0.9,
                           color=WHITE, stroke_width=2,
                           fill_opacity=0.05)
            r.move_to([x0 + (i + 0.5) * dx, room_y, 0])
            lbl = MathTex(str(i + 1), font_size=18, color=GREY_B
                           ).next_to(r, DOWN, buff=0.12)
            rooms.add(VGroup(r, lbl))
        dots_note = Tex(r"$\cdots$", font_size=32, color=GREY_B
                         ).next_to(rooms, RIGHT, buff=0.1)
        self.play(FadeIn(rooms), Write(dots_note))

        shift_tr = ValueTracker(0.0)

        def guests_phase1():
            s = shift_tr.get_value()
            grp = VGroup()
            for i in range(N):
                x_src = x0 + (i + 0.5) * dx
                x_dst = x0 + (i + 1 + 0.5) * dx
                x = (1 - s) * x_src + s * x_dst
                if x > x1 - dx * 0.2:
                    continue
                grp.add(Dot([x, room_y, 0], color=BLUE, radius=0.13))
            # New guest pops into room 1 once s > 0.5
            alpha = max(0.0, min(1.0, (s - 0.5) / 0.5))
            if alpha > 0:
                grp.add(Dot([x0 + 0.5 * dx, room_y, 0],
                              color=YELLOW, radius=0.13 * alpha + 0.02))
            return grp

        self.add(always_redraw(guests_phase1))

        phase1_note = Tex(r"$\infty + 1$: every guest moves from room $n$ to $n+1$",
                          color=YELLOW, font_size=22).to_edge(DOWN, buff=0.6)
        self.play(Write(phase1_note))

        self.play(shift_tr.animate.set_value(1.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.6)

        # Phase 2: shift n → 2n
        self.play(FadeOut(phase1_note))
        self.remove(*[m for m in self.mobjects if isinstance(m, VGroup)
                       and m not in (rooms, title)])

        shift_tr2 = ValueTracker(0.0)

        def guests_phase2():
            s = shift_tr2.get_value()
            grp = VGroup()
            for i in range(N):  # original room n (1-indexed)
                n = i + 1
                src_x = x0 + (n - 0.5) * dx
                dst_x = x0 + (2 * n - 0.5) * dx
                x = (1 - s) * src_x + s * dst_x
                if x > x1:
                    continue
                grp.add(Dot([x, room_y, 0], color=BLUE, radius=0.13))
            # New bus guests fill odd rooms once s > 0.5
            alpha = max(0.0, min(1.0, (s - 0.5) / 0.5))
            if alpha > 0:
                for k in range(N):
                    odd_n = 2 * k + 1
                    if odd_n > N:
                        break
                    x = x0 + (odd_n - 0.5) * dx
                    grp.add(Dot([x, room_y, 0],
                                  color=ORANGE,
                                  radius=0.13 * alpha + 0.02))
            return grp

        self.add(always_redraw(guests_phase2))

        phase2_note = Tex(r"$\infty + \infty$: guest $n \mapsto 2n$; odd rooms free for a bus",
                          color=ORANGE, font_size=22).to_edge(DOWN, buff=0.6)
        self.play(Write(phase2_note))

        self.play(shift_tr2.animate.set_value(1.0),
                  run_time=4, rate_func=smooth)
        self.wait(0.7)

        final = MathTex(r"|\mathbb N| = |\mathbb N \cup \{*\}| = |\mathbb N \sqcup \mathbb N|",
                         color=GREEN, font_size=26
                         ).to_edge(DOWN, buff=0.2)
        self.play(Transform(phase2_note, final))
        self.wait(0.5)
