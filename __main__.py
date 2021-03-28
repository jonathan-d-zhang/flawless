import arcade
from constants import *
from views import main_menu_view


if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = main_menu_view.MainMenuView()
    window.show_view(view)
    arcade.run()
