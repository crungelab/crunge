import os
import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
from pathlib import Path

from loguru import logger
import numpy as np
import trimesh as tm

from crunge import bgfx
from crunge.bgfx.utils import as_void_ptr
from crunge.bgfx.utils.shaders_utils import ShaderType, load_shader
from crunge.bgfx.constants import *

from crunge.bgfx.window import Window
from crunge.bgfx.utils.matrix_utils import look_at, proj, rotate_xy

logger.enable("bunny")

root_path = Path(__file__).parent.parent / "assets" / "shaders"

class Bunny(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.elapsed_time = 0

        bunny_path = Path(__file__).parent.parent / "assets" / "meshes" / "bunny.obj"
        self.bunny_mesh = bunny_mesh = tm.load(str(bunny_path))
        #Vertices
        vertices = self.vertices = bunny_mesh.vertices.astype(np.float32)
        logger.debug(f'vertices type: {type(vertices)}')
        logger.debug(f'vertices:  {vertices}')
        n_vertices = self.n_vertices = len(vertices)
        logger.debug(f'n_vertices:  {n_vertices}')
        self.vertices_p = as_void_ptr(vertices)

        #Indices
        indices = self.indices = self.bunny_mesh.faces.astype(np.uint16)
        self.indices_p = as_void_ptr(indices)
        
        logger.debug(f'indices:  {indices}')
        n_indices = self.n_indices = len(indices)
        logger.debug(f'n_indices:  {n_indices}')


    def init(self, platform_data):
        bgfx.render_frame()
        self.init_conf = init_conf = bgfx.Init()
        init_conf.platform_data = platform_data
        init_conf.debug = True
        init_conf.resolution.width = self.width
        init_conf.resolution.height = self.height
        init_conf.resolution.reset = BGFX_RESET_VSYNC
        bgfx.init(init_conf)

        bgfx.set_debug(BGFX_DEBUG_TEXT)
        bgfx.set_view_clear(0, BGFX_CLEAR_COLOR | BGFX_CLEAR_DEPTH, 0x443355FF, 1.0, 0)

        # Create time uniform
        self.time_uniform = bgfx.create_uniform("u_time", bgfx.UniformType.VEC4)

        # Create Vertex Buffer
        self.vertex_layout = bgfx.VertexLayout()
        self.vertex_layout.begin().add(bgfx.Attrib.POSITION, 3, bgfx.AttribType.FLOAT).end()

        vb_memory = bgfx.copy(self.vertices_p, self.n_vertices * sizeof(c_float) * 3)
        
        self.vertex_buffer = bgfx.create_vertex_buffer(vb_memory, self.vertex_layout)

        # Create Index Buffer
        ib_memory = bgfx.copy(self.indices_p, self.n_indices * sizeof(c_uint16) * 3)
        self.index_buffer = bgfx.create_index_buffer(ib_memory)

        # Create program from shaders.
        self.main_program = bgfx.create_program(
            load_shader(
                "mesh.VertexShader.vert", ShaderType.VERTEX, root_path=root_path
            ),
            load_shader(
                "mesh.FragmentShader.frag", ShaderType.FRAGMENT, root_path=root_path
            ),
            True,
        )

    def shutdown(self):
        bgfx.destroy(self.index_buffer)
        bgfx.destroy(self.vertex_buffer)
        bgfx.destroy(self.main_program)
        bgfx.shutdown()

    def update(self, dt):
        self.elapsed_time += dt
        mouse_x, mouse_y, buttons_states = self.get_mouse_state()

        at = (c_float * 3)(*[0.0, 1.0, 0.0])
        eye = (c_float * 3)(*[0.0, 1.0, -2.5])
        up = (c_float * 3)(*[0.0, 1.0, 0.0])

        view = look_at(eye, at, up)
        projection = proj(60.0, self.width / self.height, 0.1, 100.0)

        bgfx.set_view_transform(0, as_void_ptr(view), as_void_ptr(projection))
        bgfx.set_view_rect(0, 0, 0, self.width, self.height)

        # This dummy draw call is here to make sure that view 0 is cleared
        # if no other draw calls are submitted to view 0.
        bgfx.touch(0)

        mtx = rotate_xy(0, self.elapsed_time * 0.37)
    
        bgfx.set_uniform(
            self.time_uniform,
            as_void_ptr((c_float * 4)(self.elapsed_time, 0.0, 0.0, 0.0)),
        )

        # Set vertex and index buffer.
        #bgfx.set_vertex_buffer(0, self.vertex_buffer, 0, self.n_vertices)
        bgfx.set_vertex_buffer(0, self.vertex_buffer)
        bgfx.set_index_buffer(self.index_buffer)

        bgfx.set_state(
            0
            | BGFX_STATE_WRITE_RGB
            | BGFX_STATE_WRITE_A
            | BGFX_STATE_WRITE_Z
            | BGFX_STATE_DEPTH_TEST_LESS
            | BGFX_STATE_MSAA,
            0,
        )
        
        bgfx.submit(0, self.main_program, 0)

        bgfx.frame()

    def resize(self, width, height):
        bgfx.reset(
            self.width, self.height, BGFX_RESET_VSYNC, self.init_conf.resolution.format
        )

def main():
    bunny = Bunny(1280, 720, "examples/bunny")
    bunny.run()

if __name__ == "__main__":
    main()