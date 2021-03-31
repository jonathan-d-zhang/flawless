import random

import arcade

from constants import TILE_SIZE
from utils import Vector, center_of_tile

class Enemy(arcade.Sprite):
    def __init__(self, walls, locations, *args, **kwargs):
        super().__init__("assets/sprites/enemy.png", 1, *args, **kwargs)
        self._walls = walls
        self.center_x = int(locations['spawn']['x'])
        self.center_y = int(locations['spawn']['y'])
        self.waypoints = locations['waypoints']
        self.create_full_path()

    @property
    def position(self) -> Vector:
        return Vector(int(self.center_x), int(self.center_y))

    @position.setter
    def position(self, pos):
        self.center_x, self.center_y = pos

    def calculate_path(self, waypoint1, waypoint2):
        pos_x, pos_y = waypoint1
        yield pos_x, pos_y
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
        for waypoint1, waypoint2 in zip([self.position] + self.waypoints,
                                        self.waypoints + [self.position]):
            for point in self.calculate_path(center_of_tile(*waypoint1),
                                             center_of_tile(*waypoint2)):
                self.path.append(center_of_tile(*point))

    def move_along_path(self):
        self.pathidx += 1
        self.pathidx %= len(self.path)
        self.center_x, self.center_y = self.path[self.pathidx]

    def update(self):
        self.move_along_path()

    def draw_path(self):
        if self.path: #TODO: Paths don't go through center of the tiles
            arcade.draw_line_strip(self.path + self.path[:1], arcade.color.BLUE, 2) #TODO: Get different colors for each guard's path
