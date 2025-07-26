import signal
import traceback
import sys

def handle_sigtrap(signum, frame):
    print(f"Received signal: {signum}")
    traceback.print_stack(frame)
    sys.exit(1)

signal.signal(signal.SIGTRAP, handle_sigtrap)
