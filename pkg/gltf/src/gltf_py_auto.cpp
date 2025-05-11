#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <tiny_gltf.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/gltf/conversions.h>

namespace py = pybind11;

using namespace tinygltf;

void init_generated(py::module &_gltf, Registry &registry) {
    py::enum_<tinygltf::Type>(_gltf, "Type", py::arithmetic())
        .value("NULL_TYPE", tinygltf::Type::NULL_TYPE)
        .value("REAL_TYPE", tinygltf::Type::REAL_TYPE)
        .value("INT_TYPE", tinygltf::Type::INT_TYPE)
        .value("BOOL_TYPE", tinygltf::Type::BOOL_TYPE)
        .value("STRING_TYPE", tinygltf::Type::STRING_TYPE)
        .value("ARRAY_TYPE", tinygltf::Type::ARRAY_TYPE)
        .value("BINARY_TYPE", tinygltf::Type::BINARY_TYPE)
        .value("OBJECT_TYPE", tinygltf::Type::OBJECT_TYPE)
        .export_values()
    ;
    py::enum_<tinygltf::ParseStrictness>(_gltf, "ParseStrictness", py::arithmetic())
        .value("PERMISSIVE", tinygltf::ParseStrictness::Permissive)
        .value("STRICT", tinygltf::ParseStrictness::Strict)
        .export_values()
    ;
    _gltf
    .def("get_component_size_in_bytes", &tinygltf::GetComponentSizeInBytes
        , py::arg("component_type")
        , py::return_value_policy::automatic_reference)
    .def("get_num_components_in_type", &tinygltf::GetNumComponentsInType
        , py::arg("ty")
        , py::return_value_policy::automatic_reference)
    .def("is_data_uri", &tinygltf::IsDataURI
        , py::arg("in")
        , py::return_value_policy::automatic_reference)
    .def("decode_data_uri", [](std::vector<unsigned char> * out, std::basic_string<char> & mime_type, const std::basic_string<char> & in, unsigned long reqBytes, bool checkSize)
        {
            auto ret = tinygltf::DecodeDataURI(out, mime_type, in, reqBytes, checkSize);
            return std::make_tuple(ret, mime_type);
        }
        , py::arg("out")
        , py::arg("mime_type")
        , py::arg("in")
        , py::arg("req_bytes")
        , py::arg("check_size")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<tinygltf::Value> Value(_gltf, "Value");
    registry.on(_gltf, "Value", Value);
        Value
        .def(py::init<>())
        .def(py::init<bool>()
        , py::arg("b")
        )
        .def(py::init<int>()
        , py::arg("i")
        )
        .def(py::init<double>()
        , py::arg("n")
        )
        .def(py::init<const std::basic_string<char> &>()
        , py::arg("s")
        )
        .def(py::init<const char *>()
        , py::arg("s")
        )
        .def(py::init<const unsigned char *, unsigned long>()
        , py::arg("p")
        , py::arg("n")
        )
        .def(py::init<const std::vector<tinygltf::Value> &>()
        , py::arg("a")
        )
        .def(py::init<const std::map<std::basic_string<char>, tinygltf::Value> &>()
        , py::arg("o")
        )
        .def(py::init<const tinygltf::Value &>()
        , py::arg("")
        )
        .def("type", &tinygltf::Value::Type
            , py::return_value_policy::automatic_reference)
        .def("is_bool", &tinygltf::Value::IsBool
            , py::return_value_policy::automatic_reference)
        .def("is_int", &tinygltf::Value::IsInt
            , py::return_value_policy::automatic_reference)
        .def("is_number", &tinygltf::Value::IsNumber
            , py::return_value_policy::automatic_reference)
        .def("is_real", &tinygltf::Value::IsReal
            , py::return_value_policy::automatic_reference)
        .def("is_string", &tinygltf::Value::IsString
            , py::return_value_policy::automatic_reference)
        .def("is_binary", &tinygltf::Value::IsBinary
            , py::return_value_policy::automatic_reference)
        .def("is_array", &tinygltf::Value::IsArray
            , py::return_value_policy::automatic_reference)
        .def("is_object", &tinygltf::Value::IsObject
            , py::return_value_policy::automatic_reference)
        .def("get_number_as_double", &tinygltf::Value::GetNumberAsDouble
            , py::return_value_policy::automatic_reference)
        .def("get_number_as_int", &tinygltf::Value::GetNumberAsInt
            , py::return_value_policy::automatic_reference)
        .def("array_len", &tinygltf::Value::ArrayLen
            , py::return_value_policy::automatic_reference)
        .def("has", &tinygltf::Value::Has
            , py::arg("key")
            , py::return_value_policy::automatic_reference)
        .def("keys", &tinygltf::Value::Keys
            , py::return_value_policy::automatic_reference)
        .def("size", &tinygltf::Value::Size
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<tinygltf::Parameter> Parameter(_gltf, "Parameter");
    registry.on(_gltf, "Parameter", Parameter);
        Parameter
        .def_readwrite("bool_value", &tinygltf::Parameter::bool_value)
        .def_readwrite("has_number_value", &tinygltf::Parameter::has_number_value)
        .def_readwrite("string_value", &tinygltf::Parameter::string_value)
        .def_readwrite("number_array", &tinygltf::Parameter::number_array)
        .def_readwrite("json_double_value", &tinygltf::Parameter::json_double_value)
        .def_readwrite("number_value", &tinygltf::Parameter::number_value)
        .def("texture_index", &tinygltf::Parameter::TextureIndex
            , py::return_value_policy::automatic_reference)
        .def("texture_tex_coord", &tinygltf::Parameter::TextureTexCoord
            , py::return_value_policy::automatic_reference)
        .def("texture_scale", &tinygltf::Parameter::TextureScale
            , py::return_value_policy::automatic_reference)
        .def("texture_strength", &tinygltf::Parameter::TextureStrength
            , py::return_value_policy::automatic_reference)
        .def("factor", &tinygltf::Parameter::Factor
            , py::return_value_policy::automatic_reference)
        .def("color_factor", &tinygltf::Parameter::ColorFactor
            , py::return_value_policy::automatic_reference)
        .def(py::init<>())
        .def(py::init<const tinygltf::Parameter &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::AnimationChannel> AnimationChannel(_gltf, "AnimationChannel");
    registry.on(_gltf, "AnimationChannel", AnimationChannel);
        AnimationChannel
        .def_readwrite("sampler", &tinygltf::AnimationChannel::sampler)
        .def_readwrite("target_node", &tinygltf::AnimationChannel::target_node)
        .def_readwrite("target_path", &tinygltf::AnimationChannel::target_path)
        .def_readwrite("extras", &tinygltf::AnimationChannel::extras)
        .def_readwrite("extensions", &tinygltf::AnimationChannel::extensions)
        .def_readwrite("target_extras", &tinygltf::AnimationChannel::target_extras)
        .def_readwrite("target_extensions", &tinygltf::AnimationChannel::target_extensions)
        .def_readwrite("extras_json_string", &tinygltf::AnimationChannel::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::AnimationChannel::extensions_json_string)
        .def_readwrite("target_extras_json_string", &tinygltf::AnimationChannel::target_extras_json_string)
        .def_readwrite("target_extensions_json_string", &tinygltf::AnimationChannel::target_extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::AnimationChannel &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::AnimationSampler> AnimationSampler(_gltf, "AnimationSampler");
    registry.on(_gltf, "AnimationSampler", AnimationSampler);
        AnimationSampler
        .def_readwrite("input", &tinygltf::AnimationSampler::input)
        .def_readwrite("output", &tinygltf::AnimationSampler::output)
        .def_readwrite("interpolation", &tinygltf::AnimationSampler::interpolation)
        .def_readwrite("extras", &tinygltf::AnimationSampler::extras)
        .def_readwrite("extensions", &tinygltf::AnimationSampler::extensions)
        .def_readwrite("extras_json_string", &tinygltf::AnimationSampler::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::AnimationSampler::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::AnimationSampler &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Animation> Animation(_gltf, "Animation");
    registry.on(_gltf, "Animation", Animation);
        Animation
        .def_readwrite("name", &tinygltf::Animation::name)
        .def_readwrite("channels", &tinygltf::Animation::channels)
        .def_readwrite("samplers", &tinygltf::Animation::samplers)
        .def_readwrite("extras", &tinygltf::Animation::extras)
        .def_readwrite("extensions", &tinygltf::Animation::extensions)
        .def_readwrite("extras_json_string", &tinygltf::Animation::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Animation::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Animation &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Skin> Skin(_gltf, "Skin");
    registry.on(_gltf, "Skin", Skin);
        Skin
        .def_readwrite("name", &tinygltf::Skin::name)
        .def_readwrite("inverse_bind_matrices", &tinygltf::Skin::inverseBindMatrices)
        .def_readwrite("skeleton", &tinygltf::Skin::skeleton)
        .def_readwrite("joints", &tinygltf::Skin::joints)
        .def_readwrite("extras", &tinygltf::Skin::extras)
        .def_readwrite("extensions", &tinygltf::Skin::extensions)
        .def_readwrite("extras_json_string", &tinygltf::Skin::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Skin::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Skin &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Sampler> Sampler(_gltf, "Sampler");
    registry.on(_gltf, "Sampler", Sampler);
        Sampler
        .def_readwrite("name", &tinygltf::Sampler::name)
        .def_readwrite("min_filter", &tinygltf::Sampler::minFilter)
        .def_readwrite("mag_filter", &tinygltf::Sampler::magFilter)
        .def_readwrite("wrap_s", &tinygltf::Sampler::wrapS)
        .def_readwrite("wrap_t", &tinygltf::Sampler::wrapT)
        .def_readwrite("extras", &tinygltf::Sampler::extras)
        .def_readwrite("extensions", &tinygltf::Sampler::extensions)
        .def_readwrite("extras_json_string", &tinygltf::Sampler::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Sampler::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Sampler &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Image> Image(_gltf, "Image");
    registry.on(_gltf, "Image", Image);
        Image
        .def_readwrite("name", &tinygltf::Image::name)
        .def_readwrite("width", &tinygltf::Image::width)
        .def_readwrite("height", &tinygltf::Image::height)
        .def_readwrite("component", &tinygltf::Image::component)
        .def_readwrite("bits", &tinygltf::Image::bits)
        .def_readwrite("pixel_type", &tinygltf::Image::pixel_type)
        .def_readwrite("image", &tinygltf::Image::image)
        .def_readwrite("buffer_view", &tinygltf::Image::bufferView)
        .def_readwrite("mime_type", &tinygltf::Image::mimeType)
        .def_readwrite("uri", &tinygltf::Image::uri)
        .def_readwrite("extras", &tinygltf::Image::extras)
        .def_readwrite("extensions", &tinygltf::Image::extensions)
        .def_readwrite("extras_json_string", &tinygltf::Image::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Image::extensions_json_string)
        .def_readwrite("as_is", &tinygltf::Image::as_is)
        .def(py::init<>())
        .def(py::init<const tinygltf::Image &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Texture> Texture(_gltf, "Texture");
    registry.on(_gltf, "Texture", Texture);
        Texture
        .def_readwrite("name", &tinygltf::Texture::name)
        .def_readwrite("sampler", &tinygltf::Texture::sampler)
        .def_readwrite("source", &tinygltf::Texture::source)
        .def_readwrite("extras", &tinygltf::Texture::extras)
        .def_readwrite("extensions", &tinygltf::Texture::extensions)
        .def_readwrite("extras_json_string", &tinygltf::Texture::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Texture::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Texture &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::TextureInfo> TextureInfo(_gltf, "TextureInfo");
    registry.on(_gltf, "TextureInfo", TextureInfo);
        TextureInfo
        .def_readwrite("index", &tinygltf::TextureInfo::index)
        .def_readwrite("tex_coord", &tinygltf::TextureInfo::texCoord)
        .def_readwrite("extras", &tinygltf::TextureInfo::extras)
        .def_readwrite("extensions", &tinygltf::TextureInfo::extensions)
        .def_readwrite("extras_json_string", &tinygltf::TextureInfo::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::TextureInfo::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::TextureInfo &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::NormalTextureInfo> NormalTextureInfo(_gltf, "NormalTextureInfo");
    registry.on(_gltf, "NormalTextureInfo", NormalTextureInfo);
        NormalTextureInfo
        .def_readwrite("index", &tinygltf::NormalTextureInfo::index)
        .def_readwrite("tex_coord", &tinygltf::NormalTextureInfo::texCoord)
        .def_readwrite("scale", &tinygltf::NormalTextureInfo::scale)
        .def_readwrite("extras", &tinygltf::NormalTextureInfo::extras)
        .def_readwrite("extensions", &tinygltf::NormalTextureInfo::extensions)
        .def_readwrite("extras_json_string", &tinygltf::NormalTextureInfo::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::NormalTextureInfo::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::NormalTextureInfo &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::OcclusionTextureInfo> OcclusionTextureInfo(_gltf, "OcclusionTextureInfo");
    registry.on(_gltf, "OcclusionTextureInfo", OcclusionTextureInfo);
        OcclusionTextureInfo
        .def_readwrite("index", &tinygltf::OcclusionTextureInfo::index)
        .def_readwrite("tex_coord", &tinygltf::OcclusionTextureInfo::texCoord)
        .def_readwrite("strength", &tinygltf::OcclusionTextureInfo::strength)
        .def_readwrite("extras", &tinygltf::OcclusionTextureInfo::extras)
        .def_readwrite("extensions", &tinygltf::OcclusionTextureInfo::extensions)
        .def_readwrite("extras_json_string", &tinygltf::OcclusionTextureInfo::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::OcclusionTextureInfo::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::OcclusionTextureInfo &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::PbrMetallicRoughness> PbrMetallicRoughness(_gltf, "PbrMetallicRoughness");
    registry.on(_gltf, "PbrMetallicRoughness", PbrMetallicRoughness);
        PbrMetallicRoughness
        .def_readwrite("base_color_factor", &tinygltf::PbrMetallicRoughness::baseColorFactor)
        .def_readwrite("base_color_texture", &tinygltf::PbrMetallicRoughness::baseColorTexture)
        .def_readwrite("metallic_factor", &tinygltf::PbrMetallicRoughness::metallicFactor)
        .def_readwrite("roughness_factor", &tinygltf::PbrMetallicRoughness::roughnessFactor)
        .def_readwrite("metallic_roughness_texture", &tinygltf::PbrMetallicRoughness::metallicRoughnessTexture)
        .def_readwrite("extras", &tinygltf::PbrMetallicRoughness::extras)
        .def_readwrite("extensions", &tinygltf::PbrMetallicRoughness::extensions)
        .def_readwrite("extras_json_string", &tinygltf::PbrMetallicRoughness::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::PbrMetallicRoughness::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::PbrMetallicRoughness &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Material> Material(_gltf, "Material");
    registry.on(_gltf, "Material", Material);
        Material
        .def_readwrite("name", &tinygltf::Material::name)
        .def_readwrite("emissive_factor", &tinygltf::Material::emissiveFactor)
        .def_readwrite("alpha_mode", &tinygltf::Material::alphaMode)
        .def_readwrite("alpha_cutoff", &tinygltf::Material::alphaCutoff)
        .def_readwrite("double_sided", &tinygltf::Material::doubleSided)
        .def_readwrite("pbr_metallic_roughness", &tinygltf::Material::pbrMetallicRoughness)
        .def_readwrite("normal_texture", &tinygltf::Material::normalTexture)
        .def_readwrite("occlusion_texture", &tinygltf::Material::occlusionTexture)
        .def_readwrite("emissive_texture", &tinygltf::Material::emissiveTexture)
        .def_readwrite("values", &tinygltf::Material::values)
        .def_readwrite("additional_values", &tinygltf::Material::additionalValues)
        .def_readwrite("extensions", &tinygltf::Material::extensions)
        .def_readwrite("extras", &tinygltf::Material::extras)
        .def_readwrite("extras_json_string", &tinygltf::Material::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Material::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Material &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::BufferView> BufferView(_gltf, "BufferView");
    registry.on(_gltf, "BufferView", BufferView);
        BufferView
        .def_readwrite("name", &tinygltf::BufferView::name)
        .def_readwrite("buffer", &tinygltf::BufferView::buffer)
        .def_readwrite("byte_offset", &tinygltf::BufferView::byteOffset)
        .def_readwrite("byte_length", &tinygltf::BufferView::byteLength)
        .def_readwrite("byte_stride", &tinygltf::BufferView::byteStride)
        .def_readwrite("target", &tinygltf::BufferView::target)
        .def_readwrite("extras", &tinygltf::BufferView::extras)
        .def_readwrite("extensions", &tinygltf::BufferView::extensions)
        .def_readwrite("extras_json_string", &tinygltf::BufferView::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::BufferView::extensions_json_string)
        .def_readwrite("draco_decoded", &tinygltf::BufferView::dracoDecoded)
        .def(py::init<>())
        .def(py::init<const tinygltf::BufferView &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Accessor> Accessor(_gltf, "Accessor");
    registry.on(_gltf, "Accessor", Accessor);
        Accessor
        .def_readwrite("buffer_view", &tinygltf::Accessor::bufferView)
        .def_readwrite("name", &tinygltf::Accessor::name)
        .def_readwrite("byte_offset", &tinygltf::Accessor::byteOffset)
        .def_readwrite("normalized", &tinygltf::Accessor::normalized)
        .def_readwrite("component_type", &tinygltf::Accessor::componentType)
        .def_readwrite("count", &tinygltf::Accessor::count)
        .def_readwrite("type", &tinygltf::Accessor::type)
        .def_readwrite("extras", &tinygltf::Accessor::extras)
        .def_readwrite("extensions", &tinygltf::Accessor::extensions)
        .def_readwrite("extras_json_string", &tinygltf::Accessor::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Accessor::extensions_json_string)
        .def_readwrite("min_values", &tinygltf::Accessor::minValues)
        .def_readwrite("max_values", &tinygltf::Accessor::maxValues)
        ;

        py::class_<tinygltf::Accessor::Sparse> AccessorSparse(_gltf, "AccessorSparse");
        registry.on(_gltf, "AccessorSparse", AccessorSparse);
            AccessorSparse
            .def_readwrite("count", &tinygltf::Accessor::Sparse::count)
            .def_readwrite("is_sparse", &tinygltf::Accessor::Sparse::isSparse)
            ;

            py::class_<tinygltf::Accessor::Sparse::Indices> AccessorSparseIndices(_gltf, "AccessorSparseIndices");
            registry.on(_gltf, "AccessorSparseIndices", AccessorSparseIndices);
                AccessorSparseIndices
                .def_readwrite("byte_offset", &tinygltf::Accessor::Sparse::Indices::byteOffset)
                .def_readwrite("buffer_view", &tinygltf::Accessor::Sparse::Indices::bufferView)
                .def_readwrite("component_type", &tinygltf::Accessor::Sparse::Indices::componentType)
                .def_readwrite("extras", &tinygltf::Accessor::Sparse::Indices::extras)
                .def_readwrite("extensions", &tinygltf::Accessor::Sparse::Indices::extensions)
                .def_readwrite("extras_json_string", &tinygltf::Accessor::Sparse::Indices::extras_json_string)
                .def_readwrite("extensions_json_string", &tinygltf::Accessor::Sparse::Indices::extensions_json_string)
            ;

            AccessorSparse
            .def_readwrite("indices", &tinygltf::Accessor::Sparse::indices)
            ;

            py::class_<tinygltf::Accessor::Sparse::Values> AccessorSparseValues(_gltf, "AccessorSparseValues");
            registry.on(_gltf, "AccessorSparseValues", AccessorSparseValues);
                AccessorSparseValues
                .def_readwrite("buffer_view", &tinygltf::Accessor::Sparse::Values::bufferView)
                .def_readwrite("byte_offset", &tinygltf::Accessor::Sparse::Values::byteOffset)
                .def_readwrite("extras", &tinygltf::Accessor::Sparse::Values::extras)
                .def_readwrite("extensions", &tinygltf::Accessor::Sparse::Values::extensions)
                .def_readwrite("extras_json_string", &tinygltf::Accessor::Sparse::Values::extras_json_string)
                .def_readwrite("extensions_json_string", &tinygltf::Accessor::Sparse::Values::extensions_json_string)
            ;

            AccessorSparse
            .def_readwrite("values", &tinygltf::Accessor::Sparse::values)
            .def_readwrite("extras", &tinygltf::Accessor::Sparse::extras)
            .def_readwrite("extensions", &tinygltf::Accessor::Sparse::extensions)
            .def_readwrite("extras_json_string", &tinygltf::Accessor::Sparse::extras_json_string)
            .def_readwrite("extensions_json_string", &tinygltf::Accessor::Sparse::extensions_json_string)
        ;

        Accessor
        .def_readwrite("sparse", &tinygltf::Accessor::sparse)
        .def("byte_stride", &tinygltf::Accessor::ByteStride
            , py::arg("buffer_view_object")
            , py::return_value_policy::automatic_reference)
        .def(py::init<>())
        .def(py::init<const tinygltf::Accessor &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::PerspectiveCamera> PerspectiveCamera(_gltf, "PerspectiveCamera");
    registry.on(_gltf, "PerspectiveCamera", PerspectiveCamera);
        PerspectiveCamera
        .def_readwrite("aspect_ratio", &tinygltf::PerspectiveCamera::aspectRatio)
        .def_readwrite("yfov", &tinygltf::PerspectiveCamera::yfov)
        .def_readwrite("zfar", &tinygltf::PerspectiveCamera::zfar)
        .def_readwrite("znear", &tinygltf::PerspectiveCamera::znear)
        .def(py::init<>())
        .def(py::init<const tinygltf::PerspectiveCamera &>()
        , py::arg("")
        )
        .def_readwrite("extensions", &tinygltf::PerspectiveCamera::extensions)
        .def_readwrite("extras", &tinygltf::PerspectiveCamera::extras)
        .def_readwrite("extras_json_string", &tinygltf::PerspectiveCamera::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::PerspectiveCamera::extensions_json_string)
    ;

    py::class_<tinygltf::OrthographicCamera> OrthographicCamera(_gltf, "OrthographicCamera");
    registry.on(_gltf, "OrthographicCamera", OrthographicCamera);
        OrthographicCamera
        .def_readwrite("xmag", &tinygltf::OrthographicCamera::xmag)
        .def_readwrite("ymag", &tinygltf::OrthographicCamera::ymag)
        .def_readwrite("zfar", &tinygltf::OrthographicCamera::zfar)
        .def_readwrite("znear", &tinygltf::OrthographicCamera::znear)
        .def(py::init<>())
        .def(py::init<const tinygltf::OrthographicCamera &>()
        , py::arg("")
        )
        .def_readwrite("extensions", &tinygltf::OrthographicCamera::extensions)
        .def_readwrite("extras", &tinygltf::OrthographicCamera::extras)
        .def_readwrite("extras_json_string", &tinygltf::OrthographicCamera::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::OrthographicCamera::extensions_json_string)
    ;

    py::class_<tinygltf::Camera> Camera(_gltf, "Camera");
    registry.on(_gltf, "Camera", Camera);
        Camera
        .def_readwrite("type", &tinygltf::Camera::type)
        .def_readwrite("name", &tinygltf::Camera::name)
        .def_readwrite("perspective", &tinygltf::Camera::perspective)
        .def_readwrite("orthographic", &tinygltf::Camera::orthographic)
        .def(py::init<>())
        .def(py::init<const tinygltf::Camera &>()
        , py::arg("")
        )
        .def_readwrite("extensions", &tinygltf::Camera::extensions)
        .def_readwrite("extras", &tinygltf::Camera::extras)
        .def_readwrite("extras_json_string", &tinygltf::Camera::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Camera::extensions_json_string)
    ;

    py::class_<tinygltf::Primitive> Primitive(_gltf, "Primitive");
    registry.on(_gltf, "Primitive", Primitive);
        Primitive
        .def_readwrite("attributes", &tinygltf::Primitive::attributes)
        .def_readwrite("material", &tinygltf::Primitive::material)
        .def_readwrite("indices", &tinygltf::Primitive::indices)
        .def_readwrite("mode", &tinygltf::Primitive::mode)
        .def_readwrite("targets", &tinygltf::Primitive::targets)
        .def_readwrite("extensions", &tinygltf::Primitive::extensions)
        .def_readwrite("extras", &tinygltf::Primitive::extras)
        .def_readwrite("extras_json_string", &tinygltf::Primitive::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Primitive::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Primitive &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Mesh> Mesh(_gltf, "Mesh");
    registry.on(_gltf, "Mesh", Mesh);
        Mesh
        .def_readwrite("name", &tinygltf::Mesh::name)
        .def_readwrite("primitives", &tinygltf::Mesh::primitives)
        .def_readwrite("weights", &tinygltf::Mesh::weights)
        .def_readwrite("extensions", &tinygltf::Mesh::extensions)
        .def_readwrite("extras", &tinygltf::Mesh::extras)
        .def_readwrite("extras_json_string", &tinygltf::Mesh::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Mesh::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Mesh &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Node> Node(_gltf, "Node");
    registry.on(_gltf, "Node", Node);
        Node
        .def(py::init<>())
        .def(py::init<const tinygltf::Node &>()
        , py::arg("")
        )
        .def_readwrite("camera", &tinygltf::Node::camera)
        .def_readwrite("name", &tinygltf::Node::name)
        .def_readwrite("skin", &tinygltf::Node::skin)
        .def_readwrite("mesh", &tinygltf::Node::mesh)
        .def_readwrite("light", &tinygltf::Node::light)
        .def_readwrite("emitter", &tinygltf::Node::emitter)
        .def_readwrite("children", &tinygltf::Node::children)
        .def_readwrite("rotation", &tinygltf::Node::rotation)
        .def_readwrite("scale", &tinygltf::Node::scale)
        .def_readwrite("translation", &tinygltf::Node::translation)
        .def_readwrite("matrix", &tinygltf::Node::matrix)
        .def_readwrite("weights", &tinygltf::Node::weights)
        .def_readwrite("extensions", &tinygltf::Node::extensions)
        .def_readwrite("extras", &tinygltf::Node::extras)
        .def_readwrite("extras_json_string", &tinygltf::Node::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Node::extensions_json_string)
    ;

    py::class_<tinygltf::Buffer> Buffer(_gltf, "Buffer");
    registry.on(_gltf, "Buffer", Buffer);
        Buffer
        .def_readwrite("name", &tinygltf::Buffer::name)
        .def_readwrite("data", &tinygltf::Buffer::data)
        .def_readwrite("uri", &tinygltf::Buffer::uri)
        .def_readwrite("extras", &tinygltf::Buffer::extras)
        .def_readwrite("extensions", &tinygltf::Buffer::extensions)
        .def_readwrite("extras_json_string", &tinygltf::Buffer::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Buffer::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Buffer &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Asset> Asset(_gltf, "Asset");
    registry.on(_gltf, "Asset", Asset);
        Asset
        .def_readwrite("version", &tinygltf::Asset::version)
        .def_readwrite("generator", &tinygltf::Asset::generator)
        .def_readwrite("min_version", &tinygltf::Asset::minVersion)
        .def_readwrite("copyright", &tinygltf::Asset::copyright)
        .def_readwrite("extensions", &tinygltf::Asset::extensions)
        .def_readwrite("extras", &tinygltf::Asset::extras)
        .def_readwrite("extras_json_string", &tinygltf::Asset::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Asset::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Asset &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::Scene> Scene(_gltf, "Scene");
    registry.on(_gltf, "Scene", Scene);
        Scene
        .def_readwrite("name", &tinygltf::Scene::name)
        .def_readwrite("nodes", &tinygltf::Scene::nodes)
        .def_readwrite("audio_emitters", &tinygltf::Scene::audioEmitters)
        .def_readwrite("extensions", &tinygltf::Scene::extensions)
        .def_readwrite("extras", &tinygltf::Scene::extras)
        .def_readwrite("extras_json_string", &tinygltf::Scene::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Scene::extensions_json_string)
        .def(py::init<>())
        .def(py::init<const tinygltf::Scene &>()
        , py::arg("")
        )
    ;

    py::class_<tinygltf::SpotLight> SpotLight(_gltf, "SpotLight");
    registry.on(_gltf, "SpotLight", SpotLight);
        SpotLight
        .def_readwrite("inner_cone_angle", &tinygltf::SpotLight::innerConeAngle)
        .def_readwrite("outer_cone_angle", &tinygltf::SpotLight::outerConeAngle)
        .def(py::init<>())
        .def(py::init<const tinygltf::SpotLight &>()
        , py::arg("")
        )
        .def_readwrite("extensions", &tinygltf::SpotLight::extensions)
        .def_readwrite("extras", &tinygltf::SpotLight::extras)
        .def_readwrite("extras_json_string", &tinygltf::SpotLight::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::SpotLight::extensions_json_string)
    ;

    py::class_<tinygltf::Light> Light(_gltf, "Light");
    registry.on(_gltf, "Light", Light);
        Light
        .def_readwrite("name", &tinygltf::Light::name)
        .def_readwrite("color", &tinygltf::Light::color)
        .def_readwrite("intensity", &tinygltf::Light::intensity)
        .def_readwrite("type", &tinygltf::Light::type)
        .def_readwrite("range", &tinygltf::Light::range)
        .def_readwrite("spot", &tinygltf::Light::spot)
        .def(py::init<>())
        .def(py::init<const tinygltf::Light &>()
        , py::arg("")
        )
        .def_readwrite("extensions", &tinygltf::Light::extensions)
        .def_readwrite("extras", &tinygltf::Light::extras)
        .def_readwrite("extras_json_string", &tinygltf::Light::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Light::extensions_json_string)
    ;

    py::class_<tinygltf::PositionalEmitter> PositionalEmitter(_gltf, "PositionalEmitter");
    registry.on(_gltf, "PositionalEmitter", PositionalEmitter);
        PositionalEmitter
        .def_readwrite("cone_inner_angle", &tinygltf::PositionalEmitter::coneInnerAngle)
        .def_readwrite("cone_outer_angle", &tinygltf::PositionalEmitter::coneOuterAngle)
        .def_readwrite("cone_outer_gain", &tinygltf::PositionalEmitter::coneOuterGain)
        .def_readwrite("max_distance", &tinygltf::PositionalEmitter::maxDistance)
        .def_readwrite("ref_distance", &tinygltf::PositionalEmitter::refDistance)
        .def_readwrite("rolloff_factor", &tinygltf::PositionalEmitter::rolloffFactor)
        .def(py::init<>())
        .def(py::init<const tinygltf::PositionalEmitter &>()
        , py::arg("")
        )
        .def_readwrite("extensions", &tinygltf::PositionalEmitter::extensions)
        .def_readwrite("extras", &tinygltf::PositionalEmitter::extras)
        .def_readwrite("extras_json_string", &tinygltf::PositionalEmitter::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::PositionalEmitter::extensions_json_string)
    ;

    py::class_<tinygltf::AudioEmitter> AudioEmitter(_gltf, "AudioEmitter");
    registry.on(_gltf, "AudioEmitter", AudioEmitter);
        AudioEmitter
        .def_readwrite("name", &tinygltf::AudioEmitter::name)
        .def_readwrite("gain", &tinygltf::AudioEmitter::gain)
        .def_readwrite("loop", &tinygltf::AudioEmitter::loop)
        .def_readwrite("playing", &tinygltf::AudioEmitter::playing)
        .def_readwrite("type", &tinygltf::AudioEmitter::type)
        .def_readwrite("distance_model", &tinygltf::AudioEmitter::distanceModel)
        .def_readwrite("positional", &tinygltf::AudioEmitter::positional)
        .def_readwrite("source", &tinygltf::AudioEmitter::source)
        .def(py::init<>())
        .def(py::init<const tinygltf::AudioEmitter &>()
        , py::arg("")
        )
        .def_readwrite("extensions", &tinygltf::AudioEmitter::extensions)
        .def_readwrite("extras", &tinygltf::AudioEmitter::extras)
        .def_readwrite("extras_json_string", &tinygltf::AudioEmitter::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::AudioEmitter::extensions_json_string)
    ;

    py::class_<tinygltf::AudioSource> AudioSource(_gltf, "AudioSource");
    registry.on(_gltf, "AudioSource", AudioSource);
        AudioSource
        .def_readwrite("name", &tinygltf::AudioSource::name)
        .def_readwrite("uri", &tinygltf::AudioSource::uri)
        .def_readwrite("buffer_view", &tinygltf::AudioSource::bufferView)
        .def_readwrite("mime_type", &tinygltf::AudioSource::mimeType)
        .def(py::init<>())
        .def(py::init<const tinygltf::AudioSource &>()
        , py::arg("")
        )
        .def_readwrite("extras", &tinygltf::AudioSource::extras)
        .def_readwrite("extensions", &tinygltf::AudioSource::extensions)
        .def_readwrite("extras_json_string", &tinygltf::AudioSource::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::AudioSource::extensions_json_string)
    ;

    py::class_<tinygltf::Model> Model(_gltf, "Model");
    registry.on(_gltf, "Model", Model);
        Model
        .def(py::init<>())
        .def(py::init<const tinygltf::Model &>()
        , py::arg("")
        )
        .def_readwrite("accessors", &tinygltf::Model::accessors)
        .def_readwrite("animations", &tinygltf::Model::animations)
        .def_readwrite("buffers", &tinygltf::Model::buffers)
        .def_readwrite("buffer_views", &tinygltf::Model::bufferViews)
        .def_readwrite("materials", &tinygltf::Model::materials)
        .def_readwrite("meshes", &tinygltf::Model::meshes)
        .def_readwrite("nodes", &tinygltf::Model::nodes)
        .def_readwrite("textures", &tinygltf::Model::textures)
        .def_readwrite("images", &tinygltf::Model::images)
        .def_readwrite("skins", &tinygltf::Model::skins)
        .def_readwrite("samplers", &tinygltf::Model::samplers)
        .def_readwrite("cameras", &tinygltf::Model::cameras)
        .def_readwrite("scenes", &tinygltf::Model::scenes)
        .def_readwrite("lights", &tinygltf::Model::lights)
        .def_readwrite("audio_emitters", &tinygltf::Model::audioEmitters)
        .def_readwrite("audio_sources", &tinygltf::Model::audioSources)
        .def_readwrite("default_scene", &tinygltf::Model::defaultScene)
        .def_readwrite("extensions_used", &tinygltf::Model::extensionsUsed)
        .def_readwrite("extensions_required", &tinygltf::Model::extensionsRequired)
        .def_readwrite("asset", &tinygltf::Model::asset)
        .def_readwrite("extras", &tinygltf::Model::extras)
        .def_readwrite("extensions", &tinygltf::Model::extensions)
        .def_readwrite("extras_json_string", &tinygltf::Model::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Model::extensions_json_string)
    ;

    py::enum_<tinygltf::SectionCheck::Enum>(_gltf, "Enum", py::arithmetic())
        .value("NO_REQUIRE", tinygltf::SectionCheck::Enum::NO_REQUIRE)
        .value("REQUIRE_VERSION", tinygltf::SectionCheck::Enum::REQUIRE_VERSION)
        .value("REQUIRE_SCENE", tinygltf::SectionCheck::Enum::REQUIRE_SCENE)
        .value("REQUIRE_SCENES", tinygltf::SectionCheck::Enum::REQUIRE_SCENES)
        .value("REQUIRE_NODES", tinygltf::SectionCheck::Enum::REQUIRE_NODES)
        .value("REQUIRE_ACCESSORS", tinygltf::SectionCheck::Enum::REQUIRE_ACCESSORS)
        .value("REQUIRE_BUFFERS", tinygltf::SectionCheck::Enum::REQUIRE_BUFFERS)
        .value("REQUIRE_BUFFER_VIEWS", tinygltf::SectionCheck::Enum::REQUIRE_BUFFER_VIEWS)
        .value("REQUIRE_ALL", tinygltf::SectionCheck::Enum::REQUIRE_ALL)
        .export_values()
    ;
    _gltf
    .def("uri_decode", &tinygltf::URIDecode
        , py::arg("in_uri")
        , py::arg("out_uri")
        , py::arg("user_data")
        , py::return_value_policy::automatic_reference)
    .def("load_image_data", &tinygltf::LoadImageData
        , py::arg("image")
        , py::arg("image_idx")
        , py::arg("err")
        , py::arg("warn")
        , py::arg("req_width")
        , py::arg("req_height")
        , py::arg("bytes")
        , py::arg("size")
        , py::arg("")
        , py::return_value_policy::automatic_reference)
    .def("write_image_data", &tinygltf::WriteImageData
        , py::arg("basepath")
        , py::arg("filename")
        , py::arg("image")
        , py::arg("embed_images")
        , py::arg("uri_cb")
        , py::arg("out_uri")
        , py::arg("")
        , py::return_value_policy::automatic_reference)
    .def("file_exists", &tinygltf::FileExists
        , py::arg("abs_filename")
        , py::arg("")
        , py::return_value_policy::automatic_reference)
    .def("expand_file_path", &tinygltf::ExpandFilePath
        , py::arg("filepath")
        , py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    .def("read_whole_file", &tinygltf::ReadWholeFile
        , py::arg("out")
        , py::arg("err")
        , py::arg("filepath")
        , py::arg("")
        , py::return_value_policy::automatic_reference)
    .def("write_whole_file", &tinygltf::WriteWholeFile
        , py::arg("err")
        , py::arg("filepath")
        , py::arg("contents")
        , py::arg("")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<tinygltf::TinyGLTF> TinyGLTF(_gltf, "TinyGLTF");
    registry.on(_gltf, "TinyGLTF", TinyGLTF);
        TinyGLTF
        .def(py::init<>())
        .def("load_ascii_from_file", &tinygltf::TinyGLTF::LoadASCIIFromFile
            , py::arg("model")
            , py::arg("err")
            , py::arg("warn")
            , py::arg("filename")
            , py::arg("check_sections") = tinygltf::SectionCheck::Enum::REQUIRE_VERSION
            , py::return_value_policy::automatic_reference)
        .def("load_ascii_from_string", &tinygltf::TinyGLTF::LoadASCIIFromString
            , py::arg("model")
            , py::arg("err")
            , py::arg("warn")
            , py::arg("str")
            , py::arg("length")
            , py::arg("base_dir")
            , py::arg("check_sections") = tinygltf::SectionCheck::Enum::REQUIRE_VERSION
            , py::return_value_policy::automatic_reference)
        .def("load_binary_from_file", &tinygltf::TinyGLTF::LoadBinaryFromFile
            , py::arg("model")
            , py::arg("err")
            , py::arg("warn")
            , py::arg("filename")
            , py::arg("check_sections") = tinygltf::SectionCheck::Enum::REQUIRE_VERSION
            , py::return_value_policy::automatic_reference)
        .def("load_binary_from_memory", &tinygltf::TinyGLTF::LoadBinaryFromMemory
            , py::arg("model")
            , py::arg("err")
            , py::arg("warn")
            , py::arg("bytes")
            , py::arg("length")
            , py::arg("base_dir") = ""
            , py::arg("check_sections") = tinygltf::SectionCheck::Enum::REQUIRE_VERSION
            , py::return_value_policy::automatic_reference)
        .def("write_gltf_scene_to_file", &tinygltf::TinyGLTF::WriteGltfSceneToFile
            , py::arg("model")
            , py::arg("filename")
            , py::arg("embed_images")
            , py::arg("embed_buffers")
            , py::arg("pretty_print")
            , py::arg("write_binary")
            , py::return_value_policy::automatic_reference)
        .def("set_parse_strictness", &tinygltf::TinyGLTF::SetParseStrictness
            , py::arg("strictness")
            , py::return_value_policy::automatic_reference)
        .def("set_image_loader", &tinygltf::TinyGLTF::SetImageLoader
            , py::arg("load_image_data")
            , py::arg("user_data")
            , py::return_value_policy::automatic_reference)
        .def("remove_image_loader", &tinygltf::TinyGLTF::RemoveImageLoader
            , py::return_value_policy::automatic_reference)
        .def("set_image_writer", &tinygltf::TinyGLTF::SetImageWriter
            , py::arg("write_image_data")
            , py::arg("user_data")
            , py::return_value_policy::automatic_reference)
        .def("set_uri_callbacks", &tinygltf::TinyGLTF::SetURICallbacks
            , py::arg("callbacks")
            , py::return_value_policy::automatic_reference)
        .def("set_fs_callbacks", &tinygltf::TinyGLTF::SetFsCallbacks
            , py::arg("callbacks")
            , py::return_value_policy::automatic_reference)
        .def("set_serialize_default_values", &tinygltf::TinyGLTF::SetSerializeDefaultValues
            , py::arg("enabled")
            , py::return_value_policy::automatic_reference)
        .def("get_serialize_default_values", &tinygltf::TinyGLTF::GetSerializeDefaultValues
            , py::return_value_policy::automatic_reference)
        .def("set_store_original_json_for_extras_and_extensions", &tinygltf::TinyGLTF::SetStoreOriginalJSONForExtrasAndExtensions
            , py::arg("enabled")
            , py::return_value_policy::automatic_reference)
        .def("get_store_original_json_for_extras_and_extensions", &tinygltf::TinyGLTF::GetStoreOriginalJSONForExtrasAndExtensions
            , py::return_value_policy::automatic_reference)
        .def("set_preserve_image_channels", &tinygltf::TinyGLTF::SetPreserveImageChannels
            , py::arg("onoff")
            , py::return_value_policy::automatic_reference)
        .def("set_max_external_file_size", &tinygltf::TinyGLTF::SetMaxExternalFileSize
            , py::arg("max_bytes")
            , py::return_value_policy::automatic_reference)
        .def("get_max_external_file_size", &tinygltf::TinyGLTF::GetMaxExternalFileSize
            , py::return_value_policy::automatic_reference)
        .def("get_preserve_image_channels", &tinygltf::TinyGLTF::GetPreserveImageChannels
            , py::return_value_policy::automatic_reference)
    ;


}