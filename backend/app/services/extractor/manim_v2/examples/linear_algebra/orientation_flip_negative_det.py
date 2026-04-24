from manim import *
import numpy as np


class OrientationFlipNegativeDetExample(Scene):
    """
    Negative determinant means space gets flipped. ĵ starts to the
    LEFT of î. After a transformation with det<0, L(ĵ) is to the
    RIGHT of L(î) — orientation reversed.

    A = [[1, 1], [2, -1]] has det = -3. Show arc from î to ĵ (CCW),
    then arc from L(î) to L(ĵ) (now CW).
    """

    def construct(self):
        title = Tex(r"Negative $\det$: orientation reverses",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[1.0, 1.0], [2.0, -1.0]])
        det_A = float(np.linalg.det(A))

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=5)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=5)

        # Arc from î to ĵ (CCW in original, CW after flip)
        def arc_lbl():
            M = M_of()
            pi = M @ np.array([1, 0])
            pj = M @ np.array([0, 1])
            ai = np.arctan2(pi[1], pi[0])
            aj = np.arctan2(pj[1], pj[0])
            diff = aj - ai
            # normalize to [-pi, pi]
            while diff > PI: diff -= 2 * PI
            while diff < -PI: diff += 2 * PI
            center = plane.c2p(0, 0)
            scale = plane.x_length / (plane.x_range[1] - plane.x_range[0])
            arc = Arc(radius=0.6 * scale,
                       start_angle=ai, angle=diff,
                       color=YELLOW, stroke_width=4).move_arc_center_to(center)
            arc.add_tip(tip_length=0.2)
            return arc

        self.add(always_redraw(i_arrow), always_redraw(j_arrow), always_redraw(arc_lbl))

        # Status label
        def status_str():
            t = t_tr.get_value()
            if t < 0.05: return r"$\hat\jmath$ to the \textbf{left} of $\hat\imath$ (CCW)"
            if t < 0.95: return r"transforming..."
            return r"$L(\hat\jmath)$ to the \textbf{right} of $L(\hat\imath)$ (CW)"

        status_tex = Tex(status_str(), color=YELLOW, font_size=24).to_edge(DOWN, buff=0.4)
        self.add(status_tex)
        def update_status(mob, dt):
            new = Tex(status_str(), color=YELLOW, font_size=24).move_to(status_tex)
            status_tex.become(new)
            return status_tex
        status_tex.add_updater(update_status)

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}1&1\\2&-1\end{pmatrix}$", font_size=22),
            Tex(rf"$\det A={det_A:.1f}<0$", color=RED, font_size=22),
            Tex(r"orientation reversed",
                color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.add(info)

        self.play(t_tr.animate.set_value(1.0), run_time=3.5, rate_func=smooth)
        self.wait(1.0)
