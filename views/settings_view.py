import arcade
import arcade.gui
from constants import *


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()

        # use setting_index to grab the currently selected setting
        self.setting_index = 0

        # setting_list will store list of settings to add to the view
        self.setting_list = [
            arcade.gui.UIToggle(400, 400, 50),
        ]

    def on_draw(self):
        arcade.start_render()

    def on_show_view(self):
        self.setup()

    def on_update(self, delta_time: float):
        ...

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:
            print("inkyo")
            # self.window.show_view(game.GameView())

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        for setting in self.setting_list:
            self.ui_manager.add_ui_element(setting)


class SettingField:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y


class SettingToggle(arcade.gui.UIToggle, SettingField):
    def __init__(self, center_x, center_y, text):
        super().__init__(center_x, center_y, 20, value=False)
        self.text = text
        arcade.start_render()

    def on_toggle(self, value):
        print("toggled !")
