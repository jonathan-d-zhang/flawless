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

        self.draw_information_text(TEXT_COLOR, back=True)

        intro = """As part of the biggest heist of the century, your goal is to steal a diamond.\n
        To do this, you will have to bypass many levels of security."""

        arcade.draw_text(
            intro,
            self.width // 2,
            self.height * 0.68,
            TEXT_COLOR,
            align="center",
            anchor_x="center",
            anchor_y="top",
        )

        text = """Some levels may be secured by guards.\nYou must dodge them your way to the exit.
        \n\nSome levels will have locked doors. These can be unlocked with a key found somewhere on the map."""
        a = "Use the arrow keys to move\naround the map."
        b = "You can pause the game at\nany point by pressing ESC."

        arcade.draw_text(
            text,
            self.width // 2,
            self.height * 0.35,
            TEXT_COLOR,
            align="center",
            anchor_x="center",
        )

        arcade.draw_text(a, self.width * .8 // 5, self.height * .27, TEXT_COLOR, anchor_y="top")
        arcade.draw_text(b, self.width * 3.2 // 5, self.height * .27, TEXT_COLOR, anchor_y="top")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.parent_view)
