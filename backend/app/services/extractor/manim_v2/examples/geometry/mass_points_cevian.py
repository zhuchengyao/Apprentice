from manim import *
import numpy as np


class MassPointsCevianExample(Scene):
    """
    Mass point geometry: assign masses to vertices so a cevian balances.
    Example: triangle ABC, cevian from A to BC hits D splitting BC
    in ratio 2:3 (AD divides BC: BD:DC = 2:3). Place masses 3 at B
    and 2 at C, center of mass at D. If median from B hits AC at E
    with AE:EC = 1:4, etc.

    SINGLE_FOCUS: triangle with mass labels on vertices; show cevian
    balancing + combined mass computations.
    """

    def construct(self):
        title = Tex(r"Mass points: masses make cevians balance",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-3.0, -1.2, 0])
        B = np.array([3.0, -1.2, 0])
        C = np.array([-0.5, 2.0, 0])
        tri = Polygon(A, B, C, color=BLUE, stroke_width=3)
        self.play(Create(tri))

        # Masses at vertices
        mA = ValueTracker(3.0)
        mB = ValueTracker(2.0)
        mC = ValueTracker(1.0)

        def center_of_mass():
            a = mA.get_value()
            b = mB.get_value()
            c = mC.get_value()
            return (a * A + b * B + c * C) / (a + b + c)

        def vertex_labels():
            return VGroup(
                Tex(rf"$A({mA.get_value():.0f})$", color=GREEN, font_size=24).next_to(A, LEFT, buff=0.1),
                Tex(rf"$B({mB.get_value():.0f})$", color=ORANGE, font_size=24).next_to(B, RIGHT, buff=0.1),
                Tex(rf"$C({mC.get_value():.0f})$", color=RED, font_size=24).next_to(C, UP, buff=0.1),
            )

        def cm_dot():
            return Dot(center_of_mass(), color=YELLOW, radius=0.15)

        def cm_lbl():
            cm = center_of_mass()
            total = mA.get_value() + mB.get_value() + mC.get_value()
            return Tex(rf"G({total:.0f})", color=YELLOW, font_size=20).next_to(cm, UR, buff=0.1)

        # Midpoint on BC per ratio mB:mC
        def D_pt():
            b = mB.get_value()
            c = mC.get_value()
            return (c * B + b * C) / (b + c)

        def cevian_AD():
            return Line(A, D_pt(), color=TEAL, stroke_width=3)

        def D_dot():
            return Dot(D_pt(), color=TEAL, radius=0.1)

        def D_lbl():
            b = mB.get_value()
            c = mC.get_value()
            return Tex(rf"$D$ (BD:DC={c:.0f}:{b:.0f})",
                        color=TEAL, font_size=20).next_to(D_pt(), DOWN, buff=0.2)

        self.add(always_redraw(vertex_labels),
                 always_redraw(cevian_AD),
                 always_redraw(D_dot),
                 always_redraw(D_lbl),
                 always_redraw(cm_dot),
                 always_redraw(cm_lbl))

        info = VGroup(
            Tex(r"masses $m_A, m_B, m_C$", font_size=22),
            Tex(r"$D$ on $BC$: $BD:DC=m_C:m_B$",
                color=TEAL, font_size=20),
            Tex(r"$G$ center of mass divides $AD$:",
                font_size=20),
            Tex(r"$AG:GD=(m_B+m_C):m_A$",
                color=YELLOW, font_size=20),
            Tex(r"cevians concur at $G$ (Ceva)",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DL, buff=0.3)
        self.add(info)

        # Sweep masses
        for mB_val, mC_val in [(3, 1), (1, 3), (2, 2), (4, 1), (2, 1)]:
            self.play(mB.animate.set_value(float(mB_val)),
                      mC.animate.set_value(float(mC_val)),
                      run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
