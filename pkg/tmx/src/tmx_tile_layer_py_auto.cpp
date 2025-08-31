#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/TileLayer.hpp>

namespace py = pybind11;

void init_tmx_tile_layer_py_auto(py::module &_tmx, Registry &registry) {
    py::class_<tmx::TileLayer, tmx::Layer> TileLayer(_tmx, "TileLayer");
    registry.on(_tmx, "TileLayer", TileLayer);
        py::class_<tmx::TileLayer::Tile> TileLayerTile(_tmx, "TileLayerTile");
        registry.on(_tmx, "TileLayerTile", TileLayerTile);
            TileLayerTile
            .def_readwrite("id", &tmx::TileLayer::Tile::ID)
            .def_readwrite("flip_flags", &tmx::TileLayer::Tile::flipFlags)
        ;

        py::class_<tmx::TileLayer::Chunk> TileLayerChunk(_tmx, "TileLayerChunk");
        registry.on(_tmx, "TileLayerChunk", TileLayerChunk);
            TileLayerChunk
            .def_readwrite("position", &tmx::TileLayer::Chunk::position)
            .def_readwrite("size", &tmx::TileLayer::Chunk::size)
            .def_readwrite("tiles", &tmx::TileLayer::Chunk::tiles)
        ;

        py::enum_<tmx::TileLayer::FlipFlag>(TileLayer, "FlipFlag", py::arithmetic())
            .value("HORIZONTAL", tmx::TileLayer::FlipFlag::Horizontal)
            .value("VERTICAL", tmx::TileLayer::FlipFlag::Vertical)
            .value("DIAGONAL", tmx::TileLayer::FlipFlag::Diagonal)
            .export_values()
        ;
        TileLayer
        .def(py::init<unsigned long>()
        , py::arg("")
        )
        .def("get_type", &tmx::TileLayer::getType
            , py::return_value_policy::automatic_reference)
        .def("get_tiles", &tmx::TileLayer::getTiles
            , py::return_value_policy::reference)
        .def("get_chunks", &tmx::TileLayer::getChunks
            , py::return_value_policy::reference)
    ;


}