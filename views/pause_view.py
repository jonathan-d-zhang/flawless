import arcade
import arcade.gui

from .menu_view import MenuView, MenuField
from .settings_view import SettingsView
from .main_menu_view import MainMenuView

TEXT_COLOR = arcade.csscolor.WHITE


class PauseView(MenuView):
    def __init__(self):
        super().__init__()
        self.field_list = ["Resume", "Settings", "Exit to Main Menu", "Exit Game"]
        self.field_list = [
            PauseField(self.width // 2, self.height - i * 50 - self.height // 2, field)
            for i, field in enumerate(self.field_list)
        ]

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Game is Paused",
            self.width // 2,
            self.height * 0.75,
            TEXT_COLOR,
            20,
            anchor_x="center",
        )
        for field in self.field_list:
            field.draw()

        current_field = self.field_list[self.selection_index]
        arcade.draw_rectangle_outline(
            current_field.x, current_field.y + 8, self.width // 8, 30, TEXT_COLOR
        )

        t = "Up and down to navigate, ENTER to select"
        arcade.draw_text(t, self.width // 16, self.height // 8, TEXT_COLOR)

    def update(self, delta_time: float):
        if (self.width, self.height) != (new_size := self.window.get_size()):
            self.width, self.height = new_size
            for i, field in enumerate(self.field_list):
                field.x = self.width // 2
                field.y = self.height - i * 50 - self.height // 2

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.DOWN:
            self.selection_index = (self.selection_index + 1) % len(self.field_list)
        elif symbol == arcade.key.UP:
            self.selection_index -= 1
            if self.selection_index < 0:
                self.selection_index = len(self.field_list) - 1
        elif symbol == arcade.key.ENTER:
            current_option = self.field_list[self.selection_index].text
            if current_option == "Resume":
                # load game view
                # self.window.show_view(GameView)
                pass
            elif current_option == "Settings":
                self.window.show_view(SettingsView(self))
            elif current_option == "Exit to Main Menu":
                self.window.show_view(MainMenuView())
            elif current_option == "Exit Game":
                self.window.close() 


class PauseField(MenuField):
    def __init__(self, x, y, text):
        super().__init__(x, y, text)

    def draw(self):
        arcade.draw_text(self.text, self.x, self.y, TEXT_COLOR, anchor_x="center")
