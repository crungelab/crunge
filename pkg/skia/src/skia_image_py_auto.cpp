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
        )
    .def("raster_from_compressed_texture_data", &SkImages::RasterFromCompressedTextureData
        , py::arg("data")
        , py::arg("width")
        , py::arg("height")
        , py::arg("type")
        )
    .def("deferred_from_encoded_data", &SkImages::DeferredFromEncodedData
        , py::arg("encoded")
        , py::arg("alpha_type") = std::nullopt
        )
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
        )
    .def("deferred_from_picture", py::overload_cast<sk_sp<SkPicture>, const SkISize &, const SkMatrix *, const SkPaint *, SkImages::BitDepth, sk_sp<SkColorSpace>>(&SkImages::DeferredFromPicture)
        , py::arg("picture")
        , py::arg("dimensions")
        , py::arg("matrix")
        , py::arg("paint")
        , py::arg("bit_depth")
        , py::arg("color_space")
        )
    .def("raster_from_pixmap_copy", &SkImages::RasterFromPixmapCopy
        , py::arg("pixmap")
        )
    .def("raster_from_pixmap", &SkImages::RasterFromPixmap
        , py::arg("pixmap")
        , py::arg("raster_release_proc")
        , py::arg("release_context")
        )
    .def("raster_from_data", &SkImages::RasterFromData
        , py::arg("info")
        , py::arg("pixels")
        , py::arg("row_bytes")
        )
    .def("make_with_filter", &SkImages::MakeWithFilter
        , py::arg("src")
        , py::arg("filter")
        , py::arg("subset")
        , py::arg("clip_bounds")
        , py::arg("out_subset")
        , py::arg("offset")
        )
    ;

    py::class_<SkImage,sk_sp<SkImage>> _Image(_skia, "Image");
    registry.on(_skia, "Image", _Image);
        _Image
        .def("image_info", &SkImage::imageInfo
            )
        .def("width", &SkImage::width
            )
        .def("height", &SkImage::height
            )
        .def("dimensions", &SkImage::dimensions
            )
        .def("bounds", &SkImage::bounds
            )
        .def("unique_id", &SkImage::uniqueID
            )
        .def("alpha_type", &SkImage::alphaType
            )
        .def("color_type", &SkImage::colorType
            )
        .def("color_space", &SkImage::colorSpace
            )
        .def("ref_color_space", &SkImage::refColorSpace
            )
        .def("is_alpha_only", &SkImage::isAlphaOnly
            )
        .def("is_opaque", &SkImage::isOpaque
            )
        .def("make_shader", py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix *>(&SkImage::makeShader, py::const_)
            , py::arg("tmx")
            , py::arg("tmy")
            , py::arg("arg2")
            , py::arg("local_matrix") = nullptr
            )
        .def("make_shader", py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix &>(&SkImage::makeShader, py::const_)
            , py::arg("tmx")
            , py::arg("tmy")
            , py::arg("sampling")
            , py::arg("lm")
            )
        .def("make_shader", py::overload_cast<const SkSamplingOptions &, const SkMatrix &>(&SkImage::makeShader, py::const_)
            , py::arg("sampling")
            , py::arg("lm")
            )
        .def("make_shader", py::overload_cast<const SkSamplingOptions &, const SkMatrix *>(&SkImage::makeShader, py::const_)
            , py::arg("sampling")
            , py::arg("lm") = nullptr
            )
        .def("make_raw_shader", py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix *>(&SkImage::makeRawShader, py::const_)
            , py::arg("tmx")
            , py::arg("tmy")
            , py::arg("arg2")
            , py::arg("local_matrix") = nullptr
            )
        .def("make_raw_shader", py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix &>(&SkImage::makeRawShader, py::const_)
            , py::arg("tmx")
            , py::arg("tmy")
            , py::arg("sampling")
            , py::arg("lm")
            )
        .def("make_raw_shader", py::overload_cast<const SkSamplingOptions &, const SkMatrix &>(&SkImage::makeRawShader, py::const_)
            , py::arg("sampling")
            , py::arg("lm")
            )
        .def("make_raw_shader", py::overload_cast<const SkSamplingOptions &, const SkMatrix *>(&SkImage::makeRawShader, py::const_)
            , py::arg("sampling")
            , py::arg("lm") = nullptr
            )
        .def("peek_pixels", &SkImage::peekPixels
            , py::arg("pixmap")
            )
        .def("is_texture_backed", &SkImage::isTextureBacked
            )
        .def("texture_size", &SkImage::textureSize
            )
        ;

        py::enum_<SkImage::CachingHint>(_Image, "CachingHint", py::arithmetic())
            .value("K_ALLOW_CACHING_HINT", SkImage::CachingHint::kAllow_CachingHint)
            .value("K_DISALLOW_CACHING_HINT", SkImage::CachingHint::kDisallow_CachingHint)
            .export_values()
        ;
        _Image
        .def("read_pixels", py::overload_cast<const SkImageInfo &, void *, size_t, int, int, SkImage::CachingHint>(&SkImage::readPixels, py::const_)
            , py::arg("dst_info")
            , py::arg("dst_pixels")
            , py::arg("dst_row_bytes")
            , py::arg("src_x")
            , py::arg("src_y")
            , py::arg("caching_hint") = SkImage::CachingHint::kAllow_CachingHint
            )
        .def("read_pixels", py::overload_cast<const SkPixmap &, int, int, SkImage::CachingHint>(&SkImage::readPixels, py::const_)
            , py::arg("dst")
            , py::arg("src_x")
            , py::arg("src_y")
            , py::arg("caching_hint") = SkImage::CachingHint::kAllow_CachingHint
            )
        ;

        py::class_<SkImage::AsyncReadResult> _ImageAsyncReadResult(_skia, "ImageAsyncReadResult");
        registry.on(_skia, "ImageAsyncReadResult", _ImageAsyncReadResult);
            _ImageAsyncReadResult
            .def("count", &SkImage::AsyncReadResult::count
                )
            .def("data", &SkImage::AsyncReadResult::data
                , py::arg("i")
                )
            .def("row_bytes", &SkImage::AsyncReadResult::rowBytes
                , py::arg("i")
                )
        ;

        py::enum_<SkImage::RescaleGamma>(_Image, "RescaleGamma", py::arithmetic())
            .value("K_SRC", SkImage::RescaleGamma::kSrc)
            .value("K_LINEAR", SkImage::RescaleGamma::kLinear)
            .export_values()
        ;
        py::enum_<SkImage::RescaleMode>(_Image, "RescaleMode", py::arithmetic())
            .value("K_NEAREST", SkImage::RescaleMode::kNearest)
            .value("K_LINEAR", SkImage::RescaleMode::kLinear)
            .value("K_REPEATED_LINEAR", SkImage::RescaleMode::kRepeatedLinear)
            .value("K_REPEATED_CUBIC", SkImage::RescaleMode::kRepeatedCubic)
            .export_values()
        ;
        _Image
        .def("async_rescale_and_read_pixels", &SkImage::asyncRescaleAndReadPixels
            , py::arg("info")
            , py::arg("src_rect")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            )
        .def("async_rescale_and_read_pixels_yuv420", &SkImage::asyncRescaleAndReadPixelsYUV420
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            )
        .def("async_rescale_and_read_pixels_yuva420", &SkImage::asyncRescaleAndReadPixelsYUVA420
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            )
        .def("scale_pixels", &SkImage::scalePixels
            , py::arg("dst")
            , py::arg("arg1")
            , py::arg("caching_hint") = SkImage::CachingHint::kAllow_CachingHint
            )
        .def("make_scaled", py::overload_cast<skgpu::graphite::Recorder *, const SkImageInfo &, const SkSamplingOptions &>(&SkImage::makeScaled, py::const_)
            , py::arg("arg0")
            , py::arg("arg1")
            , py::arg("arg2")
            )
        .def("make_scaled", py::overload_cast<const SkImageInfo &, const SkSamplingOptions &>(&SkImage::makeScaled, py::const_)
            , py::arg("info")
            , py::arg("sampling")
            )
        .def("ref_encoded_data", &SkImage::refEncodedData
            )
        ;

        py::class_<SkImage::RequiredProperties> _ImageRequiredProperties(_skia, "ImageRequiredProperties");
        registry.on(_skia, "ImageRequiredProperties", _ImageRequiredProperties);
            _ImageRequiredProperties
            .def_readwrite("f_mipmapped", &SkImage::RequiredProperties::fMipmapped)
        ;

        _Image
        .def("make_subset", py::overload_cast<skgpu::graphite::Recorder *, const SkIRect &, SkImage::RequiredProperties>(&SkImage::makeSubset, py::const_)
            , py::arg("arg0")
            , py::arg("subset")
            , py::arg("arg2")
            )
        .def("has_mipmaps", &SkImage::hasMipmaps
            )
        .def("is_protected", &SkImage::isProtected
            )
        .def("with_default_mipmaps", &SkImage::withDefaultMipmaps
            )
        .def("make_raster_image", py::overload_cast<SkImage::CachingHint>(&SkImage::makeRasterImage, py::const_)
            , py::arg("caching_hint") = SkImage::CachingHint::kDisallow_CachingHint
            )
        ;

        py::enum_<SkImage::LegacyBitmapMode>(_Image, "LegacyBitmapMode", py::arithmetic())
            .value("K_RO_LEGACY_BITMAP_MODE", SkImage::LegacyBitmapMode::kRO_LegacyBitmapMode)
            .export_values()
        ;
        _Image
        .def("as_legacy_bitmap", &SkImage::asLegacyBitmap
            , py::arg("bitmap")
            , py::arg("legacy_bitmap_mode") = SkImage::LegacyBitmapMode::kRO_LegacyBitmapMode
            )
        .def("is_lazy_generated", &SkImage::isLazyGenerated
            )
        .def("make_color_space", py::overload_cast<skgpu::graphite::Recorder *, sk_sp<SkColorSpace>, SkImage::RequiredProperties>(&SkImage::makeColorSpace, py::const_)
            , py::arg("arg0")
            , py::arg("target_color_space")
            , py::arg("arg2")
            )
        .def("make_color_type_and_color_space", py::overload_cast<skgpu::graphite::Recorder *, SkColorType, sk_sp<SkColorSpace>, SkImage::RequiredProperties>(&SkImage::makeColorTypeAndColorSpace, py::const_)
            , py::arg("arg0")
            , py::arg("target_color_type")
            , py::arg("target_color_space")
            , py::arg("arg3")
            )
        .def("reinterpret_color_space", &SkImage::reinterpretColorSpace
            , py::arg("new_color_space")
            )
    ;


}