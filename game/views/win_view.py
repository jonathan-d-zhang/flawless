import arcade
import arcade.gui

from .menu_view import MenuView, MenuField


class WinView(MenuView):
    def __init__(self, views):
        super().__init__(views)

        self.field_list = [
            "Play Again",
            "Exit to Main Menu",
        ]
        self.field_list = [
            WinField(self.width // 2, self.height - i * 50 - self.height // 2, field)
            for i, field in enumerate(self.field_list)
        ]

    def on_draw(self):
        arcade.start_render()

        self.window.set_viewport(0, self.width, 0, self.height)

        arcade.draw_text(
            "You win!",
            self.width // 2,
            self.height * 0.75,
            arcade.color.WHITE,
            20,
            anchor_x="center",
        )
        for field in self.field_list:
            field.draw()

        current_field = self.field_list[self.selection_index]
        arcade.draw_rectangle_outline(
            current_field.x,
            current_field.y + 8,
            self.width // 8,
            30,
            arcade.csscolor.WHITE,
        )
        self.draw_information_text(arcade.color.WHITE, nav=True)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.selection_index -= 1
            if self.selection_index < 0:
                self.selection_index = len(self.field_list) - 1
        elif symbol == arcade.key.DOWN:
            self.selection_index = (self.selection_index + 1) % len(self.field_list)
        elif symbol == arcade.key.ENTER:
            current_option = self.field_list[self.selection_index].text
            if current_option == "Play Again":
                # TODO reset the game?
                self.switch_to("game")
            elif current_option == "Exit to Main Menu":
                self.switch_to("menu")

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()


class WinField(MenuField):
    def __init__(self, x, y, text):
        super().__init__(x, y, text)

    def draw(self, longest=None):
        arcade.draw_text(
            self.text, self.x, self.y, color=arcade.csscolor.WHITE, anchor_x="center",
        )
