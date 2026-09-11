# __main__.py
import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main(prog="python -m crunge.mia"))