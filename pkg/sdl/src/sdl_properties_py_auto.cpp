#include <stdbool.h>
#include <limits>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <SDL3/SDL.h>

#include <cxbind/cxbind.h>
#include <crunge/sdl/conversions.h>
#include <crunge/sdl/crunge-sdl.h>

namespace py = pybind11;

void init_sdl_properties_py_auto(py::module &_sdl, Registry &registry) {
    py::enum_<SDL_PropertyType>(_sdl, "PropertyType", py::arithmetic())
        .value("INVALID", SDL_PropertyType::SDL_PROPERTY_TYPE_INVALID)
        .value("POINTER", SDL_PropertyType::SDL_PROPERTY_TYPE_POINTER)
        .value("STRING", SDL_PropertyType::SDL_PROPERTY_TYPE_STRING)
        .value("NUMBER", SDL_PropertyType::SDL_PROPERTY_TYPE_NUMBER)
        .value("FLOAT", SDL_PropertyType::SDL_PROPERTY_TYPE_FLOAT)
        .value("BOOLEAN", SDL_PropertyType::SDL_PROPERTY_TYPE_BOOLEAN)
        .export_values()
    ;
    _sdl
    .def("get_global_properties", &SDL_GetGlobalProperties
        )
    .def("create_properties", &SDL_CreateProperties
        )
    .def("copy_properties", &SDL_CopyProperties
        , py::arg("src")
        , py::arg("dst")
        )
    .def("lock_properties", &SDL_LockProperties
        , py::arg("props")
        )
    .def("unlock_properties", &SDL_UnlockProperties
        , py::arg("props")
        )
    .def("set_pointer_property_with_cleanup", &SDL_SetPointerPropertyWithCleanup
        , py::arg("props")
        , py::arg("name")
        , py::arg("value")
        , py::arg("cleanup")
        , py::arg("userdata")
        )
    .def("set_pointer_property", &SDL_SetPointerProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("value")
        )
    .def("set_string_property", &SDL_SetStringProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("value")
        )
    .def("set_number_property", &SDL_SetNumberProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("value")
        )
    .def("set_float_property", &SDL_SetFloatProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("value")
        )
    .def("set_boolean_property", &SDL_SetBooleanProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("value")
        )
    .def("has_property", &SDL_HasProperty
        , py::arg("props")
        , py::arg("name")
        )
    .def("get_property_type", &SDL_GetPropertyType
        , py::arg("props")
        , py::arg("name")
        )
    .def("get_pointer_property", &SDL_GetPointerProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("default_value")
        )
    .def("get_string_property", &SDL_GetStringProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("default_value")
        )
    .def("get_number_property", &SDL_GetNumberProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("default_value")
        )
    .def("get_float_property", &SDL_GetFloatProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("default_value")
        )
    .def("get_boolean_property", &SDL_GetBooleanProperty
        , py::arg("props")
        , py::arg("name")
        , py::arg("default_value")
        )
    .def("clear_property", &SDL_ClearProperty
        , py::arg("props")
        , py::arg("name")
        )
    .def("enumerate_properties", &SDL_EnumerateProperties
        , py::arg("props")
        , py::arg("callback")
        , py::arg("userdata")
        )
    .def("destroy_properties", &SDL_DestroyProperties
        , py::arg("props")
        )
    ;


}