from enum import Enum
from typing import Optional
from glob import glob
import re

from .. import utils

from ..constants import *

import arcade
from pyglet.gl import GL_NEAREST

from ..entity.cabinet import Cabinet
from ..entity.enemy import EnemyList, Enemy
from ..entity.player import Player
from ..entity.exit import Exit

from ..ingame_ui import IngameUI

from ..music_player import MusicPlayer

from .base_view import BaseView


class GameState(Enum):
    playermove = 1
    enemymove = 2
    enemyturning = 3


class GameView(BaseView):
    door_open_sound = arcade.Sound("game/assets/sound_effects/door_open.wav")

    def __init__(self, views):
        super().__init__(views)

        self.level = 1

        files = glob("game/assets/levels/level*.tmx")
        self.last_level = sorted(
            int(re.search(r"\d+", file).group()) for file in files
        )[-1]
        assert self.last_level == len(
            files
        ), f"Missing a level, check you have a level for the full range from 1 - {len(files)} in game/levels"

        self.wall_list: Optional[arcade.SpriteList] = None
        self.floor_list: Optional[arcade.SpriteList] = None
        self.exit_list: Optional[arcade.SpriteList] = None
        self.door_list: Optional[arcade.SpriteList] = None
        self.interactable_list: Optional[arcade.SpriteList] = None
        self.enemy_list: Optional[EnemyList] = None
        self.player: Optional[Player] = None
        self.ingame_ui: Optional[IngameUI] = None
        self.gamestate = None

        self.music_player = MusicPlayer()

    def setup(self):
        self.interactable_list = arcade.SpriteList()

        # Set up the player
        self.player = Player()
        self.gamestate = GameState.playermove

        self.ingame_ui = IngameUI(self.player.inventory)

        self.load_map()
        self.set_viewport_on_player()
        self._draw()

    def win_level(self):
        # TODO: Transition to next level
        self.level += 1
        self.setup()

    def lose_level(self):
        self.setup()

    def load_map(self):

        # Process Tile Map
        level_path = f"game/assets/levels/level{self.level}.tmx"
        tile_map = arcade.tilemap.read_tmx(level_path)
        utils.map_height = tile_map.map_size[1]

        # Tile Layers
        self.wall_list = arcade.tilemap.process_layer(
            tile_map, "walls", TILE_SPRITE_SCALING, use_spatial_hash=True
        )

        self.door_list = arcade.tilemap.process_layer(
            tile_map, "doors", TILE_SPRITE_SCALING, use_spatial_hash=True
        )

        self.floor_list = arcade.tilemap.process_layer(
            tile_map, "floor", TILE_SPRITE_SCALING, use_spatial_hash=True
        )

        self.exit_list = arcade.SpriteList()

        # Object Layers
        self.object_layers = utils.process_objects(level_path)

        self.enemy_list = arcade.SpriteList()

        self.guard_locations = [
            utils.extract_locations(guard_layers)
            for guard_layers in self.object_layers["guard"]
        ]

        self.key_locations = [
            utils.extract_locations(key_layers)
            for key_layers in self.object_layers["key"]
        ]

        self.interactable_list.extend(Cabinet(loc) for loc in self.key_locations)

        self.enemy_list = EnemyList(self.wall_list, self.door_list)
        for guard_layer in self.object_layers["guard"]:
            self.enemy_list.add_from_layer(guard_layer)

        self.exit_locations = [
            utils.extract_locations(exit_layers)
            for exit_layers in self.object_layers["exit"]
        ]

        self.player_spawn = utils.extract_locations(
            self.object_layers["player_spawn"][0]
        )["spawn"]

        self.exit_list.extend(Exit(loc) for loc in self.exit_locations)

        # Set Player Location

        self.player.center_x, self.player.center_y = utils.center_of_tile(
            self.player_spawn.x, self.player_spawn.y
        )

    def handle_collision(self, key: int, modifiers: int):
        original_pos = (self.player.center_x, self.player.center_y)
        self.player.handle_user_input(key, modifiers)

        if arcade.check_for_collision_with_list(self.player, self.exit_list):
            self.win_level()
        elif arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x, self.player.center_y = original_pos
        elif collisions := arcade.check_for_collision_with_list(
            self.player, self.door_list
        ):
            if self.player.inventory.keys > 0:
                self.player.inventory.keys -= 1
                self.door_list.remove(collisions[0])
                arcade.play_sound(self.door_open_sound)
                self.enemy_list.update()
            else:
                self.player.center_x, self.player.center_y = original_pos

        else:
            self.enemy_list.update()

    def on_key_press(self, key: int, modifiers: int):
        if key in [arcade.key.UP, arcade.key.LEFT, arcade.key.RIGHT, arcade.key.DOWN]:
            while self.gamestate != GameState.playermove:
                self.enemy_moving(0)
            # Record Original Pos so if collision with wall is detected, we return the
            # player to that spot before rendering, making it impassable.
            self.handle_collision(key, modifiers)

            self.set_viewport_on_player()
            self._draw()
            self.gamestate = GameState.enemymove
        elif key == arcade.key.ESCAPE:
            self.switch_to("pause")

    def enemy_moving(self, delta_time):
        if self.gamestate == GameState.enemymove:
            self.enemy_list.move_one_square()
            self._draw()
            self.gamestate = GameState.enemyturning

        elif self.gamestate == GameState.enemyturning:
            self.enemy_list.update_direction()
            self._draw()
            if any(enemy.movesleft for enemy in self.enemy_list):
                self.gamestate = GameState.enemymove
            else:
                self.gamestate = GameState.playermove

    def set_viewport_on_player(self):
        """
        Set the viewport to be over the player. If the Viewport would display the outside blackness,
        it is clamped with the game map.
        :return:
        """
        clamped_x = min(
            SCREEN_WIDTH, max(0, self.player.center_x - HORIZONTAL_VIEWPORT_MARGIN)
        )
        clamped_y = min(
            SCREEN_HEIGHT, max(0, self.player.center_y - VERTICAL_VIEWPORT_MARGIN)
        )
        arcade.set_viewport(
            clamped_x, SCREEN_WIDTH + clamped_x, clamped_y, SCREEN_HEIGHT + clamped_y
        )

    def on_update(self, delta_time: float):
        for interactable in arcade.check_for_collision_with_list(
            self.player, self.interactable_list
        ):
            interactable.interact(self.player)

        if self.enemy_list.check_los_collision(self.player):
            self.lose_level()

        self.player.update()

        self.music_player.update()

    def _draw(self):
        arcade.start_render()

        # GL_NEAREST makes scaled Pixel art look cleaner
        self.floor_list.draw(filter=GL_NEAREST)
        self.wall_list.draw(filter=GL_NEAREST)
        self.door_list.draw(filter=GL_NEAREST)
        self.interactable_list.draw(filter=GL_NEAREST)

        self.enemy_list.draw(filter=GL_NEAREST)
        self.player.draw()

    def on_draw(self):
        self.ingame_ui.draw(self.level, self.window.get_viewport())
        self._draw()
