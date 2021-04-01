import arcade

from .menu_view import MenuView

TEXT_COLOR = arcade.csscolor.WHITE


class InstructionsView(MenuView):
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "How to Play",
            self.width // 2,
            self.height * 0.75,
            TEXT_COLOR,
            20,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press ESC to go back",
            self.width // 16,
            self.height * 7 / 8,
            arcade.color.WHITE,
        )

        intro = """As part of the biggest heist of the century, your goal is to steal a diamond.\n
        To do this, you will have to bypass many levels of security."""

        arcade.draw_text(
            intro,
            self.width // 2,
            self.height * 0.65,
            TEXT_COLOR,
            align="center",
            anchor_x="center",
            anchor_y="top",
        )

        text = """Use the arrow keys to move around the map.\n
        Some levels may be secured by guards.\n
        You must dodge them your way to the exit.\n\n
        Some levels will have locked doors.\n
        These can be unlocked with a key found somewhere on the map."""

        arcade.draw_text(
            text,
            self.width // 2,
            self.height * 0.15,
            TEXT_COLOR,
            align="center",
            anchor_x="center",
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.parent_view)
