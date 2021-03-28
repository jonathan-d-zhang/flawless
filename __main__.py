from typing import NamedTuple, Optional

import utils
from constant import *
import arcade
from pyglet.gl import GL_NEAREST


class Vector2D(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector2D(scalar * self.x, scalar * self.y)


class Player(arcade.Sprite):
    @property
    def position(self) -> Vector2D:
        return Vector2D(int(self.center_x), int(self.center_y))

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


class GameView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.wall_list: Optional[arcade.SpriteList] = None
        self.floor_list: Optional[arcade.SpriteList] = None
        self.player_list: Optional[arcade.SpriteList] = None
        self.player_sprite: Optional[Player] = None

    def setup(self):
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("assets/sprites/square.png", PLAYER_SCALING)

        # Starting position of the player
        self.player_sprite.center_x, self.player_sprite.center_y = utils.center_of_tile(
            135, 390
        )

        self.player_list.append(self.player_sprite)

        self.load_map()
        self.set_viewport_on_player()

    def load_map(self):
        tile_map = arcade.tilemap.read_tmx(f"tilemaps/TestLevel.tmx")

        self.wall_list = arcade.tilemap.process_layer(
            tile_map, "walls", TILE_SPRITE_SCALING, use_spatial_hash=True
        )

        self.floor_list = arcade.tilemap.process_layer(
            tile_map, "floor", TILE_SPRITE_SCALING, use_spatial_hash=True
        )

    def on_key_press(self, key: int, modifiers: int):
        if key in [arcade.key.UP, arcade.key.LEFT, arcade.key.RIGHT, arcade.key.DOWN]:
            # Record Original Pos so if collision with wall is detected, we return the
            # player to that spot before rendering, making it impassable.
            original_pos = (self.player_sprite.center_x, self.player_sprite.center_y)
            self.player_sprite.handle_user_input(key, modifiers)
            if arcade.check_for_collision_with_list(self.player_sprite, self.wall_list):
                self.player_sprite.center_x, self.player_sprite.center_y = original_pos

            self.set_viewport_on_player()

    def set_viewport_on_player(self):
        """
        Set the viewport to be over the player. If the Viewport would display the outside blackness,
        it is clamped with the game map.
        :return:
        """
        clamped_x = min(
            SCREEN_WIDTH,
            max(0, self.player_sprite.center_x - HORIZONTAL_VIEWPORT_MARGIN),
        )
        clamped_y = min(
            SCREEN_HEIGHT,
            max(0, self.player_sprite.center_y - VERTICAL_VIEWPORT_MARGIN),
        )
        arcade.set_viewport(
            clamped_x, SCREEN_WIDTH + clamped_x, clamped_y, SCREEN_HEIGHT + clamped_y
        )

    def on_update(self, delta_time: float):
        ...

    def on_draw(self):
        arcade.start_render()

        # GL_NEAREST makes scaled Pixel art look cleaner
        self.wall_list.draw(filter=GL_NEAREST)
        self.floor_list.draw(filter=GL_NEAREST)
        self.player_list.draw()


def main():
    main_window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    game_view = GameView(main_window)
    game_view.setup()

    main_window.show_view(game_view)

    arcade.run()


if __name__ == "__main__":
    main()
