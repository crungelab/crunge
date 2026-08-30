#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>

#include "debug_draw_py.h"

void init_debug_draw_py(py::module &_box2d, Registry &registry) {
    (void)registry;

    py::class_<PyDebugDrawBase> base(_box2d, "DebugDrawBase");

    // Plain default construction. The old two-step __init__ existed only to capture
    // the Python `self` into the C++ context; `self` is now bound for the duration
    // of world_draw() instead, so there is nothing left to initialize here.
    base.def(py::init<>());

// b2DebugDraw option flags. Note these are the *what to emit* switches, distinct
// from the draw_*() callbacks a subclass overrides.
#define B2DD_FLAG(pyname, field)                                                \
    base.def_property(                                                          \
        pyname, [](PyDebugDrawBase &self) { return self.ptr()->field; },        \
        [](PyDebugDrawBase &self, bool v) { self.ptr()->field = v; })

    B2DD_FLAG("draw_shapes", drawShapes);
    B2DD_FLAG("draw_joints", drawJoints);
    B2DD_FLAG("draw_joint_extras", drawJointExtras);
    B2DD_FLAG("draw_contacts", drawContacts);
    B2DD_FLAG("draw_anchor_a", drawAnchorA);
    B2DD_FLAG("draw_chain_normals", drawChainNormals);
    // NOTE: b2DebugDraw::drawBounds would collide with the draw_bounds() callback
    // a subclass overrides, so the flag is exposed under its meaning instead.
    B2DD_FLAG("draw_shape_bounds", drawBounds);
    B2DD_FLAG("draw_mass", drawMass);
    B2DD_FLAG("draw_body_names", drawBodyNames);
    B2DD_FLAG("draw_graph_colors", drawGraphColors);
    B2DD_FLAG("draw_contact_features", drawContactFeatures);
    B2DD_FLAG("draw_contact_normals", drawContactNormals);
    B2DD_FLAG("draw_contact_forces", drawContactForces);
    B2DD_FLAG("draw_friction_forces", drawFrictionForces);
    B2DD_FLAG("draw_islands", drawIslands);

#undef B2DD_FLAG

    base.def_property(
        "force_scale",
        [](PyDebugDrawBase &self) { return self.ptr()->forceScale; },
        [](PyDebugDrawBase &self, float v) { self.ptr()->forceScale = v; });

    base.def_property(
        "joint_scale",
        [](PyDebugDrawBase &self) { return self.ptr()->jointScale; },
        [](PyDebugDrawBase &self, float v) { self.ptr()->jointScale = v; });

    base.def_property(
        "drawing_bounds",
        [](PyDebugDrawBase &self) { return to_py(self.ptr()->drawingBounds); },
        [](PyDebugDrawBase &self, py::sequence bounds) {
            if (py::len(bounds) != 2) {
                throw_type_error(
                    "drawing_bounds expects ((lower_x, lower_y), (upper_x, upper_y))");
            }
            auto lower = bounds[0].cast<std::pair<float, float>>();
            auto upper = bounds[1].cast<std::pair<float, float>>();
            self.ptr()->drawingBounds.lowerBound = b2Vec2{lower.first, lower.second};
            self.ptr()->drawingBounds.upperBound = b2Vec2{upper.first, upper.second};
        });

    base.def_static(
        "refresh_cache", &PyDebugDrawBase::refresh_cache, py::arg("cls"),
        "Rebuild the cached method table for a class after patching a draw method onto it.");

    // Install __init_subclass__ as a *real* classmethod descriptor. Python binds the
    // new subclass as the first argument, so no py::arg annotations here.
    py::object pyBase = py::reinterpret_borrow<py::object>(base.ptr());
    pyBase.attr("__init_subclass__") = classmethod(&PyDebugDrawBase::init_subclass);

    // Give the base itself a cache so instantiating DebugDrawBase directly works.
    // We are inside module init and already hold the GIL, so no acquire is needed.
    build_debug_draw_cache(pyBase);

    // Wrapper around b2World_Draw that binds the Python instance for the call and
    // rethrows any exception a callback raised.
    _box2d.def("world_draw", &world_draw, py::arg("world_id"), py::arg("debug_draw"));

    // Lets Python tell whether positions arrive as doubles (large world mode).
    _box2d.def("is_double_precision", &b2IsDoublePrecision);
}