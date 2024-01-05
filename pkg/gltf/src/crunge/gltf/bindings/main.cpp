#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <tiny_gltf.h>

#include <crunge/core/bindtools.h>

#include <crunge/gltf/crunge-gltf.h>
#include <crunge/gltf/conversions.h>

namespace py = pybind11;

template<typename T>
pybind11::array_t<T> get_typed_array(const std::vector<T>& buffer, size_t byte_offset, size_t length) {
    // Ensure the byte offset is aligned with the size of T
    if (byte_offset % sizeof(T) != 0) {
        throw std::invalid_argument("Byte offset is not aligned with the size of the data type");
    }

    // Calculate the element offset
    size_t offset = byte_offset / sizeof(T);
    /*if (offset + length > buffer.size()) {
        throw std::out_of_range("Requested slice is out of bounds");
    }*/

    auto result = pybind11::array_t<T>(length);
    T* result_ptr = static_cast<T*>(result.request().ptr);
    std::copy(buffer.begin() + offset, buffer.begin() + offset + length, result_ptr);

    return result;
}

pybind11::object get_array(const tinygltf::Buffer& self, size_t offset, size_t length, int format) {
        switch (format) {
            case TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE:  // signed char
                return get_typed_array<unsigned char>(self.data, offset, length);
            case TINYGLTF_COMPONENT_TYPE_SHORT:  // unsigned char
                return get_typed_array<short>(reinterpret_cast<const std::vector<short>&>(self.data), offset, length);
            case TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT:  // signed int
                return get_typed_array<unsigned short>(reinterpret_cast<const std::vector<unsigned short>&>(self.data), offset, length);
            case TINYGLTF_COMPONENT_TYPE_INT:  // signed int
                return get_typed_array<int>(reinterpret_cast<const std::vector<int>&>(self.data), offset, length);
            case TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT:  // signed int
                return get_typed_array<unsigned int>(reinterpret_cast<const std::vector<unsigned int>&>(self.data), offset, length);
            case TINYGLTF_COMPONENT_TYPE_FLOAT:  // signed int
                return get_typed_array<float>(reinterpret_cast<const std::vector<float>&>(self.data), offset, length);
            case TINYGLTF_COMPONENT_TYPE_DOUBLE:  // signed int
                return get_typed_array<double>(reinterpret_cast<const std::vector<double>&>(self.data), offset, length);
            // Add more cases as needed for different data types
            default:
                throw std::invalid_argument("Unsupported format code");
        }
}
void init_main(py::module &_gltf, Registry &registry) {
    PYEXTEND_BEGIN(tinygltf::Buffer, Buffer)
        Buffer.def("get_array", &get_array, py::arg("offset"), py::arg("length"), py::arg("format"));
    PYEXTEND_END
}

