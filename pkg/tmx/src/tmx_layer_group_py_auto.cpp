#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/LayerGroup.hpp>

namespace py = pybind11;

void init_tmx_layer_group_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::LayerGroup, tmx::Layer> _LayerGroup(_tmx, "LayerGroup");
    registry.on(_tmx, "LayerGroup", _LayerGroup);
        _LayerGroup
        .def(py::init<const std::string &, const tmx::Vector2u &>()
        , py::arg("work_dir")
        , py::arg("tile_count")
        )
        .def("get_type", &tmx::LayerGroup::getType
            , py::return_value_policy::automatic_reference)
    ;


}