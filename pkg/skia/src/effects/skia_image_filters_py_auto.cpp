#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/effects/SkImageFilters.h>

#include <include/core/SkMatrix.h>
#include <include/core/SkColorFilter.h>
#include <include/core/SkSamplingOptions.h>
#include <include/core/SkPoint3.h>

#include <include/effects/SkRuntimeEffect.h>



namespace py = pybind11;

void init_skia_image_filters_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkImageFilters> ImageFilters(_skia, "ImageFilters");
    registry.on(_skia, "ImageFilters", ImageFilters);
        py::class_<SkImageFilters::CropRect> ImageFiltersCropRect(_skia, "ImageFiltersCropRect");
        registry.on(_skia, "ImageFiltersCropRect", ImageFiltersCropRect);
            ImageFiltersCropRect
            .def(py::init<>())
            .def(py::init<const SkIRect &>()
            , py::arg("crop")
            )
            .def(py::init<const SkRect &>()
            , py::arg("crop")
            )
            .def(py::init<const std::optional<SkRect> &>()
            , py::arg("crop")
            )
            .def(py::init<std::nullptr_t>()
            , py::arg("")
            )
            .def(py::init<const SkIRect *>()
            , py::arg("optional_crop")
            )
            .def(py::init<const SkRect *>()
            , py::arg("optional_crop")
            )
        ;

        ImageFilters
        .def_static("arithmetic", &SkImageFilters::Arithmetic
            , py::arg("k1")
            , py::arg("k2")
            , py::arg("k3")
            , py::arg("k4")
            , py::arg("enforce_pm_color")
            , py::arg("background")
            , py::arg("foreground")
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("blend", py::overload_cast<SkBlendMode, sk_sp<SkImageFilter>, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::Blend)
            , py::arg("mode")
            , py::arg("background")
            , py::arg("foreground") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("blend", py::overload_cast<sk_sp<SkBlender>, sk_sp<SkImageFilter>, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::Blend)
            , py::arg("blender")
            , py::arg("background")
            , py::arg("foreground") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("blur", py::overload_cast<float, float, SkTileMode, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::Blur)
            , py::arg("sigma_x")
            , py::arg("sigma_y")
            , py::arg("tile_mode")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("blur", py::overload_cast<float, float, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::Blur)
            , py::arg("sigma_x")
            , py::arg("sigma_y")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("color_filter", &SkImageFilters::ColorFilter
            , py::arg("cf")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("compose", &SkImageFilters::Compose
            , py::arg("outer")
            , py::arg("inner")
            , py::return_value_policy::automatic_reference)
        .def_static("crop", py::overload_cast<const SkRect &, SkTileMode, sk_sp<SkImageFilter>>(&SkImageFilters::Crop)
            , py::arg("rect")
            , py::arg("tile_mode")
            , py::arg("input") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("crop", py::overload_cast<const SkRect &, sk_sp<SkImageFilter>>(&SkImageFilters::Crop)
            , py::arg("rect")
            , py::arg("input") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("displacement_map", &SkImageFilters::DisplacementMap
            , py::arg("x_channel_selector")
            , py::arg("y_channel_selector")
            , py::arg("scale")
            , py::arg("displacement")
            , py::arg("color")
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("drop_shadow", py::overload_cast<float, float, float, float, SkRGBA4f<kUnpremul_SkAlphaType>, sk_sp<SkColorSpace>, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::DropShadow)
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("sigma_x")
            , py::arg("sigma_y")
            , py::arg("color")
            , py::arg("color_space")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("drop_shadow", py::overload_cast<float, float, float, float, unsigned int, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::DropShadow)
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("sigma_x")
            , py::arg("sigma_y")
            , py::arg("color")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("drop_shadow_only", py::overload_cast<float, float, float, float, SkRGBA4f<kUnpremul_SkAlphaType>, sk_sp<SkColorSpace>, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::DropShadowOnly)
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("sigma_x")
            , py::arg("sigma_y")
            , py::arg("color")
            , py::arg("")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("drop_shadow_only", py::overload_cast<float, float, float, float, unsigned int, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::DropShadowOnly)
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("sigma_x")
            , py::arg("sigma_y")
            , py::arg("color")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("empty", &SkImageFilters::Empty
            , py::return_value_policy::automatic_reference)
        .def_static("image", py::overload_cast<sk_sp<SkImage>, const SkRect &, const SkRect &, const SkSamplingOptions &>(&SkImageFilters::Image)
            , py::arg("image")
            , py::arg("src_rect")
            , py::arg("dst_rect")
            , py::arg("sampling")
            , py::return_value_policy::automatic_reference)
        .def_static("image", py::overload_cast<sk_sp<SkImage>, const SkSamplingOptions &>(&SkImageFilters::Image)
            , py::arg("image")
            , py::arg("sampling")
            , py::return_value_policy::automatic_reference)
        .def_static("magnifier", &SkImageFilters::Magnifier
            , py::arg("lens_bounds")
            , py::arg("zoom_amount")
            , py::arg("inset")
            , py::arg("sampling")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("matrix_convolution", &SkImageFilters::MatrixConvolution
            , py::arg("kernel_size")
            , py::arg("kernel")
            , py::arg("gain")
            , py::arg("bias")
            , py::arg("kernel_offset")
            , py::arg("tile_mode")
            , py::arg("convolve_alpha")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("matrix_transform", &SkImageFilters::MatrixTransform
            , py::arg("matrix")
            , py::arg("sampling")
            , py::arg("input") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("merge", py::overload_cast<sk_sp<SkImageFilter> *const, int, const SkImageFilters::CropRect &>(&SkImageFilters::Merge)
            , py::arg("filters")
            , py::arg("count")
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("merge", py::overload_cast<sk_sp<SkImageFilter>, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(&SkImageFilters::Merge)
            , py::arg("first")
            , py::arg("second")
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("offset", &SkImageFilters::Offset
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("picture", py::overload_cast<sk_sp<SkPicture>, const SkRect &>(&SkImageFilters::Picture)
            , py::arg("pic")
            , py::arg("target_rect")
            , py::return_value_policy::automatic_reference)
        .def_static("picture", py::overload_cast<sk_sp<SkPicture>>(&SkImageFilters::Picture)
            , py::arg("pic")
            , py::return_value_policy::automatic_reference)
        .def_static("runtime_shader", py::overload_cast<const SkRuntimeEffectBuilder &, std::basic_string_view<char>, sk_sp<SkImageFilter>>(&SkImageFilters::RuntimeShader)
            , py::arg("builder")
            , py::arg("child_shader_name")
            , py::arg("input") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("runtime_shader", py::overload_cast<const SkRuntimeEffectBuilder &, float, std::basic_string_view<char>, sk_sp<SkImageFilter>>(&SkImageFilters::RuntimeShader)
            , py::arg("builder")
            , py::arg("sample_radius")
            , py::arg("child_shader_name")
            , py::arg("input") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("runtime_shader", py::overload_cast<const SkRuntimeEffectBuilder &, std::basic_string_view<char>[], const sk_sp<SkImageFilter>[], int>(&SkImageFilters::RuntimeShader)
            , py::arg("builder")
            , py::arg("child_shader_names")
            , py::arg("inputs")
            , py::arg("input_count")
            , py::return_value_policy::automatic_reference)
        .def_static("runtime_shader", py::overload_cast<const SkRuntimeEffectBuilder &, float, std::basic_string_view<char>[], const sk_sp<SkImageFilter>[], int>(&SkImageFilters::RuntimeShader)
            , py::arg("builder")
            , py::arg("max_sample_radius")
            , py::arg("child_shader_names")
            , py::arg("inputs")
            , py::arg("input_count")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkImageFilters::Dither>(ImageFilters, "Dither", py::arithmetic())
            .value("K_NO", SkImageFilters::Dither::kNo)
            .value("K_YES", SkImageFilters::Dither::kYes)
            .export_values()
        ;
        ImageFilters
        .def_static("shader", py::overload_cast<sk_sp<SkShader>, const SkImageFilters::CropRect &>(&SkImageFilters::Shader)
            , py::arg("shader")
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("shader", py::overload_cast<sk_sp<SkShader>, SkImageFilters::Dither, const SkImageFilters::CropRect &>(&SkImageFilters::Shader)
            , py::arg("shader")
            , py::arg("dither")
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("tile", &SkImageFilters::Tile
            , py::arg("src")
            , py::arg("dst")
            , py::arg("input") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("dilate", &SkImageFilters::Dilate
            , py::arg("radius_x")
            , py::arg("radius_y")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("erode", &SkImageFilters::Erode
            , py::arg("radius_x")
            , py::arg("radius_y")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("distant_lit_diffuse", &SkImageFilters::DistantLitDiffuse
            , py::arg("direction")
            , py::arg("light_color")
            , py::arg("surface_scale")
            , py::arg("kd")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("point_lit_diffuse", &SkImageFilters::PointLitDiffuse
            , py::arg("location")
            , py::arg("light_color")
            , py::arg("surface_scale")
            , py::arg("kd")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("spot_lit_diffuse", &SkImageFilters::SpotLitDiffuse
            , py::arg("location")
            , py::arg("target")
            , py::arg("falloff_exponent")
            , py::arg("cutoff_angle")
            , py::arg("light_color")
            , py::arg("surface_scale")
            , py::arg("kd")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("distant_lit_specular", &SkImageFilters::DistantLitSpecular
            , py::arg("direction")
            , py::arg("light_color")
            , py::arg("surface_scale")
            , py::arg("ks")
            , py::arg("shininess")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("point_lit_specular", &SkImageFilters::PointLitSpecular
            , py::arg("location")
            , py::arg("light_color")
            , py::arg("surface_scale")
            , py::arg("ks")
            , py::arg("shininess")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
        .def_static("spot_lit_specular", &SkImageFilters::SpotLitSpecular
            , py::arg("location")
            , py::arg("target")
            , py::arg("falloff_exponent")
            , py::arg("cutoff_angle")
            , py::arg("light_color")
            , py::arg("surface_scale")
            , py::arg("ks")
            , py::arg("shininess")
            , py::arg("input") = nullptr
            , py::arg("crop_rect") = SkImageFilters::CropRect{}
            , py::return_value_policy::automatic_reference)
    ;


}