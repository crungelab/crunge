from crunge.rtaudio import RtAudio

audio = RtAudio()

ids = audio.get_device_ids()

if len(ids) == 0:
    print("No devices found.")
else:
    for device_id in ids:
        info = audio.get_device_info(device_id)
        print(f"device name = {info.name}")
        print(f": maximum output channels = {info.output_channels}")