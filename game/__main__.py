import arcade

from .constants import *
from .views import (
    BaseView,
    GameView,
    SettingsView,
    MainMenuView,
    CreditsView,
    PauseView,
    InstructionsView,
    WinView,
)

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.center_window()
window.set_mouse_visible(False)

views: dict[str, BaseView] = {}
views.update(
    game=GameView(views),
    settings=SettingsView(views),
    menu=MainMenuView(views),
    credits=CreditsView(views),
    pause=PauseView(views),
    win=WinView(views),
    instructions=InstructionsView(views),
)

window.show_view(views["menu"])
arcade.run()
