#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_init(py::module &_sdl, Registry &registry) {
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

    _sdl.def("set_app_metadata", &SDL_SetAppMetadata
    , py::arg("appname")
    , py::arg("appversion")
    , py::arg("appidentifier")
    , py::return_value_policy::automatic_reference);

    _sdl.def("set_app_metadata_property", &SDL_SetAppMetadataProperty
    , py::arg("name")
    , py::arg("value")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_app_metadata_property", &SDL_GetAppMetadataProperty
    , py::arg("name")
    , py::return_value_policy::automatic_reference);


}