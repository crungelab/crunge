from loguru import logger

from crunge.rtaudio import RtAudio


audio = RtAudio()
logger.debug(audio.get_device_count())
