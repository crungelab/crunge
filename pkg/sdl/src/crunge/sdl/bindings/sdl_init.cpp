#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <iostream>

#include <crunge/core/bindtools.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_init(py::module &_sdl, Registry &registry) {
    py::enum_<SDL_InitFlags>(_sdl, "InitFlags", py::arithmetic())
        .value("INIT_TIMER", SDL_InitFlags::SDL_INIT_TIMER)
        .value("INIT_AUDIO", SDL_InitFlags::SDL_INIT_AUDIO)
        .value("INIT_VIDEO", SDL_InitFlags::SDL_INIT_VIDEO)
        .value("INIT_JOYSTICK", SDL_InitFlags::SDL_INIT_JOYSTICK)
        .value("INIT_HAPTIC", SDL_InitFlags::SDL_INIT_HAPTIC)
        .value("INIT_GAMEPAD", SDL_InitFlags::SDL_INIT_GAMEPAD)
        .value("INIT_EVENTS", SDL_InitFlags::SDL_INIT_EVENTS)
        .value("INIT_SENSOR", SDL_InitFlags::SDL_INIT_SENSOR)
        .export_values();

    _sdl.def("init", &SDL_Init
    , py::arg("flags")
    , py::return_value_policy::automatic_reference);

    _sdl.def("init_sub_system", &SDL_InitSubSystem
    , py::arg("flags")
    , py::return_value_policy::automatic_reference);

    _sdl.def("quit_sub_system", &SDL_QuitSubSystem
    , py::arg("flags")
    , py::return_value_policy::automatic_reference);

    _sdl.def("was_init", &SDL_WasInit
    , py::arg("flags")
    , py::return_value_policy::automatic_reference);

    _sdl.def("quit", &SDL_Quit
    , py::return_value_policy::automatic_reference);


}