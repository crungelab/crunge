#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_main(py::module &, Registry& registry);
void init_sdl_init(py::module &, Registry& registry);
void init_sdl_video(py::module &, Registry& registry);
void init_sdl_events(py::module &, Registry& registry);
void init_sdl_keyboard(py::module &, Registry& registry);
void init_sdl_properties(py::module &, Registry& registry);


PYBIND11_MODULE(_sdl, m) {
    Registry r;
    init_main(m, r);
    init_sdl_init(m, r);
    init_sdl_video(m, r);
    init_sdl_events(m, r);
    init_sdl_keyboard(m, r);
    init_sdl_properties(m, r);
}