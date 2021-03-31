import arcade

from entity.player import Player
from model.interactable import Interactable


class Cabinet(arcade.Sprite, Interactable):
    def __init__(self, loc, *args, **kwargs):
        super().__init__("game/assets/sprites/cabinet.png", 1, *args, **kwargs)
        self.center_x, self.center_y = loc["spawn"].x, loc["spawn"].y  # 😠

    def interact(self, player: Player):
        player.inventory.keys += 1
        self.kill()
