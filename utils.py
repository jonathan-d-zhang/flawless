from typing import Tuple
from constant import *


def center_of_tile(x: int, y: int) -> Tuple[int, int]:
    """
    Get the exact center of the tile that co-ords xy is contained in.
    :return: The exact center (x, y)
    """
    return (
        ((x // TILE_SIZE) * TILE_SIZE) + TILE_SIZE // 2,
        ((y // TILE_SIZE) * TILE_SIZE) + TILE_SIZE // 2,
    )
