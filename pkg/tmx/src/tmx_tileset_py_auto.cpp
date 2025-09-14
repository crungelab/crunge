#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/Tileset.hpp>

namespace py = pybind11;

void init_tmx_tileset_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::Tileset> Tileset(_tmx, "Tileset");
    registry.on(_tmx, "Tileset", Tileset);
        Tileset
        .def(py::init<const std::basic_string<char> &>()
        , py::arg("working_dir") = ""
        )
        ;

        py::class_<tmx::Tileset::Tile> TilesetTile(_tmx, "TilesetTile");
        registry.on(_tmx, "TilesetTile", TilesetTile);
            TilesetTile
            .def_readwrite("id", &tmx::Tileset::Tile::ID)
            .def_readwrite("terrain_indices", &tmx::Tileset::Tile::terrainIndices)
            .def_readwrite("probability", &tmx::Tileset::Tile::probability)
            ;

            py::class_<tmx::Tileset::Tile::Animation> TilesetTileAnimation(_tmx, "TilesetTileAnimation");
            registry.on(_tmx, "TilesetTileAnimation", TilesetTileAnimation);
                py::class_<tmx::Tileset::Tile::Animation::Frame> TilesetTileAnimationFrame(_tmx, "TilesetTileAnimationFrame");
                registry.on(_tmx, "TilesetTileAnimationFrame", TilesetTileAnimationFrame);
                    TilesetTileAnimationFrame
                    .def_readwrite("tile_id", &tmx::Tileset::Tile::Animation::Frame::tileID)
                    .def_readwrite("duration", &tmx::Tileset::Tile::Animation::Frame::duration)
                ;

                TilesetTileAnimation
                .def_readwrite("frames", &tmx::Tileset::Tile::Animation::frames)
            ;

            TilesetTile
            .def_readwrite("animation", &tmx::Tileset::Tile::animation)
            .def_readwrite("object_group", &tmx::Tileset::Tile::objectGroup)
            .def_readwrite("image_path", &tmx::Tileset::Tile::imagePath)
            .def_readwrite("image_size", &tmx::Tileset::Tile::imageSize)
            .def_readwrite("image_position", &tmx::Tileset::Tile::imagePosition)
            .def_readwrite("class_name", &tmx::Tileset::Tile::className)
        ;

        py::class_<tmx::Tileset::Terrain> TilesetTerrain(_tmx, "TilesetTerrain");
        registry.on(_tmx, "TilesetTerrain", TilesetTerrain);
            TilesetTerrain
            .def_readwrite("name", &tmx::Tileset::Terrain::name)
            .def_readwrite("tile_id", &tmx::Tileset::Terrain::tileID)
            .def_readwrite("properties", &tmx::Tileset::Terrain::properties)
        ;

        py::enum_<tmx::Tileset::ObjectAlignment>(Tileset, "ObjectAlignment", py::arithmetic())
            .value("UNSPECIFIED", tmx::Tileset::ObjectAlignment::Unspecified)
            .value("TOP_LEFT", tmx::Tileset::ObjectAlignment::TopLeft)
            .value("TOP", tmx::Tileset::ObjectAlignment::Top)
            .value("TOP_RIGHT", tmx::Tileset::ObjectAlignment::TopRight)
            .value("LEFT", tmx::Tileset::ObjectAlignment::Left)
            .value("CENTER", tmx::Tileset::ObjectAlignment::Center)
            .value("RIGHT", tmx::Tileset::ObjectAlignment::Right)
            .value("BOTTOM_LEFT", tmx::Tileset::ObjectAlignment::BottomLeft)
            .value("BOTTOM", tmx::Tileset::ObjectAlignment::Bottom)
            .value("BOTTOM_RIGHT", tmx::Tileset::ObjectAlignment::BottomRight)
            .export_values()
        ;
        Tileset
        .def("load_without_map", &tmx::Tileset::loadWithoutMap
            , py::arg("path")
            , py::return_value_policy::automatic_reference)
        .def("load_without_map_from_string", &tmx::Tileset::loadWithoutMapFromString
            , py::arg("xml_str")
            , py::return_value_policy::automatic_reference)
        .def("get_first_gid", &tmx::Tileset::getFirstGID
            , py::return_value_policy::automatic_reference)
        .def("set_first_gid", &tmx::Tileset::setFirstGID
            , py::arg("first_gid")
            , py::return_value_policy::automatic_reference)
        .def("get_last_gid", &tmx::Tileset::getLastGID
            , py::return_value_policy::automatic_reference)
        .def("get_name", &tmx::Tileset::getName
            , py::return_value_policy::reference)
        .def("get_class", &tmx::Tileset::getClass
            , py::return_value_policy::reference)
        .def("get_tile_size", &tmx::Tileset::getTileSize
            , py::return_value_policy::reference)
        .def("get_spacing", &tmx::Tileset::getSpacing
            , py::return_value_policy::automatic_reference)
        .def("get_margin", &tmx::Tileset::getMargin
            , py::return_value_policy::automatic_reference)
        .def("get_tile_count", &tmx::Tileset::getTileCount
            , py::return_value_policy::automatic_reference)
        .def("get_column_count", &tmx::Tileset::getColumnCount
            , py::return_value_policy::automatic_reference)
        .def("get_object_alignment", &tmx::Tileset::getObjectAlignment
            , py::return_value_policy::automatic_reference)
        .def("get_tile_offset", &tmx::Tileset::getTileOffset
            , py::return_value_policy::reference)
        .def("get_properties", &tmx::Tileset::getProperties
            , py::return_value_policy::reference)
        .def("get_image_path", &tmx::Tileset::getImagePath
            , py::return_value_policy::reference)
        .def("get_image_size", &tmx::Tileset::getImageSize
            , py::return_value_policy::reference)
        .def("get_transparency_colour", &tmx::Tileset::getTransparencyColour
            , py::return_value_policy::reference)
        .def("has_transparency", &tmx::Tileset::hasTransparency
            , py::return_value_policy::automatic_reference)
        .def("get_terrain_types", &tmx::Tileset::getTerrainTypes
            , py::return_value_policy::reference)
        .def("get_tiles", &tmx::Tileset::getTiles
            , py::return_value_policy::reference)
        .def("has_tile", &tmx::Tileset::hasTile
            , py::arg("id")
            , py::return_value_policy::automatic_reference)
        .def("get_tile", &tmx::Tileset::getTile
            , py::arg("id")
            , py::return_value_policy::automatic_reference)
        .def_property_readonly("name", &tmx::Tileset::getName)
        .def_property_readonly("tiles", &tmx::Tileset::getTiles)
    ;


}