#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkAlphaType.h>


namespace py = pybind11;

void init_skia_alpha_type_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkAlphaType>(_skia, "AlphaType", py::arithmetic())
        .value("K_UNKNOWN_SK_ALPHA_TYPE", SkAlphaType::kUnknown_SkAlphaType)
        .value("K_OPAQUE_SK_ALPHA_TYPE", SkAlphaType::kOpaque_SkAlphaType)
        .value("K_PREMUL_SK_ALPHA_TYPE", SkAlphaType::kPremul_SkAlphaType)
        .value("K_UNPREMUL_SK_ALPHA_TYPE", SkAlphaType::kUnpremul_SkAlphaType)
        .value("K_LAST_ENUM_SK_ALPHA_TYPE", SkAlphaType::kLastEnum_SkAlphaType)
        .export_values()
    ;

}