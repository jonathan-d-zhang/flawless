import random

import arcade

from constants import TILE_SIZE


class Enemy(arcade.Sprite):
    def __init__(self, walls, *args, **kwargs):
        super().__init__("assets/sprites/enemy.png", 1, *args, **kwargs)
        self._walls = walls

    def _move_randomly(self):
        while True:
            original_pos = self.center_x, self.center_y
            val = TILE_SIZE if random.randint(0, 1) else -TILE_SIZE

            if random.randint(0, 1):
                self.center_x += val
            else:
                self.center_y += val

            if not arcade.check_for_collision_with_list(self, self._walls):
                break
            else:
                self.center_x, self.center_y = original_pos

    def update(self):
        self._move_randomly()
