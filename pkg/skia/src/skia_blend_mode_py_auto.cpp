#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkBlendMode.h>

namespace py = pybind11;

void init_skia_blend_mode_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkBlendMode>(_skia, "BlendMode", py::arithmetic())
        .value("K_CLEAR", SkBlendMode::kClear)
        .value("K_SRC", SkBlendMode::kSrc)
        .value("K_DST", SkBlendMode::kDst)
        .value("K_SRC_OVER", SkBlendMode::kSrcOver)
        .value("K_DST_OVER", SkBlendMode::kDstOver)
        .value("K_SRC_IN", SkBlendMode::kSrcIn)
        .value("K_DST_IN", SkBlendMode::kDstIn)
        .value("K_SRC_OUT", SkBlendMode::kSrcOut)
        .value("K_DST_OUT", SkBlendMode::kDstOut)
        .value("K_SRC_A_TOP", SkBlendMode::kSrcATop)
        .value("K_DST_A_TOP", SkBlendMode::kDstATop)
        .value("K_XOR", SkBlendMode::kXor)
        .value("K_PLUS", SkBlendMode::kPlus)
        .value("K_MODULATE", SkBlendMode::kModulate)
        .value("K_SCREEN", SkBlendMode::kScreen)
        .value("K_OVERLAY", SkBlendMode::kOverlay)
        .value("K_DARKEN", SkBlendMode::kDarken)
        .value("K_LIGHTEN", SkBlendMode::kLighten)
        .value("K_COLOR_DODGE", SkBlendMode::kColorDodge)
        .value("K_COLOR_BURN", SkBlendMode::kColorBurn)
        .value("K_HARD_LIGHT", SkBlendMode::kHardLight)
        .value("K_SOFT_LIGHT", SkBlendMode::kSoftLight)
        .value("K_DIFFERENCE", SkBlendMode::kDifference)
        .value("K_EXCLUSION", SkBlendMode::kExclusion)
        .value("K_MULTIPLY", SkBlendMode::kMultiply)
        .value("K_HUE", SkBlendMode::kHue)
        .value("K_SATURATION", SkBlendMode::kSaturation)
        .value("K_COLOR", SkBlendMode::kColor)
        .value("K_LUMINOSITY", SkBlendMode::kLuminosity)
        .value("K_LAST_COEFF_MODE", SkBlendMode::kLastCoeffMode)
        .value("K_LAST_SEPARABLE_MODE", SkBlendMode::kLastSeparableMode)
        .value("K_LAST_MODE", SkBlendMode::kLastMode)
        .export_values()
    ;
    py::enum_<SkBlendModeCoeff>(_skia, "BlendModeCoeff", py::arithmetic())
        .value("K_ZERO", SkBlendModeCoeff::kZero)
        .value("K_ONE", SkBlendModeCoeff::kOne)
        .value("K_SC", SkBlendModeCoeff::kSC)
        .value("K_ISC", SkBlendModeCoeff::kISC)
        .value("K_DC", SkBlendModeCoeff::kDC)
        .value("K_IDC", SkBlendModeCoeff::kIDC)
        .value("K_SA", SkBlendModeCoeff::kSA)
        .value("K_ISA", SkBlendModeCoeff::kISA)
        .value("K_DA", SkBlendModeCoeff::kDA)
        .value("K_IDA", SkBlendModeCoeff::kIDA)
        .value("K_COEFF_COUNT", SkBlendModeCoeff::kCoeffCount)
        .export_values()
    ;
    _skia
    .def("blend_mode_as_coeff", &SkBlendMode_AsCoeff
        , py::arg("mode")
        , py::arg("src")
        , py::arg("dst")
        , py::return_value_policy::automatic_reference)
    .def("blend_mode_name", &SkBlendMode_Name
        , py::arg("blend_mode")
        , py::return_value_policy::automatic_reference)
    ;


}