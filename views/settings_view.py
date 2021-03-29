from abc import ABC, abstractmethod

import arcade
import arcade.gui

from config import CONFIG


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.last_size = (width, height) = self.window.get_size()
        # use setting_index to grab the currently selected setting
        self.setting_index = 0

        # setting_list will store list of settings to add to the view
        self.setting_list = [
            SettingToggle(
                width // 2 - 25,
                height - 0 * 50 - height // 8,
                "Turn music off/on",
                "is_music_on",
            ),
            SettingSlider(
                width // 2 - 25,
                height - 1 * 50 - height // 8,
                "Adjust volume",
                "music_volume",
            ),
            SettingToggle(
                width // 2 - 25,
                height - 2 * 50 - height // 8,
                "Fullscreen",
                "is_fullscreen",
            ),
        ]

    def on_draw(self):
        arcade.start_render()
        self.setup()
        ...

    def on_show(self):
        ...

    def on_show_view(self):
        ...

    def on_update(self, delta_time: float):
        ...

    def update(self, delta_time: float):
        if self.last_size != (new_size := self.window.get_size()):
            print(f"changed the size from {self.last_size} to {new_size}")
            width, height = new_size
            for i, setting in enumerate(self.setting_list):
                setting.x = width // 2 - 25
                setting.y = height - i * 50 - height // 2
        self.last_size = new_size

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
        for setting in self.setting_list:
            setting.draw()


class SettingField(ABC):
    """
    Represents a setting the user can modify, with a text label.
    """

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
    """
    Represents a toggleable setting
    """

    def __init__(self, x, y, text, binding):
        super().__init__(x, y, text, binding)

    def decrease(self):
        self.value = False

    def increase(self):
        self.value = True


class SettingSlider(SettingField):
    """
    Represents a setting with a slider
    """

    def __init__(self, x, y, text, binding):
        super().__init__(x, y, text, binding)

    def decrease(self):
        if 1 <= self.value < 11:
            self.value -= 1

    def increase(self):
        if 1 <= self.value < 11:
            self.value += 1
