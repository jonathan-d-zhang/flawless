import random

import arcade

from constants import TILE_SIZE
from utils import Vector

# Location Example {'spawn': {'x': 144.0, 'y': 64.0}, 'waypoints': [{'x': 136.0, 'y': 88.0}, {'x': 136.0, 'y': 192.0}]}
class Enemy(arcade.Sprite):
    def __init__(self, walls, locations, *args, **kwargs):
        super().__init__("assets/sprites/enemy.png", 1, *args, **kwargs)
        self._walls = walls
        self.center_x = int(locations['spawn']['x'])
        self.center_y = int(locations['spawn']['y'])
        self.waypoints = locations['waypoints']
        self.create_path()

    @property
    def position(self) -> Vector:
        return Vector(int(self.center_x), int(self.center_y))

    @position.setter
    def position(self, pos):
        self.center_x, self.center_y = pos

    def _move_randomly(self):
        while True:
            original_pos = self.center_x, self.center_y
            val = TILE_SIZE if random.randint(0, 1) else -TILE_SIZE

            if random.randint(0, 1):
                self.center_x += val
            else:
                self.center_y += val

            if not arcade.check_for_collision_with_list(self, self._walls):
                break
            else:
                self.center_x, self.center_y = original_pos

    def create_path(self):
        """
        Creates a looping path through all way points
        and back to the starting position
        """
        self.barrierlist = arcade.AStarBarrierList(
                moving_sprite=self,
                blocking_sprites=self._walls,
                grid_size=TILE_SIZE,
                left=-10 * TILE_SIZE, #TODO CORRECT MAP EDGES
                right=280 * TILE_SIZE,
                bottom=-10 * TILE_SIZE,
                top=280 * TILE_SIZE)
        self.path = []
        self.pathidx = 0
        print("pos/waypoints", self.position, self.waypoints)
        for waypoint1, waypoint2 in zip([self.position] + self.waypoints,
                                        self.waypoints + [self.position]):
            print("pathing", waypoint1, waypoint2)
            a = arcade.astar_calculate_path(
                waypoint1,
                waypoint2,
                self.barrierlist,
                diagonal_movement=False)
            print(self.path, a)
            if a:  #TODO Why are some paths returning None? Assuming no path found, but why?
                self.path.extend(a)
        print(self.path)

    def move_along_path(self):
        self.pathidx += 1
        self.pathidx %= len(self.path)
        self.center_x, self.center_y = self.path[self.pathidx]

    def update(self):
        self.move_along_path()

    def draw_path(self):
        if self.path: #TODO: Paths don't go through center of the tiles
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2) #TODO: Get different colors for each guard's path
