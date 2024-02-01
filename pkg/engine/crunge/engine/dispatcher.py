from crunge import sdl

from loguru import logger

from .base import Base

class Dispatcher(Base):
    def __init__(self) -> None:
        pass

    def dispatch(self, event):
        #logger.debug(event)
        match event.__class__:
            case sdl.QuitEvent:
                return False
            case sdl.WindowEvent:
                self.on_window(event)
            case sdl.KeyboardEvent:
                self.on_key(event)
            case sdl.MouseMotionEvent:
                self.on_mouse_motion(event)
            case sdl.MouseButtonEvent:
                self.on_mouse_button(event)
            case sdl.MouseWheelEvent:
                self.on_mouse_wheel(event)
            case _:
                pass
        return True

    def on_window(self, event: sdl.WindowEvent):
        #logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_MOUSE_ENTER:
                self.on_mouse_enter(event)
            case sdl.EventType.WINDOW_MOUSE_LEAVE:
                self.on_mouse_leave(event)
            case _:
                pass
    
    def on_key(self, event: sdl.KeyboardEvent):
        #logger.debug(f"key: {event.keysym.sym}")
        pass

    def on_mouse_enter(self, event: sdl.WindowEvent):
        #logger.debug("mouse enter")
        pass

    def on_mouse_leave(self, event: sdl.WindowEvent):
        #logger.debug("mouse leave")
        pass

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        #logger.debug(f"mouse motion: x={event.x}, y={event.y}")
        pass

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        #logger.debug(f"mouse button: button={event.button}, state={event.state}")
        pass

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        #logger.debug(f"mouse wheel: x={event.x}, y={event.y}")
        pass
