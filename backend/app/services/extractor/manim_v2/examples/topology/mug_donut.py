from manim import *
import numpy as np


class MugDonutExample(Scene):
    """
    Continuous deformation from a coffee mug to a torus.

    A ValueTracker s slides 0 → 1. At each frame an always_redraw VMobject
    interpolates the boundary points of a 'mug' silhouette toward those
    of a 'donut' silhouette. Same number of points, same hole — the
    morph never tears or punches a new hole, illustrating that they
    are homeomorphic. Genus 1 stays invariant the whole way.
    """

    def construct(self):
        title = Text("A coffee mug deforms continuously into a donut",
                     font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        N = 200  # boundary samples for outer + inner rings

        def mug_outline(n_samples: int) -> tuple[np.ndarray, np.ndarray]:
            """Return (outer, inner) closed-loop points for a stylized mug."""
            # Outer boundary: a rounded rectangle on the left + a handle loop on the right
            outer = []
            # left rounded body — top edge, right side, bottom, left side, top
            body_w, body_h = 1.6, 2.2
            cx, cy = -1.4, 0.0
            corner_r = 0.25
            edges = [
                # top edge of body (left to right)
                ('line', [cx - body_w / 2 + corner_r, cy + body_h / 2],
                         [cx + body_w / 2 - corner_r, cy + body_h / 2]),
                ('arc', [cx + body_w / 2 - corner_r, cy + body_h / 2 - corner_r],
                        corner_r, PI / 2, 0),
                # right edge of body
                ('line', [cx + body_w / 2, cy + body_h / 2 - corner_r],
                         [cx + body_w / 2, cy - body_h / 2 + corner_r]),
                ('arc', [cx + body_w / 2 - corner_r, cy - body_h / 2 + corner_r],
                        corner_r, 0, -PI / 2),
                # bottom edge
                ('line', [cx + body_w / 2 - corner_r, cy - body_h / 2],
                         [cx - body_w / 2 + corner_r, cy - body_h / 2]),
                ('arc', [cx - body_w / 2 + corner_r, cy - body_h / 2 + corner_r],
                        corner_r, -PI / 2, -PI),
                # left edge
                ('line', [cx - body_w / 2, cy - body_h / 2 + corner_r],
                         [cx - body_w / 2, cy + body_h / 2 - corner_r]),
                ('arc', [cx - body_w / 2 + corner_r, cy + body_h / 2 - corner_r],
                        corner_r, PI, PI / 2),
            ]
            # Sample outer body roughly proportional to length
            samples_body = n_samples
            for kind, *args in edges:
                if kind == 'line':
                    a, b = np.array(args[0]), np.array(args[1])
                    seglen = np.linalg.norm(b - a)
                    n = max(2, int(samples_body * seglen / 20))
                    for t in np.linspace(0, 1, n, endpoint=False):
                        outer.append(a + t * (b - a))
                else:
                    center, r, theta_a, theta_b = args
                    n = max(2, int(samples_body * abs(theta_b - theta_a) / 6))
                    for theta in np.linspace(theta_a, theta_b, n, endpoint=False):
                        outer.append(np.array(center) + r * np.array([np.cos(theta), np.sin(theta)]))
            outer_arr = np.array(outer)
            # Resample to exactly n_samples
            outer_arr = _resample_closed(outer_arr, n_samples)

            # Inner hole boundary: an oval where the handle "hole" sits.
            # On a real mug there's a small loop on the right side. We model the hole as
            # a small ellipse to the right of the body.
            inner = []
            hx, hy = -0.2, 0.0  # hole center
            hw, hh = 0.45, 0.7
            for theta in np.linspace(0, 2 * PI, n_samples, endpoint=False):
                inner.append([hx + hw * np.cos(-theta), hy + hh * np.sin(-theta)])
            inner_arr = np.array(inner)
            return outer_arr, inner_arr

        def torus_outline(n_samples: int) -> tuple[np.ndarray, np.ndarray]:
            """Outer + inner ring of an annulus (donut viewed from above)."""
            cx = 1.4
            R_outer = 1.6
            R_inner = 0.55
            outer = np.array([[cx + R_outer * np.cos(t), R_outer * np.sin(t)]
                              for t in np.linspace(0, 2 * PI, n_samples, endpoint=False)])
            inner = np.array([[cx + R_inner * np.cos(-t), R_inner * np.sin(-t)]
                              for t in np.linspace(0, 2 * PI, n_samples, endpoint=False)])
            return outer, inner

        mug_outer, mug_inner = mug_outline(N)
        donut_outer, donut_inner = torus_outline(N)

        # Center both shapes so the morph stays in view
        mug_center_x = mug_outer[:, 0].mean()
        donut_center_x = donut_outer[:, 0].mean()
        # Don't recenter — we want the gradual translation as part of the morph

        s_tracker = ValueTracker(0.0)

        def shape_outline(outer_a, outer_b, inner_a, inner_b):
            s = s_tracker.get_value()
            outer = (1 - s) * outer_a + s * outer_b
            inner = (1 - s) * inner_a + s * inner_b
            outer_3d = [np.array([p[0], p[1], 0]) for p in outer]
            inner_3d = [np.array([p[0], p[1], 0]) for p in inner]
            outer_3d.append(outer_3d[0])
            inner_3d.append(inner_3d[0])
            outer_path = VMobject(color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.45)
            outer_path.set_points_as_corners(outer_3d)
            inner_path = VMobject(color=BLACK, stroke_width=4, fill_color=BLACK, fill_opacity=1.0)
            inner_path.set_points_as_corners(inner_3d)
            return VGroup(outer_path, inner_path)

        morphing_shape = always_redraw(
            lambda: shape_outline(mug_outer, donut_outer, mug_inner, donut_inner)
        )
        self.add(morphing_shape)

        # RIGHT COLUMN: live deformation parameter and topological invariants
        def info_panel():
            s = s_tracker.get_value()
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=WHITE, font_size=30),
                MathTex(r"\text{genus} = 1", color=GREEN, font_size=28),
                MathTex(r"\chi = V - E + F = 0", color=GREEN, font_size=26),
                Text("one hole — never torn,\nnever pinched",
                     color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, 0.5, 0])

        self.add(always_redraw(info_panel))

        # Forward and back to make the homeomorphism feel reversible
        self.play(s_tracker.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.4)
        self.play(s_tracker.animate.set_value(0.0), run_time=3, rate_func=smooth)
        self.wait(0.3)
        self.play(s_tracker.animate.set_value(0.6), run_time=2, rate_func=smooth)

        conclusion = MathTex(r"\text{mug} \cong \text{torus}",
                             font_size=40, color=YELLOW).move_to([4.4, -2.6, 0])
        self.play(Write(conclusion))
        self.wait(1.0)


def _resample_closed(points: np.ndarray, n: int) -> np.ndarray:
    """Resample a closed polyline to exactly n equally-spaced points."""
    closed = np.vstack([points, points[:1]])
    diffs = np.diff(closed, axis=0)
    seglens = np.linalg.norm(diffs, axis=1)
    cum = np.concatenate([[0], np.cumsum(seglens)])
    total = cum[-1]
    targets = np.linspace(0, total, n, endpoint=False)
    out = []
    for t in targets:
        idx = np.searchsorted(cum, t, side='right') - 1
        idx = max(0, min(idx, len(seglens) - 1))
        local = (t - cum[idx]) / seglens[idx] if seglens[idx] > 0 else 0
        out.append(closed[idx] + local * diffs[idx])
    return np.array(out)
