import pyo

print("Host APIs:")
host_apis = pyo.pa_get_host_apis()
for i, api in enumerate(host_apis):
    print(f"  {i}: {api}")

print("\nDevices:")
devices = pyo.pa_get_devices()
for i, dev in enumerate(devices):
    print(f"  {i}: {dev}")

print("\nDefault input index:", pyo.pa_get_default_input())
print("Default output index:", pyo.pa_get_default_output())

# Try to boot with the default config, but catch the error instead of segfaulting
try:
    s = pyo.Server().boot()
    print("Booted server, output device:", s.getOutputDevice())
except Exception as e:
    print("Server().boot() raised:", repr(e))
