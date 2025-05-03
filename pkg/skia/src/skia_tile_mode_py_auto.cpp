#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkTileMode.h>

namespace py = pybind11;

void init_skia_tile_mode_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkTileMode>(_skia, "TileMode", py::arithmetic())
        .value("K_CLAMP", SkTileMode::kClamp)
        .value("K_REPEAT", SkTileMode::kRepeat)
        .value("K_MIRROR", SkTileMode::kMirror)
        .value("K_DECAL", SkTileMode::kDecal)
        .value("K_LAST_TILE_MODE", SkTileMode::kLastTileMode)
        .export_values()
    ;

}