#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/TileLayer.hpp>
#include <tmxlite/ObjectGroup.hpp>
#include <tmxlite/ImageLayer.hpp>

namespace py = pybind11;

static const tmx::Tileset* find_tileset_for_gid(const std::vector<tmx::Tileset>& sets, std::uint32_t gid) {
    if (gid == 0) return nullptr; // empty tile
    for (const auto& ts : sets) {
        if (ts.getTileCount() == 0) continue;
        if (ts.hasTile(gid)) {
            return &ts;
        }
    }
    return nullptr; // may be null if gid < min firstGID
}

/*
static const tmx::Tileset* find_tileset_for_gid(const std::vector<tmx::Tileset>& sets, std::uint32_t gid) {
    if (gid == 0) return nullptr; // empty tile
    const tmx::Tileset* match = nullptr;
    for (const auto& ts : sets) {
        if (gid >= ts.getFirstGID()) {
            if (!match || ts.getFirstGID() > match->getFirstGID())
                match = &ts;
        }
    }
    return match; // may be null if gid < min firstGID
}
*/

void init_tmx_map_py(py::module &_tmx, Registry &registry)
{
    PYEXTEND_BEGIN(tmx::Map, Map)
    _Map.def_property_readonly("tilesets", [](tmx::Map& m){
        return m.getTilesets();
    });

    _Map.def_property_readonly("tile_size", [](tmx::Map& m){
        return m.getTileSize();
    });

    _Map.def_property_readonly("tile_count", [](tmx::Map& m){
        return m.getTileCount();
    });

    _Map.def_property_readonly("max_gid", [](tmx::Map& m){
        std::uint32_t max_gid = 0;
        for (auto& ts : m.getTilesets()) {
            if (ts.getTileCount() == 0) continue;
            auto ts_max_gid = ts.getLastGID();
            max_gid = std::max(max_gid, ts_max_gid);
        }
        return max_gid;
    });

    _Map.def_property_readonly("layers", [](tmx::Map& m){
        // Return a Python list of typed layers with correct dynamic cast
        py::list lst;
        for (auto& up : m.getLayers()) {
            auto* base = up.get();
            switch (base->getType()) {
                case tmx::Layer::Type::Tile:
                    lst.append(dynamic_cast<tmx::TileLayer*>(base));
                    break;
                case tmx::Layer::Type::Object:
                    lst.append(dynamic_cast<tmx::ObjectGroup*>(base));
                    break;
                case tmx::Layer::Type::Image:
                    lst.append(dynamic_cast<tmx::ImageLayer*>(base));
                    break;
                default:
                    lst.append(base); // falls back to Layer
            }
        }
        return lst;
    }, py::return_value_policy::reference_internal);

    /*
    _Map.def_property_readonly("layers", [](tmx::Map& m){
        py::list lst;
        for (auto& up : m.getLayers()) {
            tmx::Layer* base = up.get();
            if (auto tl = dynamic_cast<tmx::TileLayer*>(base)) {
                lst.append(py::cast(tl, py::return_value_policy::reference_internal));
            } else if (auto og = dynamic_cast<tmx::ObjectGroup*>(base)) {
                lst.append(py::cast(og, py::return_value_policy::reference_internal));
            } else if (auto il = dynamic_cast<tmx::ImageLayer*>(base)) {
                lst.append(py::cast(il, py::return_value_policy::reference_internal));
            } else {
                lst.append(py::cast(base, py::return_value_policy::reference_internal));
            }
        }
        return lst;
    });
    */

    /*
    _Map.def_property_readonly("layers", [](tmx::Map& m){
        // Return a Python list of typed layers with correct dynamic cast
        py::list lst;
        for (auto& up : m.getLayers()) {
            auto* base = up.get();
            lst.append(py::cast(base)); // falls back to Layer
        }
        return lst;
    });
    */

    /*
    _Map.def_property_readonly("layers", [](tmx::Map& m){
        // Return a Python list of typed layers with correct dynamic cast
        py::list lst;
        for (auto& up : m.getLayers()) {
            auto* base = up.get();
            switch (base->getType()) {
                case tmx::Layer::Type::Tile:
                    lst.append(static_cast<tmx::TileLayer*>(base));
                    break;
                case tmx::Layer::Type::Object:
                    lst.append(static_cast<tmx::ObjectGroup*>(base));
                    break;
                case tmx::Layer::Type::Image:
                    lst.append(static_cast<tmx::ImageLayer*>(base));
                    break;
                default:
                    lst.append(base); // falls back to Layer
            }
        }
        return lst;
    }, py::return_value_policy::reference_internal)
    */
    _Map.def("get_tile", [](tmx::Map& m, std::uint32_t gid) {
        const tmx::Tileset* tileset = find_tileset_for_gid(m.getTilesets(), gid);
        if (!tileset) return py::object(py::none());
        std::cout << "Found tileset: " << tileset->getName() << std::endl;

        // Get the tile from the tileset
        //auto id = gid - tileset->getFirstGID() + 1;
        //const tmx::Tileset::Tile* tile = tileset->getTile(id);
        const tmx::Tileset::Tile* tile = tileset->getTile(gid);
        //return tile ? py::cast(tile) : py::object(py::none());
        return py::cast(tile);
    });

    PYEXTEND_END
}
