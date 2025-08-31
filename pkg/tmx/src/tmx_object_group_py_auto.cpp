#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/ObjectGroup.hpp>

namespace py = pybind11;

void init_tmx_object_group_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::ObjectGroup, tmx::Layer> ObjectGroup(_tmx, "ObjectGroup");
    registry.on(_tmx, "ObjectGroup", ObjectGroup);
        py::enum_<tmx::ObjectGroup::DrawOrder>(ObjectGroup, "DrawOrder", py::arithmetic())
            .value("INDEX", tmx::ObjectGroup::DrawOrder::Index)
            .value("TOP_DOWN", tmx::ObjectGroup::DrawOrder::TopDown)
            .export_values()
        ;
        ObjectGroup
        .def(py::init<>())
        .def("get_type", &tmx::ObjectGroup::getType
            , py::return_value_policy::automatic_reference)
        .def("get_colour", &tmx::ObjectGroup::getColour
            , py::return_value_policy::reference)
        .def("get_draw_order", &tmx::ObjectGroup::getDrawOrder
            , py::return_value_policy::automatic_reference)
        .def("get_properties", &tmx::ObjectGroup::getProperties
            , py::return_value_policy::reference)
        .def("get_objects", &tmx::ObjectGroup::getObjects
            , py::return_value_policy::reference)
    ;


}