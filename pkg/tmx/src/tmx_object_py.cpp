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
#include <tmxlite/Object.hpp>

namespace py = pybind11;

/*
Boolean,
Float,
Int,
String,
Colour,
File,
Object,
Class,
Undef
*/

static py::object property_to_py(const tmx::Property& p) {
    using t = tmx::Property::Type;
    switch (p.getType()) {
        case t::String:  return py::str(p.getStringValue());
        case t::Float:   return py::float_(p.getFloatValue());
        case t::Int:     return py::int_(p.getIntValue());
        case t::Boolean:    return py::bool_(p.getBoolValue());
        case t::Colour: {
            auto c = p.getColourValue(); // sf::Color-like (r,g,b,a)
            return py::make_tuple(c.r, c.g, c.b, c.a);
        }
        case t::File:    return py::str(p.getFileValue());
        case t::Object:  return py::int_(p.getObjectValue()); // object id reference
        default:         return py::none();
    }
}

void init_tmx_object_py(py::module &_tmx, Registry &registry)
{
    PYEXTEND_BEGIN(tmx::Object, Object)
    _Object.def_property_readonly("name", [](tmx::Object& l){
        return l.getName();
    });

    _Object.def_property_readonly("properties", [](const tmx::Object& L){
        py::dict d;
        for (auto& prop : L.getProperties())
            d[py::str(prop.getName())] = property_to_py(prop);
        return d;
    });

    _Object.def_property_readonly("rotation", [](tmx::Object& l){
        return l.getRotation();
    });

    PYEXTEND_END
}
