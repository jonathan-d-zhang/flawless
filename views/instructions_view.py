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

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.parent_view)
