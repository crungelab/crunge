#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <tiny_gltf.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/gltf/conversions.h>

namespace py = pybind11;

using namespace tinygltf;

void init_generated(py::module &_gltf, Registry &registry) {
    py::class_<SkCanvas> SkCanvas(_gltf, "SkCanvas");
    registry.on(_gltf, "SkCanvas", SkCanvas);
    SkCanvas
        .def("make_raster_direct", &SkCanvas::MakeRasterDirect
            , py::arg("info")
            , py::arg("pixels")
            , py::arg("row_bytes")
            , py::arg("props") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("make_raster_direct_n32", [](int width, int height, int * pixels, unsigned long rowBytes)
            {
                auto ret = SkCanvas::MakeRasterDirectN32::(width, height, pixels, rowBytes);
                return std::make_tuple(ret, pixels);
            }
            , py::arg("width")
            , py::arg("height")
            , py::arg("pixels")
            , py::arg("row_bytes")
            , py::return_value_policy::automatic_reference)
        .def(py::init<>())
        .def_readwrite("sk_sp", &SkCanvas::sk_sp)
        .def("image_info", &SkCanvas::imageInfo
            , py::return_value_policy::automatic_reference)
        .def("get_props", [](SkCanvas& self, int * props)
            {
                auto ret = self.getProps(props);
                return std::make_tuple(ret, props);
            }
            , py::arg("props")
            , py::return_value_policy::automatic_reference)
        .def("get_base_props", &SkCanvas::getBaseProps
            , py::return_value_policy::automatic_reference)
        .def("get_top_props", &SkCanvas::getTopProps
            , py::return_value_policy::automatic_reference)
        .def("get_base_layer_size", &SkCanvas::getBaseLayerSize
            , py::return_value_policy::automatic_reference)
        .def("make_surface", &SkCanvas::makeSurface
            , py::arg("info")
            , py::arg("props") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("recording_context", &SkCanvas::recordingContext
            , py::return_value_policy::automatic_reference)
        .def("recorder", &SkCanvas::recorder
            , py::return_value_policy::automatic_reference)
        .def("get_surface", &SkCanvas::getSurface
            , py::return_value_policy::automatic_reference)
        .def("access_top_layer_pixels", [](SkCanvas& self, int * info, unsigned long * rowBytes, int * origin)
            {
                auto ret = self.accessTopLayerPixels(info, rowBytes, origin);
                return std::make_tuple(ret, info, rowBytes, origin);
            }
            , py::arg("info")
            , py::arg("row_bytes")
            , py::arg("origin") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("access_top_raster_handle", &SkCanvas::accessTopRasterHandle
            , py::return_value_policy::automatic_reference)
        .def("peek_pixels", &SkCanvas::peekPixels
            , py::arg("pixmap")
            , py::return_value_policy::automatic_reference)
        .def("read_pixels", py::overload_cast<const int &, void *, unsigned long, int, int>(&SkCanvas::readPixels)
            , py::arg("dst_info")
            , py::arg("dst_pixels")
            , py::arg("dst_row_bytes")
            , py::arg("src_x")
            , py::arg("src_y")
            , py::return_value_policy::automatic_reference)
        .def("write_pixels", py::overload_cast<const int &, const void *, unsigned long, int, int>(&SkCanvas::writePixels)
            , py::arg("info")
            , py::arg("pixels")
            , py::arg("row_bytes")
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("save", &SkCanvas::save
            , py::return_value_policy::automatic_reference)
        .def("save_layer", py::overload_cast<const int *, const int *>(&SkCanvas::saveLayer)
            , py::arg("bounds")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("save_layer_alphaf", &SkCanvas::saveLayerAlphaf
            , py::arg("bounds")
            , py::arg("alpha")
            , py::return_value_policy::automatic_reference)
        .def("save_layer_alpha", &SkCanvas::saveLayerAlpha
            , py::arg("bounds")
            , py::arg("alpha")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkCanvas::SaveLayerFlagsSet>(_gltf, "SaveLayerFlagsSet", py::arithmetic())
            .value("K_PRESERVE_LCD_TEXT_SAVE_LAYER_FLAG", SkCanvas::SaveLayerFlagsSet::kPreserveLCDText_SaveLayerFlag)
            .value("K_INIT_WITH_PREVIOUS_SAVE_LAYER_FLAG", SkCanvas::SaveLayerFlagsSet::kInitWithPrevious_SaveLayerFlag)
            .value("K_F16_COLOR_TYPE", SkCanvas::SaveLayerFlagsSet::kF16ColorType)
            .export_values()
        ;

        SkCanvas
        .def("restore", &SkCanvas::restore
            , py::return_value_policy::automatic_reference)
        .def("get_save_count", &SkCanvas::getSaveCount
            , py::return_value_policy::automatic_reference)
        .def("restore_to_count", &SkCanvas::restoreToCount
            , py::arg("save_count")
            , py::return_value_policy::automatic_reference)
        .def("translate", &SkCanvas::translate
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("scale", &SkCanvas::scale
            , py::arg("sx")
            , py::arg("sy")
            , py::return_value_policy::automatic_reference)
        .def("rotate", py::overload_cast<int>(&SkCanvas::rotate)
            , py::arg("degrees")
            , py::return_value_policy::automatic_reference)
        .def("skew", &SkCanvas::skew
            , py::arg("sx")
            , py::arg("sy")
            , py::return_value_policy::automatic_reference)
        .def("concat", py::overload_cast<const int &>(&SkCanvas::concat)
            , py::arg("matrix")
            , py::return_value_policy::automatic_reference)
        .def("set_matrix", py::overload_cast<const int &>(&SkCanvas::setMatrix)
            , py::arg("matrix")
            , py::return_value_policy::automatic_reference)
        .def("reset_matrix", &SkCanvas::resetMatrix
            , py::return_value_policy::automatic_reference)
        .def("clip_rect", py::overload_cast<const int &, int, bool>(&SkCanvas::clipRect)
            , py::arg("rect")
            , py::arg("op")
            , py::arg("do_anti_alias")
            , py::return_value_policy::automatic_reference)
        .def("clip_i_rect", &SkCanvas::clipIRect
            , py::arg("irect")
            , py::arg("op")
            , py::return_value_policy::automatic_reference)
        .def("android_framework_set_device_clip_restriction", &SkCanvas::androidFramework_setDeviceClipRestriction
            , py::arg("rect")
            , py::return_value_policy::automatic_reference)
        .def("clip_r_rect", py::overload_cast<const SkRRect &, int, bool>(&SkCanvas::clipRRect)
            , py::arg("rrect")
            , py::arg("op")
            , py::arg("do_anti_alias")
            , py::return_value_policy::automatic_reference)
        .def("clip_path", py::overload_cast<const SkPath &, int, bool>(&SkCanvas::clipPath)
            , py::arg("path")
            , py::arg("op")
            , py::arg("do_anti_alias")
            , py::return_value_policy::automatic_reference)
        .def("clip_shader", &SkCanvas::clipShader
            , py::arg("")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("clip_region", &SkCanvas::clipRegion
            , py::arg("device_rgn")
            , py::arg("op")
            , py::return_value_policy::automatic_reference)
        .def("quick_reject", py::overload_cast<const int &>(&SkCanvas::quickReject, py::const_)
            , py::arg("rect")
            , py::return_value_policy::automatic_reference)
        .def("get_local_clip_bounds", py::overload_cast<>(&SkCanvas::getLocalClipBounds, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("get_device_clip_bounds", py::overload_cast<>(&SkCanvas::getDeviceClipBounds, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("draw_color", py::overload_cast<int, int>(&SkCanvas::drawColor)
            , py::arg("color")
            , py::arg("mode")
            , py::return_value_policy::automatic_reference)
        .def("clear", py::overload_cast<int>(&SkCanvas::clear)
            , py::arg("color")
            , py::return_value_policy::automatic_reference)
        .def("discard", &SkCanvas::discard
            , py::return_value_policy::automatic_reference)
        .def("draw_paint", &SkCanvas::drawPaint
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkCanvas::PointMode>(_gltf, "PointMode", py::arithmetic())
            .value("K_POINTS_POINT_MODE", SkCanvas::PointMode::kPoints_PointMode)
            .value("K_LINES_POINT_MODE", SkCanvas::PointMode::kLines_PointMode)
            .value("K_POLYGON_POINT_MODE", SkCanvas::PointMode::kPolygon_PointMode)
            .export_values()
        ;

        SkCanvas
        .def("draw_points", &SkCanvas::drawPoints
            , py::arg("mode")
            , py::arg("count")
            , py::arg("pts")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_point", py::overload_cast<int, int, const int &>(&SkCanvas::drawPoint)
            , py::arg("x")
            , py::arg("y")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_line", py::overload_cast<int, int, int, int, const int &>(&SkCanvas::drawLine)
            , py::arg("x0")
            , py::arg("y0")
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_rect", &SkCanvas::drawRect
            , py::arg("rect")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_i_rect", &SkCanvas::drawIRect
            , py::arg("rect")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_region", &SkCanvas::drawRegion
            , py::arg("region")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_oval", &SkCanvas::drawOval
            , py::arg("oval")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_r_rect", &SkCanvas::drawRRect
            , py::arg("rrect")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_dr_rect", &SkCanvas::drawDRRect
            , py::arg("outer")
            , py::arg("inner")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_circle", py::overload_cast<int, int, int, const int &>(&SkCanvas::drawCircle)
            , py::arg("cx")
            , py::arg("cy")
            , py::arg("radius")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_arc", py::overload_cast<const int &, int, int, bool, const int &>(&SkCanvas::drawArc)
            , py::arg("oval")
            , py::arg("start_angle")
            , py::arg("sweep_angle")
            , py::arg("use_center")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_round_rect", &SkCanvas::drawRoundRect
            , py::arg("rect")
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_path", &SkCanvas::drawPath
            , py::arg("path")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_image", py::overload_cast<const SkImage *, int, int>(&SkCanvas::drawImage)
            , py::arg("image")
            , py::arg("left")
            , py::arg("top")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkCanvas::SrcRectConstraint>(_gltf, "SrcRectConstraint", py::arithmetic())
            .value("K_STRICT_SRC_RECT_CONSTRAINT", SkCanvas::SrcRectConstraint::kStrict_SrcRectConstraint)
            .value("K_FAST_SRC_RECT_CONSTRAINT", SkCanvas::SrcRectConstraint::kFast_SrcRectConstraint)
            .export_values()
        ;

        SkCanvas
        .def("draw_image_rect", py::overload_cast<const SkImage *, const int &, const int &, const int &, const int *, SkCanvas::SrcRectConstraint>(&SkCanvas::drawImageRect)
            , py::arg("")
            , py::arg("src")
            , py::arg("dst")
            , py::arg("")
            , py::arg("")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("draw_image_nine", &SkCanvas::drawImageNine
            , py::arg("image")
            , py::arg("center")
            , py::arg("dst")
            , py::arg("filter")
            , py::arg("paint") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("draw_image_lattice", py::overload_cast<const SkImage *, const SkCanvas::Lattice &, const int &, int, const int *>(&SkCanvas::drawImageLattice)
            , py::arg("image")
            , py::arg("lattice")
            , py::arg("dst")
            , py::arg("filter")
            , py::arg("paint") = nullptr
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkCanvas::QuadAAFlags>(_gltf, "QuadAAFlags", py::arithmetic())
            .value("K_LEFT_QUAD_AA_FLAG", SkCanvas::QuadAAFlags::kLeft_QuadAAFlag)
            .value("K_TOP_QUAD_AA_FLAG", SkCanvas::QuadAAFlags::kTop_QuadAAFlag)
            .value("K_RIGHT_QUAD_AA_FLAG", SkCanvas::QuadAAFlags::kRight_QuadAAFlag)
            .value("K_BOTTOM_QUAD_AA_FLAG", SkCanvas::QuadAAFlags::kBottom_QuadAAFlag)
            .value("K_NONE_QUAD_AA_FLAGS", SkCanvas::QuadAAFlags::kNone_QuadAAFlags)
            .value("K_ALL_QUAD_AA_FLAGS", SkCanvas::QuadAAFlags::kAll_QuadAAFlags)
            .export_values()
        ;

        SkCanvas
        .def("experimental_draw_edge_aa_quad", [](SkCanvas& self, const int & rect, std::array<const int, 4>& clip, SkCanvas::QuadAAFlags aaFlags, const int & color, int mode)
            {
                self.experimental_DrawEdgeAAQuad(rect, &clip[0], aaFlags, color, mode);
                return clip;
            }
            , py::arg("rect")
            , py::arg("clip")
            , py::arg("aa_flags")
            , py::arg("color")
            , py::arg("mode")
            , py::return_value_policy::automatic_reference)
        .def("experimental_draw_edge_aa_image_set", &SkCanvas::experimental_DrawEdgeAAImageSet
            , py::arg("image_set")
            , py::arg("cnt")
            , py::arg("dst_clips")
            , py::arg("pre_view_matrices")
            , py::arg("")
            , py::arg("paint") = nullptr
            , py::arg("constraint") = kStrict_SrcRectConstraint
            , py::return_value_policy::automatic_reference)
        .def("draw_simple_text", &SkCanvas::drawSimpleText
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding")
            , py::arg("x")
            , py::arg("y")
            , py::arg("font")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_string", py::overload_cast<const char[], int, int, const SkFont &, const int &>(&SkCanvas::drawString)
            , py::arg("str")
            , py::arg("x")
            , py::arg("y")
            , py::arg("font")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_glyphs", py::overload_cast<int, const int[], const int[], const unsigned int[], int, const char[], int, const SkFont &, const int &>(&SkCanvas::drawGlyphs)
            , py::arg("count")
            , py::arg("glyphs")
            , py::arg("positions")
            , py::arg("clusters")
            , py::arg("text_byte_count")
            , py::arg("utf8text")
            , py::arg("origin")
            , py::arg("font")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_text_blob", py::overload_cast<const SkTextBlob *, int, int, const int &>(&SkCanvas::drawTextBlob)
            , py::arg("blob")
            , py::arg("x")
            , py::arg("y")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_picture", py::overload_cast<const SkPicture *>(&SkCanvas::drawPicture)
            , py::arg("picture")
            , py::return_value_policy::automatic_reference)
        .def("draw_vertices", py::overload_cast<const SkVertices *, int, const int &>(&SkCanvas::drawVertices)
            , py::arg("vertices")
            , py::arg("mode")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_mesh", &SkCanvas::drawMesh
            , py::arg("mesh")
            , py::arg("blender")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_patch", [](SkCanvas& self, std::array<const int, 12>& cubics, std::array<const int, 4>& colors, std::array<const int, 4>& texCoords, int mode, const int & paint)
            {
                self.drawPatch(&cubics[0], &colors[0], &texCoords[0], mode, paint);
                return std::make_tuple(cubics, colors, texCoords);
            }
            , py::arg("cubics")
            , py::arg("colors")
            , py::arg("tex_coords")
            , py::arg("mode")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_atlas", &SkCanvas::drawAtlas
            , py::arg("atlas")
            , py::arg("xform")
            , py::arg("tex")
            , py::arg("colors")
            , py::arg("count")
            , py::arg("mode")
            , py::arg("sampling")
            , py::arg("cull_rect")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("draw_drawable", py::overload_cast<SkDrawable *, const int *>(&SkCanvas::drawDrawable)
            , py::arg("drawable")
            , py::arg("matrix") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("draw_annotation", py::overload_cast<const int &, const char[], SkData *>(&SkCanvas::drawAnnotation)
            , py::arg("rect")
            , py::arg("key")
            , py::arg("value")
            , py::return_value_policy::automatic_reference)
        .def("is_clip_empty", &SkCanvas::isClipEmpty
            , py::return_value_policy::automatic_reference)
        .def("is_clip_rect", &SkCanvas::isClipRect
            , py::return_value_policy::automatic_reference)
        .def("get_local_to_device", &SkCanvas::getLocalToDevice
            , py::return_value_policy::automatic_reference)
        .def("get_local_to_device_as3x3", &SkCanvas::getLocalToDeviceAs3x3
            , py::return_value_policy::automatic_reference)
        .def("get_total_matrix", &SkCanvas::getTotalMatrix
            , py::return_value_policy::automatic_reference)
        .def("temporary_internal_get_rgn_clip", &SkCanvas::temporary_internal_getRgnClip
            , py::arg("region")
            , py::return_value_policy::automatic_reference)
        .def("private_draw_shadow_rec", &SkCanvas::private_draw_shadow_rec
            , py::arg("")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<SkAutoCanvasRestore> SkAutoCanvasRestore(_gltf, "SkAutoCanvasRestore");
    registry.on(_gltf, "SkAutoCanvasRestore", SkAutoCanvasRestore);
    SkAutoCanvasRestore
        .def(py::init<SkCanvas *, bool>()
        , py::arg("canvas")
        , py::arg("do_save")
        )
        .def("restore", &SkAutoCanvasRestore::restore
            , py::return_value_policy::automatic_reference)
    ;


}