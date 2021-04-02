from typing import Optional
from enum import Enum

from . import utils

from .constants import *

import arcade
from pyglet.gl import GL_NEAREST

from .entity.cabinet import Cabinet
from .entity.enemy import Enemy
from .entity.player import Player

from .ingame_ui import IngameUI

from .music_player import MusicPlayer


class GameState(Enum):
    playermove = 1
    enemymove = 2
    enemyturning = 3


class GameView(arcade.View):
    door_open_sound = arcade.Sound("game/assets/sound_effects/door_open.mp3")

    def __init__(self, window):
        super().__init__(window)
        self.wall_list: Optional[arcade.SpriteList] = None
        self.floor_list: Optional[arcade.SpriteList] = None
        self.door_list: Optional[arcade.SpriteList] = None
        self.interactable_list: Optional[arcade.SpriteList] = None
        self.enemy_list: Optional[arcade.SpriteList] = None
        self.player: Optional[Player] = None
        self.ingame_ui: Optional[IngameUI] = None

        self.music_player = MusicPlayer()

        self.gamestate = GameState.playermove

    def setup(self):
        self.interactable_list = arcade.SpriteList()

        self.load_map()

        # Set up the player
        self.player = Player()

        # Starting position of the player
        self.player.center_x, self.player.center_y = utils.center_of_tile(320, 320)

        self.ingame_ui = IngameUI(self.player.inventory)

        self.set_viewport_on_player()
        self._draw()

    def load_map(self):

        # Process Tile Map
        tile_map = arcade.tilemap.read_tmx(f"game/assets/tilemaps/level1_.tmx")
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

        # Object Layers
        self.object_layers = utils.process_objects(
            f"game/assets/tilemaps/level1_.tmx"
        )

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

        self.enemy_list.extend(
            Enemy(self.wall_list, guard_location)
            for guard_location in self.guard_locations
        )

    def handle_collision(self, key: int, modifiers: int):
        original_pos = (self.player.center_x, self.player.center_y)
        self.player.handle_user_input(key, modifiers)

        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x, self.player.center_y = original_pos

        elif collisions := arcade.check_for_collision_with_list(
            self.player, self.door_list
        ):
            if self.player.inventory.keys > 0:
                self.player.inventory.keys -= 1
                self.door_list.remove(collisions[0])
                arcade.play_sound(self.door_open_sound)
            else:
                self.player.center_x, self.player.center_y = original_pos

        else:
            self.enemy_list.update()

    def on_key_press(self, key: int, modifiers: int):
        if self.gamestate != GameState.playermove:
            return
        if key in [arcade.key.UP, arcade.key.LEFT, arcade.key.RIGHT, arcade.key.DOWN]:
            # Record Original Pos so if collision with wall is detected, we return the
            # player to that spot before rendering, making it impassable.
            self.handle_collision(key, modifiers)

            self.set_viewport_on_player()
            self._draw()
            self.gamestate = GameState.enemymove

    def enemy_moving(self, delta_time):
        if self.gamestate == GameState.enemymove:
            for enemy in self.enemy_list:
                enemy.move_one()
            self._draw()
            self.gamestate = GameState.enemyturning
        elif self.gamestate == GameState.enemyturning:
            for enemy in self.enemy_list:
                enemy.update_direction()
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
            SCREEN_WIDTH, max(0, self.player.center_x - HORIZONTAL_VIEWPORT_MARGIN),
        )
        clamped_y = min(
            SCREEN_HEIGHT, max(0, self.player.center_y - VERTICAL_VIEWPORT_MARGIN),
        )

        print(clamped_x, clamped_y)

        arcade.set_viewport(
            clamped_x, SCREEN_WIDTH + clamped_x, clamped_y, SCREEN_HEIGHT + clamped_y
        )

    def on_update(self, delta_time: float):
        for interactable in arcade.check_for_collision_with_list(
            self.player, self.interactable_list
        ):
            interactable.interact(self.player)

        self.player.update()

        self.music_player.update()

    def _draw(self):
        arcade.start_render()

        # GL_NEAREST makes scaled Pixel art look cleaner
        self.wall_list.draw(filter=GL_NEAREST)
        self.floor_list.draw(filter=GL_NEAREST)
        self.door_list.draw(filter=GL_NEAREST)
        self.interactable_list.draw(filter=GL_NEAREST)

        self.enemy_list.draw(filter=GL_NEAREST)
        for enemy in self.enemy_list:
            enemy.draw_path()
            enemy.draw_vision()
        self.player.draw()

    def on_draw(self):
        self.ingame_ui.draw(
            1, self.window.get_viewport()  # TODO: Replace with actual level.
        )


def main():
    main_window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    game_view = GameView(main_window)
    game_view.setup()
    arcade.schedule(game_view.enemy_moving, 1 / 20)

    main_window.show_view(game_view)

    arcade.run()


if __name__ == "__main__":
    main()
