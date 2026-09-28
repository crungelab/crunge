#include <pybind11/pybind11.h>

namespace py = pybind11;

struct AimDrawList {
    static const size_t COMMAND_SIZE = sizeof(ImDrawCmd);
    static const size_t VERTEX_SIZE = sizeof(ImDrawVert);
    static const size_t INDEX_SIZE = sizeof(ImDrawIdx);
};

template<typename T>
void template_ImVector(py::module &module, const char* name)
{
    py::class_<ImVector<T>>(module, name)
        .def_property_readonly_static("stride", [](py::object) { return sizeof(T); })
        .def_property_readonly("data", [](const ImVector<T>& self) {
            return reinterpret_cast<std::uintptr_t>(self.Data);
        })
        .def("__len__", [](const ImVector<T>& self) { return self.size(); })
        .def("__iter__", [](const ImVector<T>& self) {
            return py::make_iterator(self.begin(), self.end());
        }, py::keep_alive<0, 1>())
        .def("__getitem__", [](const ImVector<T>& self, py::ssize_t i) -> const T& {
            if (i < 0) i += self.size();
            if (i < 0 || i >= self.size()) throw py::index_error();
            return self[static_cast<int>(i)];
        }, py::return_value_policy::reference_internal);
}