#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkPoint.h>


namespace py = pybind11;

void init_skia_point_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkIPoint> IPoint(_skia, "IPoint");
    registry.on(_skia, "IPoint", IPoint);
        IPoint
        .def_readwrite("f_x", &SkIPoint::fX)
        .def_readwrite("f_y", &SkIPoint::fY)
        .def_static("make", &SkIPoint::Make
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("x", &SkIPoint::x
            , py::return_value_policy::automatic_reference)
        .def("y", &SkIPoint::y
            , py::return_value_policy::automatic_reference)
        .def("is_zero", &SkIPoint::isZero
            , py::return_value_policy::automatic_reference)
        .def("set", &SkIPoint::set
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("equals", &SkIPoint::equals
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<SkPoint> Point(_skia, "Point");
    registry.on(_skia, "Point", Point);
        Point
        .def_readwrite("f_x", &SkPoint::fX)
        .def_readwrite("f_y", &SkPoint::fY)
        .def_static("make", &SkPoint::Make
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("x", &SkPoint::x
            , py::return_value_policy::automatic_reference)
        .def("y", &SkPoint::y
            , py::return_value_policy::automatic_reference)
        .def("is_zero", &SkPoint::isZero
            , py::return_value_policy::automatic_reference)
        .def("set", &SkPoint::set
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("iset", py::overload_cast<int, int>(&SkPoint::iset)
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("set_abs", &SkPoint::setAbs
            , py::arg("pt")
            , py::return_value_policy::automatic_reference)
        .def("offset", &SkPoint::offset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("length", &SkPoint::length
            , py::return_value_policy::automatic_reference)
        .def("distance_to_origin", &SkPoint::distanceToOrigin
            , py::return_value_policy::automatic_reference)
        .def("normalize", &SkPoint::normalize
            , py::return_value_policy::automatic_reference)
        .def("set_normalize", &SkPoint::setNormalize
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("set_length", py::overload_cast<float>(&SkPoint::setLength)
            , py::arg("length")
            , py::return_value_policy::automatic_reference)
        .def("scale", py::overload_cast<float, SkPoint *>(&SkPoint::scale, py::const_)
            , py::arg("scale")
            , py::arg("dst")
            , py::return_value_policy::automatic_reference)
        .def("negate", &SkPoint::negate
            , py::return_value_policy::automatic_reference)
        .def("is_finite", &SkPoint::isFinite
            , py::return_value_policy::automatic_reference)
        .def("equals", &SkPoint::equals
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def_static("distance", &SkPoint::Distance
            , py::arg("a")
            , py::arg("b")
            , py::return_value_policy::automatic_reference)
        .def_static("dot_product", &SkPoint::DotProduct
            , py::arg("a")
            , py::arg("b")
            , py::return_value_policy::automatic_reference)
        .def_static("cross_product", &SkPoint::CrossProduct
            , py::arg("a")
            , py::arg("b")
            , py::return_value_policy::automatic_reference)
        .def("cross", &SkPoint::cross
            , py::arg("vec")
            , py::return_value_policy::automatic_reference)
        .def("dot", &SkPoint::dot
            , py::arg("vec")
            , py::return_value_policy::automatic_reference)
    ;


}