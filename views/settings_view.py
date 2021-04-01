from functools import partial
import arcade
from config import CONFIG

from .menu_view import MenuView, MenuField


class SettingsView(MenuView):
    def __init__(self, parent_view):
        super().__init__()
        self.width, self.height = self.window.get_size()
        self.parent_view = parent_view
        # use setting_index to grab the currently selected setting

        # setting_list will store list of settings to add to the view
        # full screen setting disabled as it create a ton of scaling issues
        self.setting_list = [
            partial(SettingToggle, text="Turn music on/off", binding="is_music_on"),
            # partial(SettingToggle, text="Fullscreen", binding="is_fullscreen"),
            partial(SettingSlider, text="Adjust volume", binding="music_volume"),
        ]
        self.setting_list = [
            setting(self.width // 4, self.height - i * 70 - self.height // 3)
            for i, setting in enumerate(self.setting_list)
        ]

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Settings",
            self.width // 2,
            self.height * 0.85,
            arcade.color.WHITE,
            20,
            anchor_x="center",
        )

        self.draw_information_text(arcade.color.WHITE, back=True)

        arcade.draw_text(
            "Left and right to change settings",
            self.width // 16,
            self.height // 8,
            arcade.color.WHITE,
        )

        longest = self.width // 2
        for setting in self.setting_list:
            setting.draw(longest)

        setting = self.setting_list[self.selection_index]
        x = setting.x + (longest + 60) // 2
        width = longest + 100

        if type(setting) is SettingToggle:
            arcade.draw_rectangle_outline(
                center_x=x,
                center_y=setting.y + 8,
                width=width,
                height=40,
                color=arcade.color.WHITE,
            )
        else:
            arcade.draw_rectangle_outline(
                center_x=x,
                center_y=setting.y,
                width=width,
                height=60,
                color=arcade.color.WHITE,
            )

    def update(self, delta_time: float):
        if (self.width, self.height) != (new_size := self.window.get_size()):
            self.width, self.height = new_size
            for i, setting in enumerate(self.setting_list):
                setting.x = self.width // 4
                setting.y = self.height - i * 70 - self.height // 3

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.selection_index -= 1
            if self.selection_index < 0:
                self.selection_index = len(self.setting_list) - 1
        elif symbol == arcade.key.DOWN:
            self.selection_index = (self.selection_index + 1) % len(self.setting_list)
        elif symbol == arcade.key.LEFT:
            self.setting_list[self.selection_index].decrease()
        elif symbol == arcade.key.RIGHT:
            self.setting_list[self.selection_index].increase()
        elif symbol == arcade.key.ESCAPE:
            self.window.show_view(self.parent_view)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()


class SettingField(MenuField):
    """
    Represents a setting the user can modify, with a text label.
    """

    def __init__(self, x: int, y: int, text: str, binding: str):
        super().__init__(x, y, text)
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

    def decrease(self):
        ...

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

    def draw(self, longest=None):
        arcade.draw_text(
            self.text, self.x, self.y, color=arcade.csscolor.WHITE,
        )

        arcade.draw_rectangle_outline(
            self.x + longest + 35, self.y + 8, 49, 20, color=arcade.color.WHITE
        )

        if self.value:
            arcade.draw_rectangle_filled(
                self.x + longest + 47, self.y + 8, 23, 18, color=arcade.color.BUD_GREEN,
            )

        else:
            arcade.draw_rectangle_filled(
                self.x + longest + 23, self.y + 8, 23, 18, color=arcade.color.CG_RED,
            )


class SettingSlider(SettingField):
    """
    Represents a setting with a slider, with values ranging from [1, 10]
    """

    def __init__(self, x, y, text, binding):
        super().__init__(x, y, text, binding)

    def decrease(self):
        if 2 <= self.value:
            self.value -= 1

    def increase(self):
        if self.value < 10:
            self.value += 1

    def draw(self, longest=None):
        arcade.draw_text(
            self.text, self.x, self.y, color=arcade.csscolor.WHITE, width=self.length,
        )
        arcade.draw_line(
            self.x, self.y - 15, self.x + longest, self.y - 15, arcade.color.WHITE
        )
        arcade.draw_text(
            str(self.value),
            self.x + longest + 35,
            self.y - 10,
            arcade.color.WHITE,
            20,
            anchor_x="center",
        )

        tick_len = longest // 9
        arcade.draw_circle_filled(
            self.x + (tick_len * (self.value - 1)), self.y - 15, 8.0, arcade.color.WHITE
        )
