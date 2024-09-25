#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_main(py::module &, Registry& registry);
void init_sdl_init_auto(py::module &, Registry& registry);
void init_sdl_video_auto(py::module &, Registry& registry);
void init_sdl_events_auto(py::module &, Registry& registry);
void init_sdl_keyboard_auto(py::module &, Registry& registry);
void init_sdl_mouse_auto(py::module &, Registry& registry);
void init_sdl_scancode_auto(py::module &, Registry& registry);
void init_sdl_properties_auto(py::module &, Registry& registry);


PYBIND11_MODULE(_sdl, m) {
    Registry r;
    init_main(m, r);
    init_sdl_init_auto(m, r);
    init_sdl_video_auto(m, r);
    init_sdl_events_auto(m, r);
    init_sdl_keyboard_auto(m, r);
    init_sdl_mouse_auto(m, r);
    init_sdl_scancode_auto(m, r);
    init_sdl_properties_auto(m, r);
}