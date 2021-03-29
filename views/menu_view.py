import arcade
import arcade.gui

from abc import ABC
from config import CONFIG


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


class MenuField(ABC):
    def __init__(self, x: int, y: int, text: str):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, longest: int):
        ...
