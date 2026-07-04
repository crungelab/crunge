import pyo

print("Host APIs:")
pyo.pa_list_host_apis()

print("\nDevices:")
pyo.pa_list_devices()

print("\nDefault input index:", pyo.pa_get_default_input())
print("Default output index:", pyo.pa_get_default_output())

# Try to boot with the default config, but catch the error instead of segfaulting
try:
    s = pyo.Server().boot()
    print("Booted server, output device:", s.getOutputDevice())
except Exception as e:
    print("Server().boot() raised:", repr(e))
