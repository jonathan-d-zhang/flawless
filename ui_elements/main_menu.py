import arcade
import arcade.gui
import constants


class PlayButton(arcade.gui.UIFlatButton):
    def __init__(self, text):
        super().__init__(text, center_x=400, center_y=400, width=50, height=50)

    def on_click(self):
        print("You clicked the button!!!")


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()

    def on_draw(self):
        arcade.start_render()

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        pass

    def setup(self):
        self.ui_manager.add_ui_element(PlayButton("Play"))
