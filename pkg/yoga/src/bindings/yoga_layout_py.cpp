#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/node/Node.h>
#include "../Layout.h"

namespace py = pybind11;

//using namespace facebook::yoga;

void init_yoga_layout_py(py::module &_yoga, Registry &registry) {
    PYEXTEND_BEGIN(Layout, Layout)
    _Layout.def(py::init<>(&Layout::createDefault));
    //_Layout.def(py::init<Config *>(), Layout::createWithConfig, py::arg("config"), py::return_value_policy::take_ownership);

    _Layout.def("set_style", [](Layout& self, facebook::yoga::Style& style) {
        auto node = static_cast<facebook::yoga::Node*>(self.m_node);
        if (!node) {
            throw std::runtime_error("Layout is not initialized.");
        }
        //self.m_node->setStyle(style);
        node->setStyle(style);
        node->markDirtyAndPropagate();
    }, py::arg("style"));

    PYEXTEND_END

    /*
    PYEXTEND_BEGIN(Layout, Layout)
    _Layout.def("insert_child", [](Layout& self, Layout& child, size_t index)
    {
        child.setOwner(&self);
        self.insertChild(&child, index);
        self.markDirtyAndPropagate();
    }, py::arg("child"), py::arg("index"));

    _Layout.def("add_child", [](Layout& self, Layout& child)
    {
        child.setOwner(&self);
        self.insertChild(&child, self.getChildCount());
        self.markDirtyAndPropagate();
    }, py::arg("child"));
    PYEXTEND_END
    */
}