import arcade
from pyglet.gl import GL_NEAREST

from .entity.player import PlayerInventory
from .constants import *


class IngameUI:
    """
    Used to display in-game interface features like Key count and Current Level.
    """

    def __init__(self, player_inventory: PlayerInventory):
        self.player_inv = player_inventory
        self.inv_sprite = arcade.SpriteList()
        self.key_sprite = arcade.Sprite("game/assets/sprites/key.png", 1.25)
        self.inv_sprite.append(self.key_sprite)
        self.colour = 0x22, 0x3D, 0x28

    def _draw_info(self):
        left, right, bottom, top = self.viewport

        key_x = right - (self.key_sprite.width // 2) - 5
        key_y = top - (self.key_sprite.height // 2) - 5
        self.key_sprite.center_x = key_x
        self.key_sprite.center_y = key_y

        arcade.draw_text(
            text=str(self.player_inv.keys),
            start_x=key_x - self.key_sprite.width,
            start_y=key_y - 20,
            color=arcade.color.WHITE,
            font_name=INGAME_UI_FONT,
            font_size=self.window_size[1] // 14,
        )

        left_pos = left + 10
        arcade.draw_text(
            text="Level",
            start_x=left_pos,
            start_y=top - 55,
            color=arcade.color.WHITE,
            font_name=INGAME_UI_FONT,
            font_size=self.window_size[1] // 32,
        )
        arcade.draw_text(
            text=str(self.cur_level),
            start_x=left_pos + 10,
            start_y=top - 40,
            color=arcade.color.WHITE,
            font_name=INGAME_UI_FONT,
            font_size=self.window_size[1] // 16,
        )

        arcade.draw_text(
            text="Deaths",
            start_x=left_pos + self.window_size[0] // 16 - 5,
            start_y=top - 55,
            color=arcade.color.WHITE,
            font_name=INGAME_UI_FONT,
            font_size=self.window_size[1] // 32,
        )

        arcade.draw_text(
            text=str(self.death_counter) if self.death_counter < 100 else "∞",
            start_x=left_pos + 70,
            start_y=top - 40,
            color=arcade.color.WHITE,
            font_name=INGAME_UI_FONT,
            font_size=self.window_size[1] // 16,
        )

    def _draw_background(self):

        left, right, bottom, top = self.viewport
        width, height = self.window_size[0] // 12, self.window_size[1] // 10

        point_list = (
            (right, top),
            (right - width, top),
            (right - width, top - height),
            (right, top - height),
        )

        arcade.draw_polygon_filled(point_list, self.colour)

        width, height = self.window_size[0] / 7, self.window_size[1] // 8
        point_list = (
            (left, top),
            (left + width, top),
            (left + width, top - height),
            (left, top - height),
        )

        arcade.draw_polygon_filled(point_list, self.colour)

    def draw(
        self,
        current_level: int,
        death_counter: int,
        viewport: tuple[float, float, float, float],
        window_size: tuple[int, int],
    ):
        self.cur_level = current_level
        self.viewport = viewport
        self.window_size = window_size
        self.death_counter = death_counter

        self._draw_background()
        self._draw_info()

        self.inv_sprite.draw(filter=GL_NEAREST)
