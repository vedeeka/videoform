from manim import *
import requests


class QueueAnimation(Scene):
    def construct(self):
        audio_url = 'https://murf.ai/user-upload/one-day-temp/6f560957-b7f4-4d0f-b149-eea0687d60ff.wav'
          audio_file = 'temp_audio.mp3'
          r = requests.get(audio_url)
          with open(audio_file, 'wb') as f:
          f.write(r.content)
          self.add_sound(audio_file)
    
        # Create queue representation
        queue_length = 8
        queue_boxes = []
        queue_labels = []
        for i in range(queue_length):
            box = Rectangle(width=1, height=1, color=BLUE, fill_opacity=1)
            box.move_to(RIGHT * (i - queue_length / 2) + UP)
            label = Text(str(i + 1)).scale(0.5).move_to(box.get_center())
            queue_boxes.append(box)
            queue_labels.append(label)
        
        queue = VGroup(*queue_boxes)
        labels = VGroup(*queue_labels)
        
        intro_label = Text("Queue Animation").scale(1.5).to_edge(UP)
        self.play(Write(intro_label))
        self.play(LaggedStart(*[DrawBorderThenFill(box) for box in queue_boxes], lag_ratio=0.1), 
                  LaggedStart(*[Write(label) for label in queue_labels], lag_ratio=0.1))
        self.wait(1)

        self.play(intro_label.animate.to_edge(UP), FadeOut(intro_label))

        # Push operations
        push_label = Text("Push Operation").scale(1).to_edge(UP)
        self.play(Write(push_label))
        
        for i in range(3):  # Push elements three times
            new_box = Rectangle(width=1, height=1, color=GREEN, fill_opacity=1).move_to(RIGHT * (queue_length / 2) + UP)
            new_label = Text("P").scale(0.5).move_to(new_box.get_center())
            self.play(FadeIn(new_box), Write(new_label))
            self.play(new_box.animate.shift(LEFT), new_label.animate.shift(LEFT))
            queue_length += 1
            queue_boxes.append(new_box)
            queue_labels.append(new_label)
            new_box.move_to(RIGHT * (queue_length / 2) + UP)
            new_label.move_to(new_box.get_center())
            self.wait(0.5)

            # Scale down the last element point
            if queue_length > 4:
                self.play(queue_boxes[-4].animate.scale(0.8).set_color(ORANGE), 
                          queue_labels[-4].animate.set_color(ORANGE))
            self.wait(0.5)

        self.play(FadeOut(push_label))
        self.wait(1)

        # Pop operations
        pop_label = Text("Pop Operation").scale(1).to_edge(UP)
        self.play(Write(pop_label))

        for _ in range(3):  # Pop elements three times
            self.play(queue_boxes[0].animate.shift(UP).scale(1.2).set_color(RED), 
                      queue_labels[0].animate.shift(UP).set_color(RED))
            self.play(FadeOut(queue_boxes[0]), FadeOut(queue_labels[0]))
            queue_boxes.pop(0)
            queue_labels.pop(0)
            queue_length -= 1
            if queue_length > 0:  # re-positioning remaining boxes
                for index, box in enumerate(queue_boxes):
                    self.play(box.animate.shift(LEFT), queue_labels[index].animate.shift(LEFT))
            self.wait(0.5)

            # Scale down the last element point if present
            if queue_length > 4:
                self.play(queue_boxes[-4].animate.scale(0.8).set_color(ORANGE), 
                          queue_labels[-4].animate.set_color(ORANGE))
            self.wait(0.5)

        self.play(FadeOut(pop_label))

        # Ending scene
        end_label = Text("End of Queue Animation").scale(1).to_edge(UP)
        self.play(Write(end_label))
        self.wait(2)

        self.play(FadeOut(end_label), FadeOut(queue), FadeOut(labels))
        self.wait(1)