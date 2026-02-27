#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>

#include "debug_draw_py.h"

void init_debug_draw_py(py::module &_box2d, Registry &registry) {

    py::class_<PyDebugDrawBase> base(_box2d, "DebugDrawBase");

    //base.def(py::init<>());

    // Ensure instances are initialized against their *Python* self.
    // This is important because Box2D calls the thunks with void* context.
    /*
    base.def("__init__", [](PyDebugDrawBase& self, py::handle pyself) {
        // pybind11 will have already constructed `self` via py::init<>()
        self.initialize(pyself);
    });
    */
    base.def("__init__", [](py::object pyself) {
        auto& self = pyself.cast<PyDebugDrawBase&>();
        new (&self) PyDebugDrawBase();
        self.initialize(pyself);
    });

    // (Optional) expose some flags/scales as properties
    // You can expand this to all flags if you want.
    base.def_property(
        "draw_shapes",
        [](PyDebugDrawBase& self) { return self.ptr()->drawShapes; },
        [](PyDebugDrawBase& self, bool v) { self.ptr()->drawShapes = v; });

    base.def_property(
        "draw_joints",
        [](PyDebugDrawBase& self) { return self.ptr()->drawJoints; },
        [](PyDebugDrawBase& self, bool v) { self.ptr()->drawJoints = v; });

    base.def_property(
        "force_scale",
        [](PyDebugDrawBase& self) { return self.ptr()->forceScale; },
        [](PyDebugDrawBase& self, float v) { self.ptr()->forceScale = v; });

    base.def_property(
        "joint_scale",
        [](PyDebugDrawBase& self) { return self.ptr()->jointScale; },
        [](PyDebugDrawBase& self, float v) { self.ptr()->jointScale = v; });

    // Install __init_subclass__ as a *real* classmethod descriptor.
    // This is the critical change.
    py::object pyBase = py::reinterpret_borrow<py::object>(base.ptr());
    pyBase.attr("__init_subclass__") = classmethod(
        &PyDebugDrawBase::init_subclass,
        //py::arg("cls"),
        py::arg("kwargs") = py::kwargs()
        
    );

    // Also create a default cache on the base itself (so type(self) always has _b2dd_cache,
    // even if someone instantiates DebugDrawBase directly).
    {
        py::gil_scoped_acquire gil;
        PyDebugDrawBase::init_subclass(pyBase, py::kwargs());
    }

    //m.def("world_draw", &world_draw, py::arg("world_id"), py::arg("debug_draw"));
}
