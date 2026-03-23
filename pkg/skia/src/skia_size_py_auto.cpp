#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkSize.h>
//#include <include/core/SkString.h>

namespace py = pybind11;

void init_skia_size_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkISize> _ISize(_skia, "ISize");
    registry.on(_skia, "ISize", _ISize);
        _ISize
        .def_readwrite("f_width", &SkISize::fWidth)
        .def_readwrite("f_height", &SkISize::fHeight)
        .def_static("make", &SkISize::Make
            , py::arg("w")
            , py::arg("h")
            )
        .def_static("make_empty", &SkISize::MakeEmpty
            )
        .def("set", &SkISize::set
            , py::arg("w")
            , py::arg("h")
            )
        .def("is_zero", &SkISize::isZero
            )
        .def("is_empty", &SkISize::isEmpty
            )
        .def("set_empty", &SkISize::setEmpty
            )
        .def("width", &SkISize::width
            )
        .def("height", &SkISize::height
            )
        .def("area", &SkISize::area
            )
        .def("equals", &SkISize::equals
            , py::arg("w")
            , py::arg("h")
            )
    ;

    py::class_<SkSize> _Size(_skia, "Size");
    registry.on(_skia, "Size", _Size);
        _Size
        .def_readwrite("f_width", &SkSize::fWidth)
        .def_readwrite("f_height", &SkSize::fHeight)
        .def_static("make", py::overload_cast<SkScalar, SkScalar>(&SkSize::Make)
            , py::arg("w")
            , py::arg("h")
            )
        .def_static("make", py::overload_cast<const SkISize &>(&SkSize::Make)
            , py::arg("src")
            )
        .def_static("make_empty", &SkSize::MakeEmpty
            )
        .def("set", &SkSize::set
            , py::arg("w")
            , py::arg("h")
            )
        .def("is_zero", &SkSize::isZero
            )
        .def("is_empty", &SkSize::isEmpty
            )
        .def("set_empty", &SkSize::setEmpty
            )
        .def("width", &SkSize::width
            )
        .def("height", &SkSize::height
            )
        .def("equals", &SkSize::equals
            , py::arg("w")
            , py::arg("h")
            )
        .def("to_round", &SkSize::toRound
            )
        .def("to_ceil", &SkSize::toCeil
            )
        .def("to_floor", &SkSize::toFloor
            )
    ;


}