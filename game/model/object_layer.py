from dataclasses import dataclass
from typing import Optional


@dataclass
class Object:
    name: str
    type: str
    x: float
    y: float
    width: float
    height: float


@dataclass
class ObjectLayer:
    name: str
    type: Optional[str]
    object_count: int
    objects: list[Object]
