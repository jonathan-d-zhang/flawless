import arcade

from .menu_view import MenuView, MenuField
from ..views import settings_view, credits_view, game_view, instructions_view

TEXT_COLOR = arcade.csscolor.WHITE


class MainMenuView(MenuView):
    def __init__(self):
        super().__init__()
        options = "Play", "Settings", "How to Play", "Credits", "Exit"

        self.field_list = [
            MainMenuField(
                self.width * 0.85, self.height - i * 50 - self.height // 3, option
            )
            for i, option in enumerate(options)
        ]

        self.background = arcade.load_texture("game/assets/main_menu_background.png")

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)

        arcade.draw_text(
            "Flawless",
            self.width // 2,
            self.height * 0.90,
            TEXT_COLOR,
            20,
            anchor_x="center",
        )

        field = self.field_list[self.selection_index]

        arcade.draw_rectangle_outline(
            center_x=field.x - 40,
            center_y=field.y + 8,
            width=self.width // 8 - 20,
            height=30,
            color=TEXT_COLOR,
        )
        for field in self.field_list:
            field.draw()

        self.draw_information_text(TEXT_COLOR, nav=True)

    def on_show_view(self):
        self.setup()

    def update(self, delta_time: float):
        if (self.width, self.height) != (new_size := self.window.get_size()):
            self.width, self.height = new_size
            for i, field in enumerate(self.field_list):
                field.x = self.width // 2
                field.y = self.height - i * 50 - self.height // 2.5

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.DOWN:
            self.selection_index = (self.selection_index + 1) % len(self.field_list)
        elif symbol == arcade.key.UP:
            self.selection_index -= 1
            if self.selection_index < 0:
                self.selection_index = len(self.field_list) - 1
        elif symbol == arcade.key.ENTER:
            if self.selection_index == 0:
                view = game_view.GameView(self.window)
                view.setup()
                arcade.schedule(view.enemy_moving, 1 / 20)
                self.window.show_view(view)
            elif self.selection_index == 1:
                self.window.show_view(settings_view.SettingsView(self))
            elif self.selection_index == 2:
                self.window.show_view(instructions_view.InstructionsView(self))
            elif self.selection_index == 3:
                self.window.show_view(credits_view.CreditsView(self))
            elif self.selection_index == 4:
                self.window.close()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        ...


class MainMenuField(MenuField):
    def __init__(self, x, y, text):
        super().__init__(x, y, text)

    def draw(self, longest=None):
        arcade.draw_text(
            self.text, self.x, self.y, color=TEXT_COLOR, anchor_x="right",
        )
