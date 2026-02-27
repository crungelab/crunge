// debug_draw_py.cpp
//
// Complete pybind11 implementation of Box2D v3-style b2DebugDraw bridging to Python,
// using per-SUBCLASS caching via __init_subclass__ installed as a real classmethod
// (via PyClassMethod_New).
//
// Python usage:
//
//   import box2d
//
//   class DebugDraw(box2d.DebugDrawBase):
//       def draw_line(self, p1, p2, color): ...
//       def draw_polygon(self, vertices, color): ...
//
//   dbg = DebugDraw()
//   box2d.world_draw(world_id, dbg)
//
// Notes:
// - This file uses placeholder Box2D types for illustration. Replace those with real headers.
// - We cache *unbound* functions on the subclass. Thunks call fn(self, ...).
// - Exceptions inside callbacks are caught; they will not unwind through C callbacks.
//

#include <cstdint>
#include <memory>
#include <string>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <box2d/types.h>

namespace py = pybind11;

/*
// -----------------------------------------------------------------------------
// Replace these placeholders with your real Box2D includes/types.
// -----------------------------------------------------------------------------
struct b2Vec2 { float x, y; };
struct b2Rot { float c, s; };
struct b2Transform { b2Vec2 p; b2Rot q; };
using b2HexColor = uint32_t;
struct b2AABB { b2Vec2 lowerBound, upperBound; };

// Example world id placeholder
struct b2WorldId { uint32_t index; };

// Your real function:
//   B2_API void b2World_Draw(b2WorldId worldId, b2DebugDraw* draw);
extern "C" void b2World_Draw(b2WorldId worldId, struct b2DebugDraw* draw);

typedef struct b2DebugDraw
{
    void (*DrawPolygonFcn)(const b2Vec2* vertices, int vertexCount, b2HexColor color, void* context);
    void (*DrawSolidPolygonFcn)(b2Transform transform, const b2Vec2* vertices, int vertexCount, float radius, b2HexColor color, void* context);
    void (*DrawCircleFcn)(b2Vec2 center, float radius, b2HexColor color, void* context);
    void (*DrawSolidCircleFcn)(b2Transform transform, float radius, b2HexColor color, void* context);
    void (*DrawSolidCapsuleFcn)(b2Vec2 p1, b2Vec2 p2, float radius, b2HexColor color, void* context);
    void (*DrawLineFcn)(b2Vec2 p1, b2Vec2 p2, b2HexColor color, void* context);
    void (*DrawTransformFcn)(b2Transform transform, void* context);
    void (*DrawPointFcn)(b2Vec2 p, float size, b2HexColor color, void* context);
    void (*DrawStringFcn)(b2Vec2 p, const char* s, b2HexColor color, void* context);

    b2AABB drawingBounds;
    float forceScale;
    float jointScale;

    bool drawShapes;
    bool drawJoints;
    bool drawJointExtras;
    bool drawBounds;
    bool drawMass;
    bool drawBodyNames;
    bool drawContactPoints;
    bool drawGraphColors;
    bool drawContactFeatures;
    bool drawContactNormals;
    bool drawContactForces;
    bool drawFrictionForces;
    bool drawIslands;

    void* context;
} b2DebugDraw;
*/

// -----------------------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------------------

static inline py::tuple to_py(b2Vec2 v) {
    return py::make_tuple(v.x, v.y);
}

// Represent transform as (px, py, c, s) to match typical Box2D b2Rot storage.
// Adjust if your bindings expose transform differently.
static inline py::tuple to_py(b2Transform t) {
    //return py::make_tuple(t.p.x, t.p.y, t.q.c, t.q.s);
    auto angle = b2Rot_GetAngle(t.q);
    return py::make_tuple(t.p.x, t.p.y, angle);
}

static inline py::list verts_to_py(const b2Vec2* v, int n) {
    py::list out;
    for (int i = 0; i < n; ++i) out.append(to_py(v[i]));
    return out;
}

// Install a real Python "classmethod" descriptor for a C++ function.
template <class Func, class... Extra>
py::object classmethod(Func&& f, Extra&&... extra) {
    py::object cf = py::cpp_function(std::forward<Func>(f), std::forward<Extra>(extra)...);
    return py::reinterpret_steal<py::object>(PyClassMethod_New(cf.ptr()));
}

static inline void throw_type_error(const std::string& msg) {
    throw py::type_error(msg);
}

// -----------------------------------------------------------------------------
// Per-subclass cache (owned by subclass via capsule)
// -----------------------------------------------------------------------------

struct DebugDrawCache final {
    py::object draw_polygon;
    py::object draw_solid_polygon;
    py::object draw_circle;
    py::object draw_solid_circle;
    py::object draw_solid_capsule;
    py::object draw_line;
    py::object draw_transform;
    py::object draw_point;
    py::object draw_string;
};

static void debug_draw_cache_capsule_destructor(PyObject* capsule) {
    void* p = PyCapsule_GetPointer(capsule, "box2d.DebugDrawCache");
    auto* cache = static_cast<DebugDrawCache*>(p);
    delete cache;
}

// Prefer fetching from cls.__dict__ so we only cache methods defined on that subclass.
// If you want inherited methods to count, fall back to getattr as a second step.
static py::object dict_get(py::object cls, const char* name) {
    py::dict d = cls.attr("__dict__");
    if (d.contains(name)) return d[name];
    return py::none();
}

static py::object maybe_method_from_cls(py::object cls, const char* name, bool allow_inherited) {
    py::object o = dict_get(cls, name);
    if (!o.is_none()) return o;

    if (allow_inherited && py::hasattr(cls, name)) {
        return cls.attr(name);
    }

    return py::none();
}

static inline bool callable_or_none(const py::object& o) {
    return o.is_none() || PyCallable_Check(o.ptr());
}

static DebugDrawCache* get_cache_from_type(py::handle cls) {
    py::object cache_cap = py::reinterpret_borrow<py::object>(cls).attr("_b2dd_cache");
    void* p = PyCapsule_GetPointer(cache_cap.ptr(), "box2d.DebugDrawCache");
    return static_cast<DebugDrawCache*>(p);
}

// -----------------------------------------------------------------------------
// Per-instance context passed to Box2D (points to cached subclass methods)
// -----------------------------------------------------------------------------

struct DebugDrawContext final {
    PyObject* self = nullptr;         // strong ref to Python instance
    DebugDrawCache* cache = nullptr;  // non-owning; owned by subclass capsule

    ~DebugDrawContext() {
        if (self) {
            py::gil_scoped_acquire gil;
            Py_DECREF(self);
            self = nullptr;
        }
    }
};

// -----------------------------------------------------------------------------
// PyDebugDrawBase
// -----------------------------------------------------------------------------

class PyDebugDrawBase {
public:
    PyDebugDrawBase() {
        dd_.DrawPolygonFcn      = &DrawPolygonThunk;
        dd_.DrawSolidPolygonFcn = &DrawSolidPolygonThunk;
        dd_.DrawCircleFcn       = &DrawCircleThunk;
        dd_.DrawSolidCircleFcn  = &DrawSolidCircleThunk;
        dd_.DrawSolidCapsuleFcn = &DrawSolidCapsuleThunk;
        dd_.DrawLineFcn         = &DrawLineThunk;
        dd_.DrawTransformFcn    = &DrawTransformThunk;
        dd_.DrawPointFcn        = &DrawPointThunk;
        dd_.DrawStringFcn       = &DrawStringThunk;

        // Defaults you can expose as properties
        dd_.forceScale = 1.0f;
        dd_.jointScale = 1.0f;

        dd_.drawShapes = true;
        dd_.drawJoints = true;
        dd_.drawJointExtras = false;
        dd_.drawBounds = false;
        dd_.drawMass = false;
        dd_.drawBodyNames = false;
        dd_.drawContactPoints = false;
        dd_.drawGraphColors = false;
        dd_.drawContactFeatures = false;
        dd_.drawContactNormals = false;
        dd_.drawContactForces = false;
        dd_.drawFrictionForces = false;
        dd_.drawIslands = false;

        dd_.drawingBounds.lowerBound = b2Vec2{-1.0e9f, -1.0e9f};
        dd_.drawingBounds.upperBound = b2Vec2{+1.0e9f, +1.0e9f};

        ctx_ = std::make_unique<DebugDrawContext>();
        dd_.context = ctx_.get();
    }

    b2DebugDraw* ptr() { return &dd_; }

    // Called from Python __init__ binding: captures the Python self and resolves subclass cache.
    // Make it idempotent to support calling it more than once safely.
    void initialize(py::handle pyself) {
        py::gil_scoped_acquire gil;

        // Capture strong ref once
        if (!ctx_->self) {
            PyObject* self = pyself.ptr();
            Py_INCREF(self);
            ctx_->self = self;
        }

        // Resolve cache from type(self)
        py::handle cls((PyObject*)Py_TYPE(pyself.ptr()));
        // If __init_subclass__ didn't run or cache missing, raise a helpful error.
        if (!py::hasattr(py::reinterpret_borrow<py::object>(cls), "_b2dd_cache")) {
            throw_type_error(
                "DebugDrawBase subclass is missing _b2dd_cache. "
                "Ensure __init_subclass__ is installed correctly, or do not override it."
            );
        }
        ctx_->cache = get_cache_from_type(cls);
    }

    // -------- __init_subclass__ (classmethod) --------
    //
    // Called automatically by Python during subclass creation.
    // Build a DebugDrawCache and store it on the subclass as _b2dd_cache.
    //
    static void init_subclass(py::object cls, py::kwargs kwargs) {
        (void)kwargs;
        py::gil_scoped_acquire gil;

        // Choose whether inherited methods count as "implemented".
        // For debug draw, I usually allow inherited so you can define a base Python class
        // that implements some methods and refine in subclasses.
        const bool allow_inherited = true;

        auto* cache = new DebugDrawCache();

        auto maybe = [&](const char* name) -> py::object {
            py::object o = maybe_method_from_cls(cls, name, allow_inherited);
            if (o.is_none()) return py::none();
            if (!PyCallable_Check(o.ptr())) {
                delete cache;
                throw_type_error(std::string("DebugDraw method '") + name + "' must be callable");
            }
            return o; // unbound function/descriptor; thunks will call fn(self, ...)
        };

        cache->draw_polygon        = maybe("draw_polygon");
        cache->draw_solid_polygon  = maybe("draw_solid_polygon");
        cache->draw_circle         = maybe("draw_circle");
        cache->draw_solid_circle   = maybe("draw_solid_circle");
        cache->draw_solid_capsule  = maybe("draw_solid_capsule");
        cache->draw_line           = maybe("draw_line");
        cache->draw_transform      = maybe("draw_transform");
        cache->draw_point          = maybe("draw_point");
        cache->draw_string         = maybe("draw_string");

        // Validate (defensive; maybe() already enforces callable if present)
        if (!callable_or_none(cache->draw_polygon) ||
            !callable_or_none(cache->draw_solid_polygon) ||
            !callable_or_none(cache->draw_circle) ||
            !callable_or_none(cache->draw_solid_circle) ||
            !callable_or_none(cache->draw_solid_capsule) ||
            !callable_or_none(cache->draw_line) ||
            !callable_or_none(cache->draw_transform) ||
            !callable_or_none(cache->draw_point) ||
            !callable_or_none(cache->draw_string)) {
            delete cache;
            throw_type_error("DebugDraw cache contained a non-callable value.");
        }

        // Store on subclass as capsule (owned by the class; destroyed when class is GC'd)
        cls.attr("_b2dd_cache") =
            py::capsule(cache, "box2d.DebugDrawCache", debug_draw_cache_capsule_destructor);
    }

    // -------- thunks --------
    static inline bool enabled(const py::object& fn) { return !fn.is_none(); }

    static void report(const char* which, const py::error_already_set& e) {
        // Must not throw across C callback boundary.
        py::print("[box2d.DebugDraw]", which, "raised:", e.what());
    }

    static inline py::object self_obj(DebugDrawContext* c) {
        return py::reinterpret_borrow<py::object>(c->self);
    }

    static void DrawPolygonThunk(const b2Vec2* vertices, int vertexCount, b2HexColor color, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_polygon;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), verts_to_py(vertices, vertexCount), (uint32_t)color);
        } catch (const py::error_already_set& e) {
            report("draw_polygon", e);
        }
    }

    static void DrawSolidPolygonThunk(b2Transform transform, const b2Vec2* vertices, int vertexCount,
                                      float radius, b2HexColor color, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_solid_polygon;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), to_py(transform), verts_to_py(vertices, vertexCount), radius, (uint32_t)color);
        } catch (const py::error_already_set& e) {
            report("draw_solid_polygon", e);
        }
    }

    static void DrawCircleThunk(b2Vec2 center, float radius, b2HexColor color, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_circle;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), to_py(center), radius, (uint32_t)color);
        } catch (const py::error_already_set& e) {
            report("draw_circle", e);
        }
    }

    static void DrawSolidCircleThunk(b2Transform transform, float radius, b2HexColor color, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_solid_circle;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), to_py(transform), radius, (uint32_t)color);
        } catch (const py::error_already_set& e) {
            report("draw_solid_circle", e);
        }
    }

    static void DrawSolidCapsuleThunk(b2Vec2 p1, b2Vec2 p2, float radius, b2HexColor color, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_solid_capsule;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), to_py(p1), to_py(p2), radius, (uint32_t)color);
        } catch (const py::error_already_set& e) {
            report("draw_solid_capsule", e);
        }
    }

    static void DrawLineThunk(b2Vec2 p1, b2Vec2 p2, b2HexColor color, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_line;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), to_py(p1), to_py(p2), (uint32_t)color);
        } catch (const py::error_already_set& e) {
            report("draw_line", e);
        }
    }

    static void DrawTransformThunk(b2Transform transform, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_transform;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), to_py(transform));
        } catch (const py::error_already_set& e) {
            report("draw_transform", e);
        }
    }

    static void DrawPointThunk(b2Vec2 p, float size, b2HexColor color, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_point;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), to_py(p), size, (uint32_t)color);
        } catch (const py::error_already_set& e) {
            report("draw_point", e);
        }
    }

    static void DrawStringThunk(b2Vec2 p, const char* s, b2HexColor color, void* context) {
        auto* c = static_cast<DebugDrawContext*>(context);
        if (!c || !c->self || !c->cache) return;
        const py::object& fn = c->cache->draw_string;
        if (!enabled(fn)) return;

        py::gil_scoped_acquire gil;
        try {
            fn(self_obj(c), to_py(p), py::str(s ? s : ""), (uint32_t)color);
        } catch (const py::error_already_set& e) {
            report("draw_string", e);
        }
    }

private:
    b2DebugDraw dd_{};
    std::unique_ptr<DebugDrawContext> ctx_;
};
/*
// -----------------------------------------------------------------------------
// world_draw wrapper
// -----------------------------------------------------------------------------

static void world_draw(b2WorldId worldId, PyDebugDrawBase& dbg) {
    // dbg must outlive this call; Python owns dbg during the call.
    b2World_Draw(worldId, dbg.ptr());
}

// -----------------------------------------------------------------------------
// Module
// -----------------------------------------------------------------------------

PYBIND11_MODULE(box2d, m) {
    py::class_<PyDebugDrawBase> base(m, "DebugDrawBase");

    base.def(py::init<>());

    // Ensure instances are initialized against their *Python* self.
    // This is important because Box2D calls the thunks with void* context.
    base.def("__init__", [](PyDebugDrawBase& self, py::handle pyself) {
        // pybind11 will have already constructed `self` via py::init<>()
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
        py::arg("cls"),
        py::arg("kwargs") = py::kwargs()
    );

    // Also create a default cache on the base itself (so type(self) always has _b2dd_cache,
    // even if someone instantiates DebugDrawBase directly).
    {
        py::gil_scoped_acquire gil;
        PyDebugDrawBase::init_subclass(pyBase, py::kwargs());
    }

    m.def("world_draw", &world_draw, py::arg("world_id"), py::arg("debug_draw"));
}
*/