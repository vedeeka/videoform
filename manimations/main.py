from manim import *

# Define some constants for easy styling and configuration
CONFIG = {
    "queue_capacity": 5,
    "cell_width": 1.6,
    "element_color": BLUE_C,
    "front_color": ORANGE,
    "rear_color": YELLOW,
}

class QueueExplanationImproved(Scene):
    def construct(self):
        """
        Main construction method that orchestrates the animation sequence.
        """
        self.setup_scene()
        self.animate_enqueue()
        self.animate_peek()
        self.animate_dequeue()
        self.show_fifo_principle()
        self.end_scene()

    def setup_scene(self):
        """
        Initializes all the static and dynamic Mobjects for the scene.
        """
        # ----------------------------------------------------------------
        # 1. Title and Queue Structure
        # ----------------------------------------------------------------
        title = Text("Queue Data Structure: Properties & Operations", font_size=40).to_edge(UP)
        self.play(Write(title))

        # We will use this VGroup to hold the actual element Mobjects
        self.elements_in_queue = VGroup()

        # Build the queue visual from a VGroup for easier management
        queue_box = Rectangle(
            width=CONFIG["queue_capacity"] * CONFIG["cell_width"],
            height=1.5,
            color=BLUE_D,
        )
        partitions = VGroup(*[
            Line(
                queue_box.get_corner(DL) + RIGHT * (i * CONFIG["cell_width"]),
                queue_box.get_corner(UL) + RIGHT * (i * CONFIG["cell_width"]),
                color=BLUE_D
            ) for i in range(1, CONFIG["queue_capacity"])
        ])
        self.queue_visual = VGroup(queue_box, partitions).shift(DOWN * 0.5)

        # ----------------------------------------------------------------
        # 2. Front and Rear Pointers
        # ----------------------------------------------------------------
        self.front_pointer = self.create_pointer("Front", CONFIG["front_color"])
        self.rear_pointer = self.create_pointer("Rear", CONFIG["rear_color"])

        # We use indices to track the logical position of the pointers
        self.front_index = 0
        self.rear_index = 0

        # Position pointers at the initial spot
        initial_pos = self.get_pointer_target_position(0)
        self.front_pointer.next_to(initial_pos, UP, buff=0.1)
        self.rear_pointer.next_to(initial_pos, UP, buff=0.1)

        self.play(Create(self.queue_visual), run_time=1.5)
        self.play(FadeIn(self.front_pointer), FadeIn(self.rear_pointer))
        self.wait(0.5)

        # ----------------------------------------------------------------
        # 3. Dynamic Properties Display using ValueTracker
        # ----------------------------------------------------------------
        self.size_tracker = ValueTracker(0)
        prop_title = Text("Properties:", font_size=28, weight=BOLD)

        # Use always_redraw to make these text Mobjects update automatically
        size_text = always_redraw(
            lambda: Text(f"Size: {int(self.size_tracker.get_value())}", font_size=24)
        )
        empty_text = always_redraw(
            lambda: Text(
                f"isEmpty(): {self.size_tracker.get_value() == 0}", font_size=24
            ).set_color(GREEN if self.size_tracker.get_value() == 0 else WHITE)
        )
        full_text = always_redraw(
            lambda: Text(
                f"isFull(): {self.size_tracker.get_value() == CONFIG['queue_capacity']}",
                font_size=24,
            ).set_color(GREEN if self.size_tracker.get_value() == CONFIG['queue_capacity'] else RED)
        )

        self.prop_display = VGroup(prop_title, size_text, empty_text, full_text)
        self.prop_display.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.prop_display.to_edge(LEFT, buff=0.8).shift(UP * 1)

        self.play(LaggedStart(*[FadeIn(prop, shift=UP) for prop in self.prop_display], lag_ratio=0.25))
        self.wait(1)

    def animate_enqueue(self):
        """
        Animates the Enqueue operation, adding elements to the queue.
        """
        op_title = self.create_op_title("Operation: Enqueue(value)", YELLOW)
        self.play(Write(op_title))
        self.wait(1)

        values = ["10", "22", "5", "18", "30"]
        for i, val in enumerate(values):
            elem = self.create_element(val)
            elem.move_to(RIGHT * 6 + UP * 2) # Start position off-screen
            
            self.play(FadeIn(elem, shift=LEFT * 2), run_time=0.8)

            target_pos = self.get_element_target_position(i)
            
            # Animate the rear pointer moving
            # On the first element, the rear pointer doesn't "move", it just appears with the front
            if i == 0:
                 # Rear pointer already at the start, no animation needed
                self.play(
                    elem.animate.move_to(target_pos),
                    self.size_tracker.animate.set_value(i + 1),
                )
            else:
                self.rear_index += 1
                new_rear_pos = self.get_pointer_target_position(self.rear_index)
                self.play(
                    elem.animate.move_to(target_pos),
                    self.rear_pointer.animate.next_to(new_rear_pos, UP, buff=0.1),
                    self.size_tracker.animate.set_value(i + 1),
                )
            
            self.elements_in_queue.add(elem)
            self.wait(0.3)
        
        self.play(FadeOut(op_title, shift=DOWN))
        self.wait(1.5)

    def animate_peek(self):
        """
        Animates the Peek operation, highlighting the front element.
        """
        op_title = self.create_op_title("Operation: Peek()", BLUE_A)
        self.play(Write(op_title))
        
        front_element = self.elements_in_queue[0]
        peek_result = Text(f"Returns: {front_element.submobjects[1].text}", font_size=24, color=BLUE_A, weight=BOLD)
        peek_result.next_to(self.prop_display, DOWN, aligned_edge=LEFT, buff=0.5)

        # Use the "Indicate" animation for a clean highlight effect
        self.play(Indicate(front_element, color=BLUE_A, scale_factor=1.2), run_time=1.5)
        self.play(Write(peek_result))
        self.wait(2)
        self.play(FadeOut(op_title, shift=DOWN), FadeOut(peek_result))

    def animate_dequeue(self):
        """
        Animates the Dequeue operation, removing two elements from the front.
        """
        op_title = self.create_op_title("Operation: Dequeue()", CONFIG["front_color"])
        self.play(Write(op_title))
        self.wait(1)

        # Dequeue two elements
        for _ in range(2):
            if self.size_tracker.get_value() == 0:
                break # Cannot dequeue from an empty queue

            element_to_remove = self.elements_in_queue[0]
            
            dequeue_result = Text(f"Removed: {element_to_remove.submobjects[1].text}", font_size=24, color=CONFIG["front_color"], weight=BOLD)
            dequeue_result.next_to(self.prop_display, DOWN, aligned_edge=LEFT, buff=0.5)
            self.play(Write(dequeue_result))

            self.front_index += 1
            new_front_pos = self.get_pointer_target_position(self.front_index)
            
            self.play(
                FadeOut(element_to_remove, target_position=element_to_remove.get_center() + DOWN * 2, scale=0.5),
                self.front_pointer.animate.next_to(new_front_pos, UP, buff=0.1),
                self.size_tracker.animate.set_value(self.size_tracker.get_value() - 1),
                run_time=1.5
            )
            self.elements_in_queue.remove(element_to_remove)
            self.wait(1)
            self.play(FadeOut(dequeue_result))

        self.play(FadeOut(op_title, shift=DOWN))

    def show_fifo_principle(self):
        """
        Displays the final text explaining the FIFO principle.
        """
        # Create FIFO explanation text
        fifo_title = Text("FIFO Principle", font_size=36, color=BLUE_C, weight=BOLD)
        final_text = Text("First In, First Out", font_size=30, color=BLUE_C)
        explanation = Text("The first element added is the first one removed.", font_size=24, slant=ITALIC)
        
        fifo_group = VGroup(fifo_title, final_text, explanation).arrange(DOWN, buff=0.4)
        fifo_group.to_edge(DOWN, buff=1)
        
        self.play(Write(fifo_group), run_time=2)
        
        # Highlight the first element that was enqueued (which is now gone)
        # and the next one to be dequeued.
        original_first_pos = self.get_element_target_position(0)
        ghost_rect = DashedVMobject(
            Square(side_length=1.2, color=GRAY),
            num_dashes=12
        ).move_to(original_first_pos)
        ghost_text = Text("1st In (Now Gone)", font_size=18, color=GRAY).next_to(ghost_rect, DOWN)
        
        self.play(Create(ghost_rect), Write(ghost_text))
        self.play(Indicate(self.elements_in_queue[0], color=CONFIG["front_color"]))
        self.wait(3)

    def end_scene(self):
        """
        Fades out all objects for a clean finish.
        """
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)
        self.wait(1)
        
    # ----------------------------------------------------------------
    # Helper Methods
    # ----------------------------------------------------------------
    
    def create_pointer(self, text, color):
        """Creates a styled pointer with a label."""
        arrow = Arrow(UP * 0.6, DOWN * 0.1, color=color, buff=0, stroke_width=5, tip_length=0.25)
        label = Text(text, font_size=24, color=color, weight=BOLD).next_to(arrow, UP, buff=0.1)
        return VGroup(arrow, label)

    def create_element(self, value):
        """Creates a styled element box with a value."""
        square = Square(side_length=1.2, color=CONFIG["element_color"], fill_opacity=0.7, stroke_width=3)
        text = Text(str(value), font_size=32, color=WHITE, weight=BOLD)
        return VGroup(square, text)

    def get_element_target_position(self, index):
        """Calculates the center position for an element in the queue."""
        return self.queue_visual.get_left() + RIGHT * ((CONFIG["cell_width"] / 2) + index * CONFIG["cell_width"])
    
    def get_pointer_target_position(self, index):
        """Gets the Mobject a pointer should be next_to."""
        # This returns a "point" mobject for the .next_to() method to align with
        return Dot(self.get_element_target_position(index), radius=0)

    def create_op_title(self, text, color):
        """Creates a standardized title for operations."""
        return Text(text, font_size=28, color=color, weight=BOLD).to_edge(DOWN, buff=0.5)