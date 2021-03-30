import arcade

from entity.player import Player
from model.interactable import Interactable
from model.item import Item


class Cabinet(arcade.Sprite, Interactable):
    def __init__(self, content: Item, *args, **kwargs):
        super().__init__("assets/sprites/cabinet.png", 1, *args, **kwargs)

        self.content = content
        self.sound_effect = arcade.load_sound("assets/sound_effects/key_pickup.mp3")

    def interact(self, player: Player):
        player.inventory.append(self.content)
        arcade.play_sound(self.sound_effect, volume=0.1)
        self.kill()
