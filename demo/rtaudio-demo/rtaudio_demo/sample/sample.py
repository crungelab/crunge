from pathlib import Path

from loguru import logger
import soundfile as sf
import numpy as np

from crunge.rtaudio import (
    RtAudioStreamParameters,
    AudioFormat,
    AudioErrorType,
    AudioStream,
)

from ..trial import Trial

ASSETS_DIR = Path(__file__).parent.parent / "assets"
WAV_PATH = ASSETS_DIR / "mixkit-cinematic-laser-gun-thunder-1287.wav"

N_CHANNELS = 2
BUFFER_FRAMES = 256


def load_sample(path: Path, n_channels: int) -> tuple[np.ndarray, int]:
    """Load a sound file as float32, shaped (frames, n_channels)."""
    data, samplerate = sf.read(path, dtype="float32", always_2d=True)
    if data.shape[1] == 1 and n_channels > 1:
        data = np.repeat(data, n_channels, axis=1)
    elif data.shape[1] > n_channels:
        data = data[:, :n_channels]
    return np.ascontiguousarray(data), samplerate


class SamplePlayer:
    """Feeds a preloaded buffer to the stream, then signals end-of-stream."""

    def __init__(self, data: np.ndarray):
        self.data = data
        self.playhead = 0

    def __call__(self, out_buffer, input_buffer, n_frames, stream_time, status):
        chunk = self.data[self.playhead:self.playhead + n_frames]
        n = len(chunk)
        out_buffer[:n] = chunk
        out_buffer[n:] = 0
        self.playhead += n
        # 0 = keep going, 1 = drain remaining output and stop
        return 0 if n == n_frames else 1


class SampleTrial(Trial):
    def run(self):
        logger.info("Running SampleTrial")
        audio = self.audio

        if len(audio.get_device_ids()) == 0:
            logger.error("No audio devices found!")
            return

        data, sample_rate = load_sample(WAV_PATH, N_CHANNELS)
        logger.info(f"Loaded {WAV_PATH.name}: {len(data)} frames @ {sample_rate} Hz")

        output_device_id = audio.get_default_output_device()
        logger.info(f"Output device: {audio.get_device_info(output_device_id)}")

        output_parameters = RtAudioStreamParameters(
            device_id=output_device_id,
            n_channels=N_CHANNELS,
            first_channel=0,
        )

        stream = AudioStream(
            audio=audio,
            output_parameters=output_parameters,
            input_parameters=None,
            format=AudioFormat.FLOAT32,
            sample_rate=sample_rate,
            buffer_frames=BUFFER_FRAMES,
            callback=SamplePlayer(data),
        )

        err = stream.open()
        if err != AudioErrorType.RTAUDIO_NO_ERROR:
            logger.error(f"Error opening stream: {audio.get_error_text()}")
            return

        try:
            err = stream.start()
            if err != AudioErrorType.RTAUDIO_NO_ERROR:
                logger.error(f"Error starting stream: {audio.get_error_text()}")
                return

            print("\nPlaying ... press <enter> to quit.")
            input()
        finally:
            if audio.is_stream_running():
                audio.stop_stream()
            if audio.is_stream_open():
                audio.close_stream()


def main():
    SampleTrial().run()


if __name__ == "__main__":
    main()