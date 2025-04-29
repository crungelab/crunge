#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkSize.h>
//#include <include/core/SkString.h>

namespace py = pybind11;

void init_skia_size_py_auto(py::module &_skia, Registry &registry) {
    PYCLASS(_skia, SkISize, ISize)
        .def_readwrite("f_width", &SkISize::fWidth)
        .def_readwrite("f_height", &SkISize::fHeight)
        .def_static("make", &SkISize::Make
            , py::arg("w")
            , py::arg("h")
            , py::return_value_policy::automatic_reference)
        .def_static("make_empty", &SkISize::MakeEmpty
            , py::return_value_policy::automatic_reference)
        .def("set", &SkISize::set
            , py::arg("w")
            , py::arg("h")
            , py::return_value_policy::automatic_reference)
        .def("is_zero", &SkISize::isZero
            , py::return_value_policy::automatic_reference)
        .def("is_empty", &SkISize::isEmpty
            , py::return_value_policy::automatic_reference)
        .def("set_empty", &SkISize::setEmpty
            , py::return_value_policy::automatic_reference)
        .def("width", &SkISize::width
            , py::return_value_policy::automatic_reference)
        .def("height", &SkISize::height
            , py::return_value_policy::automatic_reference)
        .def("area", &SkISize::area
            , py::return_value_policy::automatic_reference)
        .def("equals", &SkISize::equals
            , py::arg("w")
            , py::arg("h")
            , py::return_value_policy::automatic_reference)
    ;

    PYCLASS(_skia, SkSize, Size)
        .def_readwrite("f_width", &SkSize::fWidth)
        .def_readwrite("f_height", &SkSize::fHeight)
        .def_static("make", py::overload_cast<float, float>(&SkSize::Make)
            , py::arg("w")
            , py::arg("h")
            , py::return_value_policy::automatic_reference)
        .def_static("make_empty", &SkSize::MakeEmpty
            , py::return_value_policy::automatic_reference)
        .def("set", &SkSize::set
            , py::arg("w")
            , py::arg("h")
            , py::return_value_policy::automatic_reference)
        .def("is_zero", &SkSize::isZero
            , py::return_value_policy::automatic_reference)
        .def("is_empty", &SkSize::isEmpty
            , py::return_value_policy::automatic_reference)
        .def("set_empty", &SkSize::setEmpty
            , py::return_value_policy::automatic_reference)
        .def("width", &SkSize::width
            , py::return_value_policy::automatic_reference)
        .def("height", &SkSize::height
            , py::return_value_policy::automatic_reference)
        .def("equals", &SkSize::equals
            , py::arg("w")
            , py::arg("h")
            , py::return_value_policy::automatic_reference)
        .def("to_round", &SkSize::toRound
            , py::return_value_policy::automatic_reference)
        .def("to_ceil", &SkSize::toCeil
            , py::return_value_policy::automatic_reference)
        .def("to_floor", &SkSize::toFloor
            , py::return_value_policy::automatic_reference)
    ;


}