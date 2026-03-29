#include <stdbool.h>
#include <limits>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <SDL3/SDL.h>
#include <SDL3/SDL_audio.h>
#include <SDL3/SDL_iostream.h>

#include <cxbind/cxbind.h>

#include <crunge/sdl/crunge-sdl.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_audio_py(py::module &_sdl, Registry &registry) {
    _sdl.attr("AUDIO_DEVICE_DEFAULT_PLAYBACK") = py::int_(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK);
}