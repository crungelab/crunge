#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkFont.h>

#include <include/core/SkPaint.h>
#include <include/core/SkFontMetrics.h>
#include <include/core/SkPath.h>


namespace py = pybind11;

void init_skia_font_py_auto(py::module &_skia, Registry &registry) {
{{body}}
}
