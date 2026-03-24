import time
from crunge.rtaudio import (
    RtAudio,
    RtAudioFormat,
    RtAudioStreamParameters,
    RtAudioStreamStatus,
    RtAudioErrorType,
)

last_values = [0.0, 0.0]

"""
typedef std::function<int(void* outputBuffer, void* inputBuffer,
                          unsigned int nFrames,
                          double streamTime,
                          RtAudioStreamStatus status,
                          void* userData)> RtAudioCallback;
"""

def saw(output_buffer, input_buffer, n_frames, stream_time, status, user_data):
    print(type(output_buffer))
    print(repr(output_buffer))
    if status:
        print("Stream underflow detected!")

    for i in range(n_frames):
        for j in range(2):
            output_buffer[i * 2 + j] = last_values[j]
            last_values[j] += 0.005 * (j + 1 + (j * 0.1))
            if last_values[j] >= 1.0:
                last_values[j] -= 2.0

    return 0

dac = RtAudio()

ids = dac.get_device_ids()
if len(ids) == 0:
    print("No audio devices found!")
    exit(0)

parameters = RtAudioStreamParameters(
    device_id=dac.get_default_output_device(),
    n_channels=2,
    first_channel=0,
)

sample_rate = 44100
buffer_frames = 256

err, buffer_frames = dac.open_stream(
    parameters,
    None,
    RtAudioFormat.FLOAT64,
    sample_rate,
    buffer_frames,
    saw,
    None,
    None,
)

print(f"\nbuffer frames = {buffer_frames}")
print(f"error code = {err}")
if err != RtAudioErrorType.RTAUDIO_NO_ERROR:
    print(dac.get_error_text())
    exit(0)

print("Starting stream ...")

err = dac.start_stream()
if err != RtAudioErrorType.RTAUDIO_NO_ERROR:
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