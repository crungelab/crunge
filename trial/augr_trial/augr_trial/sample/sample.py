from pathlib import Path

from loguru import logger
import soundfile as sf
import numpy as np

from crunge.augr import (
    RtAudio,
    RtAudioStreamParameters,
    AudioFormat,
    AudioStreamStatus,
    AudioErrorType,
    AudioStream,
)

from ..trial import Trial

ASSETS_DIR = Path(__file__).parent.parent / "assets"

wav_path = ASSETS_DIR / "mixkit-cinematic-laser-gun-thunder-1287.wav"

data, samplerate = sf.read(wav_path, dtype='float32')
playhead = 0

def audio_callback(out_buffer, input_buffer, n_frames, stream_time, status):
    global playhead
    chunk = data[playhead:playhead + n_frames]
    out_buffer[:] = chunk
    playhead += n_frames
    return 0

class SampleTrial(Trial):
    def run(self):
        logger.info("Running SampleTrial")
        audio = self.audio
        ids = audio.get_device_ids()
        if len(ids) == 0:
            print("No audio devices found!")
            exit(0)

        output_device_id = audio.get_default_output_device()
        output_device_info = audio.get_device_info(output_device_id)
        print(f"Output device info: {output_device_info}")

        output_parameters = RtAudioStreamParameters(
            device_id=output_device_id,
            n_channels=2,
            first_channel=0,
        )

        sample_rate = 44100
        buffer_frames = 256

        stream = AudioStream(
            audio=audio,
            output_parameters=output_parameters,
            input_parameters=None,
            format=AudioFormat.FLOAT64,
            sample_rate=sample_rate,
            buffer_frames=buffer_frames,
            callback=audio_callback,
        )

        print(stream)

        err = stream.open()
        print("\n")
        print(f"buffer frames = {buffer_frames}")
        print(f"error code = {err}")
        if err != AudioErrorType.RTAUDIO_NO_ERROR:
            print(f"Error opening stream: {audio.get_error_text()}")
            print(audio.get_error_text())
            exit(0)

        print("Starting stream ...")

        #err = dac.start_stream()
        err = stream.start()

        if err != AudioErrorType.RTAUDIO_NO_ERROR:
            print(audio.get_error_text())
            if audio.is_stream_open():
                audio.close_stream()
            exit(0)

        print("\nPlaying ... press <enter> to quit.")
        input()

        if audio.is_stream_running():
            audio.stop_stream()

        if audio.is_stream_open():
            audio.close_stream()


def main():
    SampleTrial().run()


if __name__ == "__main__":
    main()
