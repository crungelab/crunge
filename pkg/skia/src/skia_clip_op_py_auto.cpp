#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkClipOp.h>

namespace py = pybind11;

void init_skia_clip_op_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkClipOp>(_skia, "ClipOp", py::arithmetic())
        .value("K_DIFFERENCE", SkClipOp::kDifference)
        .value("K_INTERSECT", SkClipOp::kIntersect)
        .value("K_MAX_ENUM_VALUE", SkClipOp::kMax_EnumValue)
        .export_values()
    ;

}