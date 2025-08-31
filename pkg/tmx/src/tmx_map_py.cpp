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

void init_tmx_map_py(py::module &_tmx, Registry &registry)
{
    PYEXTEND_BEGIN(tmx::Map, Map)
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

    PYEXTEND_END
}
