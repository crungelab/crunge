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
    py::class_<SkMatrix> _Matrix(_skia, "Matrix");
    registry.on(_skia, "Matrix", _Matrix);
        _Matrix
        .def(py::init<>())
        .def_static("scale", &SkMatrix::Scale
            , py::arg("sx")
            , py::arg("sy")
            )
        .def_static("translate", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::Translate)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def_static("translate", py::overload_cast<SkVector>(&SkMatrix::Translate)
            , py::arg("t")
            )
        .def_static("translate", py::overload_cast<SkIVector>(&SkMatrix::Translate)
            , py::arg("t")
            )
        .def_static("rotate_deg", py::overload_cast<SkScalar>(&SkMatrix::RotateDeg)
            , py::arg("deg")
            )
        .def_static("rotate_deg", py::overload_cast<SkScalar, SkPoint>(&SkMatrix::RotateDeg)
            , py::arg("deg")
            , py::arg("pt")
            )
        .def_static("rotate_rad", &SkMatrix::RotateRad
            , py::arg("rad")
            )
        .def_static("skew", &SkMatrix::Skew
            , py::arg("kx")
            , py::arg("ky")
            )
        ;

        py::enum_<SkMatrix::ScaleToFit>(_Matrix, "ScaleToFit", py::arithmetic())
            .value("K_FILL_SCALE_TO_FIT", SkMatrix::ScaleToFit::kFill_ScaleToFit)
            .value("K_START_SCALE_TO_FIT", SkMatrix::ScaleToFit::kStart_ScaleToFit)
            .value("K_CENTER_SCALE_TO_FIT", SkMatrix::ScaleToFit::kCenter_ScaleToFit)
            .value("K_END_SCALE_TO_FIT", SkMatrix::ScaleToFit::kEnd_ScaleToFit)
            .export_values()
        ;
        _Matrix
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
            )
        ;

        py::enum_<SkMatrix::TypeMask>(_Matrix, "TypeMask", py::arithmetic())
            .value("K_IDENTITY_MASK", SkMatrix::TypeMask::kIdentity_Mask)
            .value("K_TRANSLATE_MASK", SkMatrix::TypeMask::kTranslate_Mask)
            .value("K_SCALE_MASK", SkMatrix::TypeMask::kScale_Mask)
            .value("K_AFFINE_MASK", SkMatrix::TypeMask::kAffine_Mask)
            .value("K_PERSPECTIVE_MASK", SkMatrix::TypeMask::kPerspective_Mask)
            .export_values()
        ;
        _Matrix
        .def("get_type", &SkMatrix::getType
            )
        .def("is_identity", &SkMatrix::isIdentity
            )
        .def("is_scale_translate", &SkMatrix::isScaleTranslate
            )
        .def("is_translate", &SkMatrix::isTranslate
            )
        .def("rect_stays_rect", &SkMatrix::rectStaysRect
            )
        .def("preserves_axis_alignment", &SkMatrix::preservesAxisAlignment
            )
        .def("has_perspective", &SkMatrix::hasPerspective
            )
        .def("is_similarity", &SkMatrix::isSimilarity
            , py::arg("tol") = SK_ScalarNearlyZero
            )
        .def("preserves_right_angles", &SkMatrix::preservesRightAngles
            , py::arg("tol") = SK_ScalarNearlyZero
            )
        .def("get", &SkMatrix::get
            , py::arg("index")
            )
        .def("rc", &SkMatrix::rc
            , py::arg("r")
            , py::arg("c")
            )
        .def("get_scale_x", &SkMatrix::getScaleX
            )
        .def("get_scale_y", &SkMatrix::getScaleY
            )
        .def("get_skew_y", &SkMatrix::getSkewY
            )
        .def("get_skew_x", &SkMatrix::getSkewX
            )
        .def("get_translate_x", &SkMatrix::getTranslateX
            )
        .def("get_translate_y", &SkMatrix::getTranslateY
            )
        .def("get_persp_x", &SkMatrix::getPerspX
            )
        .def("get_persp_y", &SkMatrix::getPerspY
            )
        .def("set", &SkMatrix::set
            , py::arg("index")
            , py::arg("value")
            )
        .def("set_scale_x", &SkMatrix::setScaleX
            , py::arg("v")
            )
        .def("set_scale_y", &SkMatrix::setScaleY
            , py::arg("v")
            )
        .def("set_skew_y", &SkMatrix::setSkewY
            , py::arg("v")
            )
        .def("set_skew_x", &SkMatrix::setSkewX
            , py::arg("v")
            )
        .def("set_translate_x", &SkMatrix::setTranslateX
            , py::arg("v")
            )
        .def("set_translate_y", &SkMatrix::setTranslateY
            , py::arg("v")
            )
        .def("set_persp_x", &SkMatrix::setPerspX
            , py::arg("v")
            )
        .def("set_persp_y", &SkMatrix::setPerspY
            , py::arg("v")
            )
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
            )
        .def("get9", [](SkMatrix& self, std::array<SkScalar, 9>& buffer)
            {
                self.get9(&buffer[0]);
                return std::make_tuple(buffer);
            }
            , py::arg("buffer")
            )
        .def("set9", [](SkMatrix& self, std::array<SkScalar, 9>& buffer)
            {
                auto _ret = self.set9(&buffer[0]);
                return std::make_tuple(_ret, buffer);
            }
            , py::arg("buffer")
            )
        .def("reset", &SkMatrix::reset
            )
        .def("set_identity", &SkMatrix::setIdentity
            )
        .def("set_translate", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::setTranslate)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("set_translate", py::overload_cast<const SkVector &>(&SkMatrix::setTranslate)
            , py::arg("v")
            )
        .def("set_scale", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::setScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::arg("px")
            , py::arg("py")
            )
        .def("set_scale", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::setScale)
            , py::arg("sx")
            , py::arg("sy")
            )
        .def("set_rotate", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkMatrix::setRotate)
            , py::arg("degrees")
            , py::arg("px")
            , py::arg("py")
            )
        .def("set_rotate", py::overload_cast<SkScalar>(&SkMatrix::setRotate)
            , py::arg("degrees")
            )
        .def("set_sin_cos", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::setSinCos)
            , py::arg("sin_value")
            , py::arg("cos_value")
            , py::arg("px")
            , py::arg("py")
            )
        .def("set_sin_cos", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::setSinCos)
            , py::arg("sin_value")
            , py::arg("cos_value")
            )
        .def("set_rs_xform", &SkMatrix::setRSXform
            , py::arg("rsx_form")
            )
        .def("set_skew", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::setSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::arg("px")
            , py::arg("py")
            )
        .def("set_skew", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::setSkew)
            , py::arg("kx")
            , py::arg("ky")
            )
        .def("set_concat", &SkMatrix::setConcat
            , py::arg("a")
            , py::arg("b")
            )
        .def("pre_translate", &SkMatrix::preTranslate
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("pre_scale", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::preScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::arg("px")
            , py::arg("py")
            )
        .def("pre_scale", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::preScale)
            , py::arg("sx")
            , py::arg("sy")
            )
        .def("pre_rotate", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkMatrix::preRotate)
            , py::arg("degrees")
            , py::arg("px")
            , py::arg("py")
            )
        .def("pre_rotate", py::overload_cast<SkScalar>(&SkMatrix::preRotate)
            , py::arg("degrees")
            )
        .def("pre_skew", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::preSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::arg("px")
            , py::arg("py")
            )
        .def("pre_skew", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::preSkew)
            , py::arg("kx")
            , py::arg("ky")
            )
        .def("pre_concat", &SkMatrix::preConcat
            , py::arg("other")
            )
        .def("post_translate", &SkMatrix::postTranslate
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("post_scale", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::postScale)
            , py::arg("sx")
            , py::arg("sy")
            , py::arg("px")
            , py::arg("py")
            )
        .def("post_scale", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::postScale)
            , py::arg("sx")
            , py::arg("sy")
            )
        .def("post_rotate", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkMatrix::postRotate)
            , py::arg("degrees")
            , py::arg("px")
            , py::arg("py")
            )
        .def("post_rotate", py::overload_cast<SkScalar>(&SkMatrix::postRotate)
            , py::arg("degrees")
            )
        .def("post_skew", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::postSkew)
            , py::arg("kx")
            , py::arg("ky")
            , py::arg("px")
            , py::arg("py")
            )
        .def("post_skew", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::postSkew)
            , py::arg("kx")
            , py::arg("ky")
            )
        .def("post_concat", &SkMatrix::postConcat
            , py::arg("other")
            )
        .def("set_rect_to_rect", &SkMatrix::setRectToRect
            , py::arg("src")
            , py::arg("dst")
            , py::arg("stf")
            )
        .def_static("make_rect_to_rect", &SkMatrix::MakeRectToRect
            , py::arg("src")
            , py::arg("dst")
            , py::arg("stf")
            )
        .def("set_poly_to_poly", &SkMatrix::setPolyToPoly
            , py::arg("src")
            , py::arg("dst")
            , py::arg("count")
            )
        .def("invert", &SkMatrix::invert
            , py::arg("inverse")
            )
        .def_static("set_affine_identity", [](std::array<SkScalar, 6>& affine)
            {
                SkMatrix::SetAffineIdentity(&affine[0]);
                return std::make_tuple(affine);
            }
            , py::arg("affine")
            )
        .def("as_affine", [](SkMatrix& self, std::array<SkScalar, 6>& affine)
            {
                auto _ret = self.asAffine(&affine[0]);
                return std::make_tuple(_ret, affine);
            }
            , py::arg("affine")
            )
        .def("set_affine", [](SkMatrix& self, std::array<SkScalar, 6>& affine)
            {
                auto _ret = self.setAffine(&affine[0]);
                return std::make_tuple(_ret, affine);
            }
            , py::arg("affine")
            )
        .def("normalize_perspective", &SkMatrix::normalizePerspective
            )
        .def("map_points", py::overload_cast<SkPoint[], const SkPoint[], int>(&SkMatrix::mapPoints, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("count")
            )
        .def("map_points", py::overload_cast<SkPoint[], int>(&SkMatrix::mapPoints, py::const_)
            , py::arg("pts")
            , py::arg("count")
            )
        .def("map_homogeneous_points", py::overload_cast<SkPoint3[], const SkPoint3[], int>(&SkMatrix::mapHomogeneousPoints, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("count")
            )
        .def("map_homogeneous_points", py::overload_cast<SkPoint3[], const SkPoint[], int>(&SkMatrix::mapHomogeneousPoints, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("count")
            )
        .def("map_point", &SkMatrix::mapPoint
            , py::arg("pt")
            )
        .def("map_xy", py::overload_cast<SkScalar, SkScalar, SkPoint *>(&SkMatrix::mapXY, py::const_)
            , py::arg("x")
            , py::arg("y")
            , py::arg("result")
            )
        .def("map_xy", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::mapXY, py::const_)
            , py::arg("x")
            , py::arg("y")
            )
        .def("map_origin", &SkMatrix::mapOrigin
            )
        .def("map_vectors", py::overload_cast<SkVector[], const SkVector[], int>(&SkMatrix::mapVectors, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("count")
            )
        .def("map_vectors", py::overload_cast<SkVector[], int>(&SkMatrix::mapVectors, py::const_)
            , py::arg("vecs")
            , py::arg("count")
            )
        .def("map_vector", py::overload_cast<SkScalar, SkScalar, SkVector *>(&SkMatrix::mapVector, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            , py::arg("result")
            )
        .def("map_vector", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::mapVector, py::const_)
            , py::arg("dx")
            , py::arg("dy")
            )
        .def("map_rect", py::overload_cast<SkRect *, const SkRect &, SkApplyPerspectiveClip>(&SkMatrix::mapRect, py::const_)
            , py::arg("dst")
            , py::arg("src")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            )
        .def("map_rect", py::overload_cast<SkRect *, SkApplyPerspectiveClip>(&SkMatrix::mapRect, py::const_)
            , py::arg("rect")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            )
        .def("map_rect", py::overload_cast<const SkRect &, SkApplyPerspectiveClip>(&SkMatrix::mapRect, py::const_)
            , py::arg("src")
            , py::arg("pc") = SkApplyPerspectiveClip::kYes
            )
        .def("map_rect_to_quad", [](SkMatrix& self, std::array<SkPoint, 4>& dst, const SkRect & rect)
            {
                return self.mapRectToQuad(&dst[0], rect);
            }
            , py::arg("dst")
            , py::arg("rect")
            )
        .def("map_rect_scale_translate", &SkMatrix::mapRectScaleTranslate
            , py::arg("dst")
            , py::arg("src")
            )
        .def("map_radius", &SkMatrix::mapRadius
            , py::arg("radius")
            )
        .def("dump", &SkMatrix::dump
            )
        .def("get_min_scale", &SkMatrix::getMinScale
            )
        .def("get_max_scale", &SkMatrix::getMaxScale
            )
        .def("get_min_max_scales", [](SkMatrix& self, std::array<SkScalar, 2>& scaleFactors)
            {
                auto _ret = self.getMinMaxScales(&scaleFactors[0]);
                return std::make_tuple(_ret, scaleFactors);
            }
            , py::arg("scale_factors")
            )
        .def("decompose_scale", &SkMatrix::decomposeScale
            , py::arg("scale")
            , py::arg("remaining") = nullptr
            )
        .def_static("i", &SkMatrix::I
            )
        .def_static("invalid_matrix", &SkMatrix::InvalidMatrix
            )
        .def_static("concat", &SkMatrix::Concat
            , py::arg("a")
            , py::arg("b")
            )
        .def("dirty_matrix_type_cache", &SkMatrix::dirtyMatrixTypeCache
            )
        .def("set_scale_translate", &SkMatrix::setScaleTranslate
            , py::arg("sx")
            , py::arg("sy")
            , py::arg("tx")
            , py::arg("ty")
            )
        .def("is_finite", &SkMatrix::isFinite
            )
    ;


}