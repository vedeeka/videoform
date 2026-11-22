
from manim import *
import requests
from pathlib import Path

# Run:
# manim -pqh stack_animation.py StackAnimation


class StackAnimation(Scene):

    def make_item(self, number, color=BLUE_D):
        box = RoundedRectangle(
            width=3.4,
            height=0.58,
            corner_radius=0.09,
            stroke_color=WHITE,
            stroke_width=1.5,
            fill_color=color,
            fill_opacity=1
        )

        label = Text(
            f"Item {number}",
            font_size=25,
            color=WHITE,
            weight=BOLD
        )

        label.move_to(box.get_center())

        return VGroup(box, label)

    def construct(self):

        # --------------------------------------------------
        # BACKGROUND
        # --------------------------------------------------

        self.camera.background_color = "#101827"

        # Optional voice-over
        audio_url = (
            "https://murf.ai/user-upload/one-day-temp/"
            "6f560957-b7f4-4d0f-b149-eea0687d60ff.wav"
        )

        audio_file = Path("temp_audio.wav")

        try:
            response = requests.get(audio_url, timeout=20)
            response.raise_for_status()
            audio_file.write_bytes(response.content)
            self.add_sound(str(audio_file))
        except requests.RequestException as error:
            print(f"Audio unavailable: {error}")

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = Text(
            "STACK DATA STRUCTURE",
            font_size=38,
            weight=BOLD,
            color=WHITE
        ).to_edge(UP, buff=0.35)

        subtitle = Text(
            "LIFO — Last In, First Out",
            font_size=23,
            color="#60A5FA"
        ).next_to(title, DOWN, buff=0.12)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.8)

        # --------------------------------------------------
        # STACK INTRODUCTION
        # --------------------------------------------------

        stack_title = Text(
            "STACK",
            font_size=26,
            color="#93C5FD",
            weight=BOLD
        ).move_to(LEFT * 3.2 + UP * 2.1)

        self.play(FadeIn(stack_title))

        # Create initial stack
        stack_elements = []

        base_y = -2.0
        spacing = 0.66

        for i in range(5):
            item = self.make_item(i + 1)

            item.move_to(
                LEFT * 3.2 + UP * (base_y + i * spacing)
            )

            stack_elements.append(item)

        self.play(
            LaggedStart(
                *[FadeIn(item, shift=UP * 0.2)
                  for item in stack_elements],
                lag_ratio=0.18
            ),
            run_time=2
        )

        # --------------------------------------------------
        # TOP POINTER
        # --------------------------------------------------

        top_y = base_y + 4 * spacing

        top_label = Text(
            "TOP",
            font_size=24,
            color=YELLOW,
            weight=BOLD
        ).move_to(RIGHT * 0.2 + UP * top_y)

        top_arrow = Arrow(
            start=RIGHT * 1.2 + UP * top_y,
            end=RIGHT * 0.55 + UP * top_y,
            color=YELLOW,
            buff=0,
            stroke_width=5
        )

        pointer = VGroup(top_label, top_arrow)

        self.play(FadeIn(pointer))
        self.wait(1)

        # --------------------------------------------------
        # LIFO EXPLANATION
        # --------------------------------------------------

        explanation = VGroup(
            Text("How does a Stack work?", font_size=25,
                 color=WHITE, weight=BOLD),
            Text("The last inserted element", font_size=21,
                 color=GRAY_B),
            Text("is removed first.", font_size=21,
                 color=YELLOW, weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)

        explanation.move_to(RIGHT * 3.1 + UP * 0.8)

        self.play(FadeIn(explanation, shift=LEFT * 0.3))
        self.wait(2)

        self.play(FadeOut(explanation))

        # --------------------------------------------------
        # PUSH OPERATION
        # --------------------------------------------------

        push_heading = Text(
            "PUSH OPERATION",
            font_size=29,
            color="#34D399",
            weight=BOLD
        ).move_to(RIGHT * 3.1 + UP * 1.6)

        push_description = Text(
            "Insert an element at TOP",
            font_size=21,
            color=WHITE
        ).next_to(push_heading, DOWN, buff=0.3)

        self.play(
            FadeIn(push_heading),
            FadeIn(push_description)
        )

        self.play(
            Indicate(stack_elements[-1], color=YELLOW),
            run_time=0.9
        )

        # New element enters above the existing stack
        new_item = self.make_item("NEW", PURPLE)

        new_y = base_y + 5 * spacing

        new_item.move_to(
            LEFT * 3.2 + UP * (new_y + 1.5)
        )

        self.play(
            new_item.animate.move_to(
                LEFT * 3.2 + UP * new_y
            ),
            run_time=1.2,
            rate_func=smooth
        )

        # Highlight newly inserted element
        self.play(
            new_item[0].animate.set_fill("#8B5CF6"),
            Flash(new_item, color=YELLOW)
        )

        stack_elements.append(new_item)

        # Move TOP pointer
        new_top_y = new_y

        self.play(
            pointer.animate.move_to(
                RIGHT * 0.85 + UP * new_top_y
            ),
            run_time=0.8
        )

        pushed_text = Text(
            "NEW item pushed successfully!",
            font_size=23,
            color="#34D399",
            weight=BOLD
        ).move_to(RIGHT * 3.1 + DOWN * 0.2)

        self.play(FadeIn(pushed_text, shift=UP * 0.2))
        self.wait(1.5)

        self.play(
            FadeOut(pushed_text),
            FadeOut(push_heading),
            FadeOut(push_description)
        )

        # --------------------------------------------------
        # POP OPERATION
        # --------------------------------------------------

        pop_heading = Text(
            "POP OPERATION",
            font_size=29,
            color="#F87171",
            weight=BOLD
        ).move_to(RIGHT * 3.1 + UP * 1.6)

        pop_description = Text(
            "Remove the element at TOP",
            font_size=21,
            color=WHITE
        ).next_to(pop_heading, DOWN, buff=0.3)

        self.play(
            FadeIn(pop_heading),
            FadeIn(pop_description)
        )

        # Highlight the current top element
        self.play(
            Indicate(stack_elements[-1], color=YELLOW),
            run_time=1
        )

        # Remove top item
        self.play(
            stack_elements[-1].animate.shift(RIGHT * 3),
            FadeOut(stack_elements[-1]),
            run_time=1.2
        )

        stack_elements.pop()

        # Update TOP pointer to previous element
        previous_top_y = base_y + 4 * spacing

        self.play(
            pointer.animate.move_to(
                RIGHT * 0.85 + UP * previous_top_y
            ),
            run_time=0.8
        )

        popped_text = Text(
            "NEW item popped successfully!",
            font_size=23,
            color="#F87171",
            weight=BOLD
        ).move_to(RIGHT * 3.1 + DOWN * 0.2)

        self.play(FadeIn(popped_text, shift=UP * 0.2))
        self.wait(1.5)

        self.play(
            FadeOut(popped_text),
            FadeOut(pop_heading),
            FadeOut(pop_description)
        )

        # --------------------------------------------------
        # LIFO DEMONSTRATION
        # --------------------------------------------------

        lifo_title = Text(
            "REMEMBER LIFO!",
            font_size=32,
            color=YELLOW,
            weight=BOLD
        ).move_to(RIGHT * 3.1 + UP * 1.3)

        lifo_line1 = Text(
            "Last In",
            font_size=25,
            color="#A78BFA"
        ).move_to(RIGHT * 3.1 + UP * 0.3)

        lifo_arrow = Arrow(
            UP * 0.05,
            DOWN * 0.35,
            color=YELLOW,
            stroke_width=4
        ).move_to(RIGHT * 3.1 + DOWN * 0.25)

        lifo_line2 = Text(
            "First Out",
            font_size=25,
            color="#F87171"
        ).move_to(RIGHT * 3.1 + DOWN * 0.85)

        self.play(
            FadeIn(lifo_title),
            Write(lifo_line1),
            GrowArrow(lifo_arrow),
            Write(lifo_line2)
        )

        self.wait(2)

        # --------------------------------------------------
        # COMPLEXITY
        # --------------------------------------------------

        self.play(
            FadeOut(lifo_title),
            FadeOut(lifo_line1),
            FadeOut(lifo_arrow),
            FadeOut(lifo_line2)
        )

        complexity = VGroup(
            Text("TIME COMPLEXITY", font_size=23,
                 color=WHITE, weight=BOLD),
            Text("PUSH  :  O(1)", font_size=25,
                 color="#34D399"),
            Text("POP   :  O(1)", font_size=25,
                 color="#F87171"),
            Text("PEEK  :  O(1)", font_size=25,
                 color="#60A5FA")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        complexity.move_to(RIGHT * 3.1)

        self.play(FadeIn(complexity, shift=UP * 0.2))
        self.wait(2)

        # --------------------------------------------------
        # FINAL SCENE
        # --------------------------------------------------

        self.play(
            FadeOut(complexity),
            FadeOut(pointer),
            *[Indicate(item, color=YELLOW)
              for item in stack_elements],
            run_time=1.5
        )

        final_text = Text(
            "STACK OPERATIONS COMPLETE!",
            font_size=34,
            weight=BOLD,
            color="#34D399"
        ).move_to(DOWN * 3.1)

        self.play(Write(final_text))
        self.wait(2)

        self.play(
            FadeOut(final_text),
            *[FadeOut(item) for item in stack_elements],
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(stack_title)
        )

        self.wait(1)
