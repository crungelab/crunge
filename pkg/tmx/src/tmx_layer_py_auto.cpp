#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/Layer.hpp>

namespace py = pybind11;

void init_tmx_layer_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::Layer> Layer(_tmx, "Layer");
    registry.on(_tmx, "Layer", Layer);
        py::enum_<tmx::Layer::Type>(Layer, "Type", py::arithmetic())
            .value("TILE", tmx::Layer::Type::Tile)
            .value("OBJECT", tmx::Layer::Type::Object)
            .value("IMAGE", tmx::Layer::Type::Image)
            .value("GROUP", tmx::Layer::Type::Group)
            .export_values()
        ;
        Layer
        .def("get_type", &tmx::Layer::getType
            , py::return_value_policy::automatic_reference)
        .def("get_class", &tmx::Layer::getClass
            , py::return_value_policy::reference)
        .def("get_name", &tmx::Layer::getName
            , py::return_value_policy::reference)
        .def("get_opacity", &tmx::Layer::getOpacity
            , py::return_value_policy::automatic_reference)
        .def("get_visible", &tmx::Layer::getVisible
            , py::return_value_policy::automatic_reference)
        .def("get_offset", &tmx::Layer::getOffset
            , py::return_value_policy::reference)
        .def("get_parallax_factor", &tmx::Layer::getParallaxFactor
            , py::return_value_policy::reference)
        .def("get_tint_colour", &tmx::Layer::getTintColour
            , py::return_value_policy::automatic_reference)
        .def("get_size", &tmx::Layer::getSize
            , py::return_value_policy::reference)
        .def("get_properties", &tmx::Layer::getProperties
            , py::return_value_policy::reference)
    ;


}