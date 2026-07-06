#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include "include/core/SkPathBuilder.h"

#include "src/core/SkPathRaw.h"
//#include "src/core/SkPathData.h"

#include "include/core/SkString.h"

/*
#include "include/core/SkArc.h"
#include "include/core/SkPathBuilder.h"
#include "include/core/SkRRect.h"
#include "include/core/SkStream.h"
#include "include/core/SkString.h"

#include "src/core/SkCubicClipper.h"
#include "src/core/SkEdgeClipper.h"
#include "src/core/SkGeometry.h"
#include "src/core/SkMatrixPriv.h"
#include "src/core/SkPathEnums.h"
#include "src/core/SkPathMakers.h"
#include "src/core/SkPathPriv.h"
#include "src/core/SkPointPriv.h"
#include "src/core/SkStringUtils.h"
*/

namespace py = pybind11;

void init_skia_path_builder_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkPathBuilder> _PathBuilder(_skia, "PathBuilder");
    registry.on(_skia, "PathBuilder", _PathBuilder);
        _PathBuilder
        .def(py::init<>())
        .def(py::init<SkPathFillType>()
        , py::arg("fill_type")
        )
        .def(py::init<const SkPath &>()
        , py::arg("path")
        )
        .def("fill_type", &SkPathBuilder::fillType
            )
        .def("compute_finite_bounds", &SkPathBuilder::computeFiniteBounds
            )
        .def("compute_tight_bounds", &SkPathBuilder::computeTightBounds
            )
        .def("compute_bounds", &SkPathBuilder::computeBounds
            )
        .def("snapshot", &SkPathBuilder::snapshot
            , py::arg("mx") = nullptr
            )
        .def("detach", &SkPathBuilder::detach
            , py::arg("mx") = nullptr
            )
        .def("set_fill_type", &SkPathBuilder::setFillType
            , py::arg("ft")
            )
        .def("set_is_volatile", &SkPathBuilder::setIsVolatile
            , py::arg("is_volatile")
            )
        .def("reset", &SkPathBuilder::reset
            )
        .def("move_to", py::overload_cast<SkPoint>(&SkPathBuilder::moveTo)
            , py::arg("point")
            )
        .def("move_to", py::overload_cast<SkScalar, SkScalar>(&SkPathBuilder::moveTo)
            , py::arg("x")
            , py::arg("y")
            )
        .def("line_to", py::overload_cast<SkPoint>(&SkPathBuilder::lineTo)
            , py::arg("pt")
            )
        .def("line_to", py::overload_cast<SkScalar, SkScalar>(&SkPathBuilder::lineTo)
            , py::arg("x")
            , py::arg("y")
            )
        .def("quad_to", py::overload_cast<SkPoint, SkPoint>(&SkPathBuilder::quadTo)
            , py::arg("pt1")
            , py::arg("pt2")
            )
        .def("quad_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::quadTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            )
        .def("quad_to", [](SkPathBuilder& self, std::array<SkPoint, 2>& pts)
            {
                return self.quadTo(&pts[0]);
            }
            , py::arg("pts")
            )
        .def("conic_to", py::overload_cast<SkPoint, SkPoint, SkScalar>(&SkPathBuilder::conicTo)
            , py::arg("pt1")
            , py::arg("pt2")
            , py::arg("w")
            )
        .def("conic_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::conicTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::arg("w")
            )
        .def("conic_to", [](SkPathBuilder& self, std::array<SkPoint, 2>& pts, SkScalar w)
            {
                return self.conicTo(&pts[0], w);
            }
            , py::arg("pts")
            , py::arg("w")
            )
        .def("cubic_to", py::overload_cast<SkPoint, SkPoint, SkPoint>(&SkPathBuilder::cubicTo)
            , py::arg("pt1")
            , py::arg("pt2")
            , py::arg("pt3")
            )
        .def("cubic_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::cubicTo)
            , py::arg("x1")
            , py::arg("y1")
            , py::arg("x2")
            , py::arg("y2")
            , py::arg("x3")
            , py::arg("y3")
            )
        .def("cubic_to", [](SkPathBuilder& self, std::array<SkPoint, 3>& pts)
            {
                return self.cubicTo(&pts[0]);
            }
            , py::arg("pts")
            )
        .def("close", &SkPathBuilder::close
            )
        .def("polyline_to", &SkPathBuilder::polylineTo
            , py::arg("pts")
            )
        .def("r_move_to", py::overload_cast<SkVector>(&SkPathBuilder::rMoveTo)
            , py::arg("pt")
            )
        .def("r_move_to", py::overload_cast<SkScalar, SkScalar>(&SkPathBuilder::rMoveTo)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("r_line_to", py::overload_cast<SkVector>(&SkPathBuilder::rLineTo)
            , py::arg("pt")
            )
        .def("r_line_to", py::overload_cast<SkScalar, SkScalar>(&SkPathBuilder::rLineTo)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("r_quad_to", py::overload_cast<SkVector, SkVector>(&SkPathBuilder::rQuadTo)
            , py::arg("pt1")
            , py::arg("pt2")
            )
        .def("r_quad_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::rQuadTo)
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            )
        .def("r_conic_to", py::overload_cast<SkVector, SkVector, SkScalar>(&SkPathBuilder::rConicTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("w")
            )
        .def("r_conic_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::rConicTo)
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            , py::arg("w")
            )
        .def("r_cubic_to", py::overload_cast<SkVector, SkVector, SkVector>(&SkPathBuilder::rCubicTo)
            , py::arg("pt1")
            , py::arg("pt2")
            , py::arg("pt3")
            )
        .def("r_cubic_to", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::rCubicTo)
            , py::arg("dx1")
            , py::arg("dy1")
            , py::arg("dx2")
            , py::arg("dy2")
            , py::arg("dx3")
            , py::arg("dy3")
            )
        ;

        py::enum_<SkPathBuilder::ArcSize>(_PathBuilder, "ArcSize", py::arithmetic())
            .value("K_SMALL_ARC_SIZE", SkPathBuilder::ArcSize::kSmall_ArcSize)
            .value("K_LARGE_ARC_SIZE", SkPathBuilder::ArcSize::kLarge_ArcSize)
            .export_values()
        ;
        _PathBuilder
        .def("r_arc_to", &SkPathBuilder::rArcTo
            , py::arg("r")
            , py::arg("x_axis_rotate")
            , py::arg("large_arc")
            , py::arg("sweep")
            , py::arg("dxdy")
            )
        .def("arc_to", py::overload_cast<const SkRect &, SkScalar, SkScalar, bool>(&SkPathBuilder::arcTo)
            , py::arg("oval")
            , py::arg("start_angle_deg")
            , py::arg("sweep_angle_deg")
            , py::arg("force_move_to")
            )
        .def("arc_to", py::overload_cast<SkPoint, SkPoint, SkScalar>(&SkPathBuilder::arcTo)
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("radius")
            )
        .def("arc_to", py::overload_cast<SkPoint, SkScalar, SkPathBuilder::ArcSize, SkPathDirection, SkPoint>(&SkPathBuilder::arcTo)
            , py::arg("r")
            , py::arg("x_axis_rotate")
            , py::arg("large_arc")
            , py::arg("sweep")
            , py::arg("xy")
            )
        .def("add_arc", &SkPathBuilder::addArc
            , py::arg("oval")
            , py::arg("start_angle_deg")
            , py::arg("sweep_angle_deg")
            )
        .def("add_line", &SkPathBuilder::addLine
            , py::arg("a")
            , py::arg("b")
            )
        .def("add_rect", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPathBuilder::addRect)
            , py::arg("arg0")
            , py::arg("arg1")
            , py::arg("start_index")
            )
        .def("add_rect", py::overload_cast<const SkRect &, SkPathDirection>(&SkPathBuilder::addRect)
            , py::arg("rect")
            , py::arg("dir") = SkPathDirection::kDefault
            )
        .def("add_oval", py::overload_cast<const SkRect &, SkPathDirection, unsigned int>(&SkPathBuilder::addOval)
            , py::arg("arg0")
            , py::arg("arg1")
            , py::arg("start_index")
            )
        .def("add_r_rect", py::overload_cast<const SkRRect &, SkPathDirection, unsigned int>(&SkPathBuilder::addRRect)
            , py::arg("rrect")
            , py::arg("arg1")
            , py::arg("start")
            )
        .def("add_r_rect", py::overload_cast<const SkRRect &, SkPathDirection>(&SkPathBuilder::addRRect)
            , py::arg("rrect")
            , py::arg("dir") = SkPathDirection::kDefault
            )
        .def("add_oval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPathBuilder::addOval)
            , py::arg("oval")
            , py::arg("dir") = SkPathDirection::kDefault
            )
        .def("add_circle", py::overload_cast<SkPoint, float, SkPathDirection>(&SkPathBuilder::addCircle)
            , py::arg("center")
            , py::arg("radius")
            , py::arg("dir") = SkPathDirection::kDefault
            )
        .def("add_circle", py::overload_cast<float, float, float, SkPathDirection>(&SkPathBuilder::addCircle)
            , py::arg("x")
            , py::arg("y")
            , py::arg("radius")
            , py::arg("dir") = SkPathDirection::kDefault
            )
        .def("add_polygon", &SkPathBuilder::addPolygon
            , py::arg("pts")
            , py::arg("close")
            )
        .def("add_path", py::overload_cast<const SkPath &, SkScalar, SkScalar, SkPath::AddPathMode>(&SkPathBuilder::addPath)
            , py::arg("src")
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            )
        .def("add_path", py::overload_cast<const SkPath &, SkPath::AddPathMode>(&SkPathBuilder::addPath)
            , py::arg("src")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            )
        .def("add_path", py::overload_cast<const SkPath &, const SkMatrix &, SkPath::AddPathMode>(&SkPathBuilder::addPath)
            , py::arg("src")
            , py::arg("matrix")
            , py::arg("mode") = SkPath::AddPathMode::kAppend_AddPathMode
            )
        .def("inc_reserve", py::overload_cast<int, int, int>(&SkPathBuilder::incReserve)
            , py::arg("extra_pt_count")
            , py::arg("extra_verb_count")
            , py::arg("extra_conic_count")
            )
        .def("inc_reserve", py::overload_cast<int>(&SkPathBuilder::incReserve)
            , py::arg("extra_pt_count")
            )
        .def("offset", &SkPathBuilder::offset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("transform", &SkPathBuilder::transform
            , py::arg("matrix")
            )
        .def("is_finite", &SkPathBuilder::isFinite
            )
        .def("toggle_inverse_fill_type", &SkPathBuilder::toggleInverseFillType
            )
        .def("is_empty", &SkPathBuilder::isEmpty
            )
        .def("get_last_pt", &SkPathBuilder::getLastPt
            )
        .def("set_point", &SkPathBuilder::setPoint
            , py::arg("index")
            , py::arg("p")
            )
        .def("set_last_point", &SkPathBuilder::setLastPoint
            , py::arg("p")
            )
        .def("set_last_pt", py::overload_cast<SkPoint>(&SkPathBuilder::setLastPt)
            , py::arg("pt")
            )
        .def("set_last_pt", py::overload_cast<float, float>(&SkPathBuilder::setLastPt)
            , py::arg("x")
            , py::arg("y")
            )
        .def("count_points", &SkPathBuilder::countPoints
            )
        .def("is_inverse_fill_type", &SkPathBuilder::isInverseFillType
            )
        .def("points", &SkPathBuilder::points
            )
        .def("verbs", &SkPathBuilder::verbs
            )
        .def("conic_weights", &SkPathBuilder::conicWeights
            )
        ;

        py::enum_<SkPathBuilder::Reserve>(_PathBuilder, "Reserve", py::arithmetic())
            .value("K_EXACT", SkPathBuilder::Reserve::kExact)
            .value("K_GROW", SkPathBuilder::Reserve::kGrow)
            .export_values()
        ;
        _PathBuilder
        .def("add_raw", &SkPathBuilder::addRaw
            , py::arg("arg0")
            , py::arg("arg1")
            )
        .def("iter", &SkPathBuilder::iter
            )
        ;

        py::enum_<SkPathBuilder::DumpFormat>(_PathBuilder, "DumpFormat", py::arithmetic())
            .value("K_DECIMAL", SkPathBuilder::DumpFormat::kDecimal)
            .value("K_HEX", SkPathBuilder::DumpFormat::kHex)
            .export_values()
        ;
        _PathBuilder
        .def("dump_to_string", &SkPathBuilder::dumpToString
            , py::arg("arg0") = SkPathBuilder::DumpFormat::kDecimal
            )
        .def("dump", py::overload_cast<SkPathBuilder::DumpFormat>(&SkPathBuilder::dump, py::const_)
            , py::arg("arg0")
            )
        .def("dump", py::overload_cast<>(&SkPathBuilder::dump, py::const_)
            )
        .def("contains", &SkPathBuilder::contains
            , py::arg("arg0")
            )
    ;


}