from pathlib import Path

from loguru import logger

from crunge import sdl

success = sdl.init(sdl.InitFlags.INIT_VIDEO)
logger.debug(f"SDL_Init: {success}")

sdl.create_window("Hello World", 640, 480, 0)

'''
running = True
while running:
    #logger.debug("running...")
    while event := sdl.poll_event():
        logger.debug("polling event...")
        logger.debug(event)
        logger.debug(event.type)

        if event.type == sdl.EventType.QUIT:
            running = False
'''

'''
running = True
while running:
    #logger.debug("running...")
    while event := sdl.poll_event():
        logger.debug("polling event...")
        logger.debug(event)
        logger.debug(event.type)
        match event:
            case sdl.QuitEvent():
                running = False
            case _:
                pass
'''

running = True
while running:
    #logger.debug("running...")
    while event := sdl.poll_event():
        logger.debug("polling event...")
        logger.debug(event)
        logger.debug(event.type)
        match event.__class__:
            case sdl.QuitEvent:
                running = False
            case sdl.KeyboardEvent:
                logger.debug(f"key: {event.keysym.sym}")
            case _:
                pass
