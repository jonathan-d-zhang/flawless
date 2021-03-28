from typing import List

import arcade

from constant import TILE_SIZE
from model.item import Item
from utils import Vector


class Player(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventory: List[Item] = []

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
