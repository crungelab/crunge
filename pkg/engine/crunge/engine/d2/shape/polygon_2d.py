from ctypes import sizeof

from loguru import logger
import numpy as np
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils

from ...renderer import Renderer
from ...uniforms import cast_tuple4f
from ... import colors

from ..vu_2d import Vu2D
from ..uniforms_2d import ModelUniform
from ..binding_2d import ModelBindGroup

from .polygon_program_2d import PolygonProgram2D

# Define the structured dtype for the combined data
vertex_dtype = np.dtype(
    [
        ("position", np.float32, (2,)),  # Points (x, y)
    ]
)


class Polygon2D(Vu2D):
    def __init__(self, points: list[glm.vec2], color=colors.WHITE) -> None:
        super().__init__()
        # Were class attributes; instance state belongs on the instance.
        self.model_bind_group: ModelBindGroup = None
        self.vertices: np.ndarray = None
        self.vertex_buffer: wgpu.Buffer = None
        self.model_uniform_buffer: wgpu.Buffer = None
        self.model_uniform_buffer_size: int = 0

        self._points = list(points)
        self._color = color

    # -- points ------------------------------------------------------------

    @property
    def points(self) -> list[glm.vec2]:
        return self._points

    @points.setter
    def points(self, value: list[glm.vec2]) -> None:
        self._points = list(value)
        self.mark_geometry()

    # `color` is not overridden. Vu2D's setter already marks GPU dirt, and
    # the model uniform this vu owns is written from _flush_gpu.

    @property
    def size(self) -> glm.vec2:
        return glm.vec2(1.0, 1.0)

    @property
    def width(self) -> float:
        return self.size.x

    @property
    def height(self) -> float:
        return self.size.y

    # -- lifetime ----------------------------------------------------------

    def _create(self):
        super()._create()
        self.create_vertices()

    def create_program(self):
        # Was constructed in __init__, which acquires a GPU resource before
        # the lifecycle has started.
        self.program = PolygonProgram2D()

    def create_vertices(self):
        if not self._points:
            self.vertices = np.empty(0, dtype=vertex_dtype)
            return
        # One extra vertex to close the loop.
        self.vertices = np.empty(len(self._points) + 1, dtype=vertex_dtype)
        self.vertices["position"][:-1] = self._points
        self.vertices["position"][-1] = self._points[0]

    def create_buffers(self):
        super().create_buffers()
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "VERTEX", self.vertices, wgpu.BufferUsage.VERTEX
        )
        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        super().create_bind_groups()
        self.model_bind_group = ModelBindGroup(
            self.model_uniform_buffer,
            self.model_uniform_buffer_size,
        )

    # -- deferred rebuild --------------------------------------------------

    def update_vertices(self):
        """Deferred. The write itself is `_flush_geometry`."""
        self.mark_geometry()

    def _flush_geometry(self) -> bool:
        if self.vertex_buffer is None:
            return False  # not enabled yet; retry next frame

        self.create_vertices()
        utils.write_buffer(
            self.gfx.device, self.vertex_buffer, 0, self.vertices, self.vertices.nbytes
        )
        return True

    def _flush_gpu(self) -> bool:
        if self.model_uniform_buffer is None:
            return False
        if not super()._flush_gpu():
            return False

        model_uniform = ModelUniform()
        model_uniform.color = cast_tuple4f(self.color)
        self.gfx.queue.write_buffer(self.model_uniform_buffer, 0, model_uniform)
        return True

    # -- frame -------------------------------------------------------------

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        super().bind(pass_enc)
        self.model_bind_group.bind(pass_enc)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)

    def _draw(self):
        if self.vertices is None or len(self.vertices) == 0:
            return

        renderer = Renderer.get_current()
        pass_enc = renderer.pass_enc
        # Pipeline before bind groups, matching SpriteVu.
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)
        pass_enc.draw(len(self.vertices), 1, 0, 0)  # Dynamic vertex count