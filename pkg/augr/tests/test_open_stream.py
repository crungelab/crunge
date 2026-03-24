from crunge.augr import (
    RtAudio,
    RtAudioStreamParameters,
    RtAudioStreamOptions,
    AudioErrorType,
    AudioFormat,
    AudioStreamFlags,
    AudioStream,
)

dac = RtAudio()

ids = dac.get_device_ids()
if len(ids) == 0:
    exit(0)

output_parameters = RtAudioStreamParameters(
    device_id=dac.get_default_output_device(), n_channels=2
)

sample_rate = 44100
buffer_frames = 256

options = RtAudioStreamOptions(flags=AudioStreamFlags.NONINTERLEAVED)


def my_callback(output_buffer, input_buffer, n_frames, stream_time, status):
    print("callback called")
    return 0

stream = AudioStream(
    dac=dac,
    output_parameters=output_parameters,
    input_parameters=None,
    format=AudioFormat.FLOAT32,
    sample_rate=sample_rate,
    buffer_frames=buffer_frames,
    callback=my_callback,
    options=options,
)

print(stream)

err = stream.open()

if err != AudioErrorType.RTAUDIO_NO_ERROR:
    print(dac.get_error_text())
    exit(0)
