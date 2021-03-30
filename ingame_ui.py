import arcade
from pyglet.gl import GL_NEAREST

from entity.player import PlayerInventory


class IngameUI:
    """
    Used to display in-game interface features like Key count and Current Level.
    """

    def __init__(self, player_inventory: PlayerInventory):
        self.player_inv = player_inventory
        self.inv_sprite = arcade.SpriteList()
        self.key_sprite = arcade.Sprite("assets/sprites/key.png", 2)
        self.inv_sprite.append(self.key_sprite)

    def draw(self, current_level: int, viewport: tuple[float, float, float, float]):
        vp_left, vp_right, vp_bottom, vp_top = viewport
        background_width, background_height = 135, 75
        point_list = (
            (vp_right, vp_top),
            (vp_right - background_width, vp_top),
            (vp_right - background_width, vp_top - background_height),
            (vp_right, vp_top - background_width),
        )
        arcade.draw_polygon_filled(point_list, (int(0x22), int(0x3D), int(0x28)))

        padding_top, padding_right = 10, 5
        self.key_sprite.center_x = (
            vp_right - (self.key_sprite.width // 2) - padding_right
        )
        self.key_sprite.center_y = vp_top - (self.key_sprite.height // 2) - padding_top

        padding_top, padding_right = 40, self.key_sprite.width + 10
        arcade.draw_text(
            text=str(self.player_inv.keys),
            start_x=vp_right - (self.key_sprite.width // 2) - padding_right,
            start_y=vp_top - (self.key_sprite.height // 2) - padding_top,
            color=arcade.color.WHITE,
            font_size=48,
        )

        self.inv_sprite.draw(filter=GL_NEAREST)
