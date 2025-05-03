#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkMatrix.h>
#include <include/core/SkPoint3.h>
#include <include/core/SkRSXform.h>


namespace py = pybind11;

void init_skia_matrix_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkApplyPerspectiveClip>(_skia, "ApplyPerspectiveClip", py::arithmetic())
        .value("K_NO", SkApplyPerspectiveClip::kNo)
        .value("K_YES", SkApplyPerspectiveClip::kYes)
        .export_values()
    ;
    py::class_<SkMatrix> Matrix(_skia, "Matrix");
    registry.on(_skia, "Matrix", Matrix);
        Matrix
        .def(py::init<>())
        .def_static("scale", &SkMatrix::Scale
            , py::arg("sx")
            , py::arg("sy")
            , py::return_value_policy::automatic_reference)
        .def_static("translate", py::overload_cast<float, float>(&SkMatrix::Translate)
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def_static("translate", py::overload_cast<SkPoint>(&SkMatrix::Translate)
            , py::arg("t")
            , py::return_value_policy::automatic_reference)
        .def_static("translate", py::overload_cast<SkIPoint>(&SkMatrix::Translate)
            , py::arg("t")
            , py::return_value_policy::automatic_reference)
        .def_static("rotate_deg", py::overload_cast<float>(&SkMatrix::RotateDeg)
            , py::arg("deg")
            , py::return_value_policy::automatic_reference)
        .def_static("rotate_deg", py::overload_cast<float, SkPoint>(&SkMatrix::RotateDeg)
            , py::arg("deg")
            , py::arg("pt")
            , py::return_value_policy::automatic_reference)
        .def_static("rotate_rad", &SkMatrix::RotateRad
            , py::arg("rad")
            , py::return_value_policy::automatic_reference)
        .def_static("skew", &SkMatrix::Skew
            , py::arg("kx")
            , py::arg("ky")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkMatrix::ScaleToFit>(_skia, "ScaleToFit", py::arithmetic())
            .value("K_FILL_SCALE_TO_FIT", SkMatrix::ScaleToFit::kFill_ScaleToFit)
            .value("K_START_SCALE_TO_FIT", SkMatrix::ScaleToFit::kStart_ScaleToFit)
            .value("K_CENTER_SCALE_TO_FIT", SkMatrix::ScaleToFit::kCenter_ScaleToFit)
            .value("K_END_SCALE_TO_FIT", SkMatrix::ScaleToFit::kEnd_ScaleToFit)
            .export_values()
        ;
        Matrix
        .def_static("make_all", &SkMatrix::MakeAll
            , py::arg("scale_x")
            , py::arg("skew_x")
            , py::arg("trans_x")
            , py::arg("skew_y")
            , py::arg("scale_y")
            , py::arg("trans_y")
            , py::arg("pers0")
            , py::arg("pers1")
            , py::arg("pers2")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkMatrix::TypeMask>(_skia, "TypeMask", py::arithmetic())
            .value("K_IDENTITY_MASK", SkMatrix::TypeMask::kIdentity_Mask)
            .value("K_TRANSLATE_MASK", SkMatrix::TypeMask::kTranslate_Mask)
            .value("K_SCALE_MASK", SkMatrix::TypeMask::kScale_Mask)
            .value("K_AFFINE_MASK", SkMatrix::TypeMask::kAffine_Mask)
            .value("K_PERSPECTIVE_MASK", SkMatrix::TypeMask::kPerspective_Mask)
            .export_values()
        ;
        Matrix
        .def("get_type", &SkMatrix::getType
            , py::return_value_policy::automatic_reference)
        .def("is_identity", &SkMatrix::isIdentity
            , py::return_value_policy::automatic_reference)
        .def("is_scale_translate", &SkMatrix::isScaleTranslate
            , py::return_value_policy::automatic_reference)
        .def("is_translate", &SkMatrix::isTranslate
            , py::return_value_policy::automatic_reference)
        .def("rect_stays_rect", &SkMatrix::rectStaysRect
            , py::return_value_policy::automatic_reference)
        .def("preserves_axis_alignment", &SkMatrix::preservesAxisAlignment
            , py::return_value_policy::automatic_reference)
        .def("has_perspective", &SkMatrix::hasPerspective
            , py::return_value_policy::automatic_reference)
        .def("is_similarity", &SkMatrix::isSimilarity
            , py::arg("tol") = SK_ScalarNearlyZero
            , py::return_value_policy::automatic_reference)
        .def("preserves_right_angles", &SkMatrix::preservesRightAngles
            , py::arg("tol") = SK_ScalarNearlyZero
            , py::return_value_policy::automatic_reference)
        .def("get", &SkMatrix::get
            , py::arg("index")
            , py::return_value_policy::automatic_reference)
        .def("rc", &SkMatrix::rc
            , py::arg("r")
            , py::arg("c")
            , py::return_value_policy::automatic_reference)
        .def("get_scale_x", &SkMatrix::getScaleX
            , py::return_value_policy::automatic_reference)
        .def("get_scale_y", &SkMatrix::getScaleY
            , py::return_value_policy::automatic_reference)
        .def("get_skew_y", &SkMatrix::getSkewY
            , py::return_value_policy::automatic_reference)
        .def("get_skew_x", &SkMatrix::getSkewX
            , py::return_value_policy::automatic_reference)
        .def("get_translate_x", &SkMatrix::getTranslateX
            , py::return_value_policy::automatic_reference)
        .def("get_translate_y", &SkMatrix::getTranslateY
            , py::return_value_policy::automatic_reference)
        .def("get_persp_x", &SkMatrix::getPerspX
            , py::return_value_policy::automatic_reference)
        .def("get_persp_y", &SkMatrix::getPerspY
            , py::return_value_policy::automatic_reference)
        .def("set", &SkMatrix::set
            , py::arg("index")
            , py::arg("value")
            , py::return_value_policy::reference)
        .def("set_scale_x", &SkMatrix::setScaleX
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_scale_y", &SkMatrix::setScaleY
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_skew_y", &SkMatrix::setSkewY
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_skew_x", &SkMatrix::setSkewX
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_translate_x", &SkMatrix::setTranslateX
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_translate_y", &SkMatrix::setTranslateY
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_persp_x", &SkMatrix::setPerspX
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_persp_y", &SkMatrix::setPerspY
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_all", &SkMatrix::setAll
            , py::arg("scale_x")
            , py::arg("skew_x")
            , py::arg("trans_x")
            , py::arg("skew_y")
            , py::arg("scale_y")
            , py::arg("trans_y")
            , py::arg("persp0")
            , py::arg("persp1")
            , py::arg("persp2")
            , py::return_value_policy::reference)
        .def("get9", [](SkMatrix& self, std::array<SkScalar, 9>& buffer)
            {
                self.get9(&buffer[0]);
                return buffer;
            }
            , py::arg("buffer")
            , py::return_value_policy::automatic_reference)
        .def("set9", [](SkMatrix& self, std::array<float, 9>& buffer)
            {
                auto ret = self.set9(&buffer[0]);
                return std::make_tuple(ret, buffer);
            }
            , py::arg("buffer")
            , py::return_value_policy::reference)
        .def("reset", &SkMatrix::reset
            , py::return_value_policy::reference)
        .def("set_identity", &SkMatrix::setIdentity
            , py::return_value_policy::reference)
        .def("set_translate", py::overload_cast<float, float>(&SkMatrix::setTranslate)
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::reference)
        .def("set_translate", py::overload_cast<const SkPoint &>(&SkMatrix::setTranslate)
            , py::arg("v")
            , py::return_value_policy::reference)
        .def("set_scale", py::overload_cast<float, float, float, float>(&SkMatrix::setScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("set_scale", py::overload_cast<float, float>(&SkMatrix::setScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::return_value_policy::reference)
        .def("set_rotate", py::overload_cast<float, float, float>(&SkMatrix::setRotate)
            , py::arg("degrees")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("set_rotate", py::overload_cast<float>(&SkMatrix::setRotate)
            , py::arg("degrees")
            , py::return_value_policy::reference)
        .def("set_sin_cos", py::overload_cast<float, float, float, float>(&SkMatrix::setSinCos)
            , py::arg("sin_value")
            , py::arg("cos_value")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("set_sin_cos", py::overload_cast<float, float>(&SkMatrix::setSinCos)
            , py::arg("sin_value")
            , py::arg("cos_value")
            , py::return_value_policy::reference)
        .def("set_rs_xform", &SkMatrix::setRSXform
            , py::arg("rsx_form")
            , py::return_value_policy::reference)
        .def("set_skew", py::overload_cast<float, float, float, float>(&SkMatrix::setSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("set_skew", py::overload_cast<float, float>(&SkMatrix::setSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::return_value_policy::reference)
        .def("set_concat", &SkMatrix::setConcat
            , py::arg("a")
            , py::arg("b")
            , py::return_value_policy::reference)
        .def("pre_translate", &SkMatrix::preTranslate
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::reference)
        .def("pre_scale", py::overload_cast<float, float, float, float>(&SkMatrix::preScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("pre_scale", py::overload_cast<float, float>(&SkMatrix::preScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::return_value_policy::reference)
        .def("pre_rotate", py::overload_cast<float, float, float>(&SkMatrix::preRotate)
            , py::arg("degrees")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("pre_rotate", py::overload_cast<float>(&SkMatrix::preRotate)
            , py::arg("degrees")
            , py::return_value_policy::reference)
        .def("pre_skew", py::overload_cast<float, float, float, float>(&SkMatrix::preSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("pre_skew", py::overload_cast<float, float>(&SkMatrix::preSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::return_value_policy::reference)
        .def("pre_concat", &SkMatrix::preConcat
            , py::arg("other")
            , py::return_value_policy::reference)
        .def("post_translate", &SkMatrix::postTranslate
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::reference)
        .def("post_scale", py::overload_cast<float, float, float, float>(&SkMatrix::postScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("post_scale", py::overload_cast<float, float>(&SkMatrix::postScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::return_value_policy::reference)
        .def("post_rotate", py::overload_cast<float, float, float>(&SkMatrix::postRotate)
            , py::arg("degrees")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("post_rotate", py::overload_cast<float>(&SkMatrix::postRotate)
            , py::arg("degrees")
            , py::return_value_policy::reference)
        .def("post_skew", py::overload_cast<float, float, float, float>(&SkMatrix::postSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::arg("px")
            , py::arg("py")
            , py::return_value_policy::reference)
        .def("post_skew", py::overload_cast<float, float>(&SkMatrix::postSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::return_value_policy::reference)
        .def("post_concat", &SkMatrix::postConcat
            , py::arg("other")
            , py::return_value_policy::reference)
        .def("set_rect_to_rect", &SkMatrix::setRectToRect
            , py::arg("src")
            , py::arg("dst")
            , py::arg("stf")
            , py::return_value_policy::automatic_reference)
        .def_static("make_rect_to_rect", &SkMatrix::MakeRectToRect
            , py::arg("src")
            , py::arg("dst")
            , py::arg("stf")
            , py::return_value_policy::automatic_reference)
        .def("set_poly_to_poly", &SkMatrix::setPolyToPoly
            , py::arg("src")
            , py::arg("dst")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("invert", &SkMatrix::invert
            , py::arg("inverse")
            , py::return_value_policy::automatic_reference)
        .def_static("set_affine_identity", [](std::array<SkScalar, 6>& affine)
            {
                SkMatrix::SetAffineIdentity(&affine[0]);
                return affine;
            }
            , py::arg("affine")
            , py::return_value_policy::automatic_reference)
        .def("as_affine", [](SkMatrix& self, std::array<SkScalar, 6>& affine)
            {
                auto ret = self.asAffine(&affine[0]);
                return std::make_tuple(ret, affine);
            }
            , py::arg("affine")
            , py::return_value_policy::automatic_reference)
        .def("set_affine", [](SkMatrix& self, std::array<float, 6>& affine)
            {
                auto ret = self.setAffine(&affine[0]);
                return std::make_tuple(ret, affine);
            }
            , py::arg("affine")
            , py::return_value_policy::reference)
        .def("normalize_perspective", &SkMatrix::normalizePerspective
            , py::return_value_policy::automatic_reference)
        .def("map_points", py::overload_cast<SkPoint[], const SkPoint[], int>(&SkMatrix::mapPoints, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("map_points", py::overload_cast<SkPoint[], int>(&SkMatrix::mapPoints, py::const_)
            , py::arg("pts")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("map_homogeneous_points", py::overload_cast<SkPoint3[], const SkPoint3[], int>(&SkMatrix::mapHomogeneousPoints, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("map_homogeneous_points", py::overload_cast<SkPoint3[], const SkPoint[], int>(&SkMatrix::mapHomogeneousPoints, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("map_point", &SkMatrix::mapPoint
            , py::arg("pt")
            , py::return_value_policy::automatic_reference)
        .def("map_xy", py::overload_cast<float, float, SkPoint *>(&SkMatrix::mapXY, py::const_)
            , py::arg("x")
            , py::arg("y")
            , py::arg("result")
            , py::return_value_policy::automatic_reference)
        .def("map_xy", py::overload_cast<float, float>(&SkMatrix::mapXY, py::const_)
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("map_origin", &SkMatrix::mapOrigin
            , py::return_value_policy::automatic_reference)
        .def("map_vectors", py::overload_cast<SkPoint[], const SkPoint[], int>(&SkMatrix::mapVectors, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("map_vectors", py::overload_cast<SkPoint[], int>(&SkMatrix::mapVectors, py::const_)
            , py::arg("vecs")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("map_vector", py::overload_cast<float, float, SkPoint *>(&SkMatrix::mapVector, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("result")
            , py::return_value_policy::automatic_reference)
        .def("map_vector", py::overload_cast<float, float>(&SkMatrix::mapVector, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            , py::return_value_policy::automatic_reference)
        .def("map_rect", py::overload_cast<SkRect *, const SkRect &, SkApplyPerspectiveClip>(&SkMatrix::mapRect, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            , py::return_value_policy::automatic_reference)
        .def("map_rect", py::overload_cast<SkRect *, SkApplyPerspectiveClip>(&SkMatrix::mapRect, py::const_)
            , py::arg("rect")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            , py::return_value_policy::automatic_reference)
        .def("map_rect", py::overload_cast<const SkRect &, SkApplyPerspectiveClip>(&SkMatrix::mapRect, py::const_)
            , py::arg("src")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            , py::return_value_policy::automatic_reference)
        .def("map_rect_to_quad", [](SkMatrix& self, std::array<SkPoint, 4>& dst, const SkRect & rect)
            {
                self.mapRectToQuad(&dst[0], rect);
                return dst;
            }
            , py::arg("dst")
            , py::arg("rect")
            , py::return_value_policy::automatic_reference)
        .def("map_rect_scale_translate", &SkMatrix::mapRectScaleTranslate
            , py::arg("dst")
            , py::arg("src")
            , py::return_value_policy::automatic_reference)
        .def("map_radius", &SkMatrix::mapRadius
            , py::arg("radius")
            , py::return_value_policy::automatic_reference)
        .def("dump", &SkMatrix::dump
            , py::return_value_policy::automatic_reference)
        .def("get_min_scale", &SkMatrix::getMinScale
            , py::return_value_policy::automatic_reference)
        .def("get_max_scale", &SkMatrix::getMaxScale
            , py::return_value_policy::automatic_reference)
        .def("get_min_max_scales", [](SkMatrix& self, std::array<SkScalar, 2>& scaleFactors)
            {
                auto ret = self.getMinMaxScales(&scaleFactors[0]);
                return std::make_tuple(ret, scaleFactors);
            }
            , py::arg("scale_factors")
            , py::return_value_policy::automatic_reference)
        .def("decompose_scale", &SkMatrix::decomposeScale
            , py::arg("scale")
            , py::arg("remaining") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("i", &SkMatrix::I
            , py::return_value_policy::reference)
        .def_static("invalid_matrix", &SkMatrix::InvalidMatrix
            , py::return_value_policy::reference)
        .def_static("concat", &SkMatrix::Concat
            , py::arg("a")
            , py::arg("b")
            , py::return_value_policy::automatic_reference)
        .def("dirty_matrix_type_cache", &SkMatrix::dirtyMatrixTypeCache
            , py::return_value_policy::automatic_reference)
        .def("set_scale_translate", &SkMatrix::setScaleTranslate
            , py::arg("sx")
            , py::arg("sy")
            , py::arg("tx")
            , py::arg("ty")
            , py::return_value_policy::automatic_reference)
        .def("is_finite", &SkMatrix::isFinite
            , py::return_value_policy::automatic_reference)
    ;


}