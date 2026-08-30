#pragma once

// debug_draw_py.h
//
// pybind11 bridge for Box2D v3 b2DebugDraw, updated for
//   "More doubles clean up and testing (#1070)" -- 56edae7
//
// Callback table changes in that commit:
//   DrawPolygonFcn      gained a leading b2WorldTransform; vertices are now LOCAL to it
//   DrawSolidPolygonFcn b2Transform -> b2WorldTransform
//   DrawCircleFcn       b2Vec2 center -> b2Pos center
//   DrawSolidCircleFcn  b2Transform -> b2WorldTransform, and gained a b2Vec2 center
//   DrawSolidCapsuleFcn b2Vec2 p1/p2 -> b2Pos p1/p2
//   DrawLineFcn         b2Vec2 p1/p2 -> b2Pos p1/p2
//   DrawTransformFcn    b2Transform -> b2WorldTransform
//   DrawPointFcn        b2Vec2 p -> b2Pos p
//   DrawStringFcn       b2Vec2 p -> b2Pos p
//   DrawBoundsFcn       NEW: ( b2AABB aabb, b2HexColor color, void* context )
//   b2DebugDraw::origin REMOVED (callbacks receive world coordinates again)
//
// In large-world builds (BOX2D_DOUBLE_PRECISION) b2Pos/b2WorldTransform carry a
// double-precision translation; otherwise they are typedefs of b2Vec2/b2Transform,
// so the marshalling overloads below are guarded to avoid redefinition.

#include <cstdint>
#include <exception>
#include <memory>
#include <string>
#include <utility>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <box2d/box2d.h>
#include <box2d/types.h>

namespace py = pybind11;

#if defined( BOX2D_DOUBLE_PRECISION )
#define B2DD_LARGE_WORLD 1
#else
#define B2DD_LARGE_WORLD 0
#endif

// Anything holding a pybind11 type must not be exported, or GCC warns about a symbol
// with greater visibility than its members.
#if defined( __GNUC__ )
#define B2DD_HIDDEN __attribute__( ( visibility( "hidden" ) ) )
#else
#define B2DD_HIDDEN
#endif

// -----------------------------------------------------------------------------
// Marshalling
// -----------------------------------------------------------------------------

inline py::tuple to_py( b2Vec2 v ) {
    return py::make_tuple( v.x, v.y );
}

// Transforms are marshalled as (x, y, angle). If you would rather build your render
// matrix without a trig call, change this to py::make_tuple( t.p.x, t.p.y, t.q.c, t.q.s )
// -- b2Rot is already stored as cosine/sine.
inline py::tuple to_py( b2Transform t ) {
    return py::make_tuple( t.p.x, t.p.y, b2Rot_GetAngle( t.q ) );
}

#if B2DD_LARGE_WORLD
// Only distinct types when double precision is enabled.
inline py::tuple to_py( b2Pos p ) {
    return py::make_tuple( p.x, p.y );
}

inline py::tuple to_py( b2WorldTransform t ) {
    return py::make_tuple( t.p.x, t.p.y, b2Rot_GetAngle( t.q ) );
}
#endif

// b2AABB stays float even in large-world mode, so far from the origin it carries
// increasing padding. Treat it as a loose bound, not an exact one.
inline py::tuple to_py( b2AABB aabb ) {
    return py::make_tuple( to_py( aabb.lowerBound ), to_py( aabb.upperBound ) );
}

inline py::list verts_to_py( const b2Vec2 *v, int n ) {
    py::list out( n );
    for ( int i = 0; i < n; ++i ) {
        out[i] = to_py( v[i] );
    }
    return out;
}

// Install a real Python "classmethod" descriptor for a C++ function.
template <class Func, class... Extra>
inline py::object classmethod( Func &&f, Extra &&...extra ) {
    py::object cf = py::cpp_function( std::forward<Func>( f ), std::forward<Extra>( extra )... );
    return py::reinterpret_steal<py::object>( PyClassMethod_New( cf.ptr() ) );
}

inline void throw_type_error( const std::string &msg ) {
    throw py::type_error( msg );
}

// -----------------------------------------------------------------------------
// Per-subclass cache (owned by the subclass via capsule)
// -----------------------------------------------------------------------------

inline constexpr const char *kDebugDrawCacheAttr = "_b2dd_cache";
inline constexpr const char *kDebugDrawCacheName = "box2d.DebugDrawCache";

struct B2DD_HIDDEN DebugDrawCache final {
    py::object draw_polygon;
    py::object draw_solid_polygon;
    py::object draw_circle;
    py::object draw_solid_circle;
    py::object draw_solid_capsule;
    py::object draw_line;
    py::object draw_transform;
    py::object draw_point;
    py::object draw_string;
    py::object draw_bounds;
};

inline void debug_draw_cache_capsule_destructor( PyObject *capsule ) {
    void *p = PyCapsule_GetPointer( capsule, kDebugDrawCacheName );
    delete static_cast<DebugDrawCache *>( p );
}

// Prefer cls.__dict__ so we can tell "defined here" from "inherited", then fall back
// to normal attribute lookup so a Python base class can supply shared implementations.
inline py::object dict_get( py::handle cls, const char *name ) {
    // type.__dict__ is a mappingproxy, not a dict, so this has to go through the
    // mapping protocol rather than py::dict.
    py::object d = py::reinterpret_borrow<py::object>( cls ).attr( "__dict__" );
    PyObject *item = PyMapping_GetItemString( d.ptr(), name );
    if ( item == nullptr ) {
        PyErr_Clear();
        return py::none();
    }
    return py::reinterpret_steal<py::object>( item );
}

inline py::object maybe_method_from_cls( py::handle cls, const char *name, bool allow_inherited ) {
    py::object o = dict_get( cls, name );
    if ( !o.is_none() ) {
        return o;
    }

    if ( allow_inherited && py::hasattr( cls, name ) ) {
        return py::reinterpret_borrow<py::object>( cls ).attr( name );
    }

    return py::none();
}

inline DebugDrawCache *build_debug_draw_cache( py::handle cls ) {
    // Allow inherited so a Python base class can implement part of the interface.
    const bool allow_inherited = true;

    std::unique_ptr<DebugDrawCache> cache( new DebugDrawCache() );

    auto maybe = [&]( const char *name ) -> py::object {
        py::object o = maybe_method_from_cls( cls, name, allow_inherited );
        if ( o.is_none() ) {
            return py::none();
        }
        if ( !PyCallable_Check( o.ptr() ) ) {
            throw_type_error( std::string( "DebugDraw method '" ) + name + "' must be callable" );
        }
        return o; // unbound function/descriptor; thunks call fn(self, ...)
    };

    cache->draw_polygon = maybe( "draw_polygon" );
    cache->draw_solid_polygon = maybe( "draw_solid_polygon" );
    cache->draw_circle = maybe( "draw_circle" );
    cache->draw_solid_circle = maybe( "draw_solid_circle" );
    cache->draw_solid_capsule = maybe( "draw_solid_capsule" );
    cache->draw_line = maybe( "draw_line" );
    cache->draw_transform = maybe( "draw_transform" );
    cache->draw_point = maybe( "draw_point" );
    cache->draw_string = maybe( "draw_string" );
    cache->draw_bounds = maybe( "draw_bounds" );

    DebugDrawCache *raw = cache.release();

    py::reinterpret_borrow<py::object>( cls ).attr( kDebugDrawCacheAttr ) =
        py::capsule( raw, kDebugDrawCacheName, debug_draw_cache_capsule_destructor );

    return raw;
}

// Resolve the cache for a concrete type. Builds it lazily if __init_subclass__ never
// ran (dynamically created types, unusual metaclasses, cache cleared by hand).
inline DebugDrawCache *resolve_debug_draw_cache( py::handle cls ) {
    // Look in this type's own __dict__: an inherited capsule belongs to the base and
    // would report the base's methods.
    py::object cap = dict_get( cls, kDebugDrawCacheAttr );
    if ( !cap.is_none() ) {
        void *p = PyCapsule_GetPointer( cap.ptr(), kDebugDrawCacheName );
        if ( p != nullptr ) {
            return static_cast<DebugDrawCache *>( p );
        }
        PyErr_Clear();
    }

    return build_debug_draw_cache( cls );
}

// -----------------------------------------------------------------------------
// Per-instance context handed to Box2D
// -----------------------------------------------------------------------------

struct B2DD_HIDDEN DebugDrawContext final {
    PyObject *self = nullptr;        // BORROWED; valid only during world_draw
    DebugDrawCache *cache = nullptr; // non-owning; owned by the subclass capsule
    std::exception_ptr error;        // first callback failure, rethrown by world_draw
};

// -----------------------------------------------------------------------------
// PyDebugDrawBase
// -----------------------------------------------------------------------------

class B2DD_HIDDEN PyDebugDrawBase {
public:
    PyDebugDrawBase() {
        // Start from the library defaults so fields added by future Box2D releases
        // are still initialized sensibly, then install our thunks.
        dd_ = b2DefaultDebugDraw();

        dd_.DrawPolygonFcn = &DrawPolygonThunk;
        dd_.DrawSolidPolygonFcn = &DrawSolidPolygonThunk;
        dd_.DrawCircleFcn = &DrawCircleThunk;
        dd_.DrawSolidCircleFcn = &DrawSolidCircleThunk;
        dd_.DrawSolidCapsuleFcn = &DrawSolidCapsuleThunk;
        dd_.DrawLineFcn = &DrawLineThunk;
        dd_.DrawTransformFcn = &DrawTransformThunk;
        dd_.DrawPointFcn = &DrawPointThunk;
        dd_.DrawStringFcn = &DrawStringThunk;
        dd_.DrawBoundsFcn = &DrawBoundsThunk;

        dd_.drawShapes = true;
        dd_.drawJoints = true;

        ctx_ = std::make_unique<DebugDrawContext>();
        dd_.context = ctx_.get();
    }

    b2DebugDraw *ptr() {
        return &dd_;
    }

    DebugDrawContext *ctx() {
        return ctx_.get();
    }

    // Binds the Python instance and its subclass cache for the duration of one
    // b2World_Draw call. Save/restore makes re-entrant draws safe.
    class B2DD_HIDDEN ScopedBind final {
    public:
        ScopedBind( DebugDrawContext *ctx, PyObject *self, DebugDrawCache *cache )
            : ctx_( ctx ), prev_self_( ctx->self ), prev_cache_( ctx->cache ) {
            ctx_->self = self;
            ctx_->cache = cache;
        }

        ~ScopedBind() {
            ctx_->self = prev_self_;
            ctx_->cache = prev_cache_;
        }

        ScopedBind( const ScopedBind & ) = delete;
        ScopedBind &operator=( const ScopedBind & ) = delete;

    private:
        DebugDrawContext *ctx_;
        PyObject *prev_self_;
        DebugDrawCache *prev_cache_;
    };

    // -------- __init_subclass__ (classmethod) --------
    static void init_subclass( py::object cls, py::kwargs kwargs ) {
        (void)kwargs;
        build_debug_draw_cache( cls );
    }

    // Rebuild the cache for a class after monkey-patching a draw method on it.
    static void refresh_cache( py::object cls ) {
        build_debug_draw_cache( cls );
    }

    // -------- thunk plumbing --------
private:
    struct B2DD_HIDDEN Bound final {
        DebugDrawContext *ctx = nullptr;
        const py::object *fn = nullptr;

        explicit operator bool() const {
            return ctx != nullptr;
        }

        py::handle self() const {
            return py::handle( ctx->self );
        }
    };

    static Bound bind( void *context, py::object DebugDrawCache::*member ) {
        auto *c = static_cast<DebugDrawContext *>( context );
        if ( c == nullptr || c->self == nullptr || c->cache == nullptr || c->error ) {
            return {};
        }

        const py::object &fn = c->cache->*member;
        if ( fn.is_none() ) {
            return {};
        }

        return Bound{ c, &fn };
    }

    // Callbacks must not unwind into C. Stash the failure; world_draw rethrows it.
    static void capture( DebugDrawContext *c ) {
        if ( !c->error ) {
            c->error = std::current_exception();
        }
    }

    // -------- thunks --------
public:
    static void DrawPolygonThunk( b2WorldTransform transform, const b2Vec2 *vertices, int vertexCount, b2HexColor color,
                                  void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_polygon );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( transform ), verts_to_py( vertices, vertexCount ), (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawSolidPolygonThunk( b2WorldTransform transform, const b2Vec2 *vertices, int vertexCount, float radius,
                                       b2HexColor color, void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_solid_polygon );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( transform ), verts_to_py( vertices, vertexCount ), radius, (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawCircleThunk( b2Pos center, float radius, b2HexColor color, void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_circle );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( center ), radius, (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawSolidCircleThunk( b2WorldTransform transform, b2Vec2 center, float radius, b2HexColor color,
                                      void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_solid_circle );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( transform ), to_py( center ), radius, (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawSolidCapsuleThunk( b2Pos p1, b2Pos p2, float radius, b2HexColor color, void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_solid_capsule );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( p1 ), to_py( p2 ), radius, (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawLineThunk( b2Pos p1, b2Pos p2, b2HexColor color, void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_line );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( p1 ), to_py( p2 ), (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawTransformThunk( b2WorldTransform transform, void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_transform );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( transform ) );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawPointThunk( b2Pos p, float size, b2HexColor color, void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_point );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( p ), size, (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawStringThunk( b2Pos p, const char *s, b2HexColor color, void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_string );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( p ), py::str( s ? s : "" ), (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

    static void DrawBoundsThunk( b2AABB aabb, b2HexColor color, void *context ) {
        Bound b = bind( context, &DebugDrawCache::draw_bounds );
        if ( !b ) {
            return;
        }

        py::gil_scoped_acquire gil;
        try {
            ( *b.fn )( b.self(), to_py( aabb.lowerBound ), to_py( aabb.upperBound ), (uint32_t)color );
        } catch ( const py::error_already_set & ) {
            capture( b.ctx );
        }
    }

private:
    b2DebugDraw dd_{};
    std::unique_ptr<DebugDrawContext> ctx_;
};

// -----------------------------------------------------------------------------
// world_draw wrapper
// -----------------------------------------------------------------------------

inline void world_draw( b2WorldId worldId, py::object dbg ) {
    auto &self = dbg.cast<PyDebugDrawBase &>();

    DebugDrawContext *ctx = self.ctx();
    DebugDrawCache *cache = resolve_debug_draw_cache( py::handle( (PyObject *)Py_TYPE( dbg.ptr() ) ) );

    // `dbg` keeps the instance alive for the whole call, so a borrowed ref is enough
    // and avoids an uncollectable reference cycle through the C++ context.
    PyDebugDrawBase::ScopedBind bound( ctx, dbg.ptr(), cache );

    // The GIL stays held: every callback comes straight back into Python, so
    // releasing here would only pay for a re-acquire per shape.
    b2World_Draw( worldId, self.ptr() );

    if ( ctx->error ) {
        std::exception_ptr e = ctx->error;
        ctx->error = nullptr;
        std::rethrow_exception( e );
    }
}