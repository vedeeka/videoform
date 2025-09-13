from manim import *

class QueueAnimation(Scene):
    def construct(self):
        queue = VGroup()
        queue_labels = VGroup()
        max_items = 5
        item_radius = 0.5
        item_spacing = 0.5
        item_colors = [RED, GREEN, BLUE, YELLOW, ORANGE]

        for i in range(max_items):
            circle = Circle(radius=item_radius, color=item_colors[i % len(item_colors)])
            label = Text(str(i + 1), font_size=24)
            label.move_to(circle.get_center())
            circle.move_to(RIGHT * (i * (item_radius + item_spacing)))
            queue.add(circle)
            queue_labels.add(label)

        self.play(Create(queue), Write(queue_labels))
        self.wait(1)

        for i in range(3):
            self.play(queue[i].animate.scale(1.5).set_color(WHITE), queue_labels[i].animate.set_color(WHITE))
            self.wait(0.5)
            self.play(queue[i].animate.scale(1/1.5).set_color(item_colors[i % len(item_colors)]), queue_labels[i].animate.set_color(WHITE))
            self.wait(0.5)

        for i in range(max_items):
            self.play(Indicate(queue[i]))
            self.wait(0.5)

        for i in range(2):
            moving_circle = Circle(radius=item_radius, color=RED)
            moving_label = Text('PUSH', font_size=24).next_to(moving_circle, UP)
            self.play(Create(moving_circle), Write(moving_label))
            moving_circle.move_to(RIGHT * (max_items * (item_radius + item_spacing)))
            self.play(moving_circle.animate.shift(LEFT * (max_items * (item_radius + item_spacing) - item_spacing)), run_time=1)
            queue.add(moving_circle)
            queue_labels.add(moving_label)
            self.wait(0.5)

            if len(queue) > max_items:
                to_remove = queue[0]
                label_to_remove = queue_labels[0]
                self.play(FadeOut(to_remove), FadeOut(label_to_remove))
                queue.remove(to_remove)
                queue_labels.remove(label_to_remove)

            self.wait(0.5)

        self.play(queue.animate.move_to(ORIGIN), queue_labels.animate.move_to(ORIGIN), run_time=2)
        self.wait(1)

        self.play(*[FadeOut(m) for m in queue], *[FadeOut(l) for l in queue_labels])
        self.wait(1)