from __future__ import annotations
import arcade

from ..constants import TILE_SIZE
from ..utils import Direction, Vector, center_of_tile, extract_locations


class PathColors:
    pathcoloridx = 0
    pathcolorlist = [
        (97, 82, 103),
        (34, 61, 40),
        (66, 81, 100),
        (57, 48, 51),
        (230, 211, 179),
        (95, 117, 145),
        (65, 115, 76),
        (120, 101, 128),
        (230, 115, 128),
        (53, 64, 79),
    ]

    @classmethod
    def get_color(cls):
        color = cls.pathcolorlist[cls.pathcoloridx]
        cls.pathcoloridx = (cls.pathcoloridx + 1) % len(cls.pathcolorlist)
        return color


class EnemyList(arcade.SpriteList):
    def __init__(self, wall_list):
        self.wall_list = wall_list
        self.paths = arcade.ShapeElementList()
        super().__init__()

    def add_from_layer(self, layer):
        locations = extract_locations(layer)
        newenemy = Enemy(self.wall_list, locations)
        self.append(newenemy)
        self.paths.append(newenemy.pathshape)

    def move_one_square(self):
        self.moving_complete = True
        for enemy in self:
            movesleft = enemy.move_one_square()
            if movesleft:
                self.moving_complete = False

    def update_direction(self):
        for enemy in self:
            enemy.update_direction()

    def draw(self, *args, **kwargs):
        self.paths.draw()
        for enemy in self:
            enemy.draw_vision()
        super().draw(*args, **kwargs)

    def check_los_collision(self, sprite: arcade.Sprite) -> list[arcade.Sprite]:
        """
        Return list of all enemies that spotted the player
        """
        return [enemy for enemy in self if enemy.check_los_collision(sprite)]


class Enemy(arcade.Sprite):
    def __init__(self, walls, locations, *args, **kwargs):
        super().__init__("game/assets/sprites/enemy.png", 1, *args, **kwargs)
        self._walls = walls
        self.position = locations["spawn"]
        self.waypoints = locations["waypoints"]
        self.pathcolor = PathColors.get_color()
        self.create_full_path()
        self.movesleft = 0
        self.movecount = 2
        self.maxvision = 3
        self.update_direction()

    @property
    def position(self) -> Vector:
        return Vector(int(self.center_x), int(self.center_y))

    @position.setter
    def position(self, pos):
        self.center_x, self.center_y = map(int, pos)

    def calculate_path(self, waypoint1, waypoint2):
        """
        Generator that yields the points between waypoint1 to waypoint2
        excludes waypoint1 from the list
        """
        pos_x, pos_y = waypoint1
        while pos_x < waypoint2[0]:
            pos_x += TILE_SIZE
            yield pos_x, pos_y
        while pos_x > waypoint2[0]:
            pos_x -= TILE_SIZE
            yield pos_x, pos_y
        while pos_y < waypoint2[1]:
            pos_y += TILE_SIZE
            yield pos_x, pos_y
        while pos_y > waypoint2[1]:
            pos_y -= TILE_SIZE
            yield pos_x, pos_y

    def create_full_path(self):
        """
        Creates a looping path through all way points
        and back to the starting position
        """
        self.path = []
        self.pathidx = 0
        for waypoint1, waypoint2 in zip(
            [self.position] + self.waypoints, self.waypoints + [self.position]
        ):
            for point in self.calculate_path(
                center_of_tile(*waypoint1), center_of_tile(*waypoint2)
            ):
                self.path.append(center_of_tile(*point))
        self.pathshape = arcade.create_line_strip(
            self.path + self.path[:1], self.pathcolor, 2
        )

    def move_one_square(self):
        """
        Moves the enemy forward one unit along his path
        Returns True if more moves left
        """
        if self.movesleft > 0:
            self.pathidx += 1
            self.pathidx %= len(self.path)
            self.position = self.path[self.pathidx]
            self.movesleft -= 1
            self.update_vision()
        return self.movesleft > 0

    def update_direction(self):
        """
        Changes the direction the enemy is facing to face the next path location
        """
        nextposition = self.path[(self.pathidx + 1) % len(self.path)]
        basedirection = nextposition - self.position
        if basedirection[1] > 0:
            self.direction = Direction.NORTH
        elif basedirection[1] < 0:
            self.direction = Direction.SOUTH
        elif basedirection[0] > 0:
            self.direction = Direction.EAST
        elif basedirection[0] < 0:
            self.direction = Direction.WEST
        self.update_vision()

    def update_vision(self):
        self.vision_points = []
        for visiondistance in range(1, self.maxvision + 1):
            visionpoint = self.position + self.direction * visiondistance * TILE_SIZE
            if arcade.get_sprites_at_exact_point(visionpoint, self._walls):
                break
            self.vision_points.append(visionpoint)

    def update(self):
        self.movesleft = self.movecount

    def draw_vision(self):
        for vision_point in self.vision_points:
            arcade.draw_rectangle_filled(
                center_x=vision_point[0],
                center_y=vision_point[1],
                width=TILE_SIZE,
                height=TILE_SIZE,
                color=(220, 220, 79, 200),
            )

    def check_los_collision(self, sprite: arcade.Sprite) -> bool:
        pos = sprite.position
        return any(pos.x == v.x and pos.y == v.y for v in self.vision_points)
