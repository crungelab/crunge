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
    py::class_<tmx::Vector2<unsigned>> _Vector2u(_tmx, "Vector2u");
    registry.on(_tmx, "Vector2u", _Vector2u);
        _Vector2u
        .def(py::init<>())
        .def(py::init<unsigned, unsigned>()
        , py::arg("x")
        , py::arg("y")
        )
        .def_readwrite("x", &tmx::Vector2<unsigned>::x)
        .def_readwrite("y", &tmx::Vector2<unsigned>::y)
    ;

    py::class_<tmx::Vector2<float>> _Vector2f(_tmx, "Vector2f");
    registry.on(_tmx, "Vector2f", _Vector2f);
        _Vector2f
        .def(py::init<>())
        .def(py::init<float, float>()
        , py::arg("x")
        , py::arg("y")
        )
        .def_readwrite("x", &tmx::Vector2<float>::x)
        .def_readwrite("y", &tmx::Vector2<float>::y)
    ;

    py::class_<tmx::Rectangle<float>> _FloatRect(_tmx, "FloatRect");
    registry.on(_tmx, "FloatRect", _FloatRect);
        _FloatRect
        .def(py::init<>())
        .def(py::init<float, float, float, float>()
        , py::arg("l")
        , py::arg("t")
        , py::arg("w")
        , py::arg("h")
        )
        .def(py::init<tmx::Vector2<float>, tmx::Vector2<float>>()
        , py::arg("position")
        , py::arg("size")
        )
        .def_readwrite("left", &tmx::Rectangle<float>::left)
        .def_readwrite("top", &tmx::Rectangle<float>::top)
        .def_readwrite("width", &tmx::Rectangle<float>::width)
        .def_readwrite("height", &tmx::Rectangle<float>::height)
    ;

    py::class_<tmx::Rectangle<int>> _IntRect(_tmx, "IntRect");
    registry.on(_tmx, "IntRect", _IntRect);
        _IntRect
        .def(py::init<>())
        .def(py::init<int, int, int, int>()
        , py::arg("l")
        , py::arg("t")
        , py::arg("w")
        , py::arg("h")
        )
        .def(py::init<tmx::Vector2<int>, tmx::Vector2<int>>()
        , py::arg("position")
        , py::arg("size")
        )
        .def_readwrite("left", &tmx::Rectangle<int>::left)
        .def_readwrite("top", &tmx::Rectangle<int>::top)
        .def_readwrite("width", &tmx::Rectangle<int>::width)
        .def_readwrite("height", &tmx::Rectangle<int>::height)
    ;

    py::class_<tmx::Colour> _Colour(_tmx, "Colour");
    registry.on(_tmx, "Colour", _Colour);
        _Colour
        .def(py::init<uint8_t, uint8_t, uint8_t, uint8_t>()
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