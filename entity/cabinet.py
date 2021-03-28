import arcade

from entity.player import Player
from model.interactable import Interactable
from model.item import Item


class Cabinet(arcade.Sprite, Interactable):
    _instance = []

    def __new__(cls, *args, **kwargs):
        instance = super(Cabinet, cls).__new__(cls)
        cls._instance.append(instance)
        return instance

    def __init__(self, content: Item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content

    def interact(self, player: Player):
        player.inventory.append(self.content)
        self.kill()
