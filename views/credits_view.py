import arcade

from .menu_view import MenuView, MenuField

TEXT_COLOR = arcade.csscolor.WHITE


class CreditsView(MenuView):
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Credits",
            self.width // 2,
            self.height * 0.75,
            TEXT_COLOR,
            20,
            anchor_x="center",
        )

        self.draw_information_text(TEXT_COLOR, nav=True)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.parent_view)
