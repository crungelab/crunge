from crunge.augr import RtAudio

audio = RtAudio()

apis = audio.get_compiled_api()
print(apis)