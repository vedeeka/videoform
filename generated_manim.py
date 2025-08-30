from manim import *
import os

class StackAnimation(Scene):
    def construct(self):
        # Check for the audio file
        audio_file = "narration.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        # Create Stack components
        top_label = Text("Top", color=YELLOW).shift(UP * 2)
        bottom_label = Text("Bottom", color=YELLOW).shift(DOWN * 2)
        stack_elements = VGroup()
        stack_height = 3
        num_elements = 5
        for i in range(num_elements):
            element = Rectangle(width=1.5, height=0.5, fill_color=BLUE, fill_opacity=0.7)
            element_label = Text(f"Item {i + 1}", color=WHITE).scale(0.4)
            element_group = VGroup(element, element_label).arrange(DOWN).move_to(UP * (num_elements - i - 1) * 0.5)
            stack_elements.add(element_group)

        stack_background = Rectangle(width=2, height=stack_height, color=WHITE)
        stack_background.move_to(ORIGIN)

        stack_container = VGroup(stack_background, stack_elements, top_label, bottom_label)

        self.play(DrawBorderThenFill(stack_background), run_time=2)
        self.play(FadeIn(stack_elements), run_time=2)
        self.play(FadeIn(top_label), FadeIn(bottom_label), run_time=2)

        # Push operation
        for i in range(num_elements):
            self.push_operation(i)

        # Pause for visibility
        self.wait(2)

        # Pop operation
        for i in range(num_elements):
            self.pop_operation(num_elements - 1 - i)

        self.wait(2)

    def push_operation(self, index):
        item = Rectangle(width=1.5, height=0.5, fill_color=GREEN, fill_opacity=0.7)
        item_label = Text(f"Item {index + 1}", color=WHITE).scale(0.4)
        item_group = VGroup(item, item_label).arrange(DOWN).move_to(UP * (-1 * index - 0.5))

        self.play(item_group.animate.move_to(UP * (0.5 * (index + 1))).scale(0.5),
                  Create(item), run_time=1)
        self.play(FadeIn(item_label), run_time=1)
        self.play(Indicate(item), run_time=1)
        self.play(item_group.animate.scale(2).move_to(UP * (0.5 * (index) + 1)), run_time=1)

    def pop_operation(self, index):
        item_to_pop = self.get_item_group(index)
        self.play(FadeOut(item_to_pop[1]), run_time=1)
        self.play(item_to_pop.animate.scale(0.5).move_to(DOWN * (index + 1)), run_time=1)

    def get_item_group(self, index):
        return self.mobjects[-(index + 1) - 2:]

    def on_overlap(self):
        self.add_sound("overlap_audio.mp3")