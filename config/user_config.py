from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Setting(Enum):
    music = "music_setting"
    music_volume = "music_volume"


class MusicSetting(Enum):
    OFF = False
    ON = True


@dataclass
class _Config:
    music_setting: MusicSetting = MusicSetting.ON
    music_volume: int = 5


CONFIG = _Config()
