from pathlib import Path

from loguru import logger

from crunge.rtaudio import RtAudio


class Trial:
    def __init__(self):
        self.audio = RtAudio()

    def run(self):
        pass
