import arcade
import arcade.gui

from abc import ABC


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.selection_index = 0
        self.width, self.height = self.window.get_size()

    def on_draw(self):
        ...

    def on_key_press(self, symbol, modifiers):
        ...

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def draw_information_text(self, color, *, back=False, nav=False):
        width, height = self.window.get_size()
        if back:
            arcade.draw_text(
                "Press ESC to go back",
                width // 16,
                height * 7 / 8,
                arcade.color.WHITE,
            )
        if nav:
            t = "Up and down to navigate, ENTER to select"
            arcade.draw_text(t, width // 16, height // 8, color)


class MenuField(ABC):
    def __init__(self, x: int, y: int, text: str):
        self.x = x
        self.y = y
        self.text = text
        self.length = len(self.text) * 8

    def draw(self, longest: int = None):
        ...
