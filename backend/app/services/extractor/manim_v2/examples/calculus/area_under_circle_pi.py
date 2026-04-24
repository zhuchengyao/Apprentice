from manim import *
import numpy as np


class AreaUnderCirclePiExample(Scene):
    """
    Disk area = πR² by unrolling concentric rings into a triangle.

    LEFT: a disk of radius R is sliced into N concentric rings.
    RIGHT: each ring (circumference 2π·rᵢ, thickness dr) is unrolled
           into a thin horizontal strip stacked into a triangle of
           base 2π·R and height R.

    A ValueTracker s slides 0→1: at s=0 every ring sits in its
    circular position; at s=1 every ring has been unrolled and stacked
    into the triangle. The total area is conserved throughout — it's
    the same πR², viewed two ways.
    """

    def construct(self):
        title = Text("Disk area: unroll concentric rings into a triangle",
                     font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        R = 1.6
        N = 24
        dr = R / N
        s = ValueTracker(0.0)

        # LEFT region anchor (disk center)
        disk_center = np.array([-3.5, -0.4, 0])
        # RIGHT region anchor (triangle bottom-left corner)
        tri_bl = np.array([+0.5, -2.4, 0])
        tri_base_pixels = 5.0  # screen-units the triangle base spans
        tri_height_pixels = 4.0

        # Each ring's destination strip in the triangle:
        # Strip i (counted from outside in toward center, i=0..N-1) has:
        #   - vertical position y_i = i·dr_pix from the bottom
        #   - width w_i = (2π·r_i / 2π·R) · base_pixels = (r_i / R) · base_pixels
        #     where r_i is the original radius of ring i = (N - i) · dr
        # We choose: outer ring (largest r, longest strip) at the BOTTOM of the triangle.
        dr_pix_y = tri_height_pixels / N

        def ring_path(ring_idx: int) -> VMobject:
            """ring_idx 0 = outermost, N-1 = innermost"""
            r_outer = (N - ring_idx) * dr   # original outer radius
            r_inner = (N - ring_idx - 1) * dr
            r_outer_pix = r_outer * (R + 0.3) / R  # scale to 1.6 screen units max — already R units
            r_outer_pix = r_outer
            r_inner_pix = r_inner

            # circumference (perimeter we'd unroll) in original units == 2π * r_avg
            # destination strip parameters in the triangle:
            strip_w = (r_outer / R) * tri_base_pixels   # width proportional to circumference
            y_bottom = ring_idx * dr_pix_y              # outer rings at bottom
            y_top = y_bottom + dr_pix_y

            s_val = s.get_value()

            if s_val < 0.001:
                # Pure ring shape
                annulus = Annulus(inner_radius=r_inner_pix, outer_radius=r_outer_pix,
                                  fill_color=interpolate_color(BLUE_D, YELLOW, ring_idx / max(1, N - 1)),
                                  fill_opacity=0.7, stroke_width=0.4)
                annulus.move_to(disk_center)
                return annulus

            if s_val > 0.999:
                # Pure strip in triangle
                # The strip is centered horizontally on the triangle's left edge for now,
                # forming a right triangle with vertical hypotenuse on the left.
                # We make a right triangle: right angle at top-left, base along bottom.
                strip = Rectangle(width=strip_w, height=dr_pix_y * 0.95,
                                  fill_color=interpolate_color(BLUE_D, YELLOW, ring_idx / max(1, N - 1)),
                                  fill_opacity=0.7, stroke_width=0.4)
                strip.move_to(tri_bl + np.array([strip_w / 2, y_bottom + dr_pix_y / 2, 0]))
                return strip

            # Smooth interpolation: a polygon that is part-arc, part-straight.
            # We approximate by sampling K points along the ring and morphing them
            # toward a straight horizontal line forming the strip's centerline.
            K = 32
            ring_pts_inner = []
            ring_pts_outer = []
            r_avg = (r_inner + r_outer) / 2
            for k in range(K + 1):
                theta = 2 * PI * k / K
                arc_in = disk_center + r_inner * np.array([np.cos(theta), np.sin(theta), 0])
                arc_out = disk_center + r_outer * np.array([np.cos(theta), np.sin(theta), 0])

                # Strip target: a horizontal segment of width strip_w centered at the
                # strip's anchor.
                # Map θ ∈ [0, 2π] linearly to [0, strip_w] along the bottom edge of the strip
                target_x = (k / K) * strip_w
                strip_in = tri_bl + np.array([target_x, y_bottom, 0])
                strip_out = tri_bl + np.array([target_x, y_top, 0])

                ring_pts_inner.append((1 - s_val) * arc_in + s_val * strip_in)
                ring_pts_outer.append((1 - s_val) * arc_out + s_val * strip_out)

            # Form the polygon: outer points forward, inner points backward
            poly_pts = ring_pts_outer + ring_pts_inner[::-1]
            polygon = Polygon(*poly_pts,
                              fill_color=interpolate_color(BLUE_D, YELLOW, ring_idx / max(1, N - 1)),
                              fill_opacity=0.7, stroke_width=0.3)
            return polygon

        # Build the scene group
        rings_group = always_redraw(lambda: VGroup(*[ring_path(i) for i in range(N)]))
        self.add(rings_group)

        # Reference labels
        R_label = MathTex("R", font_size=28, color=WHITE).next_to(
            Dot(disk_center + np.array([R + 0.05, 0, 0]), color=GREY_B, radius=0),
            UR, buff=0.05,
        )
        # Triangle outline (drawn permanent at s=1 size to indicate the destination)
        tri_outline = Polygon(
            tri_bl,
            tri_bl + np.array([tri_base_pixels, 0, 0]),
            tri_bl + np.array([0, tri_height_pixels, 0]),
            color=GREY_B, stroke_opacity=0.5, stroke_width=2,
        )
        base_lbl = MathTex(r"2\pi R", font_size=24, color=GREY_B).next_to(
            tri_bl + np.array([tri_base_pixels / 2, 0, 0]), DOWN, buff=0.15)
        height_lbl = MathTex("R", font_size=24, color=GREY_B).next_to(
            tri_bl + np.array([0, tri_height_pixels / 2, 0]), LEFT, buff=0.15)
        self.play(Create(tri_outline), Write(base_lbl), Write(height_lbl))

        self.wait(0.4)
        self.play(s.animate.set_value(1.0), run_time=5, rate_func=smooth)
        self.wait(0.6)

        # Final formula (TWO_COLUMN positioning - in a corner)
        formula_group = VGroup(
            MathTex(r"A_{\text{disk}} = \tfrac{1}{2} \cdot 2\pi R \cdot R", font_size=28, color=YELLOW),
            MathTex(r"= \pi R^2", font_size=34, color=YELLOW),
        ).arrange(DOWN, buff=0.15).move_to([+3.5, +1.2, 0])
        self.play(Write(formula_group))
        self.wait(1.0)
