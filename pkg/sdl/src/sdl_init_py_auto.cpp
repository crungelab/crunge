#include <stdbool.h>
#include <limits>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <SDL3/SDL.h>

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
        )
    .def("init_sub_system", &SDL_InitSubSystem
        , py::arg("flags")
        )
    .def("quit_sub_system", &SDL_QuitSubSystem
        , py::arg("flags")
        )
    .def("was_init", &SDL_WasInit
        , py::arg("flags")
        )
    .def("quit", &SDL_Quit
        )
    .def("is_main_thread", &SDL_IsMainThread
        )
    .def("run_on_main_thread", &SDL_RunOnMainThread
        , py::arg("callback")
        , py::arg("userdata")
        , py::arg("wait_complete")
        )
    .def("set_app_metadata", &SDL_SetAppMetadata
        , py::arg("appname")
        , py::arg("appversion")
        , py::arg("appidentifier")
        )
    .def("set_app_metadata_property", &SDL_SetAppMetadataProperty
        , py::arg("name")
        , py::arg("value")
        )
    .def("get_app_metadata_property", &SDL_GetAppMetadataProperty
        , py::arg("name")
        )
    ;


}