#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/ImageLayer.hpp>

namespace py = pybind11;

void init_tmx_image_layer_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::ImageLayer, tmx::Layer> _ImageLayer(_tmx, "ImageLayer");
    registry.on(_tmx, "ImageLayer", _ImageLayer);
        _ImageLayer
        .def(py::init<const std::string &>()
        , py::arg("arg0")
        )
        .def("get_type", &tmx::ImageLayer::getType
            )
        .def("get_image_path", &tmx::ImageLayer::getImagePath
            )
        .def("get_transparency_colour", &tmx::ImageLayer::getTransparencyColour
            )
        .def("has_transparency", &tmx::ImageLayer::hasTransparency
            )
        .def("get_image_size", &tmx::ImageLayer::getImageSize
            )
        .def("has_repeat_x", &tmx::ImageLayer::hasRepeatX
            )
        .def("has_repeat_y", &tmx::ImageLayer::hasRepeatY
            )
    ;


}