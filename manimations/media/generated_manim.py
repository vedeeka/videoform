from manim import *
import os

class StackAnimation(Scene):
    def construct(self):
        audio_file = "narration.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.stack_elements = VGroup()
        self.create_stack()
        self.push_elements()
        self.pop_elements()

        self.wait(2)

    def create_stack(self):
        top_label = Text("Top", color=BLUE).scale(0.7).shift(UP * 3.5)
        bottom_label = Text("Bottom", color=YELLOW).scale(0.7).shift(DOWN * 3.5)

        self.stack_rectangle = Rectangle(width=1.5, height=6, fill_color=GREY, fill_opacity=0.5).move_to(ORIGIN)

        self.play(Create(self.stack_rectangle))
        self.play(FadeIn(top_label), FadeIn(bottom_label))

        self.add(top_label, bottom_label)

        self.wait(1)

    def push_elements(self):
        elements = ["A", "B", "C", "D", "E"]
        for i, value in enumerate(elements):
            rect = Rectangle(width=1.2, height=0.5, fill_color=GREEN, fill_opacity=0.8).shift(UP * (i * 0.5) + DOWN * 2.5)
            label = Text(value, color=WHITE).move_to(rect.get_center())

            self.stack_elements.add(rect)
            self.play(Create(rect), Write(label))
            self.wait(0.5)

            self.play(rect.animate.scale(1.05), run_time=0.2)
            self.play(rect.animate.scale(1/1.05), run_time=0.2)

        self.wait(1)

    def pop_elements(self):
        for i in range(len(self.stack_elements) - 1, -1, -1):
            rect = self.stack_elements[i]
            self.play(rect.animate.fade(0.5))
            self.wait(0.5)

            if i > 0:
                self.play(self.stack_elements[i-1].animate.scale(1.05), run_time=0.2)
                self.play(self.stack_elements[i-1].animate.scale(1/1.05), run_time=0.2)

        self.wait(1)