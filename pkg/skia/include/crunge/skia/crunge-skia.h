#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include <include/core/SkRefCnt.h>


namespace py = pybind11;

PYBIND11_DECLARE_HOLDER_TYPE(T, sk_sp<T>);