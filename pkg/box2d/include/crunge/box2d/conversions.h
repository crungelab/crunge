#include <box2d/math_functions.h>

#include <pybind11/pybind11.h>

namespace py = pybind11;

/*
namespace pybind11 { namespace detail {

    template <> struct type_caster<b2Vec2> {
    public:
        PYBIND11_TYPE_CASTER(b2Vec2, _("Vec2"));
        bool load(handle src, bool implicit) {
            PyObject *source = src.ptr();
            value.x = PyFloat_AsDouble(PyTuple_GetItem(source, 0));
            value.y = PyFloat_AsDouble(PyTuple_GetItem(source, 1));
            return !PyErr_Occurred();
        }
        static handle cast(b2Vec2 src, return_value_policy policy, handle parent) {
            auto tuple = PyTuple_New(2);
            PyTuple_SetItem(tuple, 0, PyFloat_FromDouble(src.x));
            PyTuple_SetItem(tuple, 1, PyFloat_FromDouble(src.y));
            return tuple;
        }
    };

}} // namespace pybind11::detail
*/