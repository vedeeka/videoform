from manim import *
import os
from gtts import gTTS

class StackScene(Scene):
    def construct(self):
        # Create Stack components
        top_label = Text("Top", font_size=24).set_color(BLUE).shift(UP * 3)
        bottom_label = Text("Bottom", font_size=24).set_color(BLUE).shift(DOWN * 3)
        stack_rect = Rectangle(width=1.5, height=5, color=GREEN).shift(RIGHT * 2)

        # Create elements in the stack
        elements = []
        element_count = 5
        for i in range(element_count):
            rect = Rectangle(width=1.5, height=0.7, color=YELLOW).shift(UP * (1.5 - i) + RIGHT * 2)
            elements.append(rect)

        # Arrange elements
        stack = VGroup(stack_rect, *elements)

        # Create labels for elements
        element_labels = []
        for i in range(element_count):
            label = Text(f"Element {i+1}", font_size=20).move_to(elements[i].get_center())
            element_labels.append(label)

        # Prepare the scene
        self.play(Create(stack_rect))
        self.play(Create(top_label), Create(bottom_label))

        for elem, label in zip(elements, element_labels):
            self.play(Create(elem), Write(label))
        
        self.wait(1)

        # Voiceover narration
        self.create_voiceover("In this animation, we will illustrate a Stack data structure. The Stack has a Top and Bottom, and we will perform push and pop operations.")
        self.add_sound("stack_intro.mp3")

        self.push_element(stack, 6)
        self.pop_element(stack)

        self.wait(2)

        self.push_element(stack, 7)
        self.pop_element(stack)

        self.wait(2)

        self.play(FadeOut(stack))

    def push_element(self, stack, new_element_index):
        new_element = Rectangle(width=1.5, height=0.7, color=YELLOW).shift(UP * 6 + RIGHT * 2)
        label = Text(f"Element {new_element_index}", font_size=20).move_to(new_element.get_center())
        
        self.play(new_element.animate.shift(UP * 5).scale(0.9), label.animate.move_to(new_element.get_center()))
        self.play(FadeIn(new_element), Write(label))
        self.wait(1)

        target_position = len(stack) * 0.7
        self.play(new_element.animate.move_to(UP * target_position + RIGHT * 2))
        stack.add(new_element)
        self.wait(1)

    def pop_element(self, stack):
        if len(stack) <= 1:
            return

        element_to_pop = stack[-1]
        stack.remove(element_to_pop)

        self.play(FadeOut(element_to_pop))
        self.wait(1)

        self.create_voiceover("An element has been popped off the Stack.")
        self.add_sound("stack_pop.mp3")

    def create_voiceover(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save("stack_intro.mp3")
        if os.path.exists("stack_intro.mp3"):
            print("Audio file created.")

        tts = gTTS(text="An element has been popped off the Stack.", lang='en')
        tts.save("stack_pop.mp3")
        if os.path.exists("stack_pop.mp3"):
            print("Audio file created.")