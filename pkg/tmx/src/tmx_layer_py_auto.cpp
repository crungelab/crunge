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
    py::class_<tmx::Layer> _Layer(_tmx, "Layer");
    registry.on(_tmx, "Layer", _Layer);
        py::enum_<tmx::Layer::Type>(_Layer, "Type", py::arithmetic())
            .value("TILE", tmx::Layer::Type::Tile)
            .value("OBJECT", tmx::Layer::Type::Object)
            .value("IMAGE", tmx::Layer::Type::Image)
            .value("GROUP", tmx::Layer::Type::Group)
            .export_values()
        ;
        _Layer
        .def("get_type", &tmx::Layer::getType
            )
        .def("get_class", &tmx::Layer::getClass
            )
        .def("get_name", &tmx::Layer::getName
            )
        .def("get_opacity", &tmx::Layer::getOpacity
            )
        .def("get_visible", &tmx::Layer::getVisible
            )
        .def("get_offset", &tmx::Layer::getOffset
            )
        .def("get_parallax_factor", &tmx::Layer::getParallaxFactor
            )
        .def("get_tint_colour", &tmx::Layer::getTintColour
            )
        .def("get_size", &tmx::Layer::getSize
            )
        .def("get_properties", &tmx::Layer::getProperties
            )
        .def_property_readonly("name", &tmx::Layer::getName)
        .def_property_readonly("opacity", &tmx::Layer::getOpacity)
    ;


}