cmake_minimum_required(VERSION 3.4)

set (CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})


#
# pybind11
#
set(-DCMAKE_CXX_STANDARD=20 -std=c++20)
set(PYBIND11_PYTHON_VERSION 3.10)

add_subdirectory(depot/pybind11)

add_subdirectory(pkg/imgui)
add_subdirectory(pkg/implot)
add_subdirectory(pkg/imnodes)

#
# bgfx
#
#add_subdirectory(depot/astc-encoder)
#add_subdirectory(src/bimg)
#add_subdirectory(src/bgfx)
#add_subdirectory(pkg/bgfx)

#
# wgpu
#
add_subdirectory(depot/dawn)
add_subdirectory(pkg/wgpu)

add_subdirectory(examples)