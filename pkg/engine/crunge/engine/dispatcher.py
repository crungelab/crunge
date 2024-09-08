from typing import TypeAlias

from crunge import sdl

from loguru import logger

from .base import Base

DispatchResult: TypeAlias = bool | None

class Dispatcher(Base):
    EVENT_HANDLED = True
    EVENT_UNHANDLED = None

    def dispatch(self, event) -> DispatchResult:
        #logger.debug(event)
        #logger.debug(event.type)
        match event.__class__:
            case sdl.WindowEvent:
                return self.on_window(event)
            case sdl.TextInputEvent:
                return self.on_text(event)
            case sdl.KeyboardEvent:
                return self.on_key(event)
            case sdl.MouseMotionEvent:
                return self.on_mouse_motion(event)
            case sdl.MouseButtonEvent:
                return self.on_mouse_button(event)
            case sdl.MouseWheelEvent:
                return self.on_mouse_wheel(event)

    def on_window(self, event: sdl.WindowEvent):
        #logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_MOUSE_ENTER:
                self.on_mouse_enter(event)
            case sdl.EventType.WINDOW_MOUSE_LEAVE:
                self.on_mouse_leave(event)
            case _:
                pass
    
    def on_text(self, event: sdl.TextInputEvent):
        #logger.debug(f"text: {event.text}")
        pass

    def on_key(self, event: sdl.KeyboardEvent):
        #logger.debug(f"key: {event.key}")
        pass

    def on_mouse_enter(self, event: sdl.WindowEvent):
        #logger.debug("mouse enter")
        pass

    def on_mouse_leave(self, event: sdl.WindowEvent):
        #logger.debug("mouse leave")
        pass

    def on_mouse_motion(self, event: sdl.MouseMotionEvent) -> DispatchResult:
        #logger.debug(f"mouse motion: x={event.x}, y={event.y}")
        pass

    def on_mouse_button(self, event: sdl.MouseButtonEvent) -> DispatchResult:
        #logger.debug(f"mouse button: button={event.button}, state={event.state}")
        pass

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent) -> DispatchResult:
        #logger.debug(f"mouse wheel: x={event.x}, y={event.y}")
        pass
