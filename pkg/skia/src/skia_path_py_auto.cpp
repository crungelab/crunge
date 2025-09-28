#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include "include/core/SkPath.h"

#include "include/core/SkArc.h"
#include "include/core/SkPathBuilder.h"
#include "include/core/SkRRect.h"
#include "include/core/SkStream.h"
#include "include/core/SkString.h"
/*#include "include/private/SkPathRef.h"
#include "include/private/base/SkFloatingPoint.h"
#include "include/private/base/SkMalloc.h"
#include "include/private/base/SkSpan_impl.h"
#include "include/private/base/SkTArray.h"
#include "include/private/base/SkTDArray.h"
#include "include/private/base/SkTo.h"*/

/*#include "src/base/SkFloatBits.h"
#include "src/base/SkTLazy.h"
#include "src/base/SkVx.h"*/
#include "src/core/SkCubicClipper.h"
#include "src/core/SkEdgeClipper.h"
#include "src/core/SkGeometry.h"
#include "src/core/SkMatrixPriv.h"
#include "src/core/SkPathEnums.h"
#include "src/core/SkPathMakers.h"
#include "src/core/SkPathPriv.h"
#include "src/core/SkPointPriv.h"
#include "src/core/SkStringUtils.h"


namespace py = pybind11;

void init_skia_path_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkPathFillType>(_skia, "PathFillType", py::arithmetic())
        .value("K_WINDING", SkPathFillType::kWinding)
        .value("K_EVEN_ODD", SkPathFillType::kEvenOdd)
        .value("K_INVERSE_WINDING", SkPathFillType::kInverseWinding)
        .value("K_INVERSE_EVEN_ODD", SkPathFillType::kInverseEvenOdd)
        .export_values()
    ;
    py::enum_<SkPathDirection>(_skia, "PathDirection", py::arithmetic())
        .value("K_CW", SkPathDirection::kCW)
        .value("K_CCW", SkPathDirection::kCCW)
        .export_values()
    ;
    py::enum_<SkPathSegmentMask>(_skia, "PathSegmentMask", py::arithmetic())
        .value("K_LINE_SK_PATH_SEGMENT_MASK", SkPathSegmentMask::kLine_SkPathSegmentMask)
        .value("K_QUAD_SK_PATH_SEGMENT_MASK", SkPathSegmentMask::kQuad_SkPathSegmentMask)
        .value("K_CONIC_SK_PATH_SEGMENT_MASK", SkPathSegmentMask::kConic_SkPathSegmentMask)
        .value("K_CUBIC_SK_PATH_SEGMENT_MASK", SkPathSegmentMask::kCubic_SkPathSegmentMask)
        .export_values()
    ;
    py::enum_<SkPathVerb>(_skia, "PathVerb", py::arithmetic())
        .value("K_MOVE", SkPathVerb::kMove)
        .value("K_LINE", SkPathVerb::kLine)
        .value("K_QUAD", SkPathVerb::kQuad)
        .value("K_CONIC", SkPathVerb::kConic)
        .value("K_CUBIC", SkPathVerb::kCubic)
        .value("K_CLOSE", SkPathVerb::kClose)
        .export_values()
    ;

    py::class_<SkPath> _Path(_skia, "Path");
    registry.on(_skia, "Path", _Path);
        _Path
        .def_static("make", &SkPath::Make
            , py::arg("")
            , py::arg("point_count")
            , py::arg("")
            , py::arg("verb_count")
            , py::arg("")
            , py::arg("conic_weight_count")
            , py::arg("")
            , py::arg("is_volatile") = false
            , py::return_value_policy::automatic_reference)
        .def_static("rect", &SkPath::Rect
            , py::arg("")
            , py::arg("") = SkPathDirection::kCW
            , py::arg("start_index") = 0
            , py::return_value_policy::automatic_reference)
        .def_static("oval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::Oval)
            , py::arg("")
            , py::arg("") = SkPathDirection::kCW
            , py::return_value_policy::automatic_reference)
        .def_static("oval", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPath::Oval)
            , py::arg("")
            , py::arg("")
            , py::arg("start_index")
            , py::return_value_policy::automatic_reference)
        .def_static("circle", &SkPath::Circle
            , py::arg("center_x")
            , py::arg("center_y")
            , py::arg("radius")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::automatic_reference)
        .def_static("r_rect", py::overload_cast<const SkRRect &, SkPathDirection>(&SkPath::RRect)
            , py::arg("")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::automatic_reference)
        .def_static("r_rect", py::overload_cast<const SkRRect &, SkPathDirection, unsigned int>(&SkPath::RRect)
            , py::arg("")
            , py::arg("")
            , py::arg("start_index")
            , py::return_value_policy::automatic_reference)
        .def_static("r_rect", py::overload_cast<const SkRect &, float, float, SkPathDirection>(&SkPath::RRect)
            , py::arg("bounds")
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::automatic_reference)
        .def_static("polygon", py::overload_cast<const SkPoint[], int, bool, SkPathFillType, bool>(&SkPath::Polygon)
            , py::arg("pts")
            , py::arg("count")
            , py::arg("is_closed")
            , py::arg("") = SkPathFillType::kWinding
            , py::arg("is_volatile") = false
            , py::return_value_policy::automatic_reference)
        .def_static("polygon", py::overload_cast<const std::initializer_list<SkPoint> &, bool, SkPathFillType, bool>(&SkPath::Polygon)
            , py::arg("list")
            , py::arg("is_closed")
            , py::arg("fill_type") = SkPathFillType::kWinding
            , py::arg("is_volatile") = false
            , py::return_value_policy::automatic_reference)
        .def_static("line", &SkPath::Line
            , py::arg("a")
            , py::arg("b")
            , py::return_value_policy::automatic_reference)
        .def(py::init<>())
        .def(py::init<const SkPath &>()
        , py::arg("path")
        )
        .def("snapshot", &SkPath::snapshot
            , py::return_value_policy::automatic_reference)
        .def("detach", &SkPath::detach
            , py::return_value_policy::automatic_reference)
        .def("is_interpolatable", &SkPath::isInterpolatable
            , py::arg("compare")
            , py::return_value_policy::automatic_reference)
        .def("interpolate", &SkPath::interpolate
            , py::arg("ending")
            , py::arg("weight")
            , py::arg("out")
            , py::return_value_policy::automatic_reference)
        .def("get_fill_type", &SkPath::getFillType
            , py::return_value_policy::automatic_reference)
        .def("set_fill_type", &SkPath::setFillType
            , py::arg("ft")
            , py::return_value_policy::automatic_reference)
        .def("is_inverse_fill_type", &SkPath::isInverseFillType
            , py::return_value_policy::automatic_reference)
        .def("toggle_inverse_fill_type", &SkPath::toggleInverseFillType
            , py::return_value_policy::automatic_reference)
        .def("is_convex", &SkPath::isConvex
            , py::return_value_policy::automatic_reference)
        .def("is_oval", &SkPath::isOval
            , py::arg("bounds")
            , py::return_value_policy::automatic_reference)
        .def("is_r_rect", &SkPath::isRRect
            , py::arg("rrect")
            , py::return_value_policy::automatic_reference)
        .def("is_arc", &SkPath::isArc
            , py::arg("arc")
            , py::return_value_policy::automatic_reference)
        .def("reset", &SkPath::reset
            , py::return_value_policy::reference)
        .def("rewind", &SkPath::rewind
            , py::return_value_policy::reference)
        .def("is_empty", &SkPath::isEmpty
            , py::return_value_policy::automatic_reference)
        .def("is_last_contour_closed", &SkPath::isLastContourClosed
            , py::return_value_policy::automatic_reference)
        .def("is_finite", &SkPath::isFinite
            , py::return_value_policy::automatic_reference)
        .def("is_volatile", &SkPath::isVolatile
            , py::return_value_policy::automatic_reference)
        .def("set_is_volatile", &SkPath::setIsVolatile
            , py::arg("is_volatile")
            , py::return_value_policy::reference)
        .def_static("is_line_degenerate", &SkPath::IsLineDegenerate
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("exact")
            , py::return_value_policy::automatic_reference)
        .def_static("is_quad_degenerate", &SkPath::IsQuadDegenerate
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("exact")
            , py::return_value_policy::automatic_reference)
        .def_static("is_cubic_degenerate", &SkPath::IsCubicDegenerate
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("p4")
            , py::arg("exact")
            , py::return_value_policy::automatic_reference)
        .def("is_line", [](SkPath& self, std::array<SkPoint, 2>& line)
            {
                auto ret = self.isLine(&line[0]);
                return std::make_tuple(ret, line);
            }
            , py::arg("line")
            , py::return_value_policy::automatic_reference)
        .def("count_points", &SkPath::countPoints
            , py::return_value_policy::automatic_reference)
        .def("get_point", &SkPath::getPoint
            , py::arg("index")
            , py::return_value_policy::automatic_reference)
        .def("get_points", &SkPath::getPoints
            , py::arg("points")
            , py::arg("max")
            , py::return_value_policy::automatic_reference)
        .def("count_verbs", &SkPath::countVerbs
            , py::return_value_policy::automatic_reference)
        .def("get_verbs", &SkPath::getVerbs
            , py::arg("verbs")
            , py::arg("max")
            , py::return_value_policy::automatic_reference)
        .def("approximate_bytes_used", &SkPath::approximateBytesUsed
            , py::return_value_policy::automatic_reference)
        .def("swap", [](SkPath& self, SkPath & other)
            {
                self.swap(other);
                return other;
            }
            , py::arg("other")
            , py::return_value_policy::automatic_reference)
        .def("get_bounds", &SkPath::getBounds
            , py::return_value_policy::reference)
        .def("update_bounds_cache", &SkPath::updateBoundsCache
            , py::return_value_policy::automatic_reference)
        .def("compute_tight_bounds", &SkPath::computeTightBounds
            , py::return_value_policy::automatic_reference)
        .def("conservatively_contains_rect", &SkPath::conservativelyContainsRect
            , py::arg("rect")
            , py::return_value_policy::automatic_reference)
        .def("inc_reserve", &SkPath::incReserve
            , py::arg("extra_pt_count")
            , py::arg("extra_verb_count") = 0
            , py::arg("extra_conic_count") = 0
            , py::return_value_policy::automatic_reference)
        .def("move_to", py::overload_cast<float, float>(&SkPath::moveTo)
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::reference)
        .def("move_to", py::overload_cast<const SkPoint &>(&SkPath::moveTo)
            , py::arg("p")
            , py::return_value_policy::reference)
        .def("r_move_to", &SkPath::rMoveTo
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::reference)
        .def("line_to", py::overload_cast<float, float>(&SkPath::lineTo)
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::reference)
        .def("line_to", py::overload_cast<const SkPoint &>(&SkPath::lineTo)
            , py::arg("p")
            , py::return_value_policy::reference)
        .def("r_line_to", &SkPath::rLineTo
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::reference)
        .def("quad_to", py::overload_cast<float, float, float, float>(&SkPath::quadTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::return_value_policy::reference)
        .def("quad_to", py::overload_cast<const SkPoint &, const SkPoint &>(&SkPath::quadTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::return_value_policy::reference)
        .def("r_quad_to", &SkPath::rQuadTo
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            , py::return_value_policy::reference)
        .def("conic_to", py::overload_cast<float, float, float, float, float>(&SkPath::conicTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::arg("w")
            , py::return_value_policy::reference)
        .def("conic_to", py::overload_cast<const SkPoint &, const SkPoint &, float>(&SkPath::conicTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("w")
            , py::return_value_policy::reference)
        .def("r_conic_to", &SkPath::rConicTo
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            , py::arg("w")
            , py::return_value_policy::reference)
        .def("cubic_to", py::overload_cast<float, float, float, float, float, float>(&SkPath::cubicTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::arg("x3")
            , py::arg("y3")
            , py::return_value_policy::reference)
        .def("cubic_to", py::overload_cast<const SkPoint &, const SkPoint &, const SkPoint &>(&SkPath::cubicTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::return_value_policy::reference)
        .def("r_cubic_to", &SkPath::rCubicTo
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            , py::arg("dx3")
            , py::arg("dy3")
            , py::return_value_policy::reference)
        .def("arc_to", py::overload_cast<const SkRect &, float, float, bool>(&SkPath::arcTo)
            , py::arg("oval")
            , py::arg("start_angle")
            , py::arg("sweep_angle")
            , py::arg("force_move_to")
            , py::return_value_policy::reference)
        .def("arc_to", py::overload_cast<float, float, float, float, float>(&SkPath::arcTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::arg("radius")
            , py::return_value_policy::reference)
        .def("arc_to", py::overload_cast<const SkPoint, const SkPoint, float>(&SkPath::arcTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("radius")
            , py::return_value_policy::reference)
        ;

        py::enum_<SkPath::ArcSize>(_Path, "ArcSize", py::arithmetic())
            .value("K_SMALL_ARC_SIZE", SkPath::ArcSize::kSmall_ArcSize)
            .value("K_LARGE_ARC_SIZE", SkPath::ArcSize::kLarge_ArcSize)
            .export_values()
        ;
        _Path
        .def("arc_to", py::overload_cast<float, float, float, SkPath::ArcSize, SkPathDirection, float, float>(&SkPath::arcTo)
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("x_axis_rotate")
            , py::arg("large_arc")
            , py::arg("sweep")
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::reference)
        .def("arc_to", py::overload_cast<const SkPoint, float, SkPath::ArcSize, SkPathDirection, const SkPoint>(&SkPath::arcTo)
            , py::arg("r")
            , py::arg("x_axis_rotate")
            , py::arg("large_arc")
            , py::arg("sweep")
            , py::arg("xy")
            , py::return_value_policy::reference)
        .def("r_arc_to", &SkPath::rArcTo
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("x_axis_rotate")
            , py::arg("large_arc")
            , py::arg("sweep")
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::reference)
        .def("close", &SkPath::close
            , py::return_value_policy::reference)
        .def_static("convert_conic_to_quads", &SkPath::ConvertConicToQuads
            , py::arg("p0")
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("w")
            , py::arg("pts")
            , py::arg("pow2")
            , py::return_value_policy::automatic_reference)
        .def("is_rect", [](SkPath& self, SkRect * rect, bool * isClosed, SkPathDirection * direction)
            {
                auto ret = self.isRect(rect, isClosed, direction);
                return std::make_tuple(ret, isClosed);
            }
            , py::arg("rect")
            , py::arg("is_closed") = nullptr
            , py::arg("direction") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("add_rect", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPath::addRect)
            , py::arg("rect")
            , py::arg("dir")
            , py::arg("start")
            , py::return_value_policy::reference)
        .def("add_rect", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::addRect)
            , py::arg("rect")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::reference)
        .def("add_rect", py::overload_cast<float, float, float, float, SkPathDirection>(&SkPath::addRect)
            , py::arg("left")
            , py::arg("top")
            , py::arg("right")
            , py::arg("bottom")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::reference)
        .def("add_oval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::addOval)
            , py::arg("oval")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::reference)
        .def("add_oval", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPath::addOval)
            , py::arg("oval")
            , py::arg("dir")
            , py::arg("start")
            , py::return_value_policy::reference)
        .def("add_circle", &SkPath::addCircle
            , py::arg("x")
            , py::arg("y")
            , py::arg("radius")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::reference)
        .def("add_arc", &SkPath::addArc
            , py::arg("oval")
            , py::arg("start_angle")
            , py::arg("sweep_angle")
            , py::return_value_policy::reference)
        .def("add_round_rect", py::overload_cast<const SkRect &, float, float, SkPathDirection>(&SkPath::addRoundRect)
            , py::arg("rect")
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::reference)
        .def("add_round_rect", py::overload_cast<const SkRect &, const float[], SkPathDirection>(&SkPath::addRoundRect)
            , py::arg("rect")
            , py::arg("radii")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::reference)
        .def("add_r_rect", py::overload_cast<const SkRRect &, SkPathDirection>(&SkPath::addRRect)
            , py::arg("rrect")
            , py::arg("dir") = SkPathDirection::kCW
            , py::return_value_policy::reference)
        .def("add_r_rect", py::overload_cast<const SkRRect &, SkPathDirection, unsigned int>(&SkPath::addRRect)
            , py::arg("rrect")
            , py::arg("dir")
            , py::arg("start")
            , py::return_value_policy::reference)
        .def("add_poly", py::overload_cast<const SkPoint[], int, bool>(&SkPath::addPoly)
            , py::arg("pts")
            , py::arg("count")
            , py::arg("close")
            , py::return_value_policy::reference)
        .def("add_poly", py::overload_cast<const std::initializer_list<SkPoint> &, bool>(&SkPath::addPoly)
            , py::arg("list")
            , py::arg("close")
            , py::return_value_policy::reference)
        ;

        py::enum_<SkPath::AddPathMode>(_Path, "AddPathMode", py::arithmetic())
            .value("K_APPEND_ADD_PATH_MODE", SkPath::AddPathMode::kAppend_AddPathMode)
            .value("K_EXTEND_ADD_PATH_MODE", SkPath::AddPathMode::kExtend_AddPathMode)
            .export_values()
        ;
        _Path
        .def("add_path", py::overload_cast<const SkPath &, float, float, SkPath::AddPathMode>(&SkPath::addPath)
            , py::arg("src")
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            , py::return_value_policy::reference)
        .def("add_path", py::overload_cast<const SkPath &, SkPath::AddPathMode>(&SkPath::addPath)
            , py::arg("src")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            , py::return_value_policy::reference)
        .def("add_path", py::overload_cast<const SkPath &, const SkMatrix &, SkPath::AddPathMode>(&SkPath::addPath)
            , py::arg("src")
            , py::arg("matrix")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            , py::return_value_policy::reference)
        .def("reverse_add_path", &SkPath::reverseAddPath
            , py::arg("src")
            , py::return_value_policy::reference)
        .def("offset", py::overload_cast<float, float, SkPath *>(&SkPath::offset, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("dst")
            , py::return_value_policy::automatic_reference)
        .def("offset", py::overload_cast<float, float>(&SkPath::offset)
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::reference)
        .def("transform", py::overload_cast<const SkMatrix &, SkPath *, SkApplyPerspectiveClip>(&SkPath::transform, py::const_)
            , py::arg("matrix")
            , py::arg("dst")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            , py::return_value_policy::automatic_reference)
        .def("transform", py::overload_cast<const SkMatrix &, SkApplyPerspectiveClip>(&SkPath::transform)
            , py::arg("matrix")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            , py::return_value_policy::reference)
        .def("make_transform", &SkPath::makeTransform
            , py::arg("m")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            , py::return_value_policy::automatic_reference)
        .def("make_scale", &SkPath::makeScale
            , py::arg("sx")
            , py::arg("sy")
            , py::return_value_policy::automatic_reference)
        .def("get_last_pt", &SkPath::getLastPt
            , py::arg("last_pt")
            , py::return_value_policy::automatic_reference)
        .def("set_last_pt", py::overload_cast<float, float>(&SkPath::setLastPt)
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("set_last_pt", py::overload_cast<const SkPoint &>(&SkPath::setLastPt)
            , py::arg("p")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkPath::SegmentMask>(_Path, "SegmentMask", py::arithmetic())
            .value("K_LINE_SEGMENT_MASK", SkPath::SegmentMask::kLine_SegmentMask)
            .value("K_QUAD_SEGMENT_MASK", SkPath::SegmentMask::kQuad_SegmentMask)
            .value("K_CONIC_SEGMENT_MASK", SkPath::SegmentMask::kConic_SegmentMask)
            .value("K_CUBIC_SEGMENT_MASK", SkPath::SegmentMask::kCubic_SegmentMask)
            .export_values()
        ;
        _Path
        .def("get_segment_masks", &SkPath::getSegmentMasks
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkPath::Verb>(_Path, "Verb", py::arithmetic())
            .value("K_MOVE_VERB", SkPath::Verb::kMove_Verb)
            .value("K_LINE_VERB", SkPath::Verb::kLine_Verb)
            .value("K_QUAD_VERB", SkPath::Verb::kQuad_Verb)
            .value("K_CONIC_VERB", SkPath::Verb::kConic_Verb)
            .value("K_CUBIC_VERB", SkPath::Verb::kCubic_Verb)
            .value("K_CLOSE_VERB", SkPath::Verb::kClose_Verb)
            .value("K_DONE_VERB", SkPath::Verb::kDone_Verb)
            .export_values()
        ;
        py::class_<SkPath::Iter> _PathIter(_skia, "PathIter");
        registry.on(_skia, "PathIter", _PathIter);
            _PathIter
            .def(py::init<>())
            .def(py::init<const SkPath &, bool>()
            , py::arg("path")
            , py::arg("force_close")
            )
            .def("set_path", &SkPath::Iter::setPath
                , py::arg("path")
                , py::arg("force_close")
                , py::return_value_policy::automatic_reference)
            .def("next", [](SkPath::Iter& self, std::array<SkPoint, 4>& pts)
                {
                    auto ret = self.next(&pts[0]);
                    return std::make_tuple(ret, pts);
                }
                , py::arg("pts")
                , py::return_value_policy::automatic_reference)
            .def("conic_weight", &SkPath::Iter::conicWeight
                , py::return_value_policy::automatic_reference)
            .def("is_close_line", &SkPath::Iter::isCloseLine
                , py::return_value_policy::automatic_reference)
            .def("is_closed_contour", &SkPath::Iter::isClosedContour
                , py::return_value_policy::automatic_reference)
        ;

        _Path
        .def("contains", &SkPath::contains
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("dump", py::overload_cast<SkWStream *, bool>(&SkPath::dump, py::const_)
            , py::arg("stream")
            , py::arg("dump_as_hex")
            , py::return_value_policy::automatic_reference)
        .def("dump", py::overload_cast<>(&SkPath::dump, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("dump_hex", &SkPath::dumpHex
            , py::return_value_policy::automatic_reference)
        .def("dump_arrays", py::overload_cast<SkWStream *, bool>(&SkPath::dumpArrays, py::const_)
            , py::arg("stream")
            , py::arg("dump_as_hex")
            , py::return_value_policy::automatic_reference)
        .def("dump_arrays", py::overload_cast<>(&SkPath::dumpArrays, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("write_to_memory", &SkPath::writeToMemory
            , py::arg("buffer")
            , py::return_value_policy::automatic_reference)
        .def("serialize", &SkPath::serialize
            , py::return_value_policy::automatic_reference)
        .def("read_from_memory", &SkPath::readFromMemory
            , py::arg("buffer")
            , py::arg("length")
            , py::return_value_policy::automatic_reference)
        .def("get_generation_id", &SkPath::getGenerationID
            , py::return_value_policy::automatic_reference)
        .def("is_valid", &SkPath::isValid
            , py::return_value_policy::automatic_reference)
    ;


}