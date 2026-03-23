#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkCanvas.h>

#include <include/core/SkAlphaType.h>
#include <include/core/SkBitmap.h>
#include <include/core/SkBlendMode.h>
#include <include/core/SkBlender.h>
#include <include/core/SkBlurTypes.h>
#include <include/core/SkColorFilter.h>
#include <include/core/SkColorSpace.h>
#include <include/core/SkColorType.h>
#include <include/core/SkImage.h>
#include <include/core/SkImageFilter.h>
#include <include/core/SkMaskFilter.h>
#include <include/core/SkPath.h>
#include <include/core/SkPathEffect.h>
#include <include/core/SkPicture.h>
#include <include/core/SkPixmap.h>
#include <include/core/SkRRect.h>
#include <include/core/SkRSXform.h>
#include <include/core/SkRasterHandleAllocator.h>
#include <include/core/SkRefCnt.h>
#include <include/core/SkRegion.h>
#include <include/core/SkShader.h>
#include <include/core/SkStrokeRec.h>
#include <include/core/SkSurface.h>
#include <include/core/SkTextBlob.h>
#include <include/core/SkTileMode.h>
#include <include/core/SkTypes.h>
#include <include/core/SkVertices.h>
#include <include/core/SkMesh.h>
#include <include/core/SkDrawable.h>
#include <src/core/SkDrawShadowInfo.h>

#include <skia/include/gpu/graphite/Recorder.h>

namespace py = pybind11;

void init_skia_canvas_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkCanvas> _Canvas(_skia, "Canvas");
    registry.on(_skia, "Canvas", _Canvas);
        _Canvas
        .def(py::init<>())
        .def(py::init<int, int, const SkSurfaceProps *>()
        , py::arg("width")
        , py::arg("height")
        , py::arg("props") = nullptr
        )
        .def(py::init<const SkBitmap &>()
        , py::arg("bitmap")
        )
        .def(py::init<const SkBitmap &, const SkSurfaceProps &>()
        , py::arg("bitmap")
        , py::arg("props")
        )
        .def("image_info", &SkCanvas::imageInfo
            )
        .def("get_props", &SkCanvas::getProps
            , py::arg("props")
            )
        .def("get_base_props", &SkCanvas::getBaseProps
            )
        .def("get_top_props", &SkCanvas::getTopProps
            )
        .def("get_base_layer_size", &SkCanvas::getBaseLayerSize
            )
        .def("make_surface", &SkCanvas::makeSurface
            , py::arg("info")
            , py::arg("props") = nullptr
            )
        .def("recorder", &SkCanvas::recorder
            )
        .def("get_surface", &SkCanvas::getSurface
            )
        .def("access_top_layer_pixels", [](SkCanvas& self, SkImageInfo * info, size_t * rowBytes, SkIPoint * origin)
            {
                auto _ret = self.accessTopLayerPixels(info, rowBytes, origin);
                return std::make_tuple(_ret, rowBytes);
            }
            , py::arg("info")
            , py::arg("row_bytes")
            , py::arg("origin") = nullptr
            )
        .def("access_top_raster_handle", &SkCanvas::accessTopRasterHandle
            )
        .def("peek_pixels", &SkCanvas::peekPixels
            , py::arg("pixmap")
            )
        .def("read_pixels", py::overload_cast<const SkImageInfo &, void *, size_t, int, int>(&SkCanvas::readPixels)
            , py::arg("dst_info")
            , py::arg("dst_pixels")
            , py::arg("dst_row_bytes")
            , py::arg("src_x")
            , py::arg("src_y")
            )
        .def("read_pixels", py::overload_cast<const SkPixmap &, int, int>(&SkCanvas::readPixels)
            , py::arg("pixmap")
            , py::arg("src_x")
            , py::arg("src_y")
            )
        .def("read_pixels", py::overload_cast<const SkBitmap &, int, int>(&SkCanvas::readPixels)
            , py::arg("bitmap")
            , py::arg("src_x")
            , py::arg("src_y")
            )
        .def("write_pixels", py::overload_cast<const SkImageInfo &, const void *, size_t, int, int>(&SkCanvas::writePixels)
            , py::arg("info")
            , py::arg("pixels")
            , py::arg("row_bytes")
            , py::arg("x")
            , py::arg("y")
            )
        .def("write_pixels", py::overload_cast<const SkBitmap &, int, int>(&SkCanvas::writePixels)
            , py::arg("bitmap")
            , py::arg("x")
            , py::arg("y")
            )
        .def("save", &SkCanvas::save
            )
        .def("save_layer", py::overload_cast<const SkRect *, const SkPaint *>(&SkCanvas::saveLayer)
            , py::arg("bounds")
            , py::arg("paint")
            )
        .def("save_layer", py::overload_cast<const SkRect &, const SkPaint *>(&SkCanvas::saveLayer)
            , py::arg("bounds")
            , py::arg("paint")
            )
        .def("save_layer_alphaf", &SkCanvas::saveLayerAlphaf
            , py::arg("bounds")
            , py::arg("alpha")
            )
        .def("save_layer_alpha", &SkCanvas::saveLayerAlpha
            , py::arg("bounds")
            , py::arg("alpha")
            )
        ;

        py::enum_<SkCanvas::SaveLayerFlagsSet>(_Canvas, "SaveLayerFlagsSet", py::arithmetic())
            .value("K_PRESERVE_LCD_TEXT_SAVE_LAYER_FLAG", SkCanvas::SaveLayerFlagsSet::kPreserveLCDText_SaveLayerFlag)
            .value("K_INIT_WITH_PREVIOUS_SAVE_LAYER_FLAG", SkCanvas::SaveLayerFlagsSet::kInitWithPrevious_SaveLayerFlag)
            .value("K_F16_COLOR_TYPE", SkCanvas::SaveLayerFlagsSet::kF16ColorType)
            .export_values()
        ;
        py::class_<SkCanvas::SaveLayerRec> _CanvasSaveLayerRec(_skia, "CanvasSaveLayerRec");
        registry.on(_skia, "CanvasSaveLayerRec", _CanvasSaveLayerRec);
            _CanvasSaveLayerRec
            .def(py::init<>())
            .def(py::init<const SkRect *, const SkPaint *, SkCanvas::SaveLayerFlags>()
            , py::arg("bounds")
            , py::arg("paint")
            , py::arg("save_layer_flags") = 0
            )
            .def(py::init<const SkRect *, const SkPaint *, const SkImageFilter *, SkCanvas::SaveLayerFlags>()
            , py::arg("bounds")
            , py::arg("paint")
            , py::arg("backdrop")
            , py::arg("save_layer_flags")
            )
            .def(py::init<const SkRect *, const SkPaint *, const SkImageFilter *, const SkColorSpace *, SkCanvas::SaveLayerFlags>()
            , py::arg("bounds")
            , py::arg("paint")
            , py::arg("backdrop")
            , py::arg("color_space")
            , py::arg("save_layer_flags")
            )
            .def(py::init<const SkRect *, const SkPaint *, const SkImageFilter *, SkTileMode, const SkColorSpace *, SkCanvas::SaveLayerFlags>()
            , py::arg("bounds")
            , py::arg("paint")
            , py::arg("backdrop")
            , py::arg("backdrop_tile_mode")
            , py::arg("color_space")
            , py::arg("save_layer_flags")
            )
            .def_readwrite("f_bounds", &SkCanvas::SaveLayerRec::fBounds)
            .def_readwrite("f_paint", &SkCanvas::SaveLayerRec::fPaint)
            .def_readwrite("f_filters", &SkCanvas::SaveLayerRec::fFilters)
            .def_readwrite("f_backdrop", &SkCanvas::SaveLayerRec::fBackdrop)
            .def_readwrite("f_backdrop_tile_mode", &SkCanvas::SaveLayerRec::fBackdropTileMode)
            .def_readwrite("f_color_space", &SkCanvas::SaveLayerRec::fColorSpace)
            .def_readwrite("f_save_layer_flags", &SkCanvas::SaveLayerRec::fSaveLayerFlags)
        ;

        _Canvas
        .def("save_layer", py::overload_cast<const SkCanvas::SaveLayerRec &>(&SkCanvas::saveLayer)
            , py::arg("layer_rec")
            )
        .def("restore", &SkCanvas::restore
            )
        .def("get_save_count", &SkCanvas::getSaveCount
            )
        .def("restore_to_count", &SkCanvas::restoreToCount
            , py::arg("save_count")
            )
        .def("translate", &SkCanvas::translate
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("scale", &SkCanvas::scale
            , py::arg("sx")
            , py::arg("sy")
            )
        .def("rotate", py::overload_cast<SkScalar>(&SkCanvas::rotate)
            , py::arg("degrees")
            )
        .def("rotate", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkCanvas::rotate)
            , py::arg("degrees")
            , py::arg("px")
            , py::arg("py")
            )
        .def("skew", &SkCanvas::skew
            , py::arg("sx")
            , py::arg("sy")
            )
        .def("concat", py::overload_cast<const SkMatrix &>(&SkCanvas::concat)
            , py::arg("matrix")
            )
        .def("concat", py::overload_cast<const SkM44 &>(&SkCanvas::concat)
            , py::arg("arg0")
            )
        .def("set_matrix", py::overload_cast<const SkM44 &>(&SkCanvas::setMatrix)
            , py::arg("matrix")
            )
        .def("set_matrix", py::overload_cast<const SkMatrix &>(&SkCanvas::setMatrix)
            , py::arg("matrix")
            )
        .def("reset_matrix", &SkCanvas::resetMatrix
            )
        .def("clip_rect", py::overload_cast<const SkRect &, SkClipOp, bool>(&SkCanvas::clipRect)
            , py::arg("rect")
            , py::arg("op")
            , py::arg("do_anti_alias")
            )
        .def("clip_rect", py::overload_cast<const SkRect &, SkClipOp>(&SkCanvas::clipRect)
            , py::arg("rect")
            , py::arg("op")
            )
        .def("clip_rect", py::overload_cast<const SkRect &, bool>(&SkCanvas::clipRect)
            , py::arg("rect")
            , py::arg("do_anti_alias") = false
            )
        .def("clip_i_rect", &SkCanvas::clipIRect
            , py::arg("irect")
            , py::arg("op") = SkClipOp::kIntersect
            )
        .def("android_framework_set_device_clip_restriction", &SkCanvas::androidFramework_setDeviceClipRestriction
            , py::arg("rect")
            )
        .def("clip_r_rect", py::overload_cast<const SkRRect &, SkClipOp, bool>(&SkCanvas::clipRRect)
            , py::arg("rrect")
            , py::arg("op")
            , py::arg("do_anti_alias")
            )
        .def("clip_r_rect", py::overload_cast<const SkRRect &, SkClipOp>(&SkCanvas::clipRRect)
            , py::arg("rrect")
            , py::arg("op")
            )
        .def("clip_r_rect", py::overload_cast<const SkRRect &, bool>(&SkCanvas::clipRRect)
            , py::arg("rrect")
            , py::arg("do_anti_alias") = false
            )
        .def("clip_path", py::overload_cast<const SkPath &, SkClipOp, bool>(&SkCanvas::clipPath)
            , py::arg("path")
            , py::arg("op")
            , py::arg("do_anti_alias")
            )
        .def("clip_path", py::overload_cast<const SkPath &, SkClipOp>(&SkCanvas::clipPath)
            , py::arg("path")
            , py::arg("op")
            )
        .def("clip_path", py::overload_cast<const SkPath &, bool>(&SkCanvas::clipPath)
            , py::arg("path")
            , py::arg("do_anti_alias") = false
            )
        .def("clip_shader", &SkCanvas::clipShader
            , py::arg("arg0")
            , py::arg("arg1") = SkClipOp::kIntersect
            )
        .def("clip_region", &SkCanvas::clipRegion
            , py::arg("device_rgn")
            , py::arg("op") = SkClipOp::kIntersect
            )
        .def("quick_reject", py::overload_cast<const SkRect &>(&SkCanvas::quickReject, py::const_)
            , py::arg("rect")
            )
        .def("quick_reject", py::overload_cast<const SkPath &>(&SkCanvas::quickReject, py::const_)
            , py::arg("path")
            )
        .def("get_local_clip_bounds", py::overload_cast<>(&SkCanvas::getLocalClipBounds, py::const_)
            )
        .def("get_local_clip_bounds", py::overload_cast<SkRect *>(&SkCanvas::getLocalClipBounds, py::const_)
            , py::arg("bounds")
            )
        .def("get_device_clip_bounds", py::overload_cast<>(&SkCanvas::getDeviceClipBounds, py::const_)
            )
        .def("get_device_clip_bounds", py::overload_cast<SkIRect *>(&SkCanvas::getDeviceClipBounds, py::const_)
            , py::arg("bounds")
            )
        .def("draw_color", py::overload_cast<SkColor, SkBlendMode>(&SkCanvas::drawColor)
            , py::arg("color")
            , py::arg("mode") = SkBlendMode::kSrcOver
            )
        .def("draw_color", py::overload_cast<const SkColor4f &, SkBlendMode>(&SkCanvas::drawColor)
            , py::arg("color")
            , py::arg("mode") = SkBlendMode::kSrcOver
            )
        .def("clear", py::overload_cast<SkColor>(&SkCanvas::clear)
            , py::arg("color")
            )
        .def("clear", py::overload_cast<const SkColor4f &>(&SkCanvas::clear)
            , py::arg("color")
            )
        .def("discard", &SkCanvas::discard
            )
        .def("draw_paint", &SkCanvas::drawPaint
            , py::arg("paint")
            )
        ;

        py::enum_<SkCanvas::PointMode>(_Canvas, "PointMode", py::arithmetic())
            .value("K_POINTS_POINT_MODE", SkCanvas::PointMode::kPoints_PointMode)
            .value("K_LINES_POINT_MODE", SkCanvas::PointMode::kLines_PointMode)
            .value("K_POLYGON_POINT_MODE", SkCanvas::PointMode::kPolygon_PointMode)
            .export_values()
        ;
        _Canvas
        .def("draw_points", &SkCanvas::drawPoints
            , py::arg("mode")
            , py::arg("count")
            , py::arg("pts")
            , py::arg("paint")
            )
        .def("draw_point", py::overload_cast<SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawPoint)
            , py::arg("x")
            , py::arg("y")
            , py::arg("paint")
            )
        .def("draw_point", py::overload_cast<SkPoint, const SkPaint &>(&SkCanvas::drawPoint)
            , py::arg("p")
            , py::arg("paint")
            )
        .def("draw_line", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawLine)
            , py::arg("x0")
            , py::arg("y0")
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("paint")
            )
        .def("draw_line", py::overload_cast<SkPoint, SkPoint, const SkPaint &>(&SkCanvas::drawLine)
            , py::arg("p0")
            , py::arg("p1")
            , py::arg("paint")
            )
        .def("draw_rect", &SkCanvas::drawRect
            , py::arg("rect")
            , py::arg("paint")
            )
        .def("draw_i_rect", &SkCanvas::drawIRect
            , py::arg("rect")
            , py::arg("paint")
            )
        .def("draw_region", &SkCanvas::drawRegion
            , py::arg("region")
            , py::arg("paint")
            )
        .def("draw_oval", &SkCanvas::drawOval
            , py::arg("oval")
            , py::arg("paint")
            )
        .def("draw_r_rect", &SkCanvas::drawRRect
            , py::arg("rrect")
            , py::arg("paint")
            )
        .def("draw_dr_rect", &SkCanvas::drawDRRect
            , py::arg("outer")
            , py::arg("inner")
            , py::arg("paint")
            )
        .def("draw_circle", py::overload_cast<SkScalar, SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawCircle)
            , py::arg("cx")
            , py::arg("cy")
            , py::arg("radius")
            , py::arg("paint")
            )
        .def("draw_circle", py::overload_cast<SkPoint, SkScalar, const SkPaint &>(&SkCanvas::drawCircle)
            , py::arg("center")
            , py::arg("radius")
            , py::arg("paint")
            )
        .def("draw_arc", py::overload_cast<const SkRect &, SkScalar, SkScalar, bool, const SkPaint &>(&SkCanvas::drawArc)
            , py::arg("oval")
            , py::arg("start_angle")
            , py::arg("sweep_angle")
            , py::arg("use_center")
            , py::arg("paint")
            )
        .def("draw_arc", py::overload_cast<const SkArc &, const SkPaint &>(&SkCanvas::drawArc)
            , py::arg("arc")
            , py::arg("paint")
            )
        .def("draw_round_rect", &SkCanvas::drawRoundRect
            , py::arg("rect")
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("paint")
            )
        .def("draw_path", &SkCanvas::drawPath
            , py::arg("path")
            , py::arg("paint")
            )
        .def("draw_image", py::overload_cast<const SkImage *, SkScalar, SkScalar>(&SkCanvas::drawImage)
            , py::arg("image")
            , py::arg("left")
            , py::arg("top")
            )
        .def("draw_image", py::overload_cast<const sk_sp<SkImage> &, SkScalar, SkScalar>(&SkCanvas::drawImage)
            , py::arg("image")
            , py::arg("left")
            , py::arg("top")
            )
        ;

        py::enum_<SkCanvas::SrcRectConstraint>(_Canvas, "SrcRectConstraint", py::arithmetic())
            .value("K_STRICT_SRC_RECT_CONSTRAINT", SkCanvas::SrcRectConstraint::kStrict_SrcRectConstraint)
            .value("K_FAST_SRC_RECT_CONSTRAINT", SkCanvas::SrcRectConstraint::kFast_SrcRectConstraint)
            .export_values()
        ;
        _Canvas
        .def("draw_image", py::overload_cast<const SkImage *, SkScalar, SkScalar, const SkSamplingOptions &, const SkPaint *>(&SkCanvas::drawImage)
            , py::arg("arg0")
            , py::arg("x")
            , py::arg("y")
            , py::arg("arg3")
            , py::arg("arg4") = nullptr
            )
        .def("draw_image", py::overload_cast<const sk_sp<SkImage> &, SkScalar, SkScalar, const SkSamplingOptions &, const SkPaint *>(&SkCanvas::drawImage)
            , py::arg("image")
            , py::arg("x")
            , py::arg("y")
            , py::arg("sampling")
            , py::arg("paint") = nullptr
            )
        .def("draw_image_rect", py::overload_cast<const SkImage *, const SkRect &, const SkRect &, const SkSamplingOptions &, const SkPaint *, SkCanvas::SrcRectConstraint>(&SkCanvas::drawImageRect)
            , py::arg("arg0")
            , py::arg("src")
            , py::arg("dst")
            , py::arg("arg3")
            , py::arg("arg4")
            , py::arg("arg5")
            )
        .def("draw_image_rect", py::overload_cast<const SkImage *, const SkRect &, const SkSamplingOptions &, const SkPaint *>(&SkCanvas::drawImageRect)
            , py::arg("arg0")
            , py::arg("dst")
            , py::arg("arg2")
            , py::arg("arg3") = nullptr
            )
        .def("draw_image_rect", py::overload_cast<const sk_sp<SkImage> &, const SkRect &, const SkRect &, const SkSamplingOptions &, const SkPaint *, SkCanvas::SrcRectConstraint>(&SkCanvas::drawImageRect)
            , py::arg("image")
            , py::arg("src")
            , py::arg("dst")
            , py::arg("sampling")
            , py::arg("paint")
            , py::arg("constraint")
            )
        .def("draw_image_rect", py::overload_cast<const sk_sp<SkImage> &, const SkRect &, const SkSamplingOptions &, const SkPaint *>(&SkCanvas::drawImageRect)
            , py::arg("image")
            , py::arg("dst")
            , py::arg("sampling")
            , py::arg("paint") = nullptr
            )
        .def("draw_image_nine", &SkCanvas::drawImageNine
            , py::arg("image")
            , py::arg("center")
            , py::arg("dst")
            , py::arg("filter")
            , py::arg("paint") = nullptr
            )
        ;

        py::class_<SkCanvas::Lattice> _CanvasLattice(_skia, "CanvasLattice");
        registry.on(_skia, "CanvasLattice", _CanvasLattice);
            py::enum_<SkCanvas::Lattice::RectType>(_CanvasLattice, "RectType", py::arithmetic())
                .value("K_DEFAULT", SkCanvas::Lattice::RectType::kDefault)
                .value("K_TRANSPARENT", SkCanvas::Lattice::RectType::kTransparent)
                .value("K_FIXED_COLOR", SkCanvas::Lattice::RectType::kFixedColor)
                .export_values()
            ;
            _CanvasLattice
            .def_readwrite("f_x_divs", &SkCanvas::Lattice::fXDivs)
            .def_readwrite("f_y_divs", &SkCanvas::Lattice::fYDivs)
            .def_readwrite("f_rect_types", &SkCanvas::Lattice::fRectTypes)
            .def_readwrite("f_x_count", &SkCanvas::Lattice::fXCount)
            .def_readwrite("f_y_count", &SkCanvas::Lattice::fYCount)
            .def_readwrite("f_bounds", &SkCanvas::Lattice::fBounds)
            .def_readwrite("f_colors", &SkCanvas::Lattice::fColors)
        ;

        _Canvas
        .def("draw_image_lattice", py::overload_cast<const SkImage *, const SkCanvas::Lattice &, const SkRect &, SkFilterMode, const SkPaint *>(&SkCanvas::drawImageLattice)
            , py::arg("image")
            , py::arg("lattice")
            , py::arg("dst")
            , py::arg("filter")
            , py::arg("paint") = nullptr
            )
        .def("draw_image_lattice", py::overload_cast<const SkImage *, const SkCanvas::Lattice &, const SkRect &>(&SkCanvas::drawImageLattice)
            , py::arg("image")
            , py::arg("lattice")
            , py::arg("dst")
            )
        ;

        py::enum_<SkCanvas::QuadAAFlags>(_Canvas, "QuadAAFlags", py::arithmetic())
            .value("K_LEFT_QUAD_AA_FLAG", SkCanvas::QuadAAFlags::kLeft_QuadAAFlag)
            .value("K_TOP_QUAD_AA_FLAG", SkCanvas::QuadAAFlags::kTop_QuadAAFlag)
            .value("K_RIGHT_QUAD_AA_FLAG", SkCanvas::QuadAAFlags::kRight_QuadAAFlag)
            .value("K_BOTTOM_QUAD_AA_FLAG", SkCanvas::QuadAAFlags::kBottom_QuadAAFlag)
            .value("K_NONE_QUAD_AA_FLAGS", SkCanvas::QuadAAFlags::kNone_QuadAAFlags)
            .value("K_ALL_QUAD_AA_FLAGS", SkCanvas::QuadAAFlags::kAll_QuadAAFlags)
            .export_values()
        ;
        py::class_<SkCanvas::ImageSetEntry> _CanvasImageSetEntry(_skia, "CanvasImageSetEntry");
        registry.on(_skia, "CanvasImageSetEntry", _CanvasImageSetEntry);
            _CanvasImageSetEntry
            .def(py::init<sk_sp<const SkImage>, const SkRect &, const SkRect &, int, float, unsigned int, bool>()
            , py::arg("image")
            , py::arg("src_rect")
            , py::arg("dst_rect")
            , py::arg("matrix_index")
            , py::arg("alpha")
            , py::arg("aa_flags")
            , py::arg("has_clip")
            )
            .def(py::init<sk_sp<const SkImage>, const SkRect &, const SkRect &, float, unsigned int>()
            , py::arg("image")
            , py::arg("src_rect")
            , py::arg("dst_rect")
            , py::arg("alpha")
            , py::arg("aa_flags")
            )
            .def(py::init<>())
            .def_readwrite("f_image", &SkCanvas::ImageSetEntry::fImage)
            .def_readwrite("f_src_rect", &SkCanvas::ImageSetEntry::fSrcRect)
            .def_readwrite("f_dst_rect", &SkCanvas::ImageSetEntry::fDstRect)
            .def_readwrite("f_matrix_index", &SkCanvas::ImageSetEntry::fMatrixIndex)
            .def_readwrite("f_alpha", &SkCanvas::ImageSetEntry::fAlpha)
            .def_readwrite("f_aa_flags", &SkCanvas::ImageSetEntry::fAAFlags)
            .def_readwrite("f_has_clip", &SkCanvas::ImageSetEntry::fHasClip)
        ;

        _Canvas
        .def("draw_simple_text", &SkCanvas::drawSimpleText
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding") = SkTextEncoding::kUTF8
            , py::arg("x")
            , py::arg("y")
            , py::arg("font")
            , py::arg("paint")
            )
        .def("draw_string", py::overload_cast<const char[], SkScalar, SkScalar, const SkFont &, const SkPaint &>(&SkCanvas::drawString)
            , py::arg("str")
            , py::arg("x")
            , py::arg("y")
            , py::arg("font")
            , py::arg("paint")
            )
        .def("draw_string", py::overload_cast<const SkString &, SkScalar, SkScalar, const SkFont &, const SkPaint &>(&SkCanvas::drawString)
            , py::arg("str")
            , py::arg("x")
            , py::arg("y")
            , py::arg("font")
            , py::arg("paint")
            )
        .def("draw_glyphs", [](SkCanvas& self, int count, const SkGlyphID glyphs[], const SkPoint positions[], const uint32_t clusters[], int textByteCount, const char utf8text[], SkPoint origin, const SkFont & font, const SkPaint & paint)
            {
                self.drawGlyphs(count, glyphs, positions, clusters, textByteCount, utf8text, origin, font, paint);
                return std::make_tuple(glyphs, clusters);
            }
            , py::arg("count")
            , py::arg("glyphs")
            , py::arg("positions")
            , py::arg("clusters")
            , py::arg("text_byte_count")
            , py::arg("utf8text")
            , py::arg("origin")
            , py::arg("font")
            , py::arg("paint")
            )
        .def("draw_glyphs", [](SkCanvas& self, int count, const SkGlyphID glyphs[], const SkPoint positions[], SkPoint origin, const SkFont & font, const SkPaint & paint)
            {
                self.drawGlyphs(count, glyphs, positions, origin, font, paint);
                return std::make_tuple(glyphs);
            }
            , py::arg("count")
            , py::arg("glyphs")
            , py::arg("positions")
            , py::arg("origin")
            , py::arg("font")
            , py::arg("paint")
            )
        .def("draw_glyphs", [](SkCanvas& self, int count, const SkGlyphID glyphs[], const SkRSXform xforms[], SkPoint origin, const SkFont & font, const SkPaint & paint)
            {
                self.drawGlyphs(count, glyphs, xforms, origin, font, paint);
                return std::make_tuple(glyphs);
            }
            , py::arg("count")
            , py::arg("glyphs")
            , py::arg("xforms")
            , py::arg("origin")
            , py::arg("font")
            , py::arg("paint")
            )
        .def("draw_text_blob", py::overload_cast<const SkTextBlob *, SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawTextBlob)
            , py::arg("blob")
            , py::arg("x")
            , py::arg("y")
            , py::arg("paint")
            )
        .def("draw_text_blob", py::overload_cast<const sk_sp<SkTextBlob> &, SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawTextBlob)
            , py::arg("blob")
            , py::arg("x")
            , py::arg("y")
            , py::arg("paint")
            )
        .def("draw_picture", py::overload_cast<const SkPicture *>(&SkCanvas::drawPicture)
            , py::arg("picture")
            )
        .def("draw_picture", py::overload_cast<const sk_sp<SkPicture> &>(&SkCanvas::drawPicture)
            , py::arg("picture")
            )
        .def("draw_picture", py::overload_cast<const SkPicture *, const SkMatrix *, const SkPaint *>(&SkCanvas::drawPicture)
            , py::arg("picture")
            , py::arg("matrix")
            , py::arg("paint")
            )
        .def("draw_picture", py::overload_cast<const sk_sp<SkPicture> &, const SkMatrix *, const SkPaint *>(&SkCanvas::drawPicture)
            , py::arg("picture")
            , py::arg("matrix")
            , py::arg("paint")
            )
        .def("draw_vertices", py::overload_cast<const SkVertices *, SkBlendMode, const SkPaint &>(&SkCanvas::drawVertices)
            , py::arg("vertices")
            , py::arg("mode")
            , py::arg("paint")
            )
        .def("draw_vertices", py::overload_cast<const sk_sp<SkVertices> &, SkBlendMode, const SkPaint &>(&SkCanvas::drawVertices)
            , py::arg("vertices")
            , py::arg("mode")
            , py::arg("paint")
            )
        .def("draw_mesh", &SkCanvas::drawMesh
            , py::arg("mesh")
            , py::arg("blender")
            , py::arg("paint")
            )
        .def("draw_atlas", [](SkCanvas& self, const SkImage * atlas, const SkRSXform xform[], const SkRect tex[], const SkColor colors[], int count, SkBlendMode mode, const SkSamplingOptions & sampling, const SkRect * cullRect, const SkPaint * paint)
            {
                self.drawAtlas(atlas, xform, tex, colors, count, mode, sampling, cullRect, paint);
                return std::make_tuple(colors);
            }
            , py::arg("atlas")
            , py::arg("xform")
            , py::arg("tex")
            , py::arg("colors")
            , py::arg("count")
            , py::arg("mode")
            , py::arg("sampling")
            , py::arg("cull_rect")
            , py::arg("paint")
            )
        .def("draw_drawable", py::overload_cast<SkDrawable *, const SkMatrix *>(&SkCanvas::drawDrawable)
            , py::arg("drawable")
            , py::arg("matrix") = nullptr
            )
        .def("draw_drawable", py::overload_cast<SkDrawable *, SkScalar, SkScalar>(&SkCanvas::drawDrawable)
            , py::arg("drawable")
            , py::arg("x")
            , py::arg("y")
            )
        .def("draw_annotation", py::overload_cast<const SkRect &, const char[], SkData *>(&SkCanvas::drawAnnotation)
            , py::arg("rect")
            , py::arg("key")
            , py::arg("value")
            )
        .def("draw_annotation", py::overload_cast<const SkRect &, const char[], const sk_sp<SkData> &>(&SkCanvas::drawAnnotation)
            , py::arg("rect")
            , py::arg("key")
            , py::arg("value")
            )
        .def("is_clip_empty", &SkCanvas::isClipEmpty
            )
        .def("is_clip_rect", &SkCanvas::isClipRect
            )
        .def("get_local_to_device", &SkCanvas::getLocalToDevice
            )
        .def("get_local_to_device_as3x3", &SkCanvas::getLocalToDeviceAs3x3
            )
        .def("get_total_matrix", &SkCanvas::getTotalMatrix
            )
        .def("temporary_internal_get_rgn_clip", &SkCanvas::temporary_internal_getRgnClip
            , py::arg("region")
            )
        .def("private_draw_shadow_rec", &SkCanvas::private_draw_shadow_rec
            , py::arg("arg0")
            , py::arg("arg1")
            )
    ;

    py::class_<SkAutoCanvasRestore> _AutoCanvasRestore(_skia, "AutoCanvasRestore");
    registry.on(_skia, "AutoCanvasRestore", _AutoCanvasRestore);
        _AutoCanvasRestore
        .def(py::init<SkCanvas *, bool>()
        , py::arg("canvas")
        , py::arg("do_save")
        )
        .def("restore", &SkAutoCanvasRestore::restore
            )
    ;


}