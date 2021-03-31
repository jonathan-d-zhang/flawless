import arcade

from constants import TILE_SIZE, PLAYER_SCALING
from utils import Vector


class PlayerInventory:
    keys: int = 0


class Player(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "game/assets/sprites/square.png", PLAYER_SCALING, *args, **kwargs
        )
        self.inventory: PlayerInventory = PlayerInventory()

    @property
    def position(self) -> Vector:
        return Vector(int(self.center_x), int(self.center_y))

    def update(self):
        ...

    def handle_user_input(self, key: int, modifiers: int):
        """
        Handle events passed from the MainWindow.
        :return:
        """
        if key == arcade.key.UP:
            self.center_y += TILE_SIZE
        elif key == arcade.key.DOWN:
            self.center_y -= TILE_SIZE
        elif key == arcade.key.LEFT:
            self.center_x -= TILE_SIZE
        elif key == arcade.key.RIGHT:
            self.center_x += TILE_SIZE
