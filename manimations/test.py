from manim import *

class CellStructureTable(Scene):
    def construct(self):
        # Create the title
        title = Text("Cell Structure Components", color=BLUE).scale(0.8)
        # Position the title at the top of the scene
        title.to_edge(UP)

        # Create the table
        table_data = [
            ["Component", "Description"],
            ["Nucleus", "Control center of the cell"],
            ["Cytoplasm", "Gel-like substance"],
            ["Cell Membrane", "Protective barrier"],
            ["Mitochondria", "Powerhouse of the cell"],
        ]
        
        # Create a Table
        cell_table = Table(
            table_data,
            include_outer_lines=True
        )

        # Highlight the Nucleus and Mitochondria cells
        cell_table[1][0].set_fill(YELLOW)  # Nucleus
        cell_table[4][0].set_fill(GREEN)   # Mitochondria

        # Animate writing the title
        self.play(Write(title))
        self.wait(1)

        # Animate table creation
        self.play(Create(cell_table))
        self.wait(2)

        # End of scene
        self.play(FadeOut(title), FadeOut(cell_table))