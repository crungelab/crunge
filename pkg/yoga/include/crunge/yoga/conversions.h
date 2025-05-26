#pragma once

#include <pybind11/pybind11.h>

#include <yoga/numeric/FloatOptional.h>

namespace py = pybind11;

namespace pybind11 { namespace detail {

template <> struct type_caster<facebook::yoga::FloatOptional> {
    public:
        PYBIND11_TYPE_CASTER(facebook::yoga::FloatOptional, _("crunge.yoga._yoga.FloatOptional"));
        bool load(handle src, bool implicit) {
            value = facebook::yoga::FloatOptional{src.cast<float>()};
            return true;
        }
        
        static handle cast(facebook::yoga::FloatOptional src, return_value_policy /* policy */, handle /* parent */) {
            return PyFloat_FromDouble(src.unwrap());
        }
    };

}} // namespace pybind11::detail