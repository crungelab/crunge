from crunge.augr import RtAudio

dac = RtAudio()

apis = dac.get_compiled_api()
print(apis)