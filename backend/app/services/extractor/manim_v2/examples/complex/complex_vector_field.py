from manim import *
import numpy as np


class ComplexVectorFieldExample(Scene):
    """
    A complex function f: ℂ → ℂ as a vector field: at each point z,
    draw an arrow from z to f(z). For f(z) = z² the field shows a
    "squaring" pattern with stagnation at origin.

    SINGLE_FOCUS:
      ValueTracker k_tr morphs f through 3 options: z² → 1/z → exp(z)
      via Transform. always_redraw field arrows at a 9×7 lattice
      with color coded by |f(z)|.
    """

    def construct(self):
        title = Tex(r"Complex function as vector field: $z \to f(z)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-2.5, 2.5, 0.5],
                               y_range=[-1.8, 1.8, 0.5],
                               x_length=10, y_length=5.8,
                               background_line_style={"stroke_opacity": 0.3}
                               ).move_to([0, -0.3, 0])
        self.play(Create(plane))

        # State object to track which function is active
        state = {"f": lambda z: z ** 2, "name": r"f(z) = z^2"}

        def field():
            grp = VGroup()
            f = state["f"]
            for xv in np.arange(-2.2, 2.3, 0.5):
                for yv in np.arange(-1.5, 1.6, 0.4):
                    z = xv + 1j * yv
                    try:
                        w = f(z)
                    except Exception:
                        continue
                    vec = np.array([w.real - xv, w.imag - yv])
                    mag = np.linalg.norm(vec)
                    if mag < 1e-4:
                        continue
                    # Scale arrow
                    s = 0.4 / max(mag, 0.4)
                    start = plane.c2p(xv, yv)
                    end = plane.c2p(xv + s * vec[0], yv + s * vec[1])
                    # color by |w| magnitude
                    intensity = min(1.0, float(abs(w)) / 3)
                    color = interpolate_color(BLUE, RED, intensity)
                    grp.add(Arrow(start, end, color=color, buff=0,
                                    stroke_width=2,
                                    max_tip_length_to_length_ratio=0.3))
            return grp

        self.add(always_redraw(field))

        def name_lbl():
            return MathTex(state["name"], color=YELLOW, font_size=28
                             ).to_corner(UR, buff=0.5).shift(DOWN * 0.5)

        lbl = name_lbl()
        self.add(lbl)

        phases = [
            (lambda z: z ** 2, r"f(z) = z^2"),
            (lambda z: 1 / z if abs(z) > 1e-4 else 0 + 0j, r"f(z) = 1/z"),
            (lambda z: np.exp(z), r"f(z) = e^z"),
        ]

        for (func, nm) in phases[1:]:
            state["f"] = func
            state["name"] = nm
            new_lbl = name_lbl()
            self.play(Transform(lbl, new_lbl), run_time=1.0)
            self.wait(1.8)

        self.wait(0.5)
