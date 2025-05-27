#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/node/Node.h>
#include "../Node.h"

namespace py = pybind11;

//using namespace facebook::yoga;

void init_yoga_node_py(py::module &_yoga, Registry &registry) {
    PYEXTEND_BEGIN(Node, Node)
    _Node.def(py::init<>(&Node::createDefault));
    //_Node.def(py::init<Config *>(), Node::createWithConfig, py::arg("config"), py::return_value_policy::take_ownership);

    _Node.def("set_style", [](Node& self, facebook::yoga::Style& style) {
        auto node = static_cast<facebook::yoga::Node*>(self.m_node);
        if (!node) {
            throw std::runtime_error("Node is not initialized.");
        }
        //self.m_node->setStyle(style);
        node->setStyle(style);
        self.markDirtyAndPropagate();
    }, py::arg("style"));

    PYEXTEND_END

    /*
    PYEXTEND_BEGIN(Node, Node)
    _Node.def("insert_child", [](Node& self, Node& child, size_t index)
    {
        child.setOwner(&self);
        self.insertChild(&child, index);
        self.markDirtyAndPropagate();
    }, py::arg("child"), py::arg("index"));

    _Node.def("add_child", [](Node& self, Node& child)
    {
        child.setOwner(&self);
        self.insertChild(&child, self.getChildCount());
        self.markDirtyAndPropagate();
    }, py::arg("child"));
    PYEXTEND_END
    */
}