from __future__ import annotations
from typing import NamedTuple, Union
from model.object_layer import Object, ObjectLayer

from constants import *

from xml.dom import minidom

Coordinate = dict[str, float]

class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> Vector:
        return Vector(scalar * self.x, scalar * self.y)

    __rmul__ = __mul__


def center_of_tile(x: int, y: int) -> Vector:
    """
    Get the exact center of the tile that co-ords xy is contained in.
    :return: The exact center (x, y)
    """
    return Vector(
        ((x // TILE_SIZE) * TILE_SIZE) + TILE_SIZE // 2,
        ((y // TILE_SIZE) * TILE_SIZE) + TILE_SIZE // 2,
    )


def process_objects(file_path: str) -> dict[str, list[ObjectLayer]]:
    """
    Reads the .tmx file that the tile infomation is stored in and process the object infomation into
    a list of ObjectLayers
    :return: A dictionary of object types and a list of those objects
    """

    entitys: dict[str, list[ObjectLayer]] = {"guard": [], "key": []}

    file = minidom.parse(file_path)
    objects = file.getElementsByTagName("objectgroup")

    for i in objects:

        object_layer = ObjectLayer(
            name=i.getAttribute("name"), objects=[], object_count=0
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
            if x.getAttribute('name') == 'type' and x.getAttribute('value') in entitys.keys():
                entitys[x.getAttribute('value')].append(object_layer)

    return entitys


def extract_guard_locations(
    layer_data: ObjectLayer,
) -> dict[str, Union[Coordinate, list[Coordinate]]]:
    """
    Extracts the infomation that can be generated from process_objects about the guards spawn location and the
    waypoints it must patrol
    :return: dictionary containing spawn (dict) and waypoints (list of dicts)
    """

    locations = {"spawn": {"x": 0, "y": 0}, "waypoints": []}

    locations["waypoints"] = [None for i in range(layer_data.object_count - 1)]

    for i in layer_data.objects:
        if i.type == "spawn":
            locations["spawn"]["x"] = i.x
            locations["spawn"]["y"] = i.y

        if i.type == "point":
            locations["waypoints"][int(i.name)] = {"x": i.x, "y": i.y}

    return locations
