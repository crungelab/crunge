#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkColorSpace.h>
#include <include/core/SkData.h>

namespace py = pybind11;

void init_skia_color_space_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkColorSpacePrimaries> _ColorSpacePrimaries(_skia, "ColorSpacePrimaries");
    registry.on(_skia, "ColorSpacePrimaries", _ColorSpacePrimaries);
        _ColorSpacePrimaries
        .def_readwrite("f_rx", &SkColorSpacePrimaries::fRX)
        .def_readwrite("f_ry", &SkColorSpacePrimaries::fRY)
        .def_readwrite("f_gx", &SkColorSpacePrimaries::fGX)
        .def_readwrite("f_gy", &SkColorSpacePrimaries::fGY)
        .def_readwrite("f_bx", &SkColorSpacePrimaries::fBX)
        .def_readwrite("f_by", &SkColorSpacePrimaries::fBY)
        .def_readwrite("f_wx", &SkColorSpacePrimaries::fWX)
        .def_readwrite("f_wy", &SkColorSpacePrimaries::fWY)
        .def("to_xyzd50", &SkColorSpacePrimaries::toXYZD50
            , py::arg("to_xyzd50")
            )
    ;

    py::class_<SkColorSpace,sk_sp<SkColorSpace>> _ColorSpace(_skia, "ColorSpace");
    registry.on(_skia, "ColorSpace", _ColorSpace);
        _ColorSpace
        .def_static("make_srgb", &SkColorSpace::MakeSRGB
            )
        .def_static("make_srgb_linear", &SkColorSpace::MakeSRGBLinear
            )
        .def_static("make_rgb", &SkColorSpace::MakeRGB
            , py::arg("transfer_fn")
            , py::arg("to_xyz")
            )
        .def_static("make_cicp", &SkColorSpace::MakeCICP
            , py::arg("color_primaries")
            , py::arg("transfer_characteristics")
            )
        .def_static("make", &SkColorSpace::Make
            , py::arg("arg0")
            )
        .def("to_profile", &SkColorSpace::toProfile
            , py::arg("arg0")
            )
        .def("gamma_close_to_srgb", &SkColorSpace::gammaCloseToSRGB
            )
        .def("gamma_is_linear", &SkColorSpace::gammaIsLinear
            )
        .def("is_numerical_transfer_fn", &SkColorSpace::isNumericalTransferFn
            , py::arg("fn")
            )
        .def("to_xyzd50", &SkColorSpace::toXYZD50
            , py::arg("to_xyzd50")
            )
        .def("to_xyzd50_hash", &SkColorSpace::toXYZD50Hash
            )
        .def("make_linear_gamma", &SkColorSpace::makeLinearGamma
            )
        .def("make_srgb_gamma", &SkColorSpace::makeSRGBGamma
            )
        .def("make_color_spin", &SkColorSpace::makeColorSpin
            )
        .def("is_srgb", &SkColorSpace::isSRGB
            )
        .def("serialize", &SkColorSpace::serialize
            )
        .def("write_to_memory", &SkColorSpace::writeToMemory
            , py::arg("memory")
            )
        .def_static("deserialize", &SkColorSpace::Deserialize
            , py::arg("data")
            , py::arg("length")
            )
        .def_static("equals", &SkColorSpace::Equals
            , py::arg("arg0")
            , py::arg("arg1")
            )
        .def("transfer_fn", [](SkColorSpace& self, std::array<float, 7>& gabcdef)
            {
                self.transferFn(&gabcdef[0]);
                return std::make_tuple(gabcdef);
            }
            , py::arg("gabcdef")
            )
        .def("transfer_fn", py::overload_cast<skcms_TransferFunction *>(&SkColorSpace::transferFn, py::const_)
            , py::arg("fn")
            )
        .def("inv_transfer_fn", &SkColorSpace::invTransferFn
            , py::arg("fn")
            )
        .def("gamut_transform_to", &SkColorSpace::gamutTransformTo
            , py::arg("dst")
            , py::arg("src_to_dst")
            )
        .def("transfer_fn_hash", &SkColorSpace::transferFnHash
            )
        .def("hash", &SkColorSpace::hash
            )
    ;


}