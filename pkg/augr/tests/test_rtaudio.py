from loguru import logger

from crunge.augr import RtAudio


def test_rtaudio():
    rt_audio = RtAudio()
    logger.debug(rt_audio.get_device_count())

if __name__ == '__main__':
    test_rtaudio()
