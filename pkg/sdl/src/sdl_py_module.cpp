#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_sdl_py(py::module &, Registry& registry);
void init_sdl_init_py_auto(py::module &, Registry& registry);
void init_sdl_video_py_auto(py::module &, Registry& registry);
void init_sdl_audio_py_auto(py::module &, Registry& registry);
void init_sdl_events_py_auto(py::module &, Registry& registry);
void init_sdl_keyboard_py_auto(py::module &, Registry& registry);
void init_sdl_mouse_py_auto(py::module &, Registry& registry);
void init_sdl_scancode_py_auto(py::module &, Registry& registry);
void init_sdl_properties_py_auto(py::module &, Registry& registry);


PYBIND11_MODULE(_sdl, m) {
    Registry r;
    init_sdl_py(m, r);
    init_sdl_init_py_auto(m, r);
    init_sdl_video_py_auto(m, r);
    init_sdl_audio_py_auto(m, r);
    init_sdl_events_py_auto(m, r);
    init_sdl_keyboard_py_auto(m, r);
    init_sdl_mouse_py_auto(m, r);
    init_sdl_scancode_py_auto(m, r);
    init_sdl_properties_py_auto(m, r);
}