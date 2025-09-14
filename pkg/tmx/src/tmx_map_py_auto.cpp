#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>

namespace py = pybind11;

void init_tmx_map_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::Version> Version(_tmx, "Version");
    registry.on(_tmx, "Version", Version);
        Version
        .def_readwrite("upper", &tmx::Version::upper)
        .def_readwrite("lower", &tmx::Version::lower)
        .def(py::init<unsigned short, unsigned short>()
        , py::arg("maj") = 0
        , py::arg("min") = 0
        )
    ;

    py::enum_<tmx::Orientation>(_tmx, "Orientation", py::arithmetic())
        .value("ORTHOGONAL", tmx::Orientation::Orthogonal)
        .value("ISOMETRIC", tmx::Orientation::Isometric)
        .value("STAGGERED", tmx::Orientation::Staggered)
        .value("HEXAGONAL", tmx::Orientation::Hexagonal)
        .value("NONE", tmx::Orientation::None)
        .export_values()
    ;
    py::enum_<tmx::RenderOrder>(_tmx, "RenderOrder", py::arithmetic())
        .value("RIGHT_DOWN", tmx::RenderOrder::RightDown)
        .value("RIGHT_UP", tmx::RenderOrder::RightUp)
        .value("LEFT_DOWN", tmx::RenderOrder::LeftDown)
        .value("LEFT_UP", tmx::RenderOrder::LeftUp)
        .value("NONE", tmx::RenderOrder::None)
        .export_values()
    ;
    py::enum_<tmx::StaggerAxis>(_tmx, "StaggerAxis", py::arithmetic())
        .value("X", tmx::StaggerAxis::X)
        .value("Y", tmx::StaggerAxis::Y)
        .value("NONE", tmx::StaggerAxis::None)
        .export_values()
    ;
    py::enum_<tmx::StaggerIndex>(_tmx, "StaggerIndex", py::arithmetic())
        .value("EVEN", tmx::StaggerIndex::Even)
        .value("ODD", tmx::StaggerIndex::Odd)
        .value("NONE", tmx::StaggerIndex::None)
        .export_values()
    ;
    py::class_<tmx::Map> Map(_tmx, "Map");
    registry.on(_tmx, "Map", Map);
        Map
        .def(py::init<>())
        .def("load", &tmx::Map::load
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("load_from_string", &tmx::Map::loadFromString
            , py::arg("data")
            , py::arg("working_dir")
            , py::return_value_policy::automatic_reference)
        .def("get_version", &tmx::Map::getVersion
            , py::return_value_policy::reference)
        .def("get_orientation", &tmx::Map::getOrientation
            , py::return_value_policy::automatic_reference)
        .def("get_render_order", &tmx::Map::getRenderOrder
            , py::return_value_policy::automatic_reference)
        .def("get_tile_count", &tmx::Map::getTileCount
            , py::return_value_policy::reference)
        .def("get_tile_size", &tmx::Map::getTileSize
            , py::return_value_policy::reference)
        .def("get_bounds", &tmx::Map::getBounds
            , py::return_value_policy::automatic_reference)
        .def("get_hex_side_length", &tmx::Map::getHexSideLength
            , py::return_value_policy::automatic_reference)
        .def("get_stagger_axis", &tmx::Map::getStaggerAxis
            , py::return_value_policy::automatic_reference)
        .def("get_stagger_index", &tmx::Map::getStaggerIndex
            , py::return_value_policy::automatic_reference)
        .def("get_background_colour", &tmx::Map::getBackgroundColour
            , py::return_value_policy::reference)
        .def("get_tilesets", &tmx::Map::getTilesets
            , py::return_value_policy::reference)
        .def("get_class", &tmx::Map::getClass
            , py::return_value_policy::reference)
        .def("get_properties", &tmx::Map::getProperties
            , py::return_value_policy::reference)
        .def("get_animated_tiles", &tmx::Map::getAnimatedTiles
            , py::return_value_policy::reference)
        .def("get_working_directory", &tmx::Map::getWorkingDirectory
            , py::return_value_policy::reference)
        .def("get_template_objects", py::overload_cast<>(&tmx::Map::getTemplateObjects)
            , py::return_value_policy::reference)
        .def("get_template_objects", py::overload_cast<>(&tmx::Map::getTemplateObjects, py::const_)
            , py::return_value_policy::reference)
        .def("get_template_tilesets", py::overload_cast<>(&tmx::Map::getTemplateTilesets)
            , py::return_value_policy::reference)
        .def("get_template_tilesets", py::overload_cast<>(&tmx::Map::getTemplateTilesets, py::const_)
            , py::return_value_policy::reference)
        .def("is_infinite", &tmx::Map::isInfinite
            , py::return_value_policy::automatic_reference)
        .def("get_parallax_origin", &tmx::Map::getParallaxOrigin
            , py::return_value_policy::automatic_reference)
        .def_property_readonly("tilesets", &tmx::Map::getTilesets)
        .def_property_readonly("tile_size", &tmx::Map::getTileSize)
        .def_property_readonly("tile_count", &tmx::Map::getTileCount)
    ;


}