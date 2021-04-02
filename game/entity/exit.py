import arcade


class Exit(arcade.Sprite):
    def __init__(self, location, *args, **kwargs):
        super().__init__(
            "game/assets/sprites/square.png", *args, **kwargs
        )  # Not gonna be rendered
        self.center_x, self.center_y = location["spawn"].x, location["spawn"].y
