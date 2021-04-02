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
        self.key_sprite = arcade.Sprite("game/assets/sprites/key.png", 2)
        self.inv_sprite.append(self.key_sprite)
        self.colour = 0x22, 0x3D, 0x28

    def _draw_level(self) -> tuple[int, int]:
        """
        :return: The xy coords for the Top Left of the containing bounding box
        """
        padding_top, padding_right = 5, 50
        arcade.draw_text(
            text="Level",
            start_x=right - (self.key_sprite.width // 2) - padding_right,
            start_y=top - (self.key_sprite.height // 2) - padding_top,
            color=arcade.color.WHITE,
            font_size=24,
        )

        padding_top, padding_right = 45, padding_right - 20
        arcade.draw_text(
            text=str(self.cur_level),
            start_x=right - (self.key_sprite.width // 2) - padding_right,
            start_y=top - (self.key_sprite.height // 2) - padding_top,
            color=arcade.color.WHITE,
            font_size=36,
        )

        return right - (self.key_sprite.width // 2) - padding_right, top

    def _draw_keys(self) -> tuple[int, int]:
        """
        :return: The xy coords for the Top Left of the containing bounding box
        """
        padding_top, padding_right = 10, 5
        left = right - (self.key_sprite.width // 2)

        self.key_sprite.center_x = left - padding_right
        self.key_sprite.center_y = top - (self.key_sprite.height // 2) - padding_top

        padding_top, padding_right = 40, self.key_sprite.width + 10
        arcade.draw_text(
            text=str(self.player_inv.keys),
            start_x=left - padding_right,
            start_y=top - (self.key_sprite.height // 2) - padding_top,
            color=arcade.color.WHITE,
            font_size=48,
        )

        return left - padding_right, top

    def _draw_background(self):

        left, right, bottom, top = self.viewport
        width, height = right // 10, top // 10

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
        # self._draw_keys()
        # self._draw_level()

        self.inv_sprite.draw(filter=GL_NEAREST)
