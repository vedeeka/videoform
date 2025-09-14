from manim import *
import requests


class StackAnimation(Scene):
    def construct(self):
         audio_url = 'https://murf.ai/user-upload/one-day-temp/6f560957-b7f4-4d0f-b149-eea0687d60ff.wav'
         audio_file = 'temp_audio.mp3'
         r = requests.get(audio_url)
         with open(audio_file, 'wb') as f:
         f.write(r.content)
         self.add_sound(audio_file)
    
        # Define colors
        background_color = WHITE
        stack_color = BLUE
        highlight_color = YELLOW
        text_color = BLACK
        
        # Create stack elements
        stack_elements = []
        for i in range(5):
            box = Rectangle(width=3, height=1, fill_color=stack_color, fill_opacity=1).set_stroke(BLACK)
            label = Text(f"Item {i + 1}", color=text_color).move_to(box.get_center())
            group = VGroup(box, label).move_to(UP * (i * 1.5))
            stack_elements.append(group)
            self.add(group)
        
        self.wait(1)

        self.play(Indicate(stack_elements[0]), run_time=0.5)
        self.play(Indicate(stack_elements[1]), run_time=0.5)
        self.play(Indicate(stack_elements[2]), run_time=0.5)

        self.wait(1)

        # Push operation
        new_element = Rectangle(width=3, height=1, fill_color=stack_color, fill_opacity=1).set_stroke(BLACK)
        new_label = Text("New Item", color=text_color).move_to(new_element.get_center())
        new_group = VGroup(new_element, new_label).move_to(UP * (len(stack_elements) * 1.5))
        
        self.play(new_group.animate.shift(DOWN * 3), run_time=1)
        self.play(FadeIn(new_group), run_time=0.5)
        self.add(new_group)

        # Highlight new element
        self.play(new_group.animate.set_fill(highlight_color, opacity=0.8), run_time=1)
        self.play(new_group.animate.set_fill(stack_color, opacity=1), run_time=1)

        # Move old stack up
        for i in range(len(stack_elements)):
            self.play(stack_elements[i].animate.shift(UP * 1.5), run_time=0.5)

        # Wait and Push Notification
        self.wait(1)
        push_text = Text("Pushed Item", color=text_color).to_edge(UP)
        self.play(FadeIn(push_text), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(push_text), run_time=0.5)

        # Pop operation
        self.play(new_group.animate.shift(UP * 1.5), run_time=1)
        self.wait(0.5)

        # Highlight pop item
        self.play(new_group.animate.set_fill(highlight_color, opacity=0.8), run_time=1)
        self.play(new_group.animate.set_fill(stack_color, opacity=1), run_time=1)

        # Move back old stack elements
        for i in reversed(range(len(stack_elements))):
            self.play(stack_elements[i].animate.shift(DOWN * 1.5), run_time=0.5)

        # Create a Pop Notification
        pop_text = Text("Popped Item", color=text_color).to_edge(UP)
        self.play(FadeIn(pop_text), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(pop_text), run_time=0.5)

        # Reiterate Push Operation
        self.play(new_group.animate.shift(DOWN * 3), run_time=1)
        self.play(FadeIn(new_group), run_time=0.5)
        self.add(new_group)

        # Ramp up highlight cycle
        self.play(new_group.animate.set_fill(highlight_color, opacity=0.8), run_time=1)
        self.play(new_group.animate.set_fill(stack_color, opacity=1), run_time=1)

        # Queue up multiple pops
        for _ in range(4):
            self.play(new_group.animate.shift(UP * 1.5), run_time=1)
            self.play(FadeOut(new_group), run_time=1)
            if len(stack_elements) > 0:
                popped_element = stack_elements.pop()
                self.play(popped_element.animate.shift(DOWN * 1.5), run_time=1)
        
        self.wait(1)

        # Finish
        end_text = Text("Stack Operations Complete!", color=text_color).to_edge(UP)
        self.play(FadeIn(end_text), run_time=1)
        self.wait(2)
        self.play(FadeOut(end_text), run_time=1)
        
        self.wait(1)