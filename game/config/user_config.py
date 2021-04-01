from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _Config:
    is_music_on: bool = True
    music_volume: int = 5
    is_fullscreen: bool = False


CONFIG = _Config()
