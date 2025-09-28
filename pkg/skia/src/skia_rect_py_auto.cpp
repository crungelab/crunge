#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkRect.h>
#include <include/core/SkString.h>

namespace py = pybind11;

void init_skia_rect_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkIRect> _IRect(_skia, "IRect");
    registry.on(_skia, "IRect", _IRect);
        _IRect
        .def_readwrite("f_left", &SkIRect::fLeft)
        .def_readwrite("f_top", &SkIRect::fTop)
        .def_readwrite("f_right", &SkIRect::fRight)
        .def_readwrite("f_bottom", &SkIRect::fBottom)
        .def("left", &SkIRect::left
            , py::return_value_policy::automatic_reference)
        .def("top", &SkIRect::top
            , py::return_value_policy::automatic_reference)
        .def("right", &SkIRect::right
            , py::return_value_policy::automatic_reference)
        .def("bottom", &SkIRect::bottom
            , py::return_value_policy::automatic_reference)
        .def("x", &SkIRect::x
            , py::return_value_policy::automatic_reference)
        .def("y", &SkIRect::y
            , py::return_value_policy::automatic_reference)
        .def("top_left", &SkIRect::topLeft
            , py::return_value_policy::automatic_reference)
        .def("width", &SkIRect::width
            , py::return_value_policy::automatic_reference)
        .def("height", &SkIRect::height
            , py::return_value_policy::automatic_reference)
        .def("size", &SkIRect::size
            , py::return_value_policy::automatic_reference)
        .def("width64", &SkIRect::width64
            , py::return_value_policy::automatic_reference)
        .def("height64", &SkIRect::height64
            , py::return_value_policy::automatic_reference)
        .def("is_empty64", &SkIRect::isEmpty64
            , py::return_value_policy::automatic_reference)
        .def("is_empty", &SkIRect::isEmpty
            , py::return_value_policy::automatic_reference)
        .def("set_empty", &SkIRect::setEmpty
            , py::return_value_policy::automatic_reference)
        .def("set_ltrb", &SkIRect::setLTRB
            , py::arg("left")
            , py::arg("top")
            , py::arg("right")
            , py::arg("bottom")
            , py::return_value_policy::automatic_reference)
        .def("set_xywh", &SkIRect::setXYWH
            , py::arg("x")
            , py::arg("y")
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def("set_wh", &SkIRect::setWH
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def("set_size", &SkIRect::setSize
            , py::arg("size")
            , py::return_value_policy::automatic_reference)
        .def("make_offset", py::overload_cast<int, int>(&SkIRect::makeOffset, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("make_offset", py::overload_cast<SkIPoint>(&SkIRect::makeOffset, py::const_)
            , py::arg("offset")
            , py::return_value_policy::automatic_reference)
        .def("make_inset", &SkIRect::makeInset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("make_outset", &SkIRect::makeOutset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("offset", py::overload_cast<int, int>(&SkIRect::offset)
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("offset", py::overload_cast<const SkIPoint &>(&SkIRect::offset)
            , py::arg("delta")
            , py::return_value_policy::automatic_reference)
        .def("offset_to", &SkIRect::offsetTo
            , py::arg("new_x")
            , py::arg("new_y")
            , py::return_value_policy::automatic_reference)
        .def("inset", &SkIRect::inset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("outset", &SkIRect::outset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("adjust", &SkIRect::adjust
            , py::arg("d_l")
            , py::arg("d_t")
            , py::arg("d_r")
            , py::arg("d_b")
            , py::return_value_policy::automatic_reference)
        .def("contains", py::overload_cast<int, int>(&SkIRect::contains, py::const_)
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("contains", py::overload_cast<const SkIRect &>(&SkIRect::contains, py::const_)
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("contains_no_empty_check", &SkIRect::containsNoEmptyCheck
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("intersect", py::overload_cast<const SkIRect &>(&SkIRect::intersect)
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("intersect", py::overload_cast<const SkIRect &, const SkIRect &>(&SkIRect::intersect)
            , py::arg("a")
            , py::arg("b")
            , py::return_value_policy::automatic_reference)
        .def("join", &SkIRect::join
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("sort", &SkIRect::sort
            , py::return_value_policy::automatic_reference)
        .def("make_sorted", &SkIRect::makeSorted
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<SkRect> _Rect(_skia, "Rect");
    registry.on(_skia, "Rect", _Rect);
        _Rect
        .def_readwrite("f_left", &SkRect::fLeft)
        .def_readwrite("f_top", &SkRect::fTop)
        .def_readwrite("f_right", &SkRect::fRight)
        .def_readwrite("f_bottom", &SkRect::fBottom)
        .def("is_empty", &SkRect::isEmpty
            , py::return_value_policy::automatic_reference)
        .def("is_sorted", &SkRect::isSorted
            , py::return_value_policy::automatic_reference)
        .def("is_finite", &SkRect::isFinite
            , py::return_value_policy::automatic_reference)
        .def("x", &SkRect::x
            , py::return_value_policy::automatic_reference)
        .def("y", &SkRect::y
            , py::return_value_policy::automatic_reference)
        .def("left", &SkRect::left
            , py::return_value_policy::automatic_reference)
        .def("top", &SkRect::top
            , py::return_value_policy::automatic_reference)
        .def("right", &SkRect::right
            , py::return_value_policy::automatic_reference)
        .def("bottom", &SkRect::bottom
            , py::return_value_policy::automatic_reference)
        .def("width", &SkRect::width
            , py::return_value_policy::automatic_reference)
        .def("height", &SkRect::height
            , py::return_value_policy::automatic_reference)
        .def("center_x", &SkRect::centerX
            , py::return_value_policy::automatic_reference)
        .def("center_y", &SkRect::centerY
            , py::return_value_policy::automatic_reference)
        .def("center", &SkRect::center
            , py::return_value_policy::automatic_reference)
        .def("to_quad", [](SkRect& self, std::array<SkPoint, 4>& quad)
            {
                self.toQuad(&quad[0]);
                return quad;
            }
            , py::arg("quad")
            , py::return_value_policy::automatic_reference)
        .def("set_empty", &SkRect::setEmpty
            , py::return_value_policy::automatic_reference)
        .def("set", py::overload_cast<const SkIRect &>(&SkRect::set)
            , py::arg("src")
            , py::return_value_policy::automatic_reference)
        .def("set_ltrb", &SkRect::setLTRB
            , py::arg("left")
            , py::arg("top")
            , py::arg("right")
            , py::arg("bottom")
            , py::return_value_policy::automatic_reference)
        .def("set_bounds", &SkRect::setBounds
            , py::arg("pts")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("set_bounds_check", &SkRect::setBoundsCheck
            , py::arg("pts")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("set_bounds_no_check", &SkRect::setBoundsNoCheck
            , py::arg("pts")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("set", py::overload_cast<const SkPoint &, const SkPoint &>(&SkRect::set)
            , py::arg("p0")
            , py::arg("p1")
            , py::return_value_policy::automatic_reference)
        .def("set_xywh", &SkRect::setXYWH
            , py::arg("x")
            , py::arg("y")
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def("set_wh", &SkRect::setWH
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def("set_iwh", &SkRect::setIWH
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def("make_offset", py::overload_cast<float, float>(&SkRect::makeOffset, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("make_offset", py::overload_cast<SkPoint>(&SkRect::makeOffset, py::const_)
            , py::arg("v")
            , py::return_value_policy::automatic_reference)
        .def("make_inset", &SkRect::makeInset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("make_outset", &SkRect::makeOutset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("offset", py::overload_cast<float, float>(&SkRect::offset)
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("offset", py::overload_cast<const SkPoint &>(&SkRect::offset)
            , py::arg("delta")
            , py::return_value_policy::automatic_reference)
        .def("offset_to", &SkRect::offsetTo
            , py::arg("new_x")
            , py::arg("new_y")
            , py::return_value_policy::automatic_reference)
        .def("inset", &SkRect::inset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("outset", &SkRect::outset
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("intersect", py::overload_cast<const SkRect &>(&SkRect::intersect)
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("intersect", py::overload_cast<const SkRect &, const SkRect &>(&SkRect::intersect)
            , py::arg("a")
            , py::arg("b")
            , py::return_value_policy::automatic_reference)
        .def("intersects", &SkRect::intersects
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("join", &SkRect::join
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("join_non_empty_arg", &SkRect::joinNonEmptyArg
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("join_possibly_empty_rect", &SkRect::joinPossiblyEmptyRect
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("contains", py::overload_cast<float, float>(&SkRect::contains, py::const_)
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("contains", py::overload_cast<const SkRect &>(&SkRect::contains, py::const_)
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("contains", py::overload_cast<const SkIRect &>(&SkRect::contains, py::const_)
            , py::arg("r")
            , py::return_value_policy::automatic_reference)
        .def("round", py::overload_cast<SkIRect *>(&SkRect::round, py::const_)
            , py::arg("dst")
            , py::return_value_policy::automatic_reference)
        .def("round_out", py::overload_cast<SkIRect *>(&SkRect::roundOut, py::const_)
            , py::arg("dst")
            , py::return_value_policy::automatic_reference)
        .def("round_out", py::overload_cast<SkRect *>(&SkRect::roundOut, py::const_)
            , py::arg("dst")
            , py::return_value_policy::automatic_reference)
        .def("round_in", py::overload_cast<SkIRect *>(&SkRect::roundIn, py::const_)
            , py::arg("dst")
            , py::return_value_policy::automatic_reference)
        .def("round", py::overload_cast<>(&SkRect::round, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("round_out", py::overload_cast<>(&SkRect::roundOut, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("round_in", py::overload_cast<>(&SkRect::roundIn, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("sort", &SkRect::sort
            , py::return_value_policy::automatic_reference)
        .def("make_sorted", &SkRect::makeSorted
            , py::return_value_policy::automatic_reference)
        .def("as_scalars", &SkRect::asScalars
            , py::return_value_policy::automatic_reference)
        .def("dump", py::overload_cast<bool>(&SkRect::dump, py::const_)
            , py::arg("as_hex")
            , py::return_value_policy::automatic_reference)
        .def("dump_to_string", &SkRect::dumpToString
            , py::arg("as_hex")
            , py::return_value_policy::automatic_reference)
        .def("dump", py::overload_cast<>(&SkRect::dump, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("dump_hex", &SkRect::dumpHex
            , py::return_value_policy::automatic_reference)
    ;


}