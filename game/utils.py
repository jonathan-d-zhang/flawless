from __future__ import annotations
from typing import NamedTuple, Union
from .model.object_layer import Object, ObjectLayer

from .constants import *

from xml.dom import minidom

Coordinate = dict[str, float]

# Map Height in grid spaces - Set in __main__, used by tile_pos_to_arcade to convert from tile to arcade positions
map_height = None


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> Vector:
        return Vector(scalar * self.x, scalar * self.y)

    def __getitem__(self, key):
        if key in (0, "x"):
            return self.x
        elif key in (1, "y"):
            return self.y
        else:
            raise IndexError

    __rmul__ = __mul__


class Direction:
    NORTH = Vector(0, 1)
    EAST = Vector(1, 0)
    SOUTH = Vector(0, -1)
    WEST = Vector(-1, 0)


def center_of_tile(x: int, y: int) -> Vector:
    """
    Get the exact center of the tile that co-ords xy is contained in.
    :return: The exact center (x, y)
    """
    return Vector(
        ((x // TILE_SIZE) * TILE_SIZE) + TILE_SIZE // 2,
        ((y // TILE_SIZE) * TILE_SIZE) + TILE_SIZE // 2,
    )


def tiled_pos_to_arcade(x: float, y: float) -> Vector:
    """
    Converts Tile style pixel locations ((0, 0) in upper left) to
    arcade style pixel locations ((0,0) in lower left)
    """
    newx = x * TILE_SPRITE_SCALING + TILE_SIZE // 2
    newy = map_height * TILE_SIZE - y * TILE_SPRITE_SCALING - TILE_SIZE // 2
    return center_of_tile(newx, newy)


def process_objects(file_path: str) -> dict[str, list[ObjectLayer]]:
    """
    Reads the .tmx file that the tile information is stored in and process the object information into
    a list of ObjectLayers
    :return: A dictionary of object types and a list of those objects
    """

    entities: dict[str, list[ObjectLayer]] = {"guard": [], "key": []}

    file = minidom.parse(file_path)
    objects = file.getElementsByTagName("objectgroup")

    for i in objects:

        object_layer = ObjectLayer(
            name=i.getAttribute("name"), objects=[], object_count=0, type=None
        )

        child_object_elements = i.getElementsByTagName("object")

        for x in child_object_elements:
            object_layer.object_count += 1

            object_infomation = Object(
                name=x.getAttribute("name"),
                type=x.getAttribute("type"),
                x=float(x.getAttribute("x")),
                y=float(x.getAttribute("y")),
                width=float(x.getAttribute("width")),
                height=float(x.getAttribute("height")),
            )

            object_layer.objects.append(object_infomation)

        property = i.getElementsByTagName("property")

        for x in property:
            if (
                x.getAttribute("name") == "type"
                and x.getAttribute("value") in entities.keys()
            ):
                entities[x.getAttribute("value")].append(object_layer)
                object_layer.type = x.getAttribute("value")

    return entities


def extract_locations(
    layer_data: ObjectLayer,
) -> dict[str, Union[Vector, list[Vector]]]:
    """
    Extract locations for each different entity.
    """
    locations = {"spawn": None, "waypoints": []}

    waypoints = {}

    for i in layer_data.objects:
        if i.type == "spawn":
            locations["spawn"] = tiled_pos_to_arcade(i.x, i.y)

        elif i.type == "point":
            waypoints[int(i.name)] = tiled_pos_to_arcade(i.x, i.y)

    locations["waypoints"] = [x[1] for x in sorted(waypoints.items())]

    return locations
