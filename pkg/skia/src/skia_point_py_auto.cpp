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
    py::class_<SkIPoint> _IPoint(_skia, "IPoint");
    registry.on(_skia, "IPoint", _IPoint);
        _IPoint
        .def_readwrite("f_x", &SkIPoint::fX)
        .def_readwrite("f_y", &SkIPoint::fY)
        .def_static("make", &SkIPoint::Make
            , py::arg("x")
            , py::arg("y")
            )
        .def("x", &SkIPoint::x
            )
        .def("y", &SkIPoint::y
            )
        .def("is_zero", &SkIPoint::isZero
            )
        .def("set", &SkIPoint::set
            , py::arg("x")
            , py::arg("y")
            )
        .def("equals", &SkIPoint::equals
            , py::arg("x")
            , py::arg("y")
            )
    ;

    py::class_<SkPoint> _Point(_skia, "Point");
    registry.on(_skia, "Point", _Point);
        _Point
        .def_readwrite("f_x", &SkPoint::fX)
        .def_readwrite("f_y", &SkPoint::fY)
        .def_static("make", &SkPoint::Make
            , py::arg("x")
            , py::arg("y")
            )
        .def("x", &SkPoint::x
            )
        .def("y", &SkPoint::y
            )
        .def("is_zero", &SkPoint::isZero
            )
        .def("set", &SkPoint::set
            , py::arg("x")
            , py::arg("y")
            )
        .def("iset", py::overload_cast<int32_t, int32_t>(&SkPoint::iset)
            , py::arg("x")
            , py::arg("y")
            )
        .def("iset", py::overload_cast<const SkIPoint &>(&SkPoint::iset)
            , py::arg("p")
            )
        .def("set_abs", &SkPoint::setAbs
            , py::arg("pt")
            )
        .def("offset", &SkPoint::offset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("length", &SkPoint::length
            )
        .def("distance_to_origin", &SkPoint::distanceToOrigin
            )
        .def("normalize", &SkPoint::normalize
            )
        .def("set_normalize", &SkPoint::setNormalize
            , py::arg("x")
            , py::arg("y")
            )
        .def("set_length", py::overload_cast<float>(&SkPoint::setLength)
            , py::arg("length")
            )
        .def("set_length", py::overload_cast<float, float, float>(&SkPoint::setLength)
            , py::arg("x")
            , py::arg("y")
            , py::arg("length")
            )
        .def("scale", py::overload_cast<float, SkPoint *>(&SkPoint::scale, py::const_)
            , py::arg("scale")
            , py::arg("dst")
            )
        .def("scale", py::overload_cast<float>(&SkPoint::scale)
            , py::arg("value")
            )
        .def("negate", &SkPoint::negate
            )
        .def("is_finite", &SkPoint::isFinite
            )
        .def("equals", &SkPoint::equals
            , py::arg("x")
            , py::arg("y")
            )
        .def_static("distance", &SkPoint::Distance
            , py::arg("a")
            , py::arg("b")
            )
        .def_static("dot_product", &SkPoint::DotProduct
            , py::arg("a")
            , py::arg("b")
            )
        .def_static("cross_product", &SkPoint::CrossProduct
            , py::arg("a")
            , py::arg("b")
            )
        .def("cross", &SkPoint::cross
            , py::arg("vec")
            )
        .def("dot", &SkPoint::dot
            , py::arg("vec")
            )
    ;


}