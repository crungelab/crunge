#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkColorType.h>


namespace py = pybind11;

void init_skia_color_type_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkColorType>(_skia, "ColorType", py::arithmetic())
        .value("K_UNKNOWN_SK_COLOR_TYPE", SkColorType::kUnknown_SkColorType)
        .value("K_ALPHA_8_SK_COLOR_TYPE", SkColorType::kAlpha_8_SkColorType)
        .value("K_RGB_565_SK_COLOR_TYPE", SkColorType::kRGB_565_SkColorType)
        .value("K_ARGB_4444_SK_COLOR_TYPE", SkColorType::kARGB_4444_SkColorType)
        .value("K_RGBA_8888_SK_COLOR_TYPE", SkColorType::kRGBA_8888_SkColorType)
        .value("K_RGB_888X_SK_COLOR_TYPE", SkColorType::kRGB_888x_SkColorType)
        .value("K_BGRA_8888_SK_COLOR_TYPE", SkColorType::kBGRA_8888_SkColorType)
        .value("K_RGBA_1010102_SK_COLOR_TYPE", SkColorType::kRGBA_1010102_SkColorType)
        .value("K_BGRA_1010102_SK_COLOR_TYPE", SkColorType::kBGRA_1010102_SkColorType)
        .value("K_RGB_101010X_SK_COLOR_TYPE", SkColorType::kRGB_101010x_SkColorType)
        .value("K_BGR_101010X_SK_COLOR_TYPE", SkColorType::kBGR_101010x_SkColorType)
        .value("K_BGR_101010X_XR_SK_COLOR_TYPE", SkColorType::kBGR_101010x_XR_SkColorType)
        .value("K_BGRA_10101010_XR_SK_COLOR_TYPE", SkColorType::kBGRA_10101010_XR_SkColorType)
        .value("K_RGBA_10X6_SK_COLOR_TYPE", SkColorType::kRGBA_10x6_SkColorType)
        .value("K_GRAY_8_SK_COLOR_TYPE", SkColorType::kGray_8_SkColorType)
        .value("K_RGBA_F16_NORM_SK_COLOR_TYPE", SkColorType::kRGBA_F16Norm_SkColorType)
        .value("K_RGBA_F16_SK_COLOR_TYPE", SkColorType::kRGBA_F16_SkColorType)
        .value("K_RGB_F16_F16_F16X_SK_COLOR_TYPE", SkColorType::kRGB_F16F16F16x_SkColorType)
        .value("K_RGBA_F32_SK_COLOR_TYPE", SkColorType::kRGBA_F32_SkColorType)
        .value("K_R8_G8_UNORM_SK_COLOR_TYPE", SkColorType::kR8G8_unorm_SkColorType)
        .value("K_A16_FLOAT_SK_COLOR_TYPE", SkColorType::kA16_float_SkColorType)
        .value("K_R16_G16_FLOAT_SK_COLOR_TYPE", SkColorType::kR16G16_float_SkColorType)
        .value("K_A16_UNORM_SK_COLOR_TYPE", SkColorType::kA16_unorm_SkColorType)
        .value("K_R16_G16_UNORM_SK_COLOR_TYPE", SkColorType::kR16G16_unorm_SkColorType)
        .value("K_R16_G16_B16_A16_UNORM_SK_COLOR_TYPE", SkColorType::kR16G16B16A16_unorm_SkColorType)
        .value("K_SRGBA_8888_SK_COLOR_TYPE", SkColorType::kSRGBA_8888_SkColorType)
        .value("K_R8_UNORM_SK_COLOR_TYPE", SkColorType::kR8_unorm_SkColorType)
        .value("K_LAST_ENUM_SK_COLOR_TYPE", SkColorType::kLastEnum_SkColorType)
        .value("K_N32_SK_COLOR_TYPE", SkColorType::kN32_SkColorType)
        .export_values()
    ;

}