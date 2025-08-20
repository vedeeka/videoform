from manim import *
from gtts import gTTS
import os

# Step 1: Create narration audio
text = """
What is a Queue?
A Queue is a linear data structure that follows the FIFO principle.
FIFO means First In, First Out.
Just like people standing in a line, the person who comes first gets served first.
"""
tts = gTTS(text=text, lang='en')
tts.save("queue_explanation.mp3")

# Step 2: Create animation
class QueueExplanation(Scene):
    def construct(self):
        # Title
        title = Text("Queue in Data Structure", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Show queue elements (rectangles)
        boxes = VGroup(*[Square(side_length=1).set_fill(BLUE, opacity=0.5) for _ in range(5)])
        boxes.arrange(RIGHT, buff=0.2).shift(DOWN)
        
        labels = VGroup(*[Text(str(i+1), font_size=36) for i in range(5)])
        for box, label in zip(boxes, labels):
            label.move_to(box.get_center())

        queue = VGroup(boxes, labels)
        
        self.play(Create(boxes), Write(labels))
        self.wait(1)

        # Play audio narration
        self.add_sound("queue_explanation.mp3")

        # Animate enqueue (adding element)
        new_box = Square(side_length=1).set_fill(GREEN, opacity=0.5)
        new_label = Text("6", font_size=36).move_to(new_box.get_center())
        new_item = VGroup(new_box, new_label).next_to(queue, RIGHT, buff=0.4)

        self.play(FadeIn(new_item))
        self.wait(1)

        # Animate dequeue (removing first element)
        self.play(FadeOut(queue[0][0][0]), FadeOut(queue[1][0]))  # first box and label
        self.wait(2)
