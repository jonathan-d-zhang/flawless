import arcade

from .constants import *
from .views import GameView, SettingsView, MainMenuView, CreditsView

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.center_window()
window.set_mouse_visible(False)

views = {}
views.update(
    game=GameView(views),
    settings=SettingsView(views),
    menu=MainMenuView(views),
    credits=CreditsView(views),
)

window.show_view(views["menu"])

arcade.run()
