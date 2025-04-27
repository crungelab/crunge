#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include <include/gpu/graphite/GraphiteTypes.h>
#include <include/gpu/graphite/BackendSemaphore.h>
#include <include/gpu/graphite/Recording.h>
#include <include/core/SkSurface.h>
#include <include/gpu/MutableTextureState.h>

namespace py = pybind11;

void init_skia_graphite_types_py_auto(py::module &_skia, Registry &registry) {
{{body}}
}