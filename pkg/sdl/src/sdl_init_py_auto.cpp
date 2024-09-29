#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_init_py_auto(py::module &_sdl, Registry &registry) {
    py::enum_<SDL_AppResult>(_sdl, "AppResult", py::arithmetic())
        .value("APP_CONTINUE", SDL_AppResult::SDL_APP_CONTINUE)
        .value("APP_SUCCESS", SDL_AppResult::SDL_APP_SUCCESS)
        .value("APP_FAILURE", SDL_AppResult::SDL_APP_FAILURE)
        .export_values()
    ;

    _sdl
    .def("init", &SDL_Init
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)

    .def("init_sub_system", &SDL_InitSubSystem
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)

    .def("quit_sub_system", &SDL_QuitSubSystem
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)

    .def("was_init", &SDL_WasInit
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)

    .def("quit", &SDL_Quit
        , py::return_value_policy::automatic_reference)

    .def("set_app_metadata", &SDL_SetAppMetadata
        , py::arg("appname")
        , py::arg("appversion")
        , py::arg("appidentifier")
        , py::return_value_policy::automatic_reference)

    .def("set_app_metadata_property", &SDL_SetAppMetadataProperty
        , py::arg("name")
        , py::arg("value")
        , py::return_value_policy::automatic_reference)

    .def("get_app_metadata_property", &SDL_GetAppMetadataProperty
        , py::arg("name")
        , py::return_value_policy::automatic_reference)

    ;

}