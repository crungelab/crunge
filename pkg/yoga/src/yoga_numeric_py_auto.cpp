#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/numeric/Comparison.h>
#include <yoga/numeric/FloatOptional.h>

namespace py = pybind11;

void init_yoga_numeric_py_auto(py::module &_yoga, Registry &registry) {
    py::class_<facebook::yoga::FloatOptional> FloatOptional(_yoga, "FloatOptional");
    registry.on(_yoga, "FloatOptional", FloatOptional);
        FloatOptional
        .def(py::init<float>()
        , py::arg("value")
        )
        .def(py::init<>())
        .def("unwrap", &facebook::yoga::FloatOptional::unwrap
            , py::return_value_policy::automatic_reference)
        .def("unwrap_or_default", &facebook::yoga::FloatOptional::unwrapOrDefault
            , py::arg("default_value")
            , py::return_value_policy::automatic_reference)
        .def("is_undefined", &facebook::yoga::FloatOptional::isUndefined
            , py::return_value_policy::automatic_reference)
        .def("is_defined", &facebook::yoga::FloatOptional::isDefined
            , py::return_value_policy::automatic_reference)
    ;


}