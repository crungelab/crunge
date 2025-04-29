#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include <include/effects/SkGradientShader.h>
#include <include/core/SkMatrix.h>


namespace py = pybind11;

void init_skia_gradient_shader_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkGradientShader> GradientShader(_skia, "GradientShader");
    registry.on(_skia, "GradientShader", GradientShader);
    GradientShader
        ;

        py::enum_<SkGradientShader::Flags>(_skia, "Flags", py::arithmetic())
            .value("K_INTERPOLATE_COLORS_IN_PREMUL_FLAG", SkGradientShader::Flags::kInterpolateColorsInPremul_Flag)
            .export_values()
        ;

    ;


}