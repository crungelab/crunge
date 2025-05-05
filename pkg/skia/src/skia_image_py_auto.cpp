#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkImage.h>
#include <include/core/SkColorSpace.h>
#include <include/core/SkPicture.h>
#include <include/core/SkShader.h>
#include <include/core/SkSamplingOptions.h>
#include <include/core/SkPixmap.h>
#include <include/core/SkData.h>
#include <include/core/SkMatrix.h>
#include <include/core/SkBitmap.h>
#include <include/core/SkImageGenerator.h>
#include <include/core/SkPaint.h>
#include <include/core/SkSurfaceProps.h>
#include <include/core/SkImageFilter.h>

#include <include/gpu/graphite/Recorder.h>


namespace py = pybind11;

void init_skia_image_py_auto(py::module &_skia, Registry &registry) {
    _skia
    .def("raster_from_bitmap", &SkImages::RasterFromBitmap
        , py::arg("bitmap")
        , py::return_value_policy::automatic_reference)
    .def("raster_from_compressed_texture_data", &SkImages::RasterFromCompressedTextureData
        , py::arg("data")
        , py::arg("width")
        , py::arg("height")
        , py::arg("type")
        , py::return_value_policy::automatic_reference)
    .def("deferred_from_encoded_data", &SkImages::DeferredFromEncodedData
        , py::arg("encoded")
        , py::arg("alpha_type") = std::nullopt
        , py::return_value_policy::automatic_reference)
    ;

    py::enum_<SkImages::BitDepth>(_skia, "BitDepth", py::arithmetic())
        .value("K_U8", SkImages::BitDepth::kU8)
        .value("K_F16", SkImages::BitDepth::kF16)
        .export_values()
    ;
    _skia
    .def("deferred_from_picture", py::overload_cast<sk_sp<SkPicture>, const SkISize &, const SkMatrix *, const SkPaint *, SkImages::BitDepth, sk_sp<SkColorSpace>, SkSurfaceProps>(&SkImages::DeferredFromPicture)
        , py::arg("picture")
        , py::arg("dimensions")
        , py::arg("matrix")
        , py::arg("paint")
        , py::arg("bit_depth")
        , py::arg("color_space")
        , py::arg("props")
        , py::return_value_policy::automatic_reference)
    .def("deferred_from_picture", py::overload_cast<sk_sp<SkPicture>, const SkISize &, const SkMatrix *, const SkPaint *, SkImages::BitDepth, sk_sp<SkColorSpace>>(&SkImages::DeferredFromPicture)
        , py::arg("picture")
        , py::arg("dimensions")
        , py::arg("matrix")
        , py::arg("paint")
        , py::arg("bit_depth")
        , py::arg("color_space")
        , py::return_value_policy::automatic_reference)
    .def("raster_from_pixmap_copy", &SkImages::RasterFromPixmapCopy
        , py::arg("pixmap")
        , py::return_value_policy::automatic_reference)
    .def("raster_from_pixmap", &SkImages::RasterFromPixmap
        , py::arg("pixmap")
        , py::arg("raster_release_proc")
        , py::arg("release_context")
        , py::return_value_policy::automatic_reference)
    .def("raster_from_data", &SkImages::RasterFromData
        , py::arg("info")
        , py::arg("pixels")
        , py::arg("row_bytes")
        , py::return_value_policy::automatic_reference)
    .def("make_with_filter", &SkImages::MakeWithFilter
        , py::arg("src")
        , py::arg("filter")
        , py::arg("subset")
        , py::arg("clip_bounds")
        , py::arg("out_subset")
        , py::arg("offset")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<SkImage,sk_sp<SkImage>> Image(_skia, "Image");
    registry.on(_skia, "Image", Image);
        Image
        .def("image_info", &SkImage::imageInfo
            , py::return_value_policy::reference)
        .def("width", &SkImage::width
            , py::return_value_policy::automatic_reference)
        .def("height", &SkImage::height
            , py::return_value_policy::automatic_reference)
        .def("dimensions", &SkImage::dimensions
            , py::return_value_policy::automatic_reference)
        .def("bounds", &SkImage::bounds
            , py::return_value_policy::automatic_reference)
        .def("unique_id", &SkImage::uniqueID
            , py::return_value_policy::automatic_reference)
        .def("alpha_type", &SkImage::alphaType
            , py::return_value_policy::automatic_reference)
        .def("color_type", &SkImage::colorType
            , py::return_value_policy::automatic_reference)
        .def("color_space", &SkImage::colorSpace
            , py::return_value_policy::automatic_reference)
        .def("ref_color_space", &SkImage::refColorSpace
            , py::return_value_policy::automatic_reference)
        .def("is_alpha_only", &SkImage::isAlphaOnly
            , py::return_value_policy::automatic_reference)
        .def("is_opaque", &SkImage::isOpaque
            , py::return_value_policy::automatic_reference)
        .def("make_shader", py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix *>(&SkImage::makeShader, py::const_)
            , py::arg("tmx")
            , py::arg("tmy")
            , py::arg("")
            , py::arg("local_matrix") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("make_shader", py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix &>(&SkImage::makeShader, py::const_)
            , py::arg("tmx")
            , py::arg("tmy")
            , py::arg("sampling")
            , py::arg("lm")
            , py::return_value_policy::automatic_reference)
        .def("make_shader", py::overload_cast<const SkSamplingOptions &, const SkMatrix &>(&SkImage::makeShader, py::const_)
            , py::arg("sampling")
            , py::arg("lm")
            , py::return_value_policy::automatic_reference)
        .def("make_shader", py::overload_cast<const SkSamplingOptions &, const SkMatrix *>(&SkImage::makeShader, py::const_)
            , py::arg("sampling")
            , py::arg("lm") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("make_raw_shader", py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix *>(&SkImage::makeRawShader, py::const_)
            , py::arg("tmx")
            , py::arg("tmy")
            , py::arg("")
            , py::arg("local_matrix") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("make_raw_shader", py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix &>(&SkImage::makeRawShader, py::const_)
            , py::arg("tmx")
            , py::arg("tmy")
            , py::arg("sampling")
            , py::arg("lm")
            , py::return_value_policy::automatic_reference)
        .def("make_raw_shader", py::overload_cast<const SkSamplingOptions &, const SkMatrix &>(&SkImage::makeRawShader, py::const_)
            , py::arg("sampling")
            , py::arg("lm")
            , py::return_value_policy::automatic_reference)
        .def("make_raw_shader", py::overload_cast<const SkSamplingOptions &, const SkMatrix *>(&SkImage::makeRawShader, py::const_)
            , py::arg("sampling")
            , py::arg("lm") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("peek_pixels", &SkImage::peekPixels
            , py::arg("pixmap")
            , py::return_value_policy::automatic_reference)
        .def("is_texture_backed", &SkImage::isTextureBacked
            , py::return_value_policy::automatic_reference)
        .def("texture_size", &SkImage::textureSize
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkImage::CachingHint>(Image, "CachingHint", py::arithmetic())
            .value("K_ALLOW_CACHING_HINT", SkImage::CachingHint::kAllow_CachingHint)
            .value("K_DISALLOW_CACHING_HINT", SkImage::CachingHint::kDisallow_CachingHint)
            .export_values()
        ;
        Image
        .def("read_pixels", py::overload_cast<const SkImageInfo &, void *, unsigned long, int, int, SkImage::CachingHint>(&SkImage::readPixels, py::const_)
            , py::arg("dst_info")
            , py::arg("dst_pixels")
            , py::arg("dst_row_bytes")
            , py::arg("src_x")
            , py::arg("src_y")
            , py::arg("caching_hint") = SkImage::CachingHint::kAllow_CachingHint
            , py::return_value_policy::automatic_reference)
        .def("read_pixels", py::overload_cast<const SkPixmap &, int, int, SkImage::CachingHint>(&SkImage::readPixels, py::const_)
            , py::arg("dst")
            , py::arg("src_x")
            , py::arg("src_y")
            , py::arg("caching_hint") = SkImage::CachingHint::kAllow_CachingHint
            , py::return_value_policy::automatic_reference)
        ;

        py::class_<SkImage::AsyncReadResult> ImageAsyncReadResult(_skia, "ImageAsyncReadResult");
        registry.on(_skia, "ImageAsyncReadResult", ImageAsyncReadResult);
            ImageAsyncReadResult
            .def("count", &SkImage::AsyncReadResult::count
                , py::return_value_policy::automatic_reference)
            .def("data", &SkImage::AsyncReadResult::data
                , py::arg("i")
                , py::return_value_policy::automatic_reference)
            .def("row_bytes", &SkImage::AsyncReadResult::rowBytes
                , py::arg("i")
                , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkImage::RescaleGamma>(Image, "RescaleGamma", py::arithmetic())
            .value("K_SRC", SkImage::RescaleGamma::kSrc)
            .value("K_LINEAR", SkImage::RescaleGamma::kLinear)
            .export_values()
        ;
        py::enum_<SkImage::RescaleMode>(Image, "RescaleMode", py::arithmetic())
            .value("K_NEAREST", SkImage::RescaleMode::kNearest)
            .value("K_LINEAR", SkImage::RescaleMode::kLinear)
            .value("K_REPEATED_LINEAR", SkImage::RescaleMode::kRepeatedLinear)
            .value("K_REPEATED_CUBIC", SkImage::RescaleMode::kRepeatedCubic)
            .export_values()
        ;
        Image
        .def("async_rescale_and_read_pixels", &SkImage::asyncRescaleAndReadPixels
            , py::arg("info")
            , py::arg("src_rect")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels_yuv420", &SkImage::asyncRescaleAndReadPixelsYUV420
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels_yuva420", &SkImage::asyncRescaleAndReadPixelsYUVA420
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("scale_pixels", &SkImage::scalePixels
            , py::arg("dst")
            , py::arg("")
            , py::arg("caching_hint") = SkImage::CachingHint::kAllow_CachingHint
            , py::return_value_policy::automatic_reference)
        .def("make_scaled", py::overload_cast<skgpu::graphite::Recorder *, const SkImageInfo &, const SkSamplingOptions &>(&SkImage::makeScaled, py::const_)
            , py::arg("")
            , py::arg("")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("make_scaled", py::overload_cast<const SkImageInfo &, const SkSamplingOptions &>(&SkImage::makeScaled, py::const_)
            , py::arg("info")
            , py::arg("sampling")
            , py::return_value_policy::automatic_reference)
        .def("ref_encoded_data", &SkImage::refEncodedData
            , py::return_value_policy::automatic_reference)
        ;

        py::class_<SkImage::RequiredProperties> ImageRequiredProperties(_skia, "ImageRequiredProperties");
        registry.on(_skia, "ImageRequiredProperties", ImageRequiredProperties);
            ImageRequiredProperties
            .def_readwrite("f_mipmapped", &SkImage::RequiredProperties::fMipmapped)
        ;

        Image
        .def("make_subset", py::overload_cast<skgpu::graphite::Recorder *, const SkIRect &, SkImage::RequiredProperties>(&SkImage::makeSubset, py::const_)
            , py::arg("")
            , py::arg("subset")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("has_mipmaps", &SkImage::hasMipmaps
            , py::return_value_policy::automatic_reference)
        .def("is_protected", &SkImage::isProtected
            , py::return_value_policy::automatic_reference)
        .def("with_default_mipmaps", &SkImage::withDefaultMipmaps
            , py::return_value_policy::automatic_reference)
        .def("make_raster_image", py::overload_cast<SkImage::CachingHint>(&SkImage::makeRasterImage, py::const_)
            , py::arg("caching_hint") = SkImage::CachingHint::kDisallow_CachingHint
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkImage::LegacyBitmapMode>(Image, "LegacyBitmapMode", py::arithmetic())
            .value("K_RO_LEGACY_BITMAP_MODE", SkImage::LegacyBitmapMode::kRO_LegacyBitmapMode)
            .export_values()
        ;
        Image
        .def("as_legacy_bitmap", &SkImage::asLegacyBitmap
            , py::arg("bitmap")
            , py::arg("legacy_bitmap_mode") = SkImage::LegacyBitmapMode::kRO_LegacyBitmapMode
            , py::return_value_policy::automatic_reference)
        .def("is_lazy_generated", &SkImage::isLazyGenerated
            , py::return_value_policy::automatic_reference)
        .def("make_color_space", py::overload_cast<skgpu::graphite::Recorder *, sk_sp<SkColorSpace>, SkImage::RequiredProperties>(&SkImage::makeColorSpace, py::const_)
            , py::arg("")
            , py::arg("target_color_space")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("make_color_type_and_color_space", py::overload_cast<skgpu::graphite::Recorder *, SkColorType, sk_sp<SkColorSpace>, SkImage::RequiredProperties>(&SkImage::makeColorTypeAndColorSpace, py::const_)
            , py::arg("")
            , py::arg("target_color_type")
            , py::arg("target_color_space")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("reinterpret_color_space", &SkImage::reinterpretColorSpace
            , py::arg("new_color_space")
            , py::return_value_policy::automatic_reference)
    ;


}