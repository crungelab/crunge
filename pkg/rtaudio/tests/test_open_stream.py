from crunge.rtaudio import (
    RtAudio,
    RtAudioFormat,
    RtAudioStreamParameters,
    RtAudioStreamOptions,
    RtAudioStreamFlags,
    RtAudioErrorType,
)

dac = RtAudio()

ids = dac.get_device_ids()
if len(ids) == 0:
    exit(0)

parameters = RtAudioStreamParameters(
    device_id=dac.get_default_output_device(), n_channels=2
)

sample_rate = 44100
buffer_frames = 256

options = RtAudioStreamOptions(flags=RtAudioStreamFlags.NONINTERLEAVED)


def my_callback(output_buffer, input_buffer, n_frames, stream_time, status):
    print("callback called")
    return 0


err, buffer_frames = dac.open_stream(
    parameters,
    None,
    RtAudioFormat.FLOAT32,
    sample_rate,
    buffer_frames,
    my_callback,
    None,
    options,
)
if err != RtAudioErrorType.RTAUDIO_NO_ERROR:
    print(dac.get_error_text())
    exit(0)
