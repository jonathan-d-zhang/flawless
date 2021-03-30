import arcade
from config import CONFIG
from constants import *

from views import main_menu_view


class GameWindow(arcade.Window):
    def __init__(self, **kwargs):
        super().__init__(
            INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT, SCREEN_TITLE, **kwargs
        )

    def on_update(self, delta_time: float):
        # not expensive if we call this function when we don't need to
        # because it checks to see if we try to change it into a state
        # it is already in, e.g. go fullscreen when we are already fullscreen
        self.set_fullscreen(CONFIG.is_fullscreen)


def main():
    window = GameWindow()
    window.center_window()
    view = main_menu_view.MainMenuView()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
