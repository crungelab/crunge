#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkColor.h>

namespace py = pybind11;

void init_skia_color_py(py::module &_skia, Registry &registry) {
    py::class_<SkColor4f>(_skia, "Color4f")
    .def(py::init<float, float, float, float>())
    .def_readwrite("r", &SkColor4f::fR)
    .def_readwrite("g", &SkColor4f::fG)
    .def_readwrite("b", &SkColor4f::fB)
    .def_readwrite("a", &SkColor4f::fA)
    .def("__repr__", [](const SkColor4f &c) {
        return "<Color4f r=" + std::to_string(c.fR) +
               " g=" + std::to_string(c.fG) +
               " b=" + std::to_string(c.fB) +
               " a=" + std::to_string(c.fA) + ">";
    });

    py::module colors = _skia.def_submodule("colors", "SkColor constants");
    colors.attr("TRANSPARENT") = SK_ColorTRANSPARENT;
    colors.attr("BLACK") = SK_ColorBLACK;
    colors.attr("DKGRAY") = SK_ColorDKGRAY;
    colors.attr("GRAY") = SK_ColorGRAY;
    colors.attr("LTGRAY") = SK_ColorLTGRAY;
    colors.attr("WHITE") = SK_ColorWHITE;
    colors.attr("RED") = SK_ColorRED;
    colors.attr("GREEN") = SK_ColorGREEN;
    colors.attr("BLUE") = SK_ColorBLUE;
    colors.attr("YELLOW") = SK_ColorYELLOW;
    colors.attr("CYAN") = SK_ColorCYAN;
    colors.attr("MAGENTA") = SK_ColorMAGENTA;
    
    py::module colors4f = _skia.def_submodule("colors4f", "SkColor4f constants");
    colors4f.attr("TRANSPARENT") = SkColors::kTransparent;
    colors4f.attr("BLACK") = SkColors::kBlack;
    colors4f.attr("DKGRAY") = SkColors::kDkGray;
    colors4f.attr("GRAY") = SkColors::kGray;
    colors4f.attr("LTGRAY") = SkColors::kLtGray;
    colors4f.attr("WHITE") = SkColors::kWhite;
    colors4f.attr("RED") = SkColors::kRed;
    colors4f.attr("GREEN") = SkColors::kGreen;
    colors4f.attr("BLUE") = SkColors::kBlue;
    colors4f.attr("YELLOW") = SkColors::kYellow;
    colors4f.attr("CYAN") = SkColors::kCyan;
    colors4f.attr("MAGENTA") = SkColors::kMagenta;
}
