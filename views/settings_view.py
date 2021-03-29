from abc import ABC, abstractmethod

import arcade
import arcade.gui
from config import CONFIG
from enum import Enum
from constants import *


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()

        # use setting_index to grab the currently selected setting
        self.setting_index = 0

        # setting_list will store list of settings to add to the view
        self.setting_list = [
            SettingToggle(
                SCREEN_WIDTH // 2 - 25,
                SCREEN_HEIGHT - 0 * 50 - 100,
                "test text 1",
                "is_music_on",
            ),
            SettingSlider(
                SCREEN_WIDTH // 2 - 25,
                SCREEN_HEIGHT - 1 * 50 - 100,
                "test text 2",
                "music_volume",
            ),
        ]

    def on_draw(self):
        ...

    def on_show_view(self):
        self.setup()

    def on_update(self, delta_time: float):
        print(CONFIG)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.setting_index -= 1
            if self.setting_index < 0:
                self.setting_index = len(self.setting_list) - 1
        elif symbol == arcade.key.DOWN:
            self.setting_index = (self.setting_index + 1) % len(self.setting_list)
        elif symbol == arcade.key.LEFT:
            self.setting_list[self.setting_index].decrease()
        elif symbol == arcade.key.RIGHT:
            self.setting_list[self.setting_index].increase()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        # arcade.start_render()
        for setting in self.setting_list:
            setting.draw()


class SettingField(ABC):
    def __init__(self, x: int, y: int, text: str, binding: str):
        self.x = x
        self.y = y
        self.text = text
        self.binding = binding

    @property
    def value(self):
        return getattr(CONFIG, self.binding)

    @value.setter
    def value(self, value):
        setattr(CONFIG, self.binding, value)

    @value.getter
    def value(self):
        return getattr(CONFIG, self.binding)

    def draw(self):
        arcade.draw_text(
            self.text, self.x, self.y, color=arcade.csscolor.WHITE, width=75
        )

    @abstractmethod
    def decrease(self):
        ...

    @abstractmethod
    def increase(self):
        ...


class SettingToggle(SettingField):
    def __init__(self, x, y, text, binding):
        super().__init__(x, y, text, binding)

    def decrease(self):
        self.value = False

    def increase(self):
        self.value = True


class SettingSlider(SettingField):
    def __init__(self, x, y, text, binding):
        super().__init__(x, y, text, binding)

    def decrease(self):
        self.value -= 1

    def increase(self):
        self.value += 1
