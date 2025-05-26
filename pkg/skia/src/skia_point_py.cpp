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

void init_skia_point_py(py::module &_skia, Registry &registry) {
    PYEXTEND_BEGIN(SkPoint, Point)
    _Point.def(py::init(&SkPoint::Make),
        py::arg("x"), py::arg("y"));
    PYEXTEND_END
}
