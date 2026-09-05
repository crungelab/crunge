# event_handler.py
from crunge import sdl
from ..base_node import DispatchResult


class EventHandler:
    """Demux an SDL event to an on_* handler. No tree, no super() chain."""

    def handle(self, event) -> DispatchResult:
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
