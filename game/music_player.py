import arcade
import time

from typing import Optional

from .config import CONFIG


class MusicPlayer:
    def __init__(self):
        self.song_list: list[str] = [
            "game/assets/music/background_01.wav",
            "game/assets/music/background_02.wav",
        ]
        self.song_index: int = 0
        self.current_player = None
        self.music: Optional[arcade.Sound] = None

    def play_song(self):
        if CONFIG.is_music_on:
            i = CONFIG.music_volume / 30
            self.music = arcade.Sound(self.song_list[self.song_index], streaming=True)
            self.current_player = self.music.play(volume=i)

            # because position is reset to 0 when a song finishes, there is a small
            # window where it is impossible to determine if a song has just finished
            # or just started. sleep for a small period to be sure if a song has finished
            time.sleep(0.03)

    def update(self):
        if self.music:
            position = self.music.get_stream_position(self.current_player)

            if position == 0:
                self.song_index = (self.song_index + 1) % len(self.song_list)
                self.play_song()
        else:
            self.play_song()

    def stop(self):
        if self.music:
            self.music.stop(self.current_player)
        self.music = None
