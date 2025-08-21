from manim import *
from gtts import gTTS
from pydub import AudioSegment
import os

# Disable noisy logs and set a background color
config.verbosity = "WARNING"
config.background_color = "#1E1E2E"

# A more professional color palette
PALETTE = {
    "background": "#1E1E2E",
    "element_blue": "#89B4FA",
    "element_green": "#A6E3A1",
    "element_pink": "#F5C2E7",
    "stack_fill": "#313244",
    "stack_stroke": "#CDD6F4",
    "pointer": "#FAB387",
    "text": "#CDD6F4",
    "success": "#A6E3A1",
    "error": "#F38BA8",
    "code": "#BAC2DE"
}

class ProfessionalStackAnimation(Scene):
    """
    A professional Manim animation of the Stack data structure.
    This version includes:
    - Visual demonstrations of Stack Overflow and Underflow.
    - On-screen pseudocode that updates with operations.
    - A refined color palette and smoother animations.
    - Synchronized audio narration explaining all concepts.
    """
    def construct(self):
        # Updated narration data to include overflow/underflow explanations.
        narration_data = [
            ("Stack?", 2.5),
            ("A stack is a linear data structure that follows the rule: Last In, First Out, or LIFO.", 5.0),
            ("This means the last element added is the first one to be removed.", 4.0),
            ("Let's build our stack. We'll add elements using the 'push' operation.", 4.0),
            ("Push adds a new element to the top of the stack.", 3.5),
            ("The 'TOP' pointer always tracks the most recently added item.", 4.0),
            ("Now let's push a few more elements onto the stack.", 3.5),
            ("Watch what happens when we try to push onto a full stack.", 3.5),
            ("This is a 'Stack Overflow'. The operation fails because the stack has no more space.", 5.0),
            ("Next, we'll remove elements using the 'pop' operation.", 3.5),
            ("Pop removes the top element, perfectly demonstrating the Last-In, First-Out principle.", 5.5),
            ("Let's pop all the elements and see what happens when the stack is empty.", 4.5),
            ("Trying to pop from an empty stack causes a 'Stack Underflow'.", 4.5),
            ("And that's a complete look at the stack data structure.", 3.0)
        ]

        audio_file = "professional_stack_narration.wav"
        self.generate_synchronized_audio(narration_data, audio_file)
        self.add_sound(audio_file)
        self.animate_stack_explanation()

    def generate_synchronized_audio(self, narration_data, output_file):
        """Generates a synchronized WAV audio file from text and duration pairs."""
        if os.path.exists(output_file):
            print("✅ Audio file already exists. Skipping generation.")
            return

        print("🎵 Generating synchronized narration audio...")
        combined_audio = AudioSegment.silent(duration=200)
        for i, (text, duration) in enumerate(narration_data):
            tts = gTTS(text=text, lang='en')
            temp_mp3 = f"temp_audio_{i}.mp3"
            tts.save(temp_mp3)
            segment = AudioSegment.from_mp3(temp_mp3)
            silence_needed = max(0, (duration * 1000) - len(segment))
            combined_audio += segment + AudioSegment.silent(duration=silence_needed)
            os.remove(temp_mp3)
        combined_audio.export(output_file, format="wav")
        print("✅ Synchronized narration audio is ready!")

    def animate_stack_explanation(self):
        """The main animation sequence."""
        # --- Initial Setup ---
        title = Text("Stack: Last-In, First-Out (LIFO)", font_size=48, color=PALETTE["text"]).to_edge(UP)
        self.play(Write(title), run_time=2.0)
        self.wait(5.5) # Wait for narrations 1 & 2

        # --- Create Stack and Code Display ---
        self.setup_stack_visuals()
        self.setup_code_display()
        self.play(
            AnimationGroup(
                Create(self.stack_visual),
                FadeIn(self.top_pointer_group),
                Write(self.code_display[0]), # FIX: Access by index
                Write(self.code_display[1]), # FIX: Access by index
                lag_ratio=0.2
            )
        )
        self.wait(1.0) # Wait for narration 3

        # --- Push Operations ---
        self.wait(4.0) # Wait for narration 4
        self.push_element("10", PALETTE["element_blue"])
        self.wait(3.5) # Wait for narration 5
        self.play(Flash(self.top_pointer_group, color=PALETTE["pointer"], flash_radius=1.0, run_time=1.5))
        self.wait(2.5) # Wait for narration 6
        self.push_element("20", PALETTE["element_green"])
        self.push_element("30", PALETTE["element_pink"])
        self.wait(3.5) # Wait for narration 7
        
        # --- Stack Overflow ---
        self.push_element("40", PALETTE["element_blue"])
        self.push_element("50", PALETTE["element_green"])
        self.wait(3.5) # Wait for narration 8
        self.handle_overflow("60", PALETTE["element_pink"])
        self.wait(5.0) # Wait for narration 9

        # --- Pop Operations ---
        self.wait(3.5) # Wait for narration 10
        self.pop_element()
        self.wait(5.5) # Wait for narration 11
        self.pop_element()
        self.pop_element()
        self.pop_element()
        self.pop_element()
        self.wait(4.5) # Wait for narration 12

        # --- Stack Underflow ---
        self.handle_underflow()
        self.wait(4.5) # Wait for narration 13

        # --- Final Scene ---
        self.play(FadeOut(self.stack_visual, self.top_pointer_group, self.code_display, *self.stack_elements))
        self.play(title.animate.scale(1.2).set_color(PALETTE["success"]))
        self.wait(3.0) # Wait for narration 14

    def setup_stack_visuals(self):
        """Creates the stack container and TOP pointer."""
        self.stack_boxes = VGroup(*[
            Rectangle(width=2.5, height=1, stroke_width=0) for _ in range(5)
        ]).arrange(DOWN, buff=0).move_to(LEFT * 3.5)

        container = Rectangle(
            width=self.stack_boxes.width + 0.2,
            height=self.stack_boxes.height + 0.2,
            stroke_color=PALETTE["stack_stroke"],
            stroke_width=3,
            fill_color=PALETTE["stack_fill"],
            fill_opacity=1
        ).move_to(self.stack_boxes)
        self.stack_visual = VGroup(container, self.stack_boxes)

        self.stack_elements = VGroup()
        pointer = Arrow(start=RIGHT, end=LEFT, color=PALETTE["pointer"], buff=0.1)
        label = Text("TOP", font_size=24, color=PALETTE["pointer"])
        self.top_pointer_group = VGroup(pointer, label).arrange(RIGHT, buff=0.2)
        self.update_pointer(animate=False)

    def setup_code_display(self):
        """Creates the on-screen pseudocode display."""
        code_bg = RoundedRectangle(width=4, height=1.5, corner_radius=0.2,
                                   fill_color=PALETTE["stack_fill"], fill_opacity=1,
                                   stroke_color=PALETTE["stack_stroke"], stroke_width=2)
        code_text = Text("stack.create()", font="Monospace", font_size=28, color=PALETTE["code"])
        self.code_display = VGroup(code_bg, code_text).to_edge(RIGHT, buff=1.5)

    def update_code_display(self, text):
        """Animates the change in the code display text."""
        new_text = Text(text, font="Monospace", font_size=28, color=PALETTE["code"])
        new_text.move_to(self.code_display[1])
        return Transform(self.code_display[1], new_text)

    def update_pointer(self, animate=True):
        """Moves the TOP pointer to the correct position."""
        if not self.stack_elements:
            target_pos = self.stack_boxes.get_bottom() + UP * 0.5
        else:
            target_pos = self.stack_elements[-1].get_center()
        
        new_pos = target_pos + RIGHT * (self.stack_boxes.width / 2 + 0.8)
        
        if animate:
            self.play(self.top_pointer_group.animate.move_to(new_pos), run_time=0.5)
        else:
            self.top_pointer_group.move_to(new_pos)

    def push_element(self, value, color):
        """Animates pushing an element onto the stack."""
        index = len(self.stack_elements)
        target_box = self.stack_boxes[-(index + 1)]
        element = VGroup(
            RoundedRectangle(width=2.2, height=0.8, corner_radius=0.1, fill_color=color, fill_opacity=1, stroke_width=0),
            Text(str(value), font_size=36, color=BLACK)
        ).move_to(self.stack_visual.get_top() + UP * 2)

        self.play(
            AnimationGroup(
                element.animate.move_to(target_box.get_center()),
                self.update_code_display(f'stack.push({value})'),
                run_time=1.0
            )
        )
        self.stack_elements.add(element)
        self.update_pointer()

    def pop_element(self):
        """Animates popping an element from the stack."""
        top_element = self.stack_elements[-1]
        self.play(
            AnimationGroup(
                Indicate(top_element, color=PALETTE["error"], scale_factor=1.2),
                self.update_code_display('stack.pop()')
            )
        )
        self.play(top_element.animate.shift(RIGHT * 5).fade(1), run_time=1.0)
        self.stack_elements.remove(top_element)
        self.remove(top_element)
        self.update_pointer()

    def handle_overflow(self, value, color):
        """Animates a stack overflow scenario."""
        element = VGroup(
            RoundedRectangle(width=2.2, height=0.8, corner_radius=0.1, fill_color=color, fill_opacity=1, stroke_width=0),
            Text(str(value), font_size=36, color=BLACK)
        ).move_to(self.stack_visual.get_top() + UP * 2)
        
        overflow_text = Text("Stack Overflow!", font_size=36, color=PALETTE["error"])
        overflow_text.next_to(self.stack_visual, UP, buff=0.5)

        self.play(
            element.animate.move_to(self.stack_visual.get_top() + UP),
            self.update_code_display(f'stack.push({value})'),
            run_time=1.0
        )
        self.play(
            Write(overflow_text),
            element.animate.set_color(PALETTE["error"]),
            Wiggle(self.stack_visual)
        )
        self.play(FadeOut(element, shift=UP), FadeOut(overflow_text))

    def handle_underflow(self):
        """Animates a stack underflow scenario."""
        underflow_text = Text("Stack Underflow!", font_size=36, color=PALETTE["error"])
        underflow_text.move_to(self.stack_boxes.get_center())
        
        self.play(self.update_code_display('stack.pop()'))
        self.play(Write(underflow_text), Flash(self.stack_visual, color=PALETTE["error"], line_length=0.3))
        self.wait(1.0)
        self.play(FadeOut(underflow_text)) 