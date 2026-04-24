from manim import *
import numpy as np


class CarWithSpeedometerExample(Scene):
    """
    A car moving along a road with position s(t) and a speedometer
    showing current speed v(t) = ds/dt. Example: s(t) = t³/10 on
    t ∈ [0, 3], so v(t) = 0.3 t².
    """

    def construct(self):
        title = Tex(r"Car with speedometer: $s(t)$ and $v(t)=ds/dt$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Road on top
        road_y = 1.5
        road = NumberLine(x_range=[0, 9, 1], length=9, include_numbers=True,
                           font_size=18).shift(UP * road_y)
        self.add(road)
        self.add(Tex(r"position $s$", font_size=20).next_to(road, RIGHT, buff=0.2))

        t_tr = ValueTracker(0.0)

        def s_of(t):
            return t ** 3 / 10 * 3  # scale s(3)=2.7 into visible range

        def v_of(t):
            return 0.3 * t * t * 3  # scaled matching

        # Car (simple rectangle)
        def car():
            t = t_tr.get_value()
            pos = road.n2p(s_of(t))
            car_body = Rectangle(width=0.6, height=0.3,
                                  color=BLUE, fill_color=BLUE,
                                  fill_opacity=0.8).move_to(pos + UP * 0.15)
            # Wheels
            wheel1 = Dot(pos + LEFT * 0.2 + DOWN * 0.05, color=GREY, radius=0.08)
            wheel2 = Dot(pos + RIGHT * 0.2 + DOWN * 0.05, color=GREY, radius=0.08)
            return VGroup(car_body, wheel1, wheel2)

        self.add(always_redraw(car))

        # Speedometer (semicircle + needle)
        speedo_center = DOWN * 1.3 + LEFT * 3
        speedo_radius = 1.3
        speedo_arc = Arc(radius=speedo_radius, start_angle=PI, angle=-PI,
                          color=WHITE, stroke_width=3).move_to(speedo_center)
        self.add(speedo_arc)
        self.add(Tex(r"0", font_size=18).move_to(speedo_center + LEFT * speedo_radius + DOWN * 0.1))
        self.add(Tex(r"v", font_size=22).move_to(speedo_center + UP * speedo_radius + UP * 0.2))
        self.add(Tex(r"max", font_size=18).move_to(speedo_center + RIGHT * speedo_radius + DOWN * 0.1))

        v_max = v_of(3.0)

        def needle():
            t = t_tr.get_value()
            v = v_of(t)
            frac = min(1.0, v / v_max)
            angle = PI - frac * PI
            tip = speedo_center + speedo_radius * np.array([np.cos(angle), np.sin(angle), 0])
            return Line(speedo_center, tip, color=RED, stroke_width=5)

        def speedo_dot():
            return Dot(speedo_center, color=RED, radius=0.08)

        self.add(always_redraw(needle), always_redraw(speedo_dot))

        # Position and velocity labels
        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=24),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$s(t)=t^3/10\cdot 3=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$v(t)=ds/dt=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DR, buff=0.3).shift(LEFT * 0.5)
        info[0][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(s_of(t_tr.get_value())))
        info[2][1].add_updater(lambda m: m.set_value(v_of(t_tr.get_value())))
        self.add(info)

        self.play(t_tr.animate.set_value(3.0), run_time=6, rate_func=linear)
        self.wait(0.8)
