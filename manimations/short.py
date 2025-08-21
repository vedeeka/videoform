from manim import *
from gtts import gTTS
from pydub import AudioSegment
import os

# Configure for vertical video (9:16 aspect ratio)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.verbosity = "WARNING"
config.background_color = "#0D0D12"

# Optimized color palette for mobile viewing
PALETTE = {
    "background": "#0D0D12",
    "element_blue": "#00D4FF",
    "element_green": "#00FF88",
    "element_pink": "#FF6B9D",
    "element_purple": "#A78BFA",
    "element_orange": "#FFAB40",
    "stack_fill": "#1A1A2E",
    "stack_stroke": "#FFFFFF",
    "pointer": "#FFD700",
    "text": "#FFFFFF",
    "success": "#00FF88",
    "error": "#FF4757",
    "code": "#E6E6FA",
    "accent": "#FF6B9D"
}

class VerticalStackReel(Scene):
    """
    Vertical stack animation optimized for mobile reels.
    Features:
    - 9:16 aspect ratio
    - Slower paced, clearer audio
    - Larger text and elements for mobile viewing
    - More detailed, beginner-friendly narration
    """
    def construct(self):
        # Narration data with durations that will now be precisely matched by the animation.
        narration_data = [
            ("Let's learn about the stack data structure.", 3.5), #0
            ("Stacks are everywhere in computer science.", 3.0), #1
            ("Think of a stack like a pile of books.", 3.6), #2
            ("You add to the top, and remove from the top.", 4.2), #3
            ("This is called Last In, First Out, or LIFO.", 4.7), #4
            ("Remember: the last element you add, is the first one you take out.", 5.2), #5
            ("You can push elements onto the stack.", 2.5), #6
            ("Push adds an item on top. Like adding a book to a pile.", 4.0), #7
            ("The top pointer shows the most recent item.", 4.3), #8
            ("Let's push more items to the stack.", 2.5), #9
            ("Pushing elements", 1.8),
            ("Pushed: Ten.", 1.8), #10
            ("Pushed: Twenty.", 1.8), #11
            ("Pushed: Thirty.", 1.8), #12
            ("Pushed: Forty.", 1.8), #12
            ("Pushed: Fifty. The stack is full!", 3.0), #13
            ("Trying to push now gives a Stack Overflow error.", 5.0), #14
            ("To remove, we pop from the top.", 3.0), #15
            ("Pop takes out the last item you added.", 4.0), #16
            ("This is LIFO in action.", 3.3), #17
            ("If the stack is empty and you pop, that's Stack Underflow.", 5.7), #18
            ("Stacks are used for undo actions, backtracking, and more!", 4.8), #19
            ("Try building a stack yourself.", 2.5), #20
            
        ]

        audio_file = "vertical_stack_reel_synced.wav"
        self.generate_synchronized_audio(narration_data, audio_file)
        self.add_sound(audio_file)
        self.animate_vertical_stack(narration_data)

    def generate_synchronized_audio(self, narration_data, output_file):
        """
        Generates a single audio file where each narration segment is padded
        with silence to match its specified duration precisely.
        """
        if os.path.exists(output_file):
            print("✅ Audio file already exists. Skipping generation.")
            return

        print("🎵 Generating precisely timed narration audio...")
        # Start with a small lead-in silence
        combined_audio = AudioSegment.silent(duration=500) 
        
        for i, (text, duration) in enumerate(narration_data):
            tts = gTTS(text=text, lang='en', slow=False) # Use normal speed for predictability
            temp_mp3 = f"temp_reel_synced_{i}.mp3"
            tts.save(temp_mp3)
            
            segment = AudioSegment.from_mp3(temp_mp3)
            
            # Calculate the silence needed to meet the target duration
            target_duration_ms = duration * 1000
            silence_duration = max(0, target_duration_ms - len(segment))
            
            silence = AudioSegment.silent(duration=silence_duration)
            combined_audio += segment + silence
            
            os.remove(temp_mp3)
            
        combined_audio.export(output_file, format="wav")
        print("✅ Precisely timed narration ready!")

    def animate_vertical_stack(self, narration_data):
        """Main vertical animation sequence synchronized with narration data."""
        
        # === INTRO WITH STYLE ===
        intro_bg = Rectangle(
            width=config.frame_width, height=config.frame_height,
            fill_color="#FF6B9D", fill_opacity=0.1, stroke_width=0
        )
        
        title = Text("STACK", font_size=80, color=PALETTE["text"], weight=BOLD)
        subtitle = Text("Last In, First Out", font_size=40, color=PALETTE["accent"])
        
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5).move_to(UP * 5)
        
        self.add(intro_bg)
        
        # Narration 0 (3.5s)
        intro_anim_time = 1.8
        self.play(
            AnimationGroup(
                Write(title, run_time=1.0),
                FadeIn(subtitle, shift=UP, run_time=0.8),
                lag_ratio=0.3
            ),
            run_time=intro_anim_time
        )
        self.wait(narration_data[0][1] - intro_anim_time)
        
        # Narration 1 (3.0s)
        title_move_time = 1.2
        self.play(title_group.animate.scale(0.6).to_edge(UP, buff=0.5), run_time=title_move_time)
        self.wait(narration_data[1][1] - title_move_time)

        # === SETUP VERTICAL STACK & EXPLAIN CONCEPT ===
        self.setup_vertical_stack()
        self.setup_mobile_code_display()
        
        # Narration 2 (3.6s)
        setup_anim_time = 1.5
        self.play(
            AnimationGroup(
                DrawBorderThenFill(self.stack_container),
                Create(self.stack_divisions),
                FadeIn(self.top_pointer_group, shift=LEFT),
                Write(self.code_display),
                lag_ratio=0.2,
            ),
            run_time=setup_anim_time
        )
        self.wait(narration_data[2][1] - setup_anim_time)

        # Narration 3, 4, 5 (LIFO Explanation)
        self.wait(narration_data[3][1])
        self.wait(narration_data[4][1])
        self.wait(narration_data[5][1])
        
        # === PUSH OPERATIONS WITH FLAIR ===
        colors = [PALETTE["element_blue"], PALETTE["element_green"], 
                 PALETTE["element_pink"], PALETTE["element_purple"], PALETTE["element_orange"]]
        values = ["10", "20", "30", "40", "50"]
        
        # Narration 6, 7 (Push Explanation)
        self.wait(narration_data[6][1])
        self.wait(narration_data[7][1])
        
        # Narration 10: "Pushed: Ten" (1.8s)
        self.push_with_effect(values[0], colors[0], duration=narration_data[10][1])
        
        # Narration 8: "The top pointer..." (4.3s)
        highlight_time = 1.5 # From highlight_pointer method
        self.highlight_pointer()
        self.wait(narration_data[8][1] - highlight_time)
        
        # Narration 9: "Let's push more..." (2.5s)
        self.wait(narration_data[9][1])
        
        # Push remaining elements, matching narration timing
        self.push_with_effect(values[1], colors[1], duration=narration_data[11][1]) # Narration 11
        self.push_with_effect(values[2], colors[2], duration=narration_data[12][1]) # Narration 12
        self.push_with_effect(values[3], colors[3], duration=narration_data[13][1]) # Narration 13 (Using "50")
        self.push_with_effect(values[4], colors[4], duration=narration_data[14][1])
        # === STACK OVERFLOW ===
        # Narration 14 (5.0s)
        self.demonstrate_overflow("60", PALETTE["error"], duration=narration_data[15][1])
        
        # === POP OPERATIONS ===
        # Narration 15 (3.0s)
        self.wait(narration_data[16][1])
        
        # Narration 16 (4.0s)
        self.pop_with_effect(duration=narration_data[17][1])
        

        self.pop_with_effect(duration=1.0)
        self.pop_with_effect(duration=1.0)
        
        self.pop_with_effect(duration=1.0)
        self.pop_with_effect(duration=1.0)
        
        # === STACK UNDERFLOW ===
        # Narration 18 (5.7s)
        self.demonstrate_underflow(duration=narration_data[19][1])
        

   
        self.wait(narration_data[21][1])
        self.create_finale(duration=narration_data[22][1])
        
        # Final pause to let the last narration line finish
        self.wait(2.0)

    def push_with_effect(self, value, color, duration=1.5):
        """Pushes element with mobile-optimized effects over a set duration."""
        # Calculate total animation time for this function
        anim_time = 0.8 + 0.3 + 0.2
        
        slot_index = len(self.stack_elements)
        if slot_index >= 5: return
        
        stack_bottom = self.stack_container.get_bottom()[1]
        element_y = stack_bottom + (slot_index + 0.5) * (8 / 5)
        
        element_rect = RoundedRectangle(width=3.5, height=1.4, corner_radius=0.3, fill_color=color, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        element_text = Text(str(value), font_size=48, color=BLACK, weight=BOLD)
        element = VGroup(element_rect, element_text).move_to([0, config.frame_height/2 + 2, 0])
        
        self.play(
            AnimationGroup(element.animate.move_to([0, element_y, 0]), self.update_code_display(f'push({value})')),
            run_time=0.8
        )
        self.play(element.animate.scale(1.1).set_opacity(1), Flash(element, color=color, line_length=0.5), run_time=0.3)
        self.play(element.animate.scale(1), run_time=0.2)
        
        self.stack_elements.add(element)
        self.update_pointer_position()
        
        # Wait for the remaining duration of the narration segment
        wait_duration = duration - anim_time
        if wait_duration > 0:
            self.wait(wait_duration)

    def pop_with_effect(self, duration=1.5):
        """Pops element with visual effects over a set duration."""
        anim_time = 0.6 + 0.8
        if not self.stack_elements: return
            
        top_element = self.stack_elements[-1]
        
        self.play(
            AnimationGroup(self.update_code_display('pop()'), Indicate(top_element, scale_factor=1.2, color=PALETTE["accent"])),
            run_time=0.6
        )
        self.play(
            AnimationGroup(top_element.animate.shift(UP * 3).fade(1), top_element.animate.scale(0.5)),
            run_time=0.8
        )
        
        self.stack_elements.remove(top_element)
        self.remove(top_element)
        self.update_pointer_position()

        wait_duration = duration - anim_time
        if wait_duration > 0:
            self.wait(wait_duration)

    def demonstrate_overflow(self, value, color, duration=5.0):
        """Shows stack overflow with dramatic effect over a set duration."""
        anim_time = 0.8 + 1.5 + 0.8
        
        element_rect = RoundedRectangle(width=3.5, height=1.4, corner_radius=0.3, fill_color=color, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        element_text = Text(str(value), font_size=48, color=WHITE, weight=BOLD)
        element = VGroup(element_rect, element_text).move_to([0, config.frame_height/2 + 2, 0])
        
        self.play(
            AnimationGroup(element.animate.move_to(self.stack_container.get_top() + UP * 0.5), self.update_code_display(f'push({value})')),
            run_time=0.8
        )
        
        overflow_text = Text("OVERFLOW!", font_size=56, color=PALETTE["error"], weight=BOLD).move_to(UP * 3)
        self.play(
            AnimationGroup(
                Write(overflow_text),
                element.animate.set_color(PALETTE["error"]),
                Flash(self.stack_container, color=PALETTE["error"], line_length=0.8),
                Wiggle(self.stack_container, scale_value=1.1)
            ),
            run_time=1.5
        )
        self.play(
            AnimationGroup(FadeOut(element, shift=DOWN), FadeOut(overflow_text, shift=UP)),
            run_time=0.8
        )
        
        wait_duration = duration - anim_time
        if wait_duration > 0:
            self.wait(wait_duration)

    def demonstrate_underflow(self, duration=5.7):
        """Shows stack underflow over a set duration."""
        anim_time = 0.5 + 1.5 + 0.8
        
        self.play(self.update_code_display('pop()'), run_time=0.5)
        
        underflow_text = Text("UNDERFLOW!", font_size=56, color=PALETTE["error"], weight=BOLD).move_to(self.stack_container.get_center())
        
        self.play(
            AnimationGroup(
                Write(underflow_text),
                Flash(self.stack_container, color=PALETTE["error"], line_length=1.0),
                self.stack_container.animate.set_stroke_color(PALETTE["error"])
            ),
            run_time=1.5
        )
        self.play(FadeOut(underflow_text), run_time=0.8)

        wait_duration = duration - anim_time
        if wait_duration > 0:
            self.wait(wait_duration)

    def create_finale(self, duration=3.0):
        """Creates an engaging finale for the reel."""
        anim_time = 1.0 # Only accounting for the initial fade out
        
        self.play(
            FadeOut(
                self.stack_container, self.stack_divisions, 
                self.top_pointer_group, self.code_display,
                *self.stack_elements
            ),
            run_time=anim_time
        )
        
        wait_duration = duration - anim_time
        if wait_duration > 0:
            self.wait(wait_duration) # This wait matches the final narration line.
        
        # The rest of the finale animation plays out visually after the narration
        finale_title = Text("STACK MASTERED!", font_size=64, color=PALETTE["success"], weight=BOLD)
        finale_subtitle = Text("LIFO: Last In, First Out", font_size=36, color=PALETTE["text"])
        
        checkmarks = VGroup(*[Text("✓", font_size=40, color=PALETTE["success"]) for _ in range(3)])
        operations = VGroup(
            Text("Push Operations", font_size=28, color=PALETTE["text"]),
            Text("Pop Operations", font_size=28, color=PALETTE["text"]),
            Text("Error Handling", font_size=28, color=PALETTE["text"])
        )
        
        checklist = VGroup()
        for check, op in zip(checkmarks, operations):
            checklist.add(VGroup(check, op).arrange(RIGHT, buff=0.5))
        checklist.arrange(DOWN, buff=0.5)
        
        finale_group = VGroup(finale_title, finale_subtitle, checklist).arrange(DOWN, buff=1)
        
        self.play(
            AnimationGroup(Write(finale_title), FadeIn(finale_subtitle, shift=UP), lag_ratio=0.3),
            run_time=1.5
        )
        for item in checklist:
            self.play(FadeIn(item, shift=LEFT), run_time=0.4)
            
        self.play(
            AnimationGroup(Flash(finale_title, color=PALETTE["success"], line_length=1.5), finale_group.animate.scale(1.1)),
            run_time=1.0
        )
        
    # --- Helper methods (Unchanged) ---
    def setup_vertical_stack(self):
        """Creates vertical stack optimized for mobile viewing."""
        stack_height = 8
        stack_width = 4
        
        self.stack_container = RoundedRectangle(
            width=stack_width, height=stack_height,
            corner_radius=0.3,
            stroke_color=PALETTE["stack_stroke"],
            stroke_width=4,
            fill_color=PALETTE["stack_fill"],
            fill_opacity=0.8
        ).move_to(DOWN * 1)
        
        divisions = VGroup()
        for i in range(4):
            y_pos = self.stack_container.get_bottom()[1] + (i + 1) * (stack_height / 5)
            line = Line(
                start=self.stack_container.get_left() + RIGHT * 0.1,
                end=self.stack_container.get_right() + LEFT * 0.1,
                color=PALETTE["stack_stroke"],
                stroke_width=2,
                stroke_opacity=0.3
            ).move_to([0, y_pos, 0])
            divisions.add(line)
        
        self.stack_divisions = divisions
        self.stack_elements = VGroup()
        
        pointer_arrow = Arrow(start=ORIGIN, end=LEFT * 1.5, color=PALETTE["pointer"], stroke_width=8, max_tip_length_to_length_ratio=0.3)
        pointer_label = Text("TOP", font_size=32, color=PALETTE["pointer"], weight=BOLD)
        self.top_pointer_group = VGroup(pointer_arrow, pointer_label).arrange(RIGHT, buff=0.3)
        self.update_pointer_position(animate=False)

    def setup_mobile_code_display(self):
        """Creates mobile-friendly code display."""
        code_bg = RoundedRectangle(width=6, height=1.2, corner_radius=0.4, fill_color="#2D2D44", fill_opacity=0.9, stroke_color=PALETTE["accent"], stroke_width=3)
        code_text = Text("stack = Stack()", font="Courier", font_size=28, color=PALETTE["code"])
        self.code_display = VGroup(code_bg, code_text).to_edge(DOWN, buff=1)

    def update_code_display(self, text):
        """Updates code display with animation."""
        new_text = Text(text, font="Courier", font_size=28, color=PALETTE["code"])
        new_text.move_to(self.code_display[1])
        return Transform(self.code_display[1], new_text)

    def update_pointer_position(self, animate=True):
        """Updates TOP pointer position."""
        if not self.stack_elements:
            target_y = self.stack_container.get_bottom()[1] + 0.8
        else:
            target_y = self.stack_elements[-1].get_center()[1]
        
        new_pos = [self.stack_container.get_right()[0] + 1.2, target_y, 0]
        
        if animate:
            self.play(self.top_pointer_group.animate.move_to(new_pos), run_time=0.4)
        else:
            self.top_pointer_group.move_to(new_pos)

    def highlight_pointer(self):
        """Highlights the TOP pointer."""
        self.play(
            AnimationGroup(
                Flash(self.top_pointer_group, color=PALETTE["pointer"], line_length=1.0),
                self.top_pointer_group.animate.scale(1.2)
            ),
            run_time=1.0
        )
        self.play(self.top_pointer_group.animate.scale(1), run_time=0.5)