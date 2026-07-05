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
        .value("K_DEFAULT", SkPathFillType::kDefault)
        .export_values()
    ;
    py::enum_<SkPathDirection>(_skia, "PathDirection", py::arithmetic())
        .value("K_CW", SkPathDirection::kCW)
        .value("K_CCW", SkPathDirection::kCCW)
        .value("K_DEFAULT", SkPathDirection::kDefault)
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
        .value("K_LAST_VERB", SkPathVerb::kLast_Verb)
        .export_values()
    ;

    py::class_<SkPath> _Path(_skia, "Path");
    registry.on(_skia, "Path", _Path);
        _Path
        .def_static("raw", &SkPath::Raw
            , py::arg("pts")
            , py::arg("verbs")
            , py::arg("conics")
            , py::arg("arg3")
            , py::arg("is_volatile") = false
            )
        .def_static("rect", py::overload_cast<const SkRect &, SkPathFillType, SkPathDirection, unsigned int>(&SkPath::Rect)
            , py::arg("arg0")
            , py::arg("arg1")
            , py::arg("arg2") = SkPathDirection::kDefault
            , py::arg("start_index") = 0
            )
        .def_static("rect", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPath::Rect)
            , py::arg("r")
            , py::arg("direction") = SkPathDirection::kDefault
            , py::arg("start_index") = 0
            )
        .def_static("oval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::Oval)
            , py::arg("arg0")
            , py::arg("arg1") = SkPathDirection::kDefault
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
            , py::arg("dir") = SkPathDirection::kDefault
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
            , py::arg("dir") = SkPathDirection::kDefault
            )
        .def_static("polygon", &SkPath::Polygon
            , py::arg("pts")
            , py::arg("is_closed")
            , py::arg("fill_type") = SkPathFillType::kDefault
            , py::arg("is_volatile") = false
            )
        .def_static("line", &SkPath::Line
            , py::arg("a")
            , py::arg("b")
            )
        .def_static("make", &SkPath::Make
            , py::arg("pts")
            , py::arg("verbs")
            , py::arg("conics")
            , py::arg("fill_type")
            , py::arg("is_volatile") = false
            )
        .def(py::init<SkPathFillType>()
        , py::arg("arg0")
        )
        .def(py::init<>())
        .def("snapshot", &SkPath::snapshot
            )
        .def("is_interpolatable", &SkPath::isInterpolatable
            , py::arg("compare")
            )
        .def("make_interpolate", &SkPath::makeInterpolate
            , py::arg("ending")
            , py::arg("weight")
            )
        .def("interpolate", &SkPath::interpolate
            , py::arg("ending")
            , py::arg("weight")
            , py::arg("out")
            )
        .def("get_fill_type", &SkPath::getFillType
            )
        .def("make_fill_type", &SkPath::makeFillType
            , py::arg("new_fill_type")
            )
        .def("is_inverse_fill_type", &SkPath::isInverseFillType
            )
        .def("make_toggle_inverse_fill_type", &SkPath::makeToggleInverseFillType
            )
        .def("is_convex", &SkPath::isConvex
            )
        .def("is_oval", &SkPath::isOval
            , py::arg("bounds")
            )
        .def("is_r_rect", &SkPath::isRRect
            , py::arg("rrect")
            )
        .def("is_empty", &SkPath::isEmpty
            )
        .def("is_last_contour_closed", &SkPath::isLastContourClosed
            )
        .def("is_finite", &SkPath::isFinite
            )
        .def("is_volatile", &SkPath::isVolatile
            )
        .def("make_is_volatile", &SkPath::makeIsVolatile
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
        .def("points", &SkPath::points
            )
        .def("verbs", &SkPath::verbs
            )
        .def("conic_weights", &SkPath::conicWeights
            )
        .def("count_points", &SkPath::countPoints
            )
        .def("count_verbs", &SkPath::countVerbs
            )
        .def("get_last_pt", py::overload_cast<>(&SkPath::getLastPt, py::const_)
            )
        .def("get_point", &SkPath::getPoint
            , py::arg("index")
            )
        .def("get_points", &SkPath::getPoints
            , py::arg("points")
            )
        .def("get_verbs", &SkPath::getVerbs
            , py::arg("verbs")
            )
        .def("get_last_pt", py::overload_cast<SkPoint *>(&SkPath::getLastPt, py::const_)
            , py::arg("last_pt")
            )
        .def("approximate_bytes_used", &SkPath::approximateBytesUsed
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
        ;

        py::enum_<SkPath::AddPathMode>(_Path, "AddPathMode", py::arithmetic())
            .value("K_APPEND_ADD_PATH_MODE", SkPath::AddPathMode::kAppend_AddPathMode)
            .value("K_EXTEND_ADD_PATH_MODE", SkPath::AddPathMode::kExtend_AddPathMode)
            .export_values()
        ;
        _Path
        .def("try_make_transform", &SkPath::tryMakeTransform
            , py::arg("matrix")
            )
        .def("try_make_offset", &SkPath::tryMakeOffset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("try_make_scale", &SkPath::tryMakeScale
            , py::arg("sx")
            , py::arg("sy")
            )
        .def("make_transform", &SkPath::makeTransform
            , py::arg("matrix")
            )
        .def("make_offset", &SkPath::makeOffset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("make_scale", &SkPath::makeScale
            , py::arg("sx")
            , py::arg("sy")
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
        _Path
        .def("set_is_volatile", &SkPath::setIsVolatile
            , py::arg("is_volatile")
            )
        .def("swap", [](SkPath& self, SkPath & other)
            {
                self.swap(other);
                return std::make_tuple(other);
            }
            , py::arg("other")
            )
        .def("set_fill_type", &SkPath::setFillType
            , py::arg("ft")
            )
        .def("toggle_inverse_fill_type", &SkPath::toggleInverseFillType
            )
        .def("reset", &SkPath::reset
            )
        .def("iter", &SkPath::iter
            )
        ;

        py::class_<SkPath::IterRec> _PathIterRec(_skia, "PathIterRec");
        registry.on(_skia, "PathIterRec", _PathIterRec);
            _PathIterRec
            .def_readwrite("f_verb", &SkPath::IterRec::fVerb)
            .def_readwrite("f_points", &SkPath::IterRec::fPoints)
            .def_readwrite("f_conic_weight", &SkPath::IterRec::fConicWeight)
            .def("conic_weight", &SkPath::IterRec::conicWeight
                )
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
            .def("next", py::overload_cast<>(&SkPath::Iter::next)
                )
            .def("conic_weight", &SkPath::Iter::conicWeight
                )
            .def("is_close_line", &SkPath::Iter::isCloseLine
                )
            .def("is_closed_contour", &SkPath::Iter::isClosedContour
                )
        ;

        _Path
        .def("contains", py::overload_cast<SkPoint>(&SkPath::contains, py::const_)
            , py::arg("point")
            )
        .def("contains", py::overload_cast<SkScalar, SkScalar>(&SkPath::contains, py::const_)
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
        .def("write_to_memory", &SkPath::writeToMemory
            , py::arg("buffer")
            )
        .def("serialize", &SkPath::serialize
            )
        .def_static("read_from_memory", [](const void * buffer, size_t length, size_t * bytesRead)
            {
                auto _ret = SkPath::ReadFromMemory(buffer, length, bytesRead);
                return std::make_tuple(_ret, bytesRead);
            }
            , py::arg("buffer")
            , py::arg("length")
            , py::arg("bytes_read") = nullptr
            )
        .def("get_generation_id", &SkPath::getGenerationID
            )
        .def("is_valid", &SkPath::isValid
            )
    ;


}