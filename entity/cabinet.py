import arcade

from entity.player import Player
from model.interactable import Interactable
from model.item import Item


class Cabinet(arcade.Sprite, Interactable):
    def __init__(self, content: Item, *args, **kwargs):
        super().__init__("assets/sprites/cabinet.png", 1, *args, **kwargs)

        self.content = content

    def interact(self, player: Player):
        player.inventory.keys += 1
        self.kill()
