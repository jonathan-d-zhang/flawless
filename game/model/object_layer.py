from dataclasses import dataclass


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
    object_count: int
    objects: list[Object]
