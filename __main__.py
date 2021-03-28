import utils
from constant import *
import arcade
from pyglet.gl import GL_NEAREST


class Player(arcade.Sprite):
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


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.wall_list = None
        self.floor_list = None
        self.player_list = None
        self.player_sprite = None

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

    def on_update(self, delta_time: float):
        ...

    def on_draw(self):
        arcade.start_render()

        # GL_NEAREST makes scaled Pixel art look cleaner
        self.wall_list.draw(filter=GL_NEAREST)
        self.floor_list.draw(filter=GL_NEAREST)

        self.player_list.draw()


def main():
    window = MainWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
