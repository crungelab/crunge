#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/effects/SkImageFilters.h>

#include <include/core/SkMatrix.h>
#include <include/core/SkColorFilter.h>
#include <include/core/SkSamplingOptions.h>
#include <include/core/SkPoint3.h>

#include <include/effects/SkRuntimeEffect.h>



namespace py = pybind11;

void init_skia_image_filters_py_auto(py::module &_skia, Registry &registry) {
{{body}}
}
