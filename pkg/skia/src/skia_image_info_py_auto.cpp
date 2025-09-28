#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkImageInfo.h>

#include <include/core/SkColorSpace.h>

namespace py = pybind11;

void init_skia_image_info_py_auto(py::module &_skia, Registry &registry) {
    _skia
    .def("color_type_bytes_per_pixel", &SkColorTypeBytesPerPixel
        , py::arg("ct")
        , py::return_value_policy::automatic_reference)
    .def("color_type_is_always_opaque", &SkColorTypeIsAlwaysOpaque
        , py::arg("ct")
        , py::return_value_policy::automatic_reference)
    .def("color_type_validate_alpha_type", &SkColorTypeValidateAlphaType
        , py::arg("color_type")
        , py::arg("alpha_type")
        , py::arg("canonical") = nullptr
        , py::return_value_policy::automatic_reference)
    ;

    py::enum_<SkYUVColorSpace>(_skia, "YUVColorSpace", py::arithmetic())
        .value("K_JPEG_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kJPEG_Full_SkYUVColorSpace)
        .value("K_REC601_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kRec601_Limited_SkYUVColorSpace)
        .value("K_REC709_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kRec709_Full_SkYUVColorSpace)
        .value("K_REC709_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kRec709_Limited_SkYUVColorSpace)
        .value("K_BT2020_8BIT_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_8bit_Full_SkYUVColorSpace)
        .value("K_BT2020_8BIT_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_8bit_Limited_SkYUVColorSpace)
        .value("K_BT2020_10BIT_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_10bit_Full_SkYUVColorSpace)
        .value("K_BT2020_10BIT_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_10bit_Limited_SkYUVColorSpace)
        .value("K_BT2020_12BIT_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_12bit_Full_SkYUVColorSpace)
        .value("K_BT2020_12BIT_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_12bit_Limited_SkYUVColorSpace)
        .value("K_BT2020_16BIT_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_16bit_Full_SkYUVColorSpace)
        .value("K_BT2020_16BIT_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_16bit_Limited_SkYUVColorSpace)
        .value("K_FCC_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kFCC_Full_SkYUVColorSpace)
        .value("K_FCC_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kFCC_Limited_SkYUVColorSpace)
        .value("K_SMPTE240_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kSMPTE240_Full_SkYUVColorSpace)
        .value("K_SMPTE240_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kSMPTE240_Limited_SkYUVColorSpace)
        .value("K_YDZDX_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYDZDX_Full_SkYUVColorSpace)
        .value("K_YDZDX_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYDZDX_Limited_SkYUVColorSpace)
        .value("K_GBR_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kGBR_Full_SkYUVColorSpace)
        .value("K_GBR_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kGBR_Limited_SkYUVColorSpace)
        .value("K_Y_CG_CO_8BIT_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYCgCo_8bit_Full_SkYUVColorSpace)
        .value("K_Y_CG_CO_8BIT_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYCgCo_8bit_Limited_SkYUVColorSpace)
        .value("K_Y_CG_CO_10BIT_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYCgCo_10bit_Full_SkYUVColorSpace)
        .value("K_Y_CG_CO_10BIT_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYCgCo_10bit_Limited_SkYUVColorSpace)
        .value("K_Y_CG_CO_12BIT_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYCgCo_12bit_Full_SkYUVColorSpace)
        .value("K_Y_CG_CO_12BIT_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYCgCo_12bit_Limited_SkYUVColorSpace)
        .value("K_Y_CG_CO_16BIT_FULL_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYCgCo_16bit_Full_SkYUVColorSpace)
        .value("K_Y_CG_CO_16BIT_LIMITED_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kYCgCo_16bit_Limited_SkYUVColorSpace)
        .value("K_IDENTITY_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kIdentity_SkYUVColorSpace)
        .value("K_LAST_ENUM_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kLastEnum_SkYUVColorSpace)
        .value("K_JPEG_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kJPEG_SkYUVColorSpace)
        .value("K_REC601_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kRec601_SkYUVColorSpace)
        .value("K_REC709_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kRec709_SkYUVColorSpace)
        .value("K_BT2020_SK_YUV_COLOR_SPACE", SkYUVColorSpace::kBT2020_SkYUVColorSpace)
        .export_values()
    ;
    _skia
    .def("yuv_color_space_is_limited_range", &SkYUVColorSpaceIsLimitedRange
        , py::arg("cs")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<SkColorInfo> _ColorInfo(_skia, "ColorInfo");
    registry.on(_skia, "ColorInfo", _ColorInfo);
        _ColorInfo
        .def(py::init<>())
        .def(py::init<SkColorType, SkAlphaType, sk_sp<SkColorSpace>>()
        , py::arg("ct")
        , py::arg("at")
        , py::arg("cs")
        )
        .def(py::init<const SkColorInfo &>()
        , py::arg("")
        )
        .def("color_space", &SkColorInfo::colorSpace
            , py::return_value_policy::automatic_reference)
        .def("ref_color_space", &SkColorInfo::refColorSpace
            , py::return_value_policy::automatic_reference)
        .def("color_type", &SkColorInfo::colorType
            , py::return_value_policy::automatic_reference)
        .def("alpha_type", &SkColorInfo::alphaType
            , py::return_value_policy::automatic_reference)
        .def("is_opaque", &SkColorInfo::isOpaque
            , py::return_value_policy::automatic_reference)
        .def("gamma_close_to_srgb", &SkColorInfo::gammaCloseToSRGB
            , py::return_value_policy::automatic_reference)
        .def("make_alpha_type", &SkColorInfo::makeAlphaType
            , py::arg("new_alpha_type")
            , py::return_value_policy::automatic_reference)
        .def("make_color_type", &SkColorInfo::makeColorType
            , py::arg("new_color_type")
            , py::return_value_policy::automatic_reference)
        .def("make_color_space", &SkColorInfo::makeColorSpace
            , py::arg("cs")
            , py::return_value_policy::automatic_reference)
        .def("bytes_per_pixel", &SkColorInfo::bytesPerPixel
            , py::return_value_policy::automatic_reference)
        .def("shift_per_pixel", &SkColorInfo::shiftPerPixel
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<SkImageInfo> _ImageInfo(_skia, "ImageInfo");
    registry.on(_skia, "ImageInfo", _ImageInfo);
        _ImageInfo
        .def(py::init<>())
        .def_static("make", py::overload_cast<int, int, SkColorType, SkAlphaType>(&SkImageInfo::Make)
            , py::arg("width")
            , py::arg("height")
            , py::arg("ct")
            , py::arg("at")
            , py::return_value_policy::automatic_reference)
        .def_static("make", py::overload_cast<int, int, SkColorType, SkAlphaType, sk_sp<SkColorSpace>>(&SkImageInfo::Make)
            , py::arg("width")
            , py::arg("height")
            , py::arg("ct")
            , py::arg("at")
            , py::arg("cs")
            , py::return_value_policy::automatic_reference)
        .def_static("make", py::overload_cast<SkISize, SkColorType, SkAlphaType>(&SkImageInfo::Make)
            , py::arg("dimensions")
            , py::arg("ct")
            , py::arg("at")
            , py::return_value_policy::automatic_reference)
        .def_static("make", py::overload_cast<SkISize, SkColorType, SkAlphaType, sk_sp<SkColorSpace>>(&SkImageInfo::Make)
            , py::arg("dimensions")
            , py::arg("ct")
            , py::arg("at")
            , py::arg("cs")
            , py::return_value_policy::automatic_reference)
        .def_static("make", py::overload_cast<SkISize, const SkColorInfo &>(&SkImageInfo::Make)
            , py::arg("dimensions")
            , py::arg("color_info")
            , py::return_value_policy::automatic_reference)
        .def_static("make_n32", py::overload_cast<int, int, SkAlphaType>(&SkImageInfo::MakeN32)
            , py::arg("width")
            , py::arg("height")
            , py::arg("at")
            , py::return_value_policy::automatic_reference)
        .def_static("make_n32", py::overload_cast<int, int, SkAlphaType, sk_sp<SkColorSpace>>(&SkImageInfo::MakeN32)
            , py::arg("width")
            , py::arg("height")
            , py::arg("at")
            , py::arg("cs")
            , py::return_value_policy::automatic_reference)
        .def_static("make_s32", &SkImageInfo::MakeS32
            , py::arg("width")
            , py::arg("height")
            , py::arg("at")
            , py::return_value_policy::automatic_reference)
        .def_static("make_n32_premul", py::overload_cast<int, int>(&SkImageInfo::MakeN32Premul)
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def_static("make_n32_premul", py::overload_cast<int, int, sk_sp<SkColorSpace>>(&SkImageInfo::MakeN32Premul)
            , py::arg("width")
            , py::arg("height")
            , py::arg("cs")
            , py::return_value_policy::automatic_reference)
        .def_static("make_n32_premul", py::overload_cast<SkISize>(&SkImageInfo::MakeN32Premul)
            , py::arg("dimensions")
            , py::return_value_policy::automatic_reference)
        .def_static("make_n32_premul", py::overload_cast<SkISize, sk_sp<SkColorSpace>>(&SkImageInfo::MakeN32Premul)
            , py::arg("dimensions")
            , py::arg("cs")
            , py::return_value_policy::automatic_reference)
        .def_static("make_a8", py::overload_cast<int, int>(&SkImageInfo::MakeA8)
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def_static("make_a8", py::overload_cast<SkISize>(&SkImageInfo::MakeA8)
            , py::arg("dimensions")
            , py::return_value_policy::automatic_reference)
        .def_static("make_unknown", py::overload_cast<int, int>(&SkImageInfo::MakeUnknown)
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def_static("make_unknown", py::overload_cast<>(&SkImageInfo::MakeUnknown)
            , py::return_value_policy::automatic_reference)
        .def("width", &SkImageInfo::width
            , py::return_value_policy::automatic_reference)
        .def("height", &SkImageInfo::height
            , py::return_value_policy::automatic_reference)
        .def("color_type", &SkImageInfo::colorType
            , py::return_value_policy::automatic_reference)
        .def("alpha_type", &SkImageInfo::alphaType
            , py::return_value_policy::automatic_reference)
        .def("color_space", &SkImageInfo::colorSpace
            , py::return_value_policy::automatic_reference)
        .def("ref_color_space", &SkImageInfo::refColorSpace
            , py::return_value_policy::automatic_reference)
        .def("is_empty", &SkImageInfo::isEmpty
            , py::return_value_policy::automatic_reference)
        .def("color_info", &SkImageInfo::colorInfo
            , py::return_value_policy::reference)
        .def("is_opaque", &SkImageInfo::isOpaque
            , py::return_value_policy::automatic_reference)
        .def("dimensions", &SkImageInfo::dimensions
            , py::return_value_policy::automatic_reference)
        .def("bounds", &SkImageInfo::bounds
            , py::return_value_policy::automatic_reference)
        .def("gamma_close_to_srgb", &SkImageInfo::gammaCloseToSRGB
            , py::return_value_policy::automatic_reference)
        .def("make_wh", &SkImageInfo::makeWH
            , py::arg("new_width")
            , py::arg("new_height")
            , py::return_value_policy::automatic_reference)
        .def("make_dimensions", &SkImageInfo::makeDimensions
            , py::arg("new_size")
            , py::return_value_policy::automatic_reference)
        .def("make_alpha_type", &SkImageInfo::makeAlphaType
            , py::arg("new_alpha_type")
            , py::return_value_policy::automatic_reference)
        .def("make_color_type", &SkImageInfo::makeColorType
            , py::arg("new_color_type")
            , py::return_value_policy::automatic_reference)
        .def("make_color_space", &SkImageInfo::makeColorSpace
            , py::arg("cs")
            , py::return_value_policy::automatic_reference)
        .def("bytes_per_pixel", &SkImageInfo::bytesPerPixel
            , py::return_value_policy::automatic_reference)
        .def("shift_per_pixel", &SkImageInfo::shiftPerPixel
            , py::return_value_policy::automatic_reference)
        .def("min_row_bytes64", &SkImageInfo::minRowBytes64
            , py::return_value_policy::automatic_reference)
        .def("min_row_bytes", &SkImageInfo::minRowBytes
            , py::return_value_policy::automatic_reference)
        .def("compute_offset", &SkImageInfo::computeOffset
            , py::arg("x")
            , py::arg("y")
            , py::arg("row_bytes")
            , py::return_value_policy::automatic_reference)
        .def("compute_byte_size", &SkImageInfo::computeByteSize
            , py::arg("row_bytes")
            , py::return_value_policy::automatic_reference)
        .def("compute_min_byte_size", &SkImageInfo::computeMinByteSize
            , py::return_value_policy::automatic_reference)
        .def_static("byte_size_overflowed", &SkImageInfo::ByteSizeOverflowed
            , py::arg("byte_size")
            , py::return_value_policy::automatic_reference)
        .def("valid_row_bytes", &SkImageInfo::validRowBytes
            , py::arg("row_bytes")
            , py::return_value_policy::automatic_reference)
        .def("reset", &SkImageInfo::reset
            , py::return_value_policy::automatic_reference)
        .def("validate", &SkImageInfo::validate
            , py::return_value_policy::automatic_reference)
    ;


}