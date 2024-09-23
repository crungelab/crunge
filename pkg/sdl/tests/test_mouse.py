from pathlib import Path

from loguru import logger

from crunge import sdl

'''
PYCLASS_BEGIN(_sdl, SDL_MouseMotionEvent, MouseMotionEvent)
    MouseMotionEvent.def_readwrite("type", &SDL_MouseMotionEvent::type);
    MouseMotionEvent.def_readwrite("timestamp", &SDL_MouseMotionEvent::timestamp);
    MouseMotionEvent.def_readwrite("window_id", &SDL_MouseMotionEvent::windowID);
    MouseMotionEvent.def_readwrite("which", &SDL_MouseMotionEvent::which);
    MouseMotionEvent.def_readwrite("state", &SDL_MouseMotionEvent::state);
    MouseMotionEvent.def_readwrite("x", &SDL_MouseMotionEvent::x);
    MouseMotionEvent.def_readwrite("y", &SDL_MouseMotionEvent::y);
    MouseMotionEvent.def_readwrite("xrel", &SDL_MouseMotionEvent::xrel);
    MouseMotionEvent.def_readwrite("yrel", &SDL_MouseMotionEvent::yrel);
PYCLASS_END(_sdl, SDL_MouseMotionEvent, MouseMotionEvent)
'''

'''
PYCLASS_BEGIN(_sdl, SDL_MouseButtonEvent, MouseButtonEvent)
    MouseButtonEvent.def_readwrite("type", &SDL_MouseButtonEvent::type);
    MouseButtonEvent.def_readwrite("timestamp", &SDL_MouseButtonEvent::timestamp);
    MouseButtonEvent.def_readwrite("window_id", &SDL_MouseButtonEvent::windowID);
    MouseButtonEvent.def_readwrite("which", &SDL_MouseButtonEvent::which);
    MouseButtonEvent.def_readwrite("button", &SDL_MouseButtonEvent::button);
    MouseButtonEvent.def_readwrite("state", &SDL_MouseButtonEvent::state);
    MouseButtonEvent.def_readwrite("clicks", &SDL_MouseButtonEvent::clicks);
    MouseButtonEvent.def_readwrite("padding", &SDL_MouseButtonEvent::padding);
    MouseButtonEvent.def_readwrite("x", &SDL_MouseButtonEvent::x);
    MouseButtonEvent.def_readwrite("y", &SDL_MouseButtonEvent::y);
PYCLASS_END(_sdl, SDL_MouseButtonEvent, MouseButtonEvent)
'''

'''
PYCLASS_BEGIN(_sdl, SDL_MouseWheelEvent, MouseWheelEvent)
    MouseWheelEvent.def_readwrite("type", &SDL_MouseWheelEvent::type);
    MouseWheelEvent.def_readwrite("timestamp", &SDL_MouseWheelEvent::timestamp);
    MouseWheelEvent.def_readwrite("window_id", &SDL_MouseWheelEvent::windowID);
    MouseWheelEvent.def_readwrite("which", &SDL_MouseWheelEvent::which);
    MouseWheelEvent.def_readwrite("x", &SDL_MouseWheelEvent::x);
    MouseWheelEvent.def_readwrite("y", &SDL_MouseWheelEvent::y);
    MouseWheelEvent.def_readwrite("direction", &SDL_MouseWheelEvent::direction);
    MouseWheelEvent.def_readwrite("mouse_x", &SDL_MouseWheelEvent::mouseX);
    MouseWheelEvent.def_readwrite("mouse_y", &SDL_MouseWheelEvent::mouseY);
PYCLASS_END(_sdl, SDL_MouseWheelEvent, MouseWheelEvent)
'''

success = sdl.init(sdl.InitFlags.INIT_VIDEO)
logger.debug(f"SDL_Init: {success}")

sdl.create_window("Test Keyboard", 640, 480, sdl.WindowFlags.RESIZABLE)

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
            case sdl.MouseMotionEvent:
                logger.debug(f"mouse motion: x={event.x}, y={event.y}")
            case sdl.MouseButtonEvent:
                logger.debug(f"mouse button: button={event.button}, down={event.down}")
            case sdl.MouseWheelEvent:
                logger.debug(f"mouse wheel: x={event.x}, y={event.y}")
            case _:
                pass
