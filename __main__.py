import arcade
from constants import *
from views import main_menu_view, settings_view


if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # view = main_menu_view.MainMenuView()
    view = settings_view.SettingsView()
    window.show_view(view)
    arcade.run()
