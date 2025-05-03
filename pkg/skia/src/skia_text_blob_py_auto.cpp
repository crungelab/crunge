#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkTextBlob.h>
#include <include/core/SkSerialProcs.h>
#include <include/core/SkData.h>
#include <include/core/SkRSXform.h>
#include <include/core/SkPaint.h>

namespace py = pybind11;

template<>
struct py::detail::has_operator_delete<SkTextBlob, void> : std::false_type {};

void init_skia_text_blob_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkTextBlob,sk_sp<SkTextBlob>> TextBlob(_skia, "TextBlob");
    registry.on(_skia, "TextBlob", TextBlob);
        TextBlob
        .def("bounds", &SkTextBlob::bounds
            , py::return_value_policy::reference)
        .def("unique_id", &SkTextBlob::uniqueID
            , py::return_value_policy::automatic_reference)
        .def("get_intercepts", [](SkTextBlob& self, std::array<float, 2>& bounds, float intervals[], const SkPaint * paint)
            {
                auto ret = self.getIntercepts(&bounds[0], intervals, paint);
                return std::make_tuple(ret, bounds);
            }
            , py::arg("bounds")
            , py::arg("intervals")
            , py::arg("paint") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_text", &SkTextBlob::MakeFromText
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("font")
            , py::arg("encoding") = SkTextEncoding::kUTF8
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_string", &SkTextBlob::MakeFromString
            , py::arg("string")
            , py::arg("font")
            , py::arg("encoding") = SkTextEncoding::kUTF8
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_pos_text_h", &SkTextBlob::MakeFromPosTextH
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("xpos")
            , py::arg("const_y")
            , py::arg("font")
            , py::arg("encoding") = SkTextEncoding::kUTF8
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_pos_text", &SkTextBlob::MakeFromPosText
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("pos")
            , py::arg("font")
            , py::arg("encoding") = SkTextEncoding::kUTF8
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_rs_xform", &SkTextBlob::MakeFromRSXform
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("xform")
            , py::arg("font")
            , py::arg("encoding") = SkTextEncoding::kUTF8
            , py::return_value_policy::automatic_reference)
        .def("serialize", py::overload_cast<const SkSerialProcs &, void *, unsigned long>(&SkTextBlob::serialize, py::const_)
            , py::arg("procs")
            , py::arg("memory")
            , py::arg("memory_size")
            , py::return_value_policy::automatic_reference)
        .def("serialize", py::overload_cast<const SkSerialProcs &>(&SkTextBlob::serialize, py::const_)
            , py::arg("procs")
            , py::return_value_policy::automatic_reference)
        .def_static("deserialize", &SkTextBlob::Deserialize
            , py::arg("data")
            , py::arg("size")
            , py::arg("procs")
            , py::return_value_policy::automatic_reference)
        ;

        py::class_<SkTextBlob::Iter> TextBlobIter(_skia, "TextBlobIter");
        registry.on(_skia, "TextBlobIter", TextBlobIter);
            py::class_<SkTextBlob::Iter::Run> TextBlobIterRun(_skia, "TextBlobIterRun");
            registry.on(_skia, "TextBlobIterRun", TextBlobIterRun);
                TextBlobIterRun
                .def_readwrite("f_typeface", &SkTextBlob::Iter::Run::fTypeface)
                .def_readwrite("f_glyph_count", &SkTextBlob::Iter::Run::fGlyphCount)
                .def_readwrite("f_glyph_indices", &SkTextBlob::Iter::Run::fGlyphIndices)
            ;

            TextBlobIter
            .def(py::init<const SkTextBlob &>()
            , py::arg("")
            )
            .def("next", &SkTextBlob::Iter::next
                , py::arg("")
                , py::return_value_policy::automatic_reference)
            ;

            py::class_<SkTextBlob::Iter::ExperimentalRun> TextBlobIterExperimentalRun(_skia, "TextBlobIterExperimentalRun");
            registry.on(_skia, "TextBlobIterExperimentalRun", TextBlobIterExperimentalRun);
                TextBlobIterExperimentalRun
                .def_readwrite("font", &SkTextBlob::Iter::ExperimentalRun::font)
                .def_readwrite("count", &SkTextBlob::Iter::ExperimentalRun::count)
                .def_readwrite("glyphs", &SkTextBlob::Iter::ExperimentalRun::glyphs)
                .def_readwrite("positions", &SkTextBlob::Iter::ExperimentalRun::positions)
            ;

            TextBlobIter
            .def("experimental_next", &SkTextBlob::Iter::experimentalNext
                , py::arg("")
                , py::return_value_policy::automatic_reference)
        ;

    py::class_<SkTextBlobBuilder> TextBlobBuilder(_skia, "TextBlobBuilder");
    registry.on(_skia, "TextBlobBuilder", TextBlobBuilder);
        TextBlobBuilder
        .def(py::init<>())
        .def("make", &SkTextBlobBuilder::make
            , py::return_value_policy::automatic_reference)
        ;

        py::class_<SkTextBlobBuilder::RunBuffer> TextBlobBuilderRunBuffer(_skia, "TextBlobBuilderRunBuffer");
        registry.on(_skia, "TextBlobBuilderRunBuffer", TextBlobBuilderRunBuffer);
            TextBlobBuilderRunBuffer
            .def_readwrite("glyphs", &SkTextBlobBuilder::RunBuffer::glyphs)
            .def_readwrite("pos", &SkTextBlobBuilder::RunBuffer::pos)
            .def_property("utf8text",
                [](const SkTextBlobBuilder::RunBuffer& self){ return self.utf8text; },
                [](SkTextBlobBuilder::RunBuffer& self, const char* source){ self.utf8text = strdup(source); }
            )
            .def_readwrite("clusters", &SkTextBlobBuilder::RunBuffer::clusters)
            .def("points", &SkTextBlobBuilder::RunBuffer::points
                , py::return_value_policy::automatic_reference)
            .def("xforms", &SkTextBlobBuilder::RunBuffer::xforms
                , py::return_value_policy::automatic_reference)
        ;

        TextBlobBuilder
        .def("alloc_run", &SkTextBlobBuilder::allocRun
            , py::arg("font")
            , py::arg("count")
            , py::arg("x")
            , py::arg("y")
            , py::arg("bounds") = nullptr
            , py::return_value_policy::reference)
        .def("alloc_run_pos_h", &SkTextBlobBuilder::allocRunPosH
            , py::arg("font")
            , py::arg("count")
            , py::arg("y")
            , py::arg("bounds") = nullptr
            , py::return_value_policy::reference)
        .def("alloc_run_pos", &SkTextBlobBuilder::allocRunPos
            , py::arg("font")
            , py::arg("count")
            , py::arg("bounds") = nullptr
            , py::return_value_policy::reference)
        .def("alloc_run_rs_xform", &SkTextBlobBuilder::allocRunRSXform
            , py::arg("font")
            , py::arg("count")
            , py::return_value_policy::reference)
        .def("alloc_run_text", &SkTextBlobBuilder::allocRunText
            , py::arg("font")
            , py::arg("count")
            , py::arg("x")
            , py::arg("y")
            , py::arg("text_byte_count")
            , py::arg("bounds") = nullptr
            , py::return_value_policy::reference)
        .def("alloc_run_text_pos_h", &SkTextBlobBuilder::allocRunTextPosH
            , py::arg("font")
            , py::arg("count")
            , py::arg("y")
            , py::arg("text_byte_count")
            , py::arg("bounds") = nullptr
            , py::return_value_policy::reference)
        .def("alloc_run_text_pos", &SkTextBlobBuilder::allocRunTextPos
            , py::arg("font")
            , py::arg("count")
            , py::arg("text_byte_count")
            , py::arg("bounds") = nullptr
            , py::return_value_policy::reference)
        .def("alloc_run_text_rs_xform", &SkTextBlobBuilder::allocRunTextRSXform
            , py::arg("font")
            , py::arg("count")
            , py::arg("text_byte_count")
            , py::arg("bounds") = nullptr
            , py::return_value_policy::reference)
    ;


}