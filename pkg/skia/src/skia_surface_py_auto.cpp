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
        , py::return_value_policy::automatic_reference)
    .def("raster", py::overload_cast<const SkImageInfo &, unsigned long, const SkSurfaceProps *>(&SkSurfaces::Raster)
        , py::arg("image_info")
        , py::arg("row_bytes")
        , py::arg("surface_props")
        , py::return_value_policy::automatic_reference)
    .def("wrap_pixels", py::overload_cast<const SkImageInfo &, void *, unsigned long, const SkSurfaceProps *>(&SkSurfaces::WrapPixels)
        , py::arg("image_info")
        , py::arg("pixels")
        , py::arg("row_bytes")
        , py::arg("surface_props") = nullptr
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<SkSurface> Surface(_skia, "Surface");
    registry.on(_skia, "Surface", Surface);
        Surface
        .def("width", &SkSurface::width
            , py::return_value_policy::automatic_reference)
        .def("height", &SkSurface::height
            , py::return_value_policy::automatic_reference)
        .def("image_info", &SkSurface::imageInfo
            , py::return_value_policy::automatic_reference)
        .def("generation_id", &SkSurface::generationID
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkSurface::ContentChangeMode>(_skia, "ContentChangeMode", py::arithmetic())
            .value("K_DISCARD_CONTENT_CHANGE_MODE", SkSurface::ContentChangeMode::kDiscard_ContentChangeMode)
            .value("K_RETAIN_CONTENT_CHANGE_MODE", SkSurface::ContentChangeMode::kRetain_ContentChangeMode)
            .export_values()
        ;

        Surface
        .def("notify_content_will_change", &SkSurface::notifyContentWillChange
            , py::arg("mode")
            , py::return_value_policy::automatic_reference)
        .def("recorder", &SkSurface::recorder
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkSurface::BackendHandleAccess>(_skia, "BackendHandleAccess", py::arithmetic())
            .value("K_FLUSH_READ", SkSurface::BackendHandleAccess::kFlushRead)
            .value("K_FLUSH_WRITE", SkSurface::BackendHandleAccess::kFlushWrite)
            .value("K_DISCARD_WRITE", SkSurface::BackendHandleAccess::kDiscardWrite)
            .value("K_FLUSH_READ_BACKEND_HANDLE_ACCESS", SkSurface::BackendHandleAccess::kFlushRead_BackendHandleAccess)
            .value("K_FLUSH_WRITE_BACKEND_HANDLE_ACCESS", SkSurface::BackendHandleAccess::kFlushWrite_BackendHandleAccess)
            .value("K_DISCARD_WRITE_BACKEND_HANDLE_ACCESS", SkSurface::BackendHandleAccess::kDiscardWrite_BackendHandleAccess)
            .export_values()
        ;

        Surface
        .def("get_canvas", &SkSurface::getCanvas
            , py::return_value_policy::automatic_reference)
        .def("capabilities", &SkSurface::capabilities
            , py::return_value_policy::automatic_reference)
        .def("make_surface", py::overload_cast<const SkImageInfo &>(&SkSurface::makeSurface)
            , py::arg("image_info")
            , py::return_value_policy::automatic_reference)
        .def("make_image_snapshot", py::overload_cast<>(&SkSurface::makeImageSnapshot)
            , py::return_value_policy::automatic_reference)
        .def("make_temporary_image", &SkSurface::makeTemporaryImage
            , py::return_value_policy::automatic_reference)
        .def("draw", py::overload_cast<SkCanvas *, float, float, const SkSamplingOptions &, const SkPaint *>(&SkSurface::draw)
            , py::arg("canvas")
            , py::arg("x")
            , py::arg("y")
            , py::arg("sampling")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("peek_pixels", &SkSurface::peekPixels
            , py::arg("pixmap")
            , py::return_value_policy::automatic_reference)
        .def("read_pixels", py::overload_cast<const SkPixmap &, int, int>(&SkSurface::readPixels)
            , py::arg("dst")
            , py::arg("src_x")
            , py::arg("src_y")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels", &SkSurface::asyncRescaleAndReadPixels
            , py::arg("info")
            , py::arg("src_rect")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels_yuv420", &SkSurface::asyncRescaleAndReadPixelsYUV420
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels_yuva420", &SkSurface::asyncRescaleAndReadPixelsYUVA420
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("write_pixels", py::overload_cast<const SkPixmap &, int, int>(&SkSurface::writePixels)
            , py::arg("src")
            , py::arg("dst_x")
            , py::arg("dst_y")
            , py::return_value_policy::automatic_reference)
        .def("props", &SkSurface::props
            , py::return_value_policy::reference)
    ;


}