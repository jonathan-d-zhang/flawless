import arcade
from pyglet.gl import GL_NEAREST

TILE_SPRITE_SCALING = 2
PLAYER_SCALING = 0.2

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 482
SCREEN_TITLE = "You better run..."


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
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            PLAYER_SCALING,
        )

        # Starting position of the player
        self.player_sprite.center_x = 135
        self.player_sprite.center_y = 400

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

    def on_draw(self):
        arcade.start_render()

        # GL_NEAREST makes scaled Pixel art look cleaner
        self.wall_list.draw(filter=GL_NEAREST)
        self.floor_list.draw(filter=GL_NEAREST)

        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            ...
        elif key == arcade.key.LEFT:
            ...
        elif key == arcade.key.RIGHT:
            ...
        elif key == arcade.key.DOWN:
            ...

    def on_update(self, delta_time):
        ...


def main():
    window = MainWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
