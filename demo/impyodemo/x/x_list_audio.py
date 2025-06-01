import pyo

print("Audio host APIS:")
pyo.pa_list_host_apis()
pyo.pa_list_devices()
print("Default input device: %i" % pyo.pa_get_default_input())
print("Default output device: %i" % pyo.pa_get_default_output())
