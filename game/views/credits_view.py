import arcade

from ..constants import *
from .menu_view import MenuView

TEXT_COLOR = arcade.csscolor.WHITE


class CreditsView(MenuView):
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Credits",
            self.width // 2,
            self.height * 0.75,
            TEXT_COLOR,
            20,
            anchor_x="center",
            font_name=CREDITS_FONT,
        )
        self.draw_information_text(TEXT_COLOR, back=True, nav=True)

        arcade.draw_text(
            "Music",
            self.width // 4,
            self.height * 0.65,
            TEXT_COLOR,
            18,
            font_name=CREDITS_FONT,
        )
        music_credits = "Music is original and created in GarageBand.\n\nAll loops Copyright 2021 Apple Inc."
        arcade.draw_text(
            music_credits,
            self.width // 4,
            self.height * 0.54,
            TEXT_COLOR,
            11,
            font_name=CREDITS_FONT,
        )

        arcade.draw_text(
            "Sprites",
            self.width // 4,
            self.height * 0.45,
            TEXT_COLOR,
            18,
            font_name=CREDITS_FONT,
        )
        sprites_credits = (
            "Sprites were created by our team member eddpmett using Photoshop"
        )
        arcade.draw_text(
            sprites_credits,
            self.width // 4,
            self.height * 0.40,
            TEXT_COLOR,
            11,
            font_name=CREDITS_FONT,
        )

        arcade.draw_text(
            "Tilemaps",
            self.width // 4,
            self.height * 0.30,
            TEXT_COLOR,
            18,
            font_name=CREDITS_FONT,
        )
        tilemaps_credits = (
            "Tilemaps/levels were created by our team members using Tiled."
        )
        arcade.draw_text(
            tilemaps_credits,
            self.width // 4,
            self.height * 0.25,
            TEXT_COLOR,
            11,
            font_name=CREDITS_FONT,
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.switch_to("menu")
