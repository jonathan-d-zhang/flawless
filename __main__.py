import arcade
from pyglet.gl import GL_NEAREST
import constants
from ui_elements import main_menu

SCREEN_TITLE = "You better run..."


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, SCREEN_TITLE)


def main():
    window = MainWindow()
    view = main_menu.MainMenuView()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
