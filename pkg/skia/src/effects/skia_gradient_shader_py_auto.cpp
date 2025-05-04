#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/effects/SkGradientShader.h>
#include <include/core/SkMatrix.h>


namespace py = pybind11;

void init_skia_gradient_shader_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkGradientShader> GradientShader(_skia, "GradientShader");
    registry.on(_skia, "GradientShader", GradientShader);
        py::enum_<SkGradientShader::Flags>(GradientShader, "Flags", py::arithmetic())
            .value("K_INTERPOLATE_COLORS_IN_PREMUL_FLAG", SkGradientShader::Flags::kInterpolateColorsInPremul_Flag)
            .export_values()
        ;
        py::class_<SkGradientShader::Interpolation> GradientShaderInterpolation(_skia, "GradientShaderInterpolation");
        registry.on(_skia, "GradientShaderInterpolation", GradientShaderInterpolation);
            py::enum_<SkGradientShader::Interpolation::InPremul>(GradientShaderInterpolation, "InPremul", py::arithmetic())
                .value("K_NO", SkGradientShader::Interpolation::InPremul::kNo)
                .value("K_YES", SkGradientShader::Interpolation::InPremul::kYes)
                .export_values()
            ;
            py::enum_<SkGradientShader::Interpolation::ColorSpace>(GradientShaderInterpolation, "ColorSpace", py::arithmetic())
                .value("K_DESTINATION", SkGradientShader::Interpolation::ColorSpace::kDestination)
                .value("K_SRGB_LINEAR", SkGradientShader::Interpolation::ColorSpace::kSRGBLinear)
                .value("K_LAB", SkGradientShader::Interpolation::ColorSpace::kLab)
                .value("K_OK_LAB", SkGradientShader::Interpolation::ColorSpace::kOKLab)
                .value("K_OK_LAB_GAMUT_MAP", SkGradientShader::Interpolation::ColorSpace::kOKLabGamutMap)
                .value("K_LCH", SkGradientShader::Interpolation::ColorSpace::kLCH)
                .value("K_OKLCH", SkGradientShader::Interpolation::ColorSpace::kOKLCH)
                .value("K_OKLCH_GAMUT_MAP", SkGradientShader::Interpolation::ColorSpace::kOKLCHGamutMap)
                .value("K_SRGB", SkGradientShader::Interpolation::ColorSpace::kSRGB)
                .value("K_HSL", SkGradientShader::Interpolation::ColorSpace::kHSL)
                .value("K_HWB", SkGradientShader::Interpolation::ColorSpace::kHWB)
                .value("K_DISPLAY_P3", SkGradientShader::Interpolation::ColorSpace::kDisplayP3)
                .value("K_REC2020", SkGradientShader::Interpolation::ColorSpace::kRec2020)
                .value("K_PROPHOTO_RGB", SkGradientShader::Interpolation::ColorSpace::kProphotoRGB)
                .value("K_A98RGB", SkGradientShader::Interpolation::ColorSpace::kA98RGB)
                .value("K_LAST_COLOR_SPACE", SkGradientShader::Interpolation::ColorSpace::kLastColorSpace)
                .export_values()
            ;
            py::enum_<SkGradientShader::Interpolation::HueMethod>(GradientShaderInterpolation, "HueMethod", py::arithmetic())
                .value("K_SHORTER", SkGradientShader::Interpolation::HueMethod::kShorter)
                .value("K_LONGER", SkGradientShader::Interpolation::HueMethod::kLonger)
                .value("K_INCREASING", SkGradientShader::Interpolation::HueMethod::kIncreasing)
                .value("K_DECREASING", SkGradientShader::Interpolation::HueMethod::kDecreasing)
                .value("K_LAST_HUE_METHOD", SkGradientShader::Interpolation::HueMethod::kLastHueMethod)
                .export_values()
            ;
            GradientShaderInterpolation
            .def_readwrite("f_in_premul", &SkGradientShader::Interpolation::fInPremul)
            .def_readwrite("f_color_space", &SkGradientShader::Interpolation::fColorSpace)
            .def_readwrite("f_hue_method", &SkGradientShader::Interpolation::fHueMethod)
            .def_static("from_flags", &SkGradientShader::Interpolation::FromFlags
                , py::arg("flags")
                , py::return_value_policy::automatic_reference)
        ;


}