#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include <include/gpu/graphite/Recorder.h>
#include <include/gpu/graphite/ImageProvider.h>
#include <include/gpu/graphite/BackendTexture.h>

#include <include/core/SkPixmap.h>
#include <include/core/SkTraceMemoryDump.h>
#include <include/core/SkCanvas.h>


namespace py = pybind11;

void init_skia_recorder_py_auto(py::module &_skia, Registry &registry) {
{{body}}
}