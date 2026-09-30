from loguru import logger

from crunge.rtaudio import RtAudio


def test_rtaudio():
    audio = RtAudio()
    logger.debug(audio.get_device_count())

if __name__ == '__main__':
    test_rtaudio()
