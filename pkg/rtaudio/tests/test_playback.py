import time
from crunge.rtaudio import (
    RtAudio,
    AudioFormat,
    RtAudioStreamParameters,
    AudioStreamStatus,
    AudioErrorType,
    AudioStream,
)

last_values = [0.0, 0.0]

def saw(output_buffer, input_buffer, n_frames, stream_time, status):
    if status:
        print("Stream underflow detected!")
    # output_buffer is a (256, 2) numpy array
    for i in range(n_frames):
        for j in range(2):
            output_buffer[i, j] = last_values[j]
            last_values[j] += 0.005 * (j + 1 + (j * 0.1))
            if last_values[j] >= 1.0:
                last_values[j] -= 2.0
    return 0

dac = RtAudio()

ids = dac.get_device_ids()
if len(ids) == 0:
    print("No audio devices found!")
    exit(0)

output_device_id = dac.get_default_output_device()
output_device_info = dac.get_device_info(output_device_id)
print(f"Output device info: {output_device_info}")

output_parameters = RtAudioStreamParameters(
    device_id=output_device_id,
    n_channels=2,
    first_channel=0,
)

sample_rate = 44100
buffer_frames = 256

stream = AudioStream(
    dac=dac,
    output_parameters=output_parameters,
    input_parameters=None,
    format=AudioFormat.FLOAT64,
    sample_rate=sample_rate,
    buffer_frames=buffer_frames,
    callback=saw,
)

print(stream)

err = stream.open()
print("\n")
print(f"buffer frames = {buffer_frames}")
print(f"error code = {err}")
if err != AudioErrorType.RTAUDIO_NO_ERROR:
    print(f"Error opening stream: {dac.get_error_text()}")
    print(dac.get_error_text())
    exit(0)

print("Starting stream ...")

#err = dac.start_stream()
err = stream.start()

if err != AudioErrorType.RTAUDIO_NO_ERROR:
    print(dac.get_error_text())
    if dac.is_stream_open():
        dac.close_stream()
    exit(0)

print("\nPlaying ... press <enter> to quit.")
input()

if dac.is_stream_running():
    dac.stop_stream()

if dac.is_stream_open():
    dac.close_stream()