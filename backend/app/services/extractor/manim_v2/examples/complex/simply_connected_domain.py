from manim import *
import numpy as np


class SimplyConnectedDomainExample(Scene):
    """
    A domain is simply connected iff every closed loop can be
    contracted to a point. Disk is simply connected; annulus is not.

    COMPARISON:
      LEFT disk with loop contracting; RIGHT annulus with loop
      around hole that cannot contract. ValueTracker contract_tr
      shrinks both loops.
    """

    def construct(self):
        title = Tex(r"Simply connected: every loop contracts to a point",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: disk
        left_center = np.array([-3.5, -0.3, 0])
        disk = Circle(radius=2.0, color=BLUE, fill_opacity=0.25,
                        stroke_width=2).move_to(left_center)
        self.play(Create(disk))
        disk_lbl = Tex("disk (simply connected)", color=BLUE, font_size=20
                        ).move_to(left_center + np.array([0, 2.4, 0]))
        self.play(Write(disk_lbl))

        # RIGHT: annulus
        right_center = np.array([3.5, -0.3, 0])
        outer = Circle(radius=2.0, color=ORANGE, fill_opacity=0.25,
                         stroke_width=2).move_to(right_center)
        inner = Circle(radius=0.5, color=BLACK, fill_opacity=1.0,
                         stroke_width=2, stroke_color=ORANGE
                         ).move_to(right_center)
        self.play(Create(outer), Create(inner))
        ann_lbl = Tex("annulus (not simply connected)",
                       color=ORANGE, font_size=20
                       ).move_to(right_center + np.array([0, 2.4, 0]))
        self.play(Write(ann_lbl))

        contract_tr = ValueTracker(1.0)  # 1 = full size, 0 = contracted

        def disk_loop():
            s = contract_tr.get_value()
            radius = 1.3 * s + 0.01
            return Circle(radius=radius, color=GREEN,
                            stroke_width=3).move_to(left_center)

        def ann_loop():
            s = contract_tr.get_value()
            # Loop around inner hole; can't contract below inner radius
            radius = max(1.3 * s, 0.7)
            return Circle(radius=radius, color=RED,
                            stroke_width=3).move_to(right_center)

        self.add(always_redraw(disk_loop), always_redraw(ann_loop))

        def info():
            s = contract_tr.get_value()
            disk_r = 1.3 * s + 0.01
            ann_r = max(1.3 * s, 0.7)
            return VGroup(
                MathTex(rf"\text{{scale}} = {s:.2f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\text{{disk loop radius}} = {disk_r:.2f}",
                         color=GREEN, font_size=18),
                MathTex(rf"\text{{ann loop radius}} = {ann_r:.2f}",
                         color=RED, font_size=18),
                Tex(r"ann stuck $\ge$ hole radius $= 0.5$",
                     color=RED, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(contract_tr.animate.set_value(0.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(contract_tr.animate.set_value(1.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
