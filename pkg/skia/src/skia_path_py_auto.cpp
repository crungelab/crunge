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
        .def_static("make", [](const SkPoint arg0[], int pointCount, const uint8_t arg2[], int verbCount, const SkScalar arg4[], int conicWeightCount, SkPathFillType arg6, bool isVolatile)
            {
                auto _ret = SkPath::Make(arg0, pointCount, arg2, verbCount, arg4, conicWeightCount, arg6, isVolatile);
                return std::make_tuple(_ret, arg4);
            }
            , py::arg("arg0")
            , py::arg("point_count")
            , py::arg("arg2")
            , py::arg("verb_count")
            , py::arg("arg4")
            , py::arg("conic_weight_count")
            , py::arg("arg6")
            , py::arg("is_volatile") = false
            )
        .def_static("rect", &SkPath::Rect
            , py::arg("arg0")
            , py::arg("arg1") = SkPathDirection::kCW
            , py::arg("start_index") = 0
            )
        .def_static("oval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::Oval)
            , py::arg("arg0")
            , py::arg("arg1") = SkPathDirection::kCW
            )
        .def_static("oval", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPath::Oval)
            , py::arg("arg0")
            , py::arg("arg1")
            , py::arg("start_index")
            )
        .def_static("circle", &SkPath::Circle
            , py::arg("center_x")
            , py::arg("center_y")
            , py::arg("radius")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def_static("r_rect", py::overload_cast<const SkRRect &, SkPathDirection>(&SkPath::RRect)
            , py::arg("arg0")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def_static("r_rect", py::overload_cast<const SkRRect &, SkPathDirection, unsigned int>(&SkPath::RRect)
            , py::arg("arg0")
            , py::arg("arg1")
            , py::arg("start_index")
            )
        .def_static("r_rect", py::overload_cast<const SkRect &, SkScalar, SkScalar, SkPathDirection>(&SkPath::RRect)
            , py::arg("bounds")
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def_static("polygon", py::overload_cast<const SkPoint[], int, bool, SkPathFillType, bool>(&SkPath::Polygon)
            , py::arg("pts")
            , py::arg("count")
            , py::arg("is_closed")
            , py::arg("arg3") = SkPathFillType::kWinding
            , py::arg("is_volatile") = false
            )
        .def_static("polygon", py::overload_cast<const std::initializer_list<SkPoint> &, bool, SkPathFillType, bool>(&SkPath::Polygon)
            , py::arg("list")
            , py::arg("is_closed")
            , py::arg("fill_type") = SkPathFillType::kWinding
            , py::arg("is_volatile") = false
            )
        .def_static("line", &SkPath::Line
            , py::arg("a")
            , py::arg("b")
            )
        .def(py::init<>())
        .def("snapshot", &SkPath::snapshot
            )
        .def("detach", &SkPath::detach
            )
        .def("is_interpolatable", &SkPath::isInterpolatable
            , py::arg("compare")
            )
        .def("interpolate", &SkPath::interpolate
            , py::arg("ending")
            , py::arg("weight")
            , py::arg("out")
            )
        .def("get_fill_type", &SkPath::getFillType
            )
        .def("set_fill_type", &SkPath::setFillType
            , py::arg("ft")
            )
        .def("is_inverse_fill_type", &SkPath::isInverseFillType
            )
        .def("toggle_inverse_fill_type", &SkPath::toggleInverseFillType
            )
        .def("is_convex", &SkPath::isConvex
            )
        .def("is_oval", &SkPath::isOval
            , py::arg("bounds")
            )
        .def("is_r_rect", &SkPath::isRRect
            , py::arg("rrect")
            )
        .def("is_arc", &SkPath::isArc
            , py::arg("arc")
            )
        .def("reset", &SkPath::reset
            )
        .def("rewind", &SkPath::rewind
            )
        .def("is_empty", &SkPath::isEmpty
            )
        .def("is_last_contour_closed", &SkPath::isLastContourClosed
            )
        .def("is_finite", &SkPath::isFinite
            )
        .def("is_volatile", &SkPath::isVolatile
            )
        .def("set_is_volatile", &SkPath::setIsVolatile
            , py::arg("is_volatile")
            )
        .def_static("is_line_degenerate", &SkPath::IsLineDegenerate
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("exact")
            )
        .def_static("is_quad_degenerate", &SkPath::IsQuadDegenerate
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("exact")
            )
        .def_static("is_cubic_degenerate", &SkPath::IsCubicDegenerate
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("p4")
            , py::arg("exact")
            )
        .def("is_line", [](SkPath& self, std::array<SkPoint, 2>& line)
            {
                return self.isLine(&line[0]);
            }
            , py::arg("line")
            )
        .def("count_points", &SkPath::countPoints
            )
        .def("get_point", &SkPath::getPoint
            , py::arg("index")
            )
        .def("get_points", &SkPath::getPoints
            , py::arg("points")
            , py::arg("max")
            )
        .def("count_verbs", &SkPath::countVerbs
            )
        .def("get_verbs", &SkPath::getVerbs
            , py::arg("verbs")
            , py::arg("max")
            )
        .def("approximate_bytes_used", &SkPath::approximateBytesUsed
            )
        .def("swap", [](SkPath& self, SkPath & other)
            {
                self.swap(other);
                return std::make_tuple(other);
            }
            , py::arg("other")
            )
        .def("get_bounds", &SkPath::getBounds
            )
        .def("update_bounds_cache", &SkPath::updateBoundsCache
            )
        .def("compute_tight_bounds", &SkPath::computeTightBounds
            )
        .def("conservatively_contains_rect", &SkPath::conservativelyContainsRect
            , py::arg("rect")
            )
        .def("inc_reserve", &SkPath::incReserve
            , py::arg("extra_pt_count")
            , py::arg("extra_verb_count") = 0
            , py::arg("extra_conic_count") = 0
            )
        .def("move_to", py::overload_cast<SkScalar, SkScalar>(&SkPath::moveTo)
            , py::arg("x")
            , py::arg("y")
            )
        .def("move_to", py::overload_cast<const SkPoint &>(&SkPath::moveTo)
            , py::arg("p")
            )
        .def("r_move_to", &SkPath::rMoveTo
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("line_to", py::overload_cast<SkScalar, SkScalar>(&SkPath::lineTo)
            , py::arg("x")
            , py::arg("y")
            )
        .def("line_to", py::overload_cast<const SkPoint &>(&SkPath::lineTo)
            , py::arg("p")
            )
        .def("r_line_to", &SkPath::rLineTo
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("quad_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkPath::quadTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            )
        .def("quad_to", py::overload_cast<const SkPoint &, const SkPoint &>(&SkPath::quadTo)
            , py::arg("p1")
            , py::arg("p2")
            )
        .def("r_quad_to", &SkPath::rQuadTo
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            )
        .def("conic_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPath::conicTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::arg("w")
            )
        .def("conic_to", py::overload_cast<const SkPoint &, const SkPoint &, SkScalar>(&SkPath::conicTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("w")
            )
        .def("r_conic_to", &SkPath::rConicTo
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            , py::arg("w")
            )
        .def("cubic_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPath::cubicTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::arg("x3")
            , py::arg("y3")
            )
        .def("cubic_to", py::overload_cast<const SkPoint &, const SkPoint &, const SkPoint &>(&SkPath::cubicTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            )
        .def("r_cubic_to", &SkPath::rCubicTo
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            , py::arg("dx3")
            , py::arg("dy3")
            )
        .def("arc_to", py::overload_cast<const SkRect &, SkScalar, SkScalar, bool>(&SkPath::arcTo)
            , py::arg("oval")
            , py::arg("start_angle")
            , py::arg("sweep_angle")
            , py::arg("force_move_to")
            )
        .def("arc_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPath::arcTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::arg("radius")
            )
        .def("arc_to", py::overload_cast<const SkPoint, const SkPoint, SkScalar>(&SkPath::arcTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("radius")
            )
        ;

        py::enum_<SkPath::ArcSize>(_Path, "ArcSize", py::arithmetic())
            .value("K_SMALL_ARC_SIZE", SkPath::ArcSize::kSmall_ArcSize)
            .value("K_LARGE_ARC_SIZE", SkPath::ArcSize::kLarge_ArcSize)
            .export_values()
        ;
        _Path
        .def("arc_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkPath::ArcSize, SkPathDirection, SkScalar, SkScalar>(&SkPath::arcTo)
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("x_axis_rotate")
            , py::arg("large_arc")
            , py::arg("sweep")
            , py::arg("x")
            , py::arg("y")
            )
        .def("arc_to", py::overload_cast<const SkPoint, SkScalar, SkPath::ArcSize, SkPathDirection, const SkPoint>(&SkPath::arcTo)
            , py::arg("r")
            , py::arg("x_axis_rotate")
            , py::arg("large_arc")
            , py::arg("sweep")
            , py::arg("xy")
            )
        .def("r_arc_to", &SkPath::rArcTo
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("x_axis_rotate")
            , py::arg("large_arc")
            , py::arg("sweep")
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("close", &SkPath::close
            )
        .def_static("convert_conic_to_quads", &SkPath::ConvertConicToQuads
            , py::arg("p0")
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("w")
            , py::arg("pts")
            , py::arg("pow2")
            )
        .def("is_rect", [](SkPath& self, SkRect * rect, bool * isClosed, SkPathDirection * direction)
            {
                auto _ret = self.isRect(rect, isClosed, direction);
                return std::make_tuple(_ret, isClosed, direction);
            }
            , py::arg("rect")
            , py::arg("is_closed") = nullptr
            , py::arg("direction") = nullptr
            )
        .def("add_rect", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPath::addRect)
            , py::arg("rect")
            , py::arg("dir")
            , py::arg("start")
            )
        .def("add_rect", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::addRect)
            , py::arg("rect")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def("add_rect", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkPathDirection>(&SkPath::addRect)
            , py::arg("left")
            , py::arg("top")
            , py::arg("right")
            , py::arg("bottom")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def("add_oval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::addOval)
            , py::arg("oval")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def("add_oval", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPath::addOval)
            , py::arg("oval")
            , py::arg("dir")
            , py::arg("start")
            )
        .def("add_circle", &SkPath::addCircle
            , py::arg("x")
            , py::arg("y")
            , py::arg("radius")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def("add_arc", &SkPath::addArc
            , py::arg("oval")
            , py::arg("start_angle")
            , py::arg("sweep_angle")
            )
        .def("add_round_rect", py::overload_cast<const SkRect &, SkScalar, SkScalar, SkPathDirection>(&SkPath::addRoundRect)
            , py::arg("rect")
            , py::arg("rx")
            , py::arg("ry")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def("add_round_rect", [](SkPath& self, const SkRect & rect, const SkScalar radii[], SkPathDirection dir)
            {
                auto _ret = self.addRoundRect(rect, radii, dir);
                return std::make_tuple(_ret, radii);
            }
            , py::arg("rect")
            , py::arg("radii")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def("add_r_rect", py::overload_cast<const SkRRect &, SkPathDirection>(&SkPath::addRRect)
            , py::arg("rrect")
            , py::arg("dir") = SkPathDirection::kCW
            )
        .def("add_r_rect", py::overload_cast<const SkRRect &, SkPathDirection, unsigned int>(&SkPath::addRRect)
            , py::arg("rrect")
            , py::arg("dir")
            , py::arg("start")
            )
        .def("add_poly", py::overload_cast<const SkPoint[], int, bool>(&SkPath::addPoly)
            , py::arg("pts")
            , py::arg("count")
            , py::arg("close")
            )
        .def("add_poly", py::overload_cast<const std::initializer_list<SkPoint> &, bool>(&SkPath::addPoly)
            , py::arg("list")
            , py::arg("close")
            )
        ;

        py::enum_<SkPath::AddPathMode>(_Path, "AddPathMode", py::arithmetic())
            .value("K_APPEND_ADD_PATH_MODE", SkPath::AddPathMode::kAppend_AddPathMode)
            .value("K_EXTEND_ADD_PATH_MODE", SkPath::AddPathMode::kExtend_AddPathMode)
            .export_values()
        ;
        _Path
        .def("add_path", py::overload_cast<const SkPath &, SkScalar, SkScalar, SkPath::AddPathMode>(&SkPath::addPath)
            , py::arg("src")
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            )
        .def("add_path", py::overload_cast<const SkPath &, SkPath::AddPathMode>(&SkPath::addPath)
            , py::arg("src")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            )
        .def("add_path", py::overload_cast<const SkPath &, const SkMatrix &, SkPath::AddPathMode>(&SkPath::addPath)
            , py::arg("src")
            , py::arg("matrix")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            )
        .def("reverse_add_path", &SkPath::reverseAddPath
            , py::arg("src")
            )
        .def("offset", py::overload_cast<SkScalar, SkScalar, SkPath *>(&SkPath::offset, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("dst")
            )
        .def("offset", py::overload_cast<SkScalar, SkScalar>(&SkPath::offset)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("transform", py::overload_cast<const SkMatrix &, SkPath *, SkApplyPerspectiveClip>(&SkPath::transform, py::const_)
            , py::arg("matrix")
            , py::arg("dst")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            )
        .def("transform", py::overload_cast<const SkMatrix &, SkApplyPerspectiveClip>(&SkPath::transform)
            , py::arg("matrix")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            )
        .def("make_transform", &SkPath::makeTransform
            , py::arg("m")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            )
        .def("make_scale", &SkPath::makeScale
            , py::arg("sx")
            , py::arg("sy")
            )
        .def("get_last_pt", &SkPath::getLastPt
            , py::arg("last_pt")
            )
        .def("set_last_pt", py::overload_cast<SkScalar, SkScalar>(&SkPath::setLastPt)
            , py::arg("x")
            , py::arg("y")
            )
        .def("set_last_pt", py::overload_cast<const SkPoint &>(&SkPath::setLastPt)
            , py::arg("p")
            )
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
            )
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
                )
            .def("next", [](SkPath::Iter& self, std::array<SkPoint, 4>& pts)
                {
                    return self.next(&pts[0]);
                }
                , py::arg("pts")
                )
            .def("conic_weight", &SkPath::Iter::conicWeight
                )
            .def("is_close_line", &SkPath::Iter::isCloseLine
                )
            .def("is_closed_contour", &SkPath::Iter::isClosedContour
                )
        ;

        _Path
        .def("contains", &SkPath::contains
            , py::arg("x")
            , py::arg("y")
            )
        .def("dump", py::overload_cast<SkWStream *, bool>(&SkPath::dump, py::const_)
            , py::arg("stream")
            , py::arg("dump_as_hex")
            )
        .def("dump", py::overload_cast<>(&SkPath::dump, py::const_)
            )
        .def("dump_hex", &SkPath::dumpHex
            )
        .def("dump_arrays", py::overload_cast<SkWStream *, bool>(&SkPath::dumpArrays, py::const_)
            , py::arg("stream")
            , py::arg("dump_as_hex")
            )
        .def("dump_arrays", py::overload_cast<>(&SkPath::dumpArrays, py::const_)
            )
        .def("write_to_memory", &SkPath::writeToMemory
            , py::arg("buffer")
            )
        .def("serialize", &SkPath::serialize
            )
        .def("read_from_memory", &SkPath::readFromMemory
            , py::arg("buffer")
            , py::arg("length")
            )
        .def("get_generation_id", &SkPath::getGenerationID
            )
        .def("is_valid", &SkPath::isValid
            )
    ;


}