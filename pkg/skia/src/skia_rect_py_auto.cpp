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
            )
        .def("top", &SkIRect::top
            )
        .def("right", &SkIRect::right
            )
        .def("bottom", &SkIRect::bottom
            )
        .def("x", &SkIRect::x
            )
        .def("y", &SkIRect::y
            )
        .def("top_left", &SkIRect::topLeft
            )
        .def("width", &SkIRect::width
            )
        .def("height", &SkIRect::height
            )
        .def("size", &SkIRect::size
            )
        .def("width64", &SkIRect::width64
            )
        .def("height64", &SkIRect::height64
            )
        .def("is_empty64", &SkIRect::isEmpty64
            )
        .def("is_empty", &SkIRect::isEmpty
            )
        .def("set_empty", &SkIRect::setEmpty
            )
        .def("set_ltrb", &SkIRect::setLTRB
            , py::arg("left")
            , py::arg("top")
            , py::arg("right")
            , py::arg("bottom")
            )
        .def("set_xywh", &SkIRect::setXYWH
            , py::arg("x")
            , py::arg("y")
            , py::arg("width")
            , py::arg("height")
            )
        .def("set_wh", &SkIRect::setWH
            , py::arg("width")
            , py::arg("height")
            )
        .def("set_size", &SkIRect::setSize
            , py::arg("size")
            )
        .def("make_offset", py::overload_cast<int32_t, int32_t>(&SkIRect::makeOffset, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("make_offset", py::overload_cast<SkIVector>(&SkIRect::makeOffset, py::const_)
            , py::arg("offset")
            )
        .def("make_inset", &SkIRect::makeInset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("make_outset", &SkIRect::makeOutset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("offset", py::overload_cast<int32_t, int32_t>(&SkIRect::offset)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("offset", py::overload_cast<const SkIPoint &>(&SkIRect::offset)
            , py::arg("delta")
            )
        .def("offset_to", &SkIRect::offsetTo
            , py::arg("new_x")
            , py::arg("new_y")
            )
        .def("inset", &SkIRect::inset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("outset", &SkIRect::outset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("adjust", &SkIRect::adjust
            , py::arg("d_l")
            , py::arg("d_t")
            , py::arg("d_r")
            , py::arg("d_b")
            )
        .def("contains", py::overload_cast<int32_t, int32_t>(&SkIRect::contains, py::const_)
            , py::arg("x")
            , py::arg("y")
            )
        .def("contains", py::overload_cast<const SkIRect &>(&SkIRect::contains, py::const_)
            , py::arg("r")
            )
        .def("contains_no_empty_check", &SkIRect::containsNoEmptyCheck
            , py::arg("r")
            )
        .def("intersect", py::overload_cast<const SkIRect &>(&SkIRect::intersect)
            , py::arg("r")
            )
        .def("intersect", py::overload_cast<const SkIRect &, const SkIRect &>(&SkIRect::intersect)
            , py::arg("a")
            , py::arg("b")
            )
        .def("join", &SkIRect::join
            , py::arg("r")
            )
        .def("sort", &SkIRect::sort
            )
        .def("make_sorted", &SkIRect::makeSorted
            )
    ;

    py::class_<SkRect> _Rect(_skia, "Rect");
    registry.on(_skia, "Rect", _Rect);
        _Rect
        .def_readwrite("f_left", &SkRect::fLeft)
        .def_readwrite("f_top", &SkRect::fTop)
        .def_readwrite("f_right", &SkRect::fRight)
        .def_readwrite("f_bottom", &SkRect::fBottom)
        .def("is_empty", &SkRect::isEmpty
            )
        .def("is_sorted", &SkRect::isSorted
            )
        .def("is_finite", &SkRect::isFinite
            )
        .def("x", &SkRect::x
            )
        .def("y", &SkRect::y
            )
        .def("left", &SkRect::left
            )
        .def("top", &SkRect::top
            )
        .def("right", &SkRect::right
            )
        .def("bottom", &SkRect::bottom
            )
        .def("width", &SkRect::width
            )
        .def("height", &SkRect::height
            )
        .def("center_x", &SkRect::centerX
            )
        .def("center_y", &SkRect::centerY
            )
        .def("center", &SkRect::center
            )
        .def("to_quad", [](SkRect& self, std::array<SkPoint, 4>& quad)
            {
                return self.toQuad(&quad[0]);
            }
            , py::arg("quad")
            )
        .def("set_empty", &SkRect::setEmpty
            )
        .def("set", py::overload_cast<const SkIRect &>(&SkRect::set)
            , py::arg("src")
            )
        .def("set_ltrb", &SkRect::setLTRB
            , py::arg("left")
            , py::arg("top")
            , py::arg("right")
            , py::arg("bottom")
            )
        .def("set_bounds", &SkRect::setBounds
            , py::arg("pts")
            , py::arg("count")
            )
        .def("set_bounds_check", &SkRect::setBoundsCheck
            , py::arg("pts")
            , py::arg("count")
            )
        .def("set_bounds_no_check", &SkRect::setBoundsNoCheck
            , py::arg("pts")
            , py::arg("count")
            )
        .def("set", py::overload_cast<const SkPoint &, const SkPoint &>(&SkRect::set)
            , py::arg("p0")
            , py::arg("p1")
            )
        .def("set_xywh", &SkRect::setXYWH
            , py::arg("x")
            , py::arg("y")
            , py::arg("width")
            , py::arg("height")
            )
        .def("set_wh", &SkRect::setWH
            , py::arg("width")
            , py::arg("height")
            )
        .def("set_iwh", &SkRect::setIWH
            , py::arg("width")
            , py::arg("height")
            )
        .def("make_offset", py::overload_cast<float, float>(&SkRect::makeOffset, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("make_offset", py::overload_cast<SkVector>(&SkRect::makeOffset, py::const_)
            , py::arg("v")
            )
        .def("make_inset", &SkRect::makeInset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("make_outset", &SkRect::makeOutset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("offset", py::overload_cast<float, float>(&SkRect::offset)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("offset", py::overload_cast<const SkPoint &>(&SkRect::offset)
            , py::arg("delta")
            )
        .def("offset_to", &SkRect::offsetTo
            , py::arg("new_x")
            , py::arg("new_y")
            )
        .def("inset", &SkRect::inset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("outset", &SkRect::outset
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("intersect", py::overload_cast<const SkRect &>(&SkRect::intersect)
            , py::arg("r")
            )
        .def("intersect", py::overload_cast<const SkRect &, const SkRect &>(&SkRect::intersect)
            , py::arg("a")
            , py::arg("b")
            )
        .def("intersects", &SkRect::intersects
            , py::arg("r")
            )
        .def("join", &SkRect::join
            , py::arg("r")
            )
        .def("join_non_empty_arg", &SkRect::joinNonEmptyArg
            , py::arg("r")
            )
        .def("join_possibly_empty_rect", &SkRect::joinPossiblyEmptyRect
            , py::arg("r")
            )
        .def("contains", py::overload_cast<float, float>(&SkRect::contains, py::const_)
            , py::arg("x")
            , py::arg("y")
            )
        .def("contains", py::overload_cast<const SkRect &>(&SkRect::contains, py::const_)
            , py::arg("r")
            )
        .def("contains", py::overload_cast<const SkIRect &>(&SkRect::contains, py::const_)
            , py::arg("r")
            )
        .def("round", py::overload_cast<SkIRect *>(&SkRect::round, py::const_)
            , py::arg("dst")
            )
        .def("round_out", py::overload_cast<SkIRect *>(&SkRect::roundOut, py::const_)
            , py::arg("dst")
            )
        .def("round_out", py::overload_cast<SkRect *>(&SkRect::roundOut, py::const_)
            , py::arg("dst")
            )
        .def("round_in", py::overload_cast<SkIRect *>(&SkRect::roundIn, py::const_)
            , py::arg("dst")
            )
        .def("round", py::overload_cast<>(&SkRect::round, py::const_)
            )
        .def("round_out", py::overload_cast<>(&SkRect::roundOut, py::const_)
            )
        .def("round_in", py::overload_cast<>(&SkRect::roundIn, py::const_)
            )
        .def("sort", &SkRect::sort
            )
        .def("make_sorted", &SkRect::makeSorted
            )
        .def("as_scalars", &SkRect::asScalars
            )
        .def("dump", py::overload_cast<bool>(&SkRect::dump, py::const_)
            , py::arg("as_hex")
            )
        .def("dump_to_string", &SkRect::dumpToString
            , py::arg("as_hex")
            )
        .def("dump", py::overload_cast<>(&SkRect::dump, py::const_)
            )
        .def("dump_hex", &SkRect::dumpHex
            )
    ;


}