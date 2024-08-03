from pathlib import Path

from loguru import logger

from crunge import sdl

success = sdl.init(sdl.InitFlags.INIT_VIDEO)
logger.debug(f"SDL_Init: {success}")

window = sdl.create_window("Test Properties", 640, 480, 0)

properties = sdl.get_window_properties(window)

logger.debug(f"window properties: {properties}")

# Display
display = sdl.get_property(properties, "SDL.window.x11.display", None)
logger.debug(f"display: {display}")

display = sdl.get_property(properties, sdl.WindowProperties.X11_DISPLAY_POINTER, None)
logger.debug(f"display: {display}")

# Window Handle
hwnd = sdl.get_number_property(properties, "SDL.window.x11.window", 0)
logger.debug(f"hwnd: {hwnd}")

hwnd = sdl.get_number_property(properties, sdl.WindowProperties.X11_WINDOW_NUMBER, 0)
logger.debug(f"hwnd: {hwnd}")