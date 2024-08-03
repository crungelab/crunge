from pathlib import Path

from loguru import logger

from crunge import sdl

success = sdl.init(sdl.InitFlags.INIT_VIDEO)
logger.debug(f"SDL_Init: {success}")
