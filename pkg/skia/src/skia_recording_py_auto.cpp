#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/gpu/graphite/Recording.h>

namespace py = pybind11;

void init_skia_recording_py_auto(py::module &_skia, Registry &registry) {
    py::class_<skgpu::graphite::Recording> _Recording(_skia, "Recording");
    registry.on(_skia, "Recording", _Recording);

}