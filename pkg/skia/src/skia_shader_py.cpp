#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkShader.h>
#include <include/core/SkImage.h>
#include <include/core/SkColorFilter.h>
#include <include/core/SkMatrix.h>

namespace py = pybind11;

void init_skia_shader_py(py::module &_skia, Registry &registry) {
    //py::class_<SkMatrix> Matrix(_skia, "Matrix");
    //py::class_<SkShader, sk_sp<SkShader>, SkFlattenable> shader(
        py::class_<SkShader, sk_sp<SkShader>> shader(
        _skia, "Shader", R"docstring(
        Shaders specify the source color(s) for what is being drawn.
    
        If a paint has no shader, then the paint's color is used. If the paint has a
        shader, then the shader's color(s) are use instead, but they are modulated
        by the paint's alpha. This makes it easy to create a shader once (e.g.
        bitmap tiling or gradient) and then change its transparency w/o having to
        modify the original shader... only the paint's alpha needs to be modified.
    
        .. rubric:: Subclasses
    
        .. autosummary::
            :nosignatures:
    
            ~skia.Shaders
            ~skia.GradientShader
            ~skia.PerlinNoiseShader
        )docstring");
    
    shader
        .def("isOpaque", &SkShader::isOpaque,
            R"docstring(
            Returns true if the shader is guaranteed to produce only opaque colors,
            subject to the :py:class:`Paint` using the shader to apply an opaque
            alpha value.
    
            Subclasses should override this to allow some optimizations.
            )docstring")
        .def("isAImage",
            [] (const SkShader& shader, SkMatrix* localMatrix,
                std::vector<SkTileMode>& xy) {
                if (xy.size() != 2)
                    throw std::runtime_error("xy must have two elements.");
                return sk_sp<SkImage>(shader.isAImage(localMatrix, &xy[0]));
            },
            R"docstring(
            Iff this shader is backed by a single :py:class:`Image`, return its ptr
            (the caller must ref this if they want to keep it longer than the
            lifetime of the shader).
    
            If not, return nullptr.
            )docstring",
            py::arg("localMatrix"), py::arg("xy") = nullptr)
        .def("isAImage", py::overload_cast<>(&SkShader::isAImage, py::const_))
    /*
        .def("asAGradient", &SkShader::asAGradient, py::arg("info"))
    */
        .def("makeWithLocalMatrix", &SkShader::makeWithLocalMatrix,
            R"docstring(
            Return a shader that will apply the specified localMatrix to this
            shader.
    
            The specified matrix will be applied before any matrix associated with
            this shader.
            )docstring",
            py::arg("matrix"))
        .def("makeWithColorFilter", &SkShader::makeWithColorFilter,
            R"docstring(
            Create a new shader that produces the same colors as invoking this
            shader and then applying the colorfilter.
            )docstring",
            py::arg("colorFilter"))
    /*
        .def_static("Deserialize",
            [] (py::buffer b) {
                auto info = b.request();
                auto shader = SkShader::Deserialize(
                    SkFlattenable::Type::kSkShaderBase_Type, info.ptr,
                    info.shape[0] * info.strides[0]);
                return sk_sp<SkShader>(
                    reinterpret_cast<SkShader*>(shader.release()));
            },
            py::arg("data"))
    */
        ;    
}
