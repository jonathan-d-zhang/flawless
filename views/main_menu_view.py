import arcade
import arcade.gui
from constants import *

# import game
from views import settings_view


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()

    def on_draw(self):
        # arcade.start_render()
        ...

    def on_show_view(self):
        self.setup()

    def on_update(self, delta_time: float):
        ...

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.S:
            self.window.show_view(settings_view.SettingsView())
            # self.window.show_view(game.GameView())

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        ...
