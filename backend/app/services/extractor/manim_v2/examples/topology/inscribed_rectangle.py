from manim import *
import numpy as np


class InscribedRectangleExample(Scene):
    """
    Search for inscribed rectangles in a smooth loop.

    SINGLE_FOCUS: a smooth closed loop. ValueTracker θ rotates a "test
    direction"; for each θ, two parallel chords through the centroid
    perpendicular to direction θ are found, and we draw a candidate
    rectangle whose sides are along/perpendicular to that direction.
    Only when the two perpendicular chord-pairs land on the curve
    correctly does it form an inscribed rectangle. We highlight when
    a near-rectangle is detected.
    """

    def construct(self):
        title = Tex(r"Inscribed rectangle: rotate a test direction; rectangles emerge",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Loop parametrization
        def loop_pt(t):
            return np.array([
                2.4 * np.cos(t) + 0.3 * np.cos(3 * t),
                1.6 * np.sin(t) + 0.2 * np.sin(2 * t) + 0.15 * np.cos(t),
                0,
            ])

        loop = ParametricFunction(loop_pt, t_range=[0, 2 * PI, 0.05],
                                   color=BLUE, stroke_width=3)
        self.play(Create(loop))

        # Sample loop densely for chord-finding
        ts = np.linspace(0, 2 * PI, 600, endpoint=False)
        loop_samples = np.array([loop_pt(t)[:2] for t in ts])

        theta_tr = ValueTracker(0.0)

        def two_chords_perp_to(theta_val):
            """Return two parallel chords perpendicular to direction θ
            through the centroid; each is a pair of intersection points
            of the perpendicular line with the loop, taken at +d offset
            and -d offset from centroid. Pick d so that both intersection
            chords have approximately equal length."""
            direction = np.array([np.cos(theta_val), np.sin(theta_val)])
            perp = np.array([-direction[1], direction[0]])
            centroid = loop_samples.mean(axis=0)

            # For each perpendicular distance d, find intersections of the
            # line {centroid + d*direction + t*perp} with the loop.
            def chord_at_offset(d):
                base = centroid + d * direction
                # Loop sample dot perp gives signed distance along the perp axis
                proj_perp = (loop_samples - base) @ perp
                proj_dir = (loop_samples - base) @ direction
                # We want points where proj_dir crosses 0 (i.e., on the line)
                hits = []
                for i in range(len(proj_dir)):
                    a, b = proj_dir[i], proj_dir[(i + 1) % len(proj_dir)]
                    if a * b < 0:
                        # Linear interp for crossing point
                        frac = a / (a - b)
                        i_next = (i + 1) % len(proj_dir)
                        pt = loop_samples[i] + frac * (loop_samples[i_next] - loop_samples[i])
                        hits.append(pt)
                if len(hits) < 2:
                    return None
                # Take the two outermost (most negative perp and most positive)
                ts_perp = [(p - base) @ perp for p in hits]
                idx_min = int(np.argmin(ts_perp))
                idx_max = int(np.argmax(ts_perp))
                return hits[idx_min], hits[idx_max]

            d_value = 0.5
            chord1 = chord_at_offset(+d_value)
            chord2 = chord_at_offset(-d_value)
            return chord1, chord2

        def rectangle_attempt():
            t = theta_tr.get_value()
            chord1, chord2 = two_chords_perp_to(t)
            if chord1 is None or chord2 is None:
                return VGroup()
            p1, p2 = chord1
            p3, p4 = chord2
            # Pair up endpoints to form a quadrilateral (p1, p2, p4, p3 ordering)
            poly = Polygon(
                [p1[0], p1[1], 0],
                [p2[0], p2[1], 0],
                [p4[0], p4[1], 0],
                [p3[0], p3[1], 0],
                color=YELLOW, fill_opacity=0.25, stroke_width=3,
            )
            return poly

        # Test direction indicator at center
        def direction_arrow():
            t = theta_tr.get_value()
            d = 1.5 * np.array([np.cos(t), np.sin(t), 0])
            return Arrow([0, 0, 0], d, buff=0, color=ORANGE,
                         stroke_width=4, max_tip_length_to_length_ratio=0.15)

        self.add(always_redraw(rectangle_attempt),
                 always_redraw(direction_arrow))

        # Right-side panel
        rcol_x = +5.0

        def info_panel():
            return VGroup(
                MathTex(rf"\theta = {np.degrees(theta_tr.get_value()):.0f}^\circ",
                        color=ORANGE, font_size=22),
                Tex(r"yellow = candidate", color=YELLOW, font_size=20),
                Tex(r"4 vertices on loop", color=GREY_B, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([rcol_x, +1.0, 0])

        self.add(always_redraw(info_panel))

        thm_lbl = Tex(r"Toeplitz: $\exists$ inscribed rectangles for every smooth loop",
                      color=GREEN, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(Write(thm_lbl))

        self.play(theta_tr.animate.set_value(PI), run_time=10, rate_func=linear)
        self.wait(0.8)
