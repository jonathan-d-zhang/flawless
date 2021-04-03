import arcade

from .menu_view import MenuView
from ..constants import *


TEXT_COLOR = arcade.csscolor.WHITE


class InstructionsView(MenuView):
    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "How to Play",
            self.width // 2,
            self.height * 0.75,
            TEXT_COLOR,
            20,
            anchor_x="center",
            font_name=INSTRUCTIONS_FONT,
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
            font_name=INSTRUCTIONS_FONT,
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
            font_name=INSTRUCTIONS_FONT,
        )

        arcade.draw_text(
            a,
            self.width * 0.8 // 5,
            self.height * 0.27,
            TEXT_COLOR,
            anchor_y="top",
            font_name=INSTRUCTIONS_FONT,
        )
        arcade.draw_text(
            b,
            self.width * 3.2 // 5,
            self.height * 0.27,
            TEXT_COLOR,
            anchor_y="top",
            font_name=INSTRUCTIONS_FONT,
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.switch_to("menu")
