from __future__ import annotations
from typing import NamedTuple

from constants import *


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
