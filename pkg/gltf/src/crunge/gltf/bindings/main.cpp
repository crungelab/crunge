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
pybind11::array_t<T> get_typed_array(const std::vector<unsigned char>& buffer, size_t byte_offset, const std::array<size_t, 2>& shape) {
    // Ensure the byte offset is aligned with the size of T
    if (byte_offset % alignof(T) != 0) {
        throw std::invalid_argument("Byte offset is not aligned with the size of the data type");
    }

    // Calculate the total number of elements from the shape
    size_t total_elements = shape[0] * shape[1];

    // Check that the slice is within the bounds of the buffer
    if (byte_offset + total_elements * sizeof(T) > buffer.size()) {
        throw std::out_of_range("Requested slice is out of bounds");
    }

    // Create a new NumPy array with the specified shape
    auto result = pybind11::array_t<T>({shape[0], shape[1]});

    // Obtain a pointer to the array's data
    T* result_ptr = static_cast<T*>(result.request().ptr);

    // Reinterpret the buffer slice as an array of type T and copy the data
    const T* buffer_ptr = reinterpret_cast<const T*>(buffer.data() + byte_offset);
    std::copy(buffer_ptr, buffer_ptr + total_elements, result_ptr);

    return result;
}

pybind11::object get_array(const tinygltf::Buffer& self, size_t byte_offset, size_t count, uint32_t type, uint32_t componentType) {
    size_t componentCount = tinygltf::GetNumComponentsInType(type);
    std::array<size_t, 2> shape = {count, componentCount};
    switch (componentType) {
        case TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE:  // signed char
            return get_typed_array<unsigned char>(self.data, byte_offset, shape);
        case TINYGLTF_COMPONENT_TYPE_SHORT:  // unsigned char
            return get_typed_array<short>(self.data, byte_offset, shape);
        case TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT:  // signed int
            return get_typed_array<unsigned short>(self.data, byte_offset, shape);
        case TINYGLTF_COMPONENT_TYPE_INT:  // signed int
            return get_typed_array<int>(self.data, byte_offset, shape);
        case TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT:  // signed int
            return get_typed_array<unsigned int>(self.data, byte_offset, shape);
        case TINYGLTF_COMPONENT_TYPE_FLOAT:  // signed int
            return get_typed_array<float>(self.data, byte_offset, shape);
        case TINYGLTF_COMPONENT_TYPE_DOUBLE:  // signed int
            return get_typed_array<double>(self.data, byte_offset, shape);
        // Add more cases as needed for different data types
        default:
            throw std::invalid_argument("Unsupported componentType");
    }
}

void init_main(py::module &_gltf, Registry &registry) {
    PYEXTEND_BEGIN(tinygltf::Buffer, Buffer)
        Buffer.def("get_array", &get_array, py::arg("byte_offset"), py::arg("count"), py::arg("type"), py::arg("component_type"));
    PYEXTEND_END
}

