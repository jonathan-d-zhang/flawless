import arcade


class Exit(arcade.Sprite):
    def __init__(self, location, *args, **kwargs):
        super().__init__("game/assets/sprites/exit.png", *args, **kwargs)
        self.center_x, self.center_y = location["spawn"].x, location["spawn"].y
