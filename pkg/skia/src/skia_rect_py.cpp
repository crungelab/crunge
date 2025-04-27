#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include "include/core/SkRect.h"

namespace py = pybind11;

void init_skia_rect_py(py::module &_skia, Registry &registry) {
    PYEXTEND_BEGIN(SkRect, Rect)
    Rect.def(py::init(&SkRect::MakeXYWH),
        py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"));

    /*
    Rect.def(py::init(
                 [](py::tuple t)
                 {
                     if (t.size() == 0)
                         return SkRect::MakeEmpty();
                     else if (t.size() == 2)
                         return SkRect::MakeWH(
                             t[0].cast<SkScalar>(), t[1].cast<SkScalar>());
                     else if (t.size() == 4)
                         return SkRect::MakeXYWH(
                             t[0].cast<SkScalar>(), t[1].cast<SkScalar>(),
                             t[2].cast<SkScalar>(), t[3].cast<SkScalar>());
                     else
                         throw py::value_error("Invalid tuple.");
                 }),
             py::arg("t"));
    */
    PYEXTEND_END
}
