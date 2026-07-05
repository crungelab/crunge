#include <limits>
#include <filesystem>
#include <string>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/iostream.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkScalar.h>
#include <include/core/SkPoint.h>
#include <include/core/SkColor.h>

#include <dawn/native/DawnNative.h>
#include <dawn/dawn_proc.h>

namespace py = pybind11;

//PYBIND11_MAKE_OPAQUE(std::vector<SkScalar>)
//PYBIND11_MAKE_OPAQUE(std::vector<SkPoint>)
//PYBIND11_MAKE_OPAQUE(std::vector<SkColor>)

void CreateProcTable()
{
    DawnProcTable procs(dawn::native::GetProcs());
    dawnProcSetProcs(&procs);
}

void init_main(py::module &_skia, Registry &registry) {
    CreateProcTable();
    //py::bind_vector<std::vector<SkScalar>>(_skia, "SkScalars", "SkScalar Vector");
    //py::bind_vector<std::vector<SkPoint>>(_skia, "SkPoints", "SkPoint Vector");
    //py::bind_vector<std::vector<SkColor>>(_skia, "SkColors", "SkColor Vector");
}
