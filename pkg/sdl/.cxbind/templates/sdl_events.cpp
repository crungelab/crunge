#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_events(py::module &_sdl, Registry &registry) {
{{body}}
}