import arcade
from pyglet.gl import GL_NEAREST

from .entity.player import PlayerInventory


class IngameUI:
    """
    Used to display in-game interface features like Key count and Current Level.
    """

    def __init__(self, player_inventory: PlayerInventory):
        self.player_inv = player_inventory
        self.inv_sprite = arcade.SpriteList()
        self.key_sprite = arcade.Sprite("game/assets/sprites/key.png", 0.75)
        self.inv_sprite.append(self.key_sprite)
        self.colour = 0x22, 0x3D, 0x28

    def _draw_level(self):
        left, right, bottom, top = self.viewport

        arcade.draw_text(
            text="Level",
            start_x=right - ((right // 14) * 2),
            start_y=top - (top // 10),
            color=arcade.color.WHITE,
            font_size=top // 24,
        )
        arcade.draw_text(
            text=str(self.cur_level),
            start_x=right - ((right // 16) * 2),
            start_y=top - (top // 13),
            color=arcade.color.WHITE,
            font_size=top // 16,
        )

    def _draw_keys(self):
        left, right, bottom, top = self.viewport

        self.key_sprite.center_x = right - (self.key_sprite.width // 2) - 5
        self.key_sprite.center_y = top - (self.key_sprite.height // 2) - 5

        arcade.draw_text(
            text=str(self.player_inv.keys),
            start_x=right - (right // 14),
            start_y=top - (top // 10),
            color=arcade.color.WHITE,
            font_size=top // 14,
        )

    def _draw_background(self):

        left, right, bottom, top = self.viewport
        width, height = right // 6.5, top // 10

        point_list = (
            (right, top),
            (right - width, top),
            (right - width, top - height),
            (right, top - height),
        )

        arcade.draw_polygon_filled(point_list, self.colour)

    def draw(
        self,
        current_level: int,
        viewport: tuple[float, float, float, float],
        window_size: tuple[int, int],
    ):
        self.cur_level = current_level
        self.viewport = viewport
        self.window_size = window_size

        self._draw_background()
        self._draw_keys()
        self._draw_level()

        self.inv_sprite.draw(filter=GL_NEAREST)
