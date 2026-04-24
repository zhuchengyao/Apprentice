from manim import *
import numpy as np


class MengerSpongeExample(ThreeDScene):
    """
    Menger sponge: 3D analog of Sierpinski carpet. Cube divided
    into 27 sub-cubes, 7 removed (6 face-centers + center), 20 kept.
    Fractal dimension log 20 / log 3 ≈ 2.727.

    ValueTracker level_tr ∈ {0, 1, 2} (level 3 prohibitively many
    cubes). always_redraw rebuilds.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=40 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.08)

        axes = ThreeDAxes(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[-2.5, 2.5, 1],
                          x_length=4.0, y_length=4.0, z_length=4.0)
        self.add(axes)

        size = 4.0

        def subcubes_at_level(L):
            if L == 0:
                return [(0.0, 0.0, 0.0, 1.0)]
            sub = subcubes_at_level(L - 1)
            kept = []
            for (cx, cy, cz, s) in sub:
                s_new = s / 3
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        for dz in range(-1, 2):
                            # Remove if at face center or true center
                            # Face center: exactly one of dx, dy, dz is 0 AND other two are 0 as well → center
                            # Actually Menger: keep if number of nonzeros >= 2
                            nonzero = sum(1 for d in (dx, dy, dz) if d != 0)
                            if nonzero >= 2:
                                kept.append((cx + dx * s_new, cy + dy * s_new,
                                              cz + dz * s_new, s_new))
            return kept

        level_tr = ValueTracker(0.0)

        def sponge():
            L = int(round(level_tr.get_value()))
            L = max(0, min(2, L))
            cubes = subcubes_at_level(L)
            grp = VGroup()
            for (cx, cy, cz, s) in cubes:
                c = Cube(side_length=s * size,
                         fill_opacity=0.7,
                         stroke_width=0.8)
                c.set_color(
                    interpolate_color(BLUE, ORANGE, abs(cx + cy + cz)))
                c.move_to(np.array([cx * size, cy * size, cz * size]))
                grp.add(c)
            return grp

        self.add(always_redraw(sponge))

        title = Tex(r"Menger sponge: $d=\log 20/\log 3\approx 2.727$",
                    font_size=24)
        info = VGroup(
            VGroup(Tex(r"level $L=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"cubes $=20^L=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"volume $(20/27)^L\to 0$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        def L_now():
            return max(0, min(2, int(round(level_tr.get_value()))))
        info[0][1].add_updater(lambda m: m.set_value(L_now()))
        info[1][1].add_updater(lambda m: m.set_value(20 ** L_now()))

        for L in [1, 2]:
            self.play(level_tr.animate.set_value(float(L)),
                      run_time=2.2, rate_func=smooth)
            self.wait(0.5)
        self.wait(1.0)
        self.stop_ambient_camera_rotation()
