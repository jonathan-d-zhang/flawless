from __future__ import annotations
from typing import NamedTuple, Union
from model.object_layer import Object, ObjectLayer

from constants import *

from xml.dom import minidom


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
                and x.getAttribute("value") in entitys.keys()
            ):
                entitys[x.getAttribute("value")].append(object_layer)
                object_layer.type = x.getAttribute("value")

    return entitys


def extract_locations(
    layer_data: ObjectLayer,
) -> dict[str, Union[Vector, list[Vector]]]:
    """
    Extract locations for each different entity.
    """

    locations = {"spawn": None}

    for object in layer_data.objects:
        if object.type == "spawn":
            locations["spawn"] = Vector(object.x, object.y)

        if object.type == "point":

            if not "waypoints" in locations.keys():
                locations["waypoints"] = [None for _ in range(layer_data.object_count - 1)]

            locations["waypoints"][int(object.name)] = Vector(object.x, object.y)

    return locations
