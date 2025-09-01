#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Types.hpp>

namespace py = pybind11;

void init_tmx_types_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::Vector2<unsigned>> Vector2_unsigned(_tmx, "Vector2_unsigned");
    registry.on(_tmx, "Vector2_unsigned", Vector2_unsigned);
        Vector2_unsigned
        .def(py::init<>())
        .def(py::init<unsigned, unsigned>()
        , py::arg("x")
        , py::arg("y")
        )
        .def_readwrite("x", &tmx::Vector2<unsigned>::x)
        .def_readwrite("y", &tmx::Vector2<unsigned>::y)
    ;

    py::class_<tmx::Colour> Colour(_tmx, "Colour");
    registry.on(_tmx, "Colour", Colour);
        Colour
        .def(py::init<unsigned char, unsigned char, unsigned char, unsigned char>()
        , py::arg("red") = 0
        , py::arg("green") = 0
        , py::arg("blue") = 0
        , py::arg("alpha") = 255
        )
        .def_readwrite("r", &tmx::Colour::r)
        .def_readwrite("g", &tmx::Colour::g)
        .def_readwrite("b", &tmx::Colour::b)
        .def_readwrite("a", &tmx::Colour::a)
    ;


}