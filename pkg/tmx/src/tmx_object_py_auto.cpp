#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/Object.hpp>

namespace py = pybind11;

void init_tmx_object_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::Text> _Text(_tmx, "Text");
    registry.on(_tmx, "Text", _Text);
        _Text
        .def_readwrite("font_family", &tmx::Text::fontFamily)
        .def_readwrite("pixel_size", &tmx::Text::pixelSize)
        .def_readwrite("wrap", &tmx::Text::wrap)
        .def_readwrite("colour", &tmx::Text::colour)
        .def_readwrite("bold", &tmx::Text::bold)
        .def_readwrite("italic", &tmx::Text::italic)
        .def_readwrite("underline", &tmx::Text::underline)
        .def_readwrite("strikethough", &tmx::Text::strikethough)
        .def_readwrite("kerning", &tmx::Text::kerning)
        ;

        py::enum_<tmx::Text::HAlign>(_Text, "HAlign", py::arithmetic())
            .value("LEFT", tmx::Text::HAlign::Left)
            .value("CENTRE", tmx::Text::HAlign::Centre)
            .value("RIGHT", tmx::Text::HAlign::Right)
            .export_values()
        ;
        _Text
        .def_readwrite("h_align", &tmx::Text::hAlign)
        ;

        py::enum_<tmx::Text::VAlign>(_Text, "VAlign", py::arithmetic())
            .value("TOP", tmx::Text::VAlign::Top)
            .value("CENTRE", tmx::Text::VAlign::Centre)
            .value("BOTTOM", tmx::Text::VAlign::Bottom)
            .export_values()
        ;
        _Text
        .def_readwrite("v_align", &tmx::Text::vAlign)
        .def_readwrite("content", &tmx::Text::content)
    ;

    py::class_<tmx::Object> _Object(_tmx, "Object");
    registry.on(_tmx, "Object", _Object);
        py::enum_<tmx::Object::Shape>(_Object, "Shape", py::arithmetic())
            .value("RECTANGLE", tmx::Object::Shape::Rectangle)
            .value("ELLIPSE", tmx::Object::Shape::Ellipse)
            .value("POINT", tmx::Object::Shape::Point)
            .value("POLYGON", tmx::Object::Shape::Polygon)
            .value("POLYLINE", tmx::Object::Shape::Polyline)
            .value("TEXT", tmx::Object::Shape::Text)
            .export_values()
        ;
        _Object
        .def(py::init<>())
        .def("get_uid", &tmx::Object::getUID
            )
        .def("get_name", &tmx::Object::getName
            )
        .def("get_type", &tmx::Object::getType
            )
        .def("get_class", &tmx::Object::getClass
            )
        .def("get_position", &tmx::Object::getPosition
            )
        .def("get_aabb", &tmx::Object::getAABB
            )
        .def("get_rotation", &tmx::Object::getRotation
            )
        .def("get_tile_id", &tmx::Object::getTileID
            )
        .def("get_flip_flags", &tmx::Object::getFlipFlags
            )
        .def("visible", &tmx::Object::visible
            )
        .def("get_shape", &tmx::Object::getShape
            )
        .def("get_points", &tmx::Object::getPoints
            )
        .def("get_properties", &tmx::Object::getProperties
            )
        .def("get_text", py::overload_cast<>(&tmx::Object::getText, py::const_)
            )
        .def("get_text", py::overload_cast<>(&tmx::Object::getText)
            )
        .def("get_tileset_name", &tmx::Object::getTilesetName
            )
        .def_property_readonly("name", &tmx::Object::getName)
        .def_property_readonly("rotation", &tmx::Object::getRotation)
    ;


}