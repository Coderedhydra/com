```python
from manim import *

class CircleToSquare(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)
        square = Square(side_length=2, color=GREEN, fill_opacity=0.5)
        square.rotate(PI/4)
        square.move_to(circle.get_center())

        title = Tex("Circle to Square Transformation").scale(1.5).to_edge(UP)
        self.play(Write(title))
        self.wait(1)


        self.play(Create(circle))
        self.wait(1)

        self.play(
            Transform(circle, square),
            run_time=3
        )
        self.wait(1)

        self.play(
            circle.animate.rotate(PI/2),
            run_time=2
        )
        self.wait(1)

        self.play(
            Unwrite(title),
            FadeOut(circle)
        )

        self.wait(1)


```