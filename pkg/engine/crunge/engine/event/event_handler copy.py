# event_handler.py
from loguru import logger

import glm

from crunge import sdl
from crunge.core.dispatch import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED

from .input import Input

class EventHandler:
    """Demux an SDL event to an on_* handler. No tree, no super() chain."""

    def handle(self, input: Input) -> DispatchResult:
        event = input.event
        match event:
            case sdl.WindowEvent():
                return self.on_window(event)
            case sdl.TextInputEvent():
                return self.on_text_input(event)
            case sdl.KeyboardEvent():
                return self.on_key(event)
            case sdl.MouseMotionEvent():
                return self.on_mouse_motion(event)
            case sdl.MouseButtonEvent():
                return self.on_mouse_button(event)
            case sdl.MouseWheelEvent():
                return self.on_mouse_wheel(event)
        return None

    def handle_2d(self, event, point) -> DispatchResult:
        match event:
            case sdl.MouseMotionEvent():
                #logger.debug(f"mouse motion 2d: x={point.x}, y={point.y}")
                # Handlers read local coordinates off the event, but it's one
                # shared object: put the originals back for everyone after us.
                x, y = event.x, event.y
                event.x, event.y = point.x, point.y
                try:
                    return self.handle(event)
                finally:
                    event.x, event.y = x, y
            case sdl.MouseButtonEvent():
                logger.debug(f"{self.__class__.__name__} mouse button 2d: x={point.x}, y={point.y}")
                event.x = point.x
                event.y = point.y
                return self.handle(event)
            case _:
                return self.handle(event)

        return None

    def on_window(self, event: sdl.WindowEvent) -> DispatchResult:
        match event.type:
            case sdl.EventType.WINDOW_MOUSE_ENTER:
                return self.on_mouse_enter(event)
            case sdl.EventType.WINDOW_MOUSE_LEAVE:
                return self.on_mouse_leave(event)
        return None

    def on_text_input(self, event: sdl.TextInputEvent):
        # logger.debug(f"text: {event.text}")
        pass

    def on_key(self, event: sdl.KeyboardEvent):
        # logger.debug(f"key: {event.key}")
        pass

    def on_mouse_enter(self, event: sdl.WindowEvent):
        # logger.debug("mouse enter")
        pass

    def on_mouse_leave(self, event: sdl.WindowEvent):
        # logger.debug("mouse leave")
        pass

    def on_mouse_motion(self, event: sdl.MouseMotionEvent) -> DispatchResult:
        # logger.debug(f"mouse motion: x={event.x}, y={event.y}")
        pass

    def on_mouse_button(self, event: sdl.MouseButtonEvent) -> DispatchResult:
        # logger.debug(f"mouse button: button={event.button}, down={event.down}")
        pass

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent) -> DispatchResult:
        # logger.debug(f"mouse wheel: x={event.x}, y={event.y}")
        pass
