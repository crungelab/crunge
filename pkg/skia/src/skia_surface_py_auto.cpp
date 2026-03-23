#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include "include/core/SkSurface.h"
#include "include/gpu/graphite/Recorder.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkCapabilities.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkBitmap.h"

namespace py = pybind11;

void init_skia_surface_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkSurfaces::BackendSurfaceAccess>(_skia, "BackendSurfaceAccess", py::arithmetic())
        .value("K_NO_ACCESS", SkSurfaces::BackendSurfaceAccess::kNoAccess)
        .value("K_PRESENT", SkSurfaces::BackendSurfaceAccess::kPresent)
        .export_values()
    ;
    _skia
    .def("null", &SkSurfaces::Null
        , py::arg("width")
        , py::arg("height")
        )
    .def("raster", py::overload_cast<const SkImageInfo &, size_t, const SkSurfaceProps *>(&SkSurfaces::Raster)
        , py::arg("image_info")
        , py::arg("row_bytes")
        , py::arg("surface_props")
        )
    .def("wrap_pixels", py::overload_cast<const SkImageInfo &, void *, size_t, const SkSurfaceProps *>(&SkSurfaces::WrapPixels)
        , py::arg("image_info")
        , py::arg("pixels")
        , py::arg("row_bytes")
        , py::arg("surface_props") = nullptr
        )
    .def("wrap_pixels", py::overload_cast<const SkImageInfo &, void *, size_t, SkSurfaces::PixelsReleaseProc, void *, const SkSurfaceProps *>(&SkSurfaces::WrapPixels)
        , py::arg("image_info")
        , py::arg("pixels")
        , py::arg("row_bytes")
        , py::arg("arg3")
        , py::arg("context")
        , py::arg("surface_props") = nullptr
        )
    ;

    py::class_<SkSurface> _Surface(_skia, "Surface");
    registry.on(_skia, "Surface", _Surface);
        _Surface
        .def("width", &SkSurface::width
            )
        .def("height", &SkSurface::height
            )
        .def("image_info", &SkSurface::imageInfo
            )
        .def("generation_id", &SkSurface::generationID
            )
        ;

        py::enum_<SkSurface::ContentChangeMode>(_Surface, "ContentChangeMode", py::arithmetic())
            .value("K_DISCARD_CONTENT_CHANGE_MODE", SkSurface::ContentChangeMode::kDiscard_ContentChangeMode)
            .value("K_RETAIN_CONTENT_CHANGE_MODE", SkSurface::ContentChangeMode::kRetain_ContentChangeMode)
            .export_values()
        ;
        _Surface
        .def("notify_content_will_change", &SkSurface::notifyContentWillChange
            , py::arg("mode")
            )
        .def("recorder", &SkSurface::recorder
            )
        ;

        py::enum_<SkSurface::BackendHandleAccess>(_Surface, "BackendHandleAccess", py::arithmetic())
            .value("K_FLUSH_READ", SkSurface::BackendHandleAccess::kFlushRead)
            .value("K_FLUSH_WRITE", SkSurface::BackendHandleAccess::kFlushWrite)
            .value("K_DISCARD_WRITE", SkSurface::BackendHandleAccess::kDiscardWrite)
            .value("K_FLUSH_READ_BACKEND_HANDLE_ACCESS", SkSurface::BackendHandleAccess::kFlushRead_BackendHandleAccess)
            .value("K_FLUSH_WRITE_BACKEND_HANDLE_ACCESS", SkSurface::BackendHandleAccess::kFlushWrite_BackendHandleAccess)
            .value("K_DISCARD_WRITE_BACKEND_HANDLE_ACCESS", SkSurface::BackendHandleAccess::kDiscardWrite_BackendHandleAccess)
            .export_values()
        ;
        _Surface
        .def("get_canvas", &SkSurface::getCanvas
            , py::return_value_policy::reference_internal)
        .def("capabilities", &SkSurface::capabilities
            )
        .def("make_surface", py::overload_cast<const SkImageInfo &>(&SkSurface::makeSurface)
            , py::arg("image_info")
            )
        .def("make_surface", py::overload_cast<int, int>(&SkSurface::makeSurface)
            , py::arg("width")
            , py::arg("height")
            )
        .def("make_image_snapshot", py::overload_cast<>(&SkSurface::makeImageSnapshot)
            )
        .def("make_image_snapshot", py::overload_cast<const SkIRect &>(&SkSurface::makeImageSnapshot)
            , py::arg("bounds")
            )
        .def("make_temporary_image", &SkSurface::makeTemporaryImage
            )
        .def("draw", py::overload_cast<SkCanvas *, SkScalar, SkScalar, const SkSamplingOptions &, const SkPaint *>(&SkSurface::draw)
            , py::arg("canvas")
            , py::arg("x")
            , py::arg("y")
            , py::arg("sampling")
            , py::arg("paint")
            )
        .def("draw", py::overload_cast<SkCanvas *, SkScalar, SkScalar, const SkPaint *>(&SkSurface::draw)
            , py::arg("canvas")
            , py::arg("x")
            , py::arg("y")
            , py::arg("paint") = nullptr
            )
        .def("peek_pixels", &SkSurface::peekPixels
            , py::arg("pixmap")
            )
        .def("read_pixels", py::overload_cast<const SkPixmap &, int, int>(&SkSurface::readPixels)
            , py::arg("dst")
            , py::arg("src_x")
            , py::arg("src_y")
            )
        .def("read_pixels", py::overload_cast<const SkImageInfo &, void *, size_t, int, int>(&SkSurface::readPixels)
            , py::arg("dst_info")
            , py::arg("dst_pixels")
            , py::arg("dst_row_bytes")
            , py::arg("src_x")
            , py::arg("src_y")
            )
        .def("read_pixels", py::overload_cast<const SkBitmap &, int, int>(&SkSurface::readPixels)
            , py::arg("dst")
            , py::arg("src_x")
            , py::arg("src_y")
            )
        .def("async_rescale_and_read_pixels", &SkSurface::asyncRescaleAndReadPixels
            , py::arg("info")
            , py::arg("src_rect")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            )
        .def("async_rescale_and_read_pixels_yuv420", &SkSurface::asyncRescaleAndReadPixelsYUV420
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            )
        .def("async_rescale_and_read_pixels_yuva420", &SkSurface::asyncRescaleAndReadPixelsYUVA420
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            )
        .def("write_pixels", py::overload_cast<const SkPixmap &, int, int>(&SkSurface::writePixels)
            , py::arg("src")
            , py::arg("dst_x")
            , py::arg("dst_y")
            )
        .def("write_pixels", py::overload_cast<const SkBitmap &, int, int>(&SkSurface::writePixels)
            , py::arg("src")
            , py::arg("dst_x")
            , py::arg("dst_y")
            )
        .def("props", &SkSurface::props
            )
    ;


}