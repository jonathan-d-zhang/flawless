from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


@dataclass
class _Config:
    is_music_on: bool = True
    music_volume: int = 5


CONFIG = _Config()
