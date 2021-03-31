import arcade

from .menu_view import MenuView, MenuField

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

        intro = """Your goal is to steal a diamond as part of a heist.\n
        To do this, you will have to bypass many levels of security.\n
        To pass each level, you must dodge the cops and get to the exit.\n"""

        arcade.draw_text(
            intro,
            self.width // 2,
            self.height * 0.65,
            TEXT_COLOR,
            align="center",
            anchor_x="center",
            anchor_y="top",
        )

        text = """For some levels, you will need to collect a key in order to unlock the door/exit.\n
        There will also be knives for you to collect.\n
        You can use these knives to kill guards if you approach them from behind or from the side."""

        arcade.draw_text(
            text,
            self.width // 2,
            self.height * 0.25,
            TEXT_COLOR,
            align="center",
            anchor_x="center"
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.parent_view)
