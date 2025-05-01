#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkPaint.h>
#include <include/core/SkShader.h>

namespace py = pybind11;

void init_skia_paint_py(py::module &_skia, Registry &registry) {
    /*
    PYEXTEND_BEGIN(SkPaint, Paint)
    Paint
    .def("set_shader",
        [] (SkPaint& paint, const SkShader& shader) {
            paint.setShader(sk_ref_sp(&shader));
        },
        py::arg("shader"));

    PYEXTEND_END
    */
}
