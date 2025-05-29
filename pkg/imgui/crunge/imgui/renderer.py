from abc import ABC, abstractmethod

from crunge import imgui

class Renderer(ABC):
    def __init__(self):
        if not imgui.get_current_context():
            raise RuntimeError(
                "No valid ImGui context. Use imgui.create_context() first and/or "
                "imgui.set_current_context()."
            )
        self.io = imgui.get_io()

        self._font_texture = None

        self.io.delta_time = 1.0 / 60.0

    @classmethod
    def produce(cls):
        renderer = cls()
        renderer.create()
        return renderer

    def create(self):
        self._create_device_objects()
        self.refresh_font_texture()
        return self

    @abstractmethod
    def render(self, draw_data):
        pass

    @abstractmethod
    def refresh_font_texture(self):
        pass

    @abstractmethod
    def _create_device_objects(self):
        pass

    @abstractmethod
    def _invalidate_device_objects(self):
        pass

    def shutdown(self):
        self._invalidate_device_objects()
