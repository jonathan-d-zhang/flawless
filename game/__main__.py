import arcade

from .constants import *
from .views import MainMenuView


def main():
    main_window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # game_view = GameView(main_window)
    # game_view.setup()
    # arcade.schedule(game_view.enemy_moving, 1 / 20)
    #
    # main_window.show_view(game_view)
    view = MainMenuView()
    main_window.show_view(view)

    arcade.run()


if __name__ == "__main__":
    main()
