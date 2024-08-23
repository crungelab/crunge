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
        .export_values();

    py::enum_<tinygltf::ParseStrictness>(_gltf, "ParseStrictness", py::arithmetic())
        .value("PERMISSIVE", tinygltf::ParseStrictness::Permissive)
        .value("STRICT", tinygltf::ParseStrictness::Strict)
        .export_values();

    _gltf.def("get_component_size_in_bytes", &tinygltf::GetComponentSizeInBytes
    , py::arg("component_type")
    , py::return_value_policy::automatic_reference);

    _gltf.def("get_num_components_in_type", &tinygltf::GetNumComponentsInType
    , py::arg("ty")
    , py::return_value_policy::automatic_reference);

    _gltf.def("is_data_uri", &tinygltf::IsDataURI
    , py::arg("in")
    , py::return_value_policy::automatic_reference);

    _gltf.def("decode_data_uri", [](std::vector<unsigned char> * out, std::string & mime_type, const std::string & in, size_t reqBytes, bool checkSize)
    {
        auto ret = tinygltf::DecodeDataURI(out, mime_type, in, reqBytes, checkSize);
        return std::make_tuple(ret, mime_type);
    }
    , py::arg("out")
    , py::arg("mime_type")
    , py::arg("in")
    , py::arg("req_bytes")
    , py::arg("check_size")
    , py::return_value_policy::automatic_reference);

    PYCLASS_BEGIN(_gltf, tinygltf::Value, Value)
        Value.def(py::init<>());
        Value.def(py::init<bool>()
        , py::arg("b")
        );
        Value.def(py::init<int>()
        , py::arg("i")
        );
        Value.def(py::init<double>()
        , py::arg("n")
        );
        Value.def(py::init<const std::string &>()
        , py::arg("s")
        );
        Value.def(py::init<const char *>()
        , py::arg("s")
        );
        Value.def(py::init<const unsigned char *, size_t>()
        , py::arg("p")
        , py::arg("n")
        );
        Value.def(py::init<const tinygltf::Value::Array &>()
        , py::arg("a")
        );
        Value.def(py::init<const tinygltf::Value::Object &>()
        , py::arg("o")
        );
        Value.def(py::init<const tinygltf::Value &>()
        , py::arg("")
        );
        Value.def("type", &tinygltf::Value::Type
        , py::return_value_policy::automatic_reference);

        Value.def("is_bool", &tinygltf::Value::IsBool
        , py::return_value_policy::automatic_reference);

        Value.def("is_int", &tinygltf::Value::IsInt
        , py::return_value_policy::automatic_reference);

        Value.def("is_number", &tinygltf::Value::IsNumber
        , py::return_value_policy::automatic_reference);

        Value.def("is_real", &tinygltf::Value::IsReal
        , py::return_value_policy::automatic_reference);

        Value.def("is_string", &tinygltf::Value::IsString
        , py::return_value_policy::automatic_reference);

        Value.def("is_binary", &tinygltf::Value::IsBinary
        , py::return_value_policy::automatic_reference);

        Value.def("is_array", &tinygltf::Value::IsArray
        , py::return_value_policy::automatic_reference);

        Value.def("is_object", &tinygltf::Value::IsObject
        , py::return_value_policy::automatic_reference);

        Value.def("get_number_as_double", &tinygltf::Value::GetNumberAsDouble
        , py::return_value_policy::automatic_reference);

        Value.def("get_number_as_int", &tinygltf::Value::GetNumberAsInt
        , py::return_value_policy::automatic_reference);

        Value.def("array_len", &tinygltf::Value::ArrayLen
        , py::return_value_policy::automatic_reference);

        Value.def("has", &tinygltf::Value::Has
        , py::arg("key")
        , py::return_value_policy::automatic_reference);

        Value.def("keys", &tinygltf::Value::Keys
        , py::return_value_policy::automatic_reference);

        Value.def("size", &tinygltf::Value::Size
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_gltf, tinygltf::Value, Value)

    PYCLASS_BEGIN(_gltf, tinygltf::Parameter, Parameter)
        Parameter.def_readwrite("bool_value", &tinygltf::Parameter::bool_value);
        Parameter.def_readwrite("has_number_value", &tinygltf::Parameter::has_number_value);
        Parameter.def_readwrite("string_value", &tinygltf::Parameter::string_value);
        Parameter.def_readwrite("number_array", &tinygltf::Parameter::number_array);
        Parameter.def_readwrite("json_double_value", &tinygltf::Parameter::json_double_value);
        Parameter.def_readwrite("number_value", &tinygltf::Parameter::number_value);
        Parameter.def("texture_index", &tinygltf::Parameter::TextureIndex
        , py::return_value_policy::automatic_reference);

        Parameter.def("texture_tex_coord", &tinygltf::Parameter::TextureTexCoord
        , py::return_value_policy::automatic_reference);

        Parameter.def("texture_scale", &tinygltf::Parameter::TextureScale
        , py::return_value_policy::automatic_reference);

        Parameter.def("texture_strength", &tinygltf::Parameter::TextureStrength
        , py::return_value_policy::automatic_reference);

        Parameter.def("factor", &tinygltf::Parameter::Factor
        , py::return_value_policy::automatic_reference);

        Parameter.def("color_factor", &tinygltf::Parameter::ColorFactor
        , py::return_value_policy::automatic_reference);

        Parameter.def(py::init<>());
        Parameter.def(py::init<const tinygltf::Parameter &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Parameter, Parameter)

    PYCLASS_BEGIN(_gltf, tinygltf::AnimationChannel, AnimationChannel)
        AnimationChannel.def_readwrite("sampler", &tinygltf::AnimationChannel::sampler);
        AnimationChannel.def_readwrite("target_node", &tinygltf::AnimationChannel::target_node);
        AnimationChannel.def_readwrite("target_path", &tinygltf::AnimationChannel::target_path);
        AnimationChannel.def_readwrite("extras", &tinygltf::AnimationChannel::extras);
        AnimationChannel.def_readwrite("extensions", &tinygltf::AnimationChannel::extensions);
        AnimationChannel.def_readwrite("target_extras", &tinygltf::AnimationChannel::target_extras);
        AnimationChannel.def_readwrite("target_extensions", &tinygltf::AnimationChannel::target_extensions);
        AnimationChannel.def_readwrite("extras_json_string", &tinygltf::AnimationChannel::extras_json_string);
        AnimationChannel.def_readwrite("extensions_json_string", &tinygltf::AnimationChannel::extensions_json_string);
        AnimationChannel.def_readwrite("target_extras_json_string", &tinygltf::AnimationChannel::target_extras_json_string);
        AnimationChannel.def_readwrite("target_extensions_json_string", &tinygltf::AnimationChannel::target_extensions_json_string);
        AnimationChannel.def(py::init<>());
        AnimationChannel.def(py::init<const tinygltf::AnimationChannel &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::AnimationChannel, AnimationChannel)

    PYCLASS_BEGIN(_gltf, tinygltf::AnimationSampler, AnimationSampler)
        AnimationSampler.def_readwrite("input", &tinygltf::AnimationSampler::input);
        AnimationSampler.def_readwrite("output", &tinygltf::AnimationSampler::output);
        AnimationSampler.def_readwrite("interpolation", &tinygltf::AnimationSampler::interpolation);
        AnimationSampler.def_readwrite("extras", &tinygltf::AnimationSampler::extras);
        AnimationSampler.def_readwrite("extensions", &tinygltf::AnimationSampler::extensions);
        AnimationSampler.def_readwrite("extras_json_string", &tinygltf::AnimationSampler::extras_json_string);
        AnimationSampler.def_readwrite("extensions_json_string", &tinygltf::AnimationSampler::extensions_json_string);
        AnimationSampler.def(py::init<>());
        AnimationSampler.def(py::init<const tinygltf::AnimationSampler &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::AnimationSampler, AnimationSampler)

    PYCLASS_BEGIN(_gltf, tinygltf::Animation, Animation)
        Animation.def_readwrite("name", &tinygltf::Animation::name);
        Animation.def_readwrite("channels", &tinygltf::Animation::channels);
        Animation.def_readwrite("samplers", &tinygltf::Animation::samplers);
        Animation.def_readwrite("extras", &tinygltf::Animation::extras);
        Animation.def_readwrite("extensions", &tinygltf::Animation::extensions);
        Animation.def_readwrite("extras_json_string", &tinygltf::Animation::extras_json_string);
        Animation.def_readwrite("extensions_json_string", &tinygltf::Animation::extensions_json_string);
        Animation.def(py::init<>());
        Animation.def(py::init<const tinygltf::Animation &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Animation, Animation)

    PYCLASS_BEGIN(_gltf, tinygltf::Skin, Skin)
        Skin.def_readwrite("name", &tinygltf::Skin::name);
        Skin.def_readwrite("inverse_bind_matrices", &tinygltf::Skin::inverseBindMatrices);
        Skin.def_readwrite("skeleton", &tinygltf::Skin::skeleton);
        Skin.def_readwrite("joints", &tinygltf::Skin::joints);
        Skin.def_readwrite("extras", &tinygltf::Skin::extras);
        Skin.def_readwrite("extensions", &tinygltf::Skin::extensions);
        Skin.def_readwrite("extras_json_string", &tinygltf::Skin::extras_json_string);
        Skin.def_readwrite("extensions_json_string", &tinygltf::Skin::extensions_json_string);
        Skin.def(py::init<>());
        Skin.def(py::init<const tinygltf::Skin &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Skin, Skin)

    PYCLASS_BEGIN(_gltf, tinygltf::Sampler, Sampler)
        Sampler.def_readwrite("name", &tinygltf::Sampler::name);
        Sampler.def_readwrite("min_filter", &tinygltf::Sampler::minFilter);
        Sampler.def_readwrite("mag_filter", &tinygltf::Sampler::magFilter);
        Sampler.def_readwrite("wrap_s", &tinygltf::Sampler::wrapS);
        Sampler.def_readwrite("wrap_t", &tinygltf::Sampler::wrapT);
        Sampler.def_readwrite("extras", &tinygltf::Sampler::extras);
        Sampler.def_readwrite("extensions", &tinygltf::Sampler::extensions);
        Sampler.def_readwrite("extras_json_string", &tinygltf::Sampler::extras_json_string);
        Sampler.def_readwrite("extensions_json_string", &tinygltf::Sampler::extensions_json_string);
        Sampler.def(py::init<>());
        Sampler.def(py::init<const tinygltf::Sampler &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Sampler, Sampler)

    PYCLASS_BEGIN(_gltf, tinygltf::Image, Image)
        Image.def_readwrite("name", &tinygltf::Image::name);
        Image.def_readwrite("width", &tinygltf::Image::width);
        Image.def_readwrite("height", &tinygltf::Image::height);
        Image.def_readwrite("component", &tinygltf::Image::component);
        Image.def_readwrite("bits", &tinygltf::Image::bits);
        Image.def_readwrite("pixel_type", &tinygltf::Image::pixel_type);
        Image.def_readwrite("image", &tinygltf::Image::image);
        Image.def_readwrite("buffer_view", &tinygltf::Image::bufferView);
        Image.def_readwrite("mime_type", &tinygltf::Image::mimeType);
        Image.def_readwrite("uri", &tinygltf::Image::uri);
        Image.def_readwrite("extras", &tinygltf::Image::extras);
        Image.def_readwrite("extensions", &tinygltf::Image::extensions);
        Image.def_readwrite("extras_json_string", &tinygltf::Image::extras_json_string);
        Image.def_readwrite("extensions_json_string", &tinygltf::Image::extensions_json_string);
        Image.def_readwrite("as_is", &tinygltf::Image::as_is);
        Image.def(py::init<>());
        Image.def(py::init<const tinygltf::Image &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Image, Image)

    PYCLASS_BEGIN(_gltf, tinygltf::Texture, Texture)
        Texture.def_readwrite("name", &tinygltf::Texture::name);
        Texture.def_readwrite("sampler", &tinygltf::Texture::sampler);
        Texture.def_readwrite("source", &tinygltf::Texture::source);
        Texture.def_readwrite("extras", &tinygltf::Texture::extras);
        Texture.def_readwrite("extensions", &tinygltf::Texture::extensions);
        Texture.def_readwrite("extras_json_string", &tinygltf::Texture::extras_json_string);
        Texture.def_readwrite("extensions_json_string", &tinygltf::Texture::extensions_json_string);
        Texture.def(py::init<>());
        Texture.def(py::init<const tinygltf::Texture &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Texture, Texture)

    PYCLASS_BEGIN(_gltf, tinygltf::TextureInfo, TextureInfo)
        TextureInfo.def_readwrite("index", &tinygltf::TextureInfo::index);
        TextureInfo.def_readwrite("tex_coord", &tinygltf::TextureInfo::texCoord);
        TextureInfo.def_readwrite("extras", &tinygltf::TextureInfo::extras);
        TextureInfo.def_readwrite("extensions", &tinygltf::TextureInfo::extensions);
        TextureInfo.def_readwrite("extras_json_string", &tinygltf::TextureInfo::extras_json_string);
        TextureInfo.def_readwrite("extensions_json_string", &tinygltf::TextureInfo::extensions_json_string);
        TextureInfo.def(py::init<>());
        TextureInfo.def(py::init<const tinygltf::TextureInfo &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::TextureInfo, TextureInfo)

    PYCLASS_BEGIN(_gltf, tinygltf::NormalTextureInfo, NormalTextureInfo)
        NormalTextureInfo.def_readwrite("index", &tinygltf::NormalTextureInfo::index);
        NormalTextureInfo.def_readwrite("tex_coord", &tinygltf::NormalTextureInfo::texCoord);
        NormalTextureInfo.def_readwrite("scale", &tinygltf::NormalTextureInfo::scale);
        NormalTextureInfo.def_readwrite("extras", &tinygltf::NormalTextureInfo::extras);
        NormalTextureInfo.def_readwrite("extensions", &tinygltf::NormalTextureInfo::extensions);
        NormalTextureInfo.def_readwrite("extras_json_string", &tinygltf::NormalTextureInfo::extras_json_string);
        NormalTextureInfo.def_readwrite("extensions_json_string", &tinygltf::NormalTextureInfo::extensions_json_string);
        NormalTextureInfo.def(py::init<>());
        NormalTextureInfo.def(py::init<const tinygltf::NormalTextureInfo &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::NormalTextureInfo, NormalTextureInfo)

    PYCLASS_BEGIN(_gltf, tinygltf::OcclusionTextureInfo, OcclusionTextureInfo)
        OcclusionTextureInfo.def_readwrite("index", &tinygltf::OcclusionTextureInfo::index);
        OcclusionTextureInfo.def_readwrite("tex_coord", &tinygltf::OcclusionTextureInfo::texCoord);
        OcclusionTextureInfo.def_readwrite("strength", &tinygltf::OcclusionTextureInfo::strength);
        OcclusionTextureInfo.def_readwrite("extras", &tinygltf::OcclusionTextureInfo::extras);
        OcclusionTextureInfo.def_readwrite("extensions", &tinygltf::OcclusionTextureInfo::extensions);
        OcclusionTextureInfo.def_readwrite("extras_json_string", &tinygltf::OcclusionTextureInfo::extras_json_string);
        OcclusionTextureInfo.def_readwrite("extensions_json_string", &tinygltf::OcclusionTextureInfo::extensions_json_string);
        OcclusionTextureInfo.def(py::init<>());
        OcclusionTextureInfo.def(py::init<const tinygltf::OcclusionTextureInfo &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::OcclusionTextureInfo, OcclusionTextureInfo)

    PYCLASS_BEGIN(_gltf, tinygltf::PbrMetallicRoughness, PbrMetallicRoughness)
        PbrMetallicRoughness.def_readwrite("base_color_factor", &tinygltf::PbrMetallicRoughness::baseColorFactor);
        PbrMetallicRoughness.def_readwrite("base_color_texture", &tinygltf::PbrMetallicRoughness::baseColorTexture);
        PbrMetallicRoughness.def_readwrite("metallic_factor", &tinygltf::PbrMetallicRoughness::metallicFactor);
        PbrMetallicRoughness.def_readwrite("roughness_factor", &tinygltf::PbrMetallicRoughness::roughnessFactor);
        PbrMetallicRoughness.def_readwrite("metallic_roughness_texture", &tinygltf::PbrMetallicRoughness::metallicRoughnessTexture);
        PbrMetallicRoughness.def_readwrite("extras", &tinygltf::PbrMetallicRoughness::extras);
        PbrMetallicRoughness.def_readwrite("extensions", &tinygltf::PbrMetallicRoughness::extensions);
        PbrMetallicRoughness.def_readwrite("extras_json_string", &tinygltf::PbrMetallicRoughness::extras_json_string);
        PbrMetallicRoughness.def_readwrite("extensions_json_string", &tinygltf::PbrMetallicRoughness::extensions_json_string);
        PbrMetallicRoughness.def(py::init<>());
        PbrMetallicRoughness.def(py::init<const tinygltf::PbrMetallicRoughness &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::PbrMetallicRoughness, PbrMetallicRoughness)

    PYCLASS_BEGIN(_gltf, tinygltf::Material, Material)
        Material.def_readwrite("name", &tinygltf::Material::name);
        Material.def_readwrite("emissive_factor", &tinygltf::Material::emissiveFactor);
        Material.def_readwrite("alpha_mode", &tinygltf::Material::alphaMode);
        Material.def_readwrite("alpha_cutoff", &tinygltf::Material::alphaCutoff);
        Material.def_readwrite("double_sided", &tinygltf::Material::doubleSided);
        Material.def_readwrite("pbr_metallic_roughness", &tinygltf::Material::pbrMetallicRoughness);
        Material.def_readwrite("normal_texture", &tinygltf::Material::normalTexture);
        Material.def_readwrite("occlusion_texture", &tinygltf::Material::occlusionTexture);
        Material.def_readwrite("emissive_texture", &tinygltf::Material::emissiveTexture);
        Material.def_readwrite("values", &tinygltf::Material::values);
        Material.def_readwrite("additional_values", &tinygltf::Material::additionalValues);
        Material.def_readwrite("extensions", &tinygltf::Material::extensions);
        Material.def_readwrite("extras", &tinygltf::Material::extras);
        Material.def_readwrite("extras_json_string", &tinygltf::Material::extras_json_string);
        Material.def_readwrite("extensions_json_string", &tinygltf::Material::extensions_json_string);
        Material.def(py::init<>());
        Material.def(py::init<const tinygltf::Material &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Material, Material)

    PYCLASS_BEGIN(_gltf, tinygltf::BufferView, BufferView)
        BufferView.def_readwrite("name", &tinygltf::BufferView::name);
        BufferView.def_readwrite("buffer", &tinygltf::BufferView::buffer);
        BufferView.def_readwrite("byte_offset", &tinygltf::BufferView::byteOffset);
        BufferView.def_readwrite("byte_length", &tinygltf::BufferView::byteLength);
        BufferView.def_readwrite("byte_stride", &tinygltf::BufferView::byteStride);
        BufferView.def_readwrite("target", &tinygltf::BufferView::target);
        BufferView.def_readwrite("extras", &tinygltf::BufferView::extras);
        BufferView.def_readwrite("extensions", &tinygltf::BufferView::extensions);
        BufferView.def_readwrite("extras_json_string", &tinygltf::BufferView::extras_json_string);
        BufferView.def_readwrite("extensions_json_string", &tinygltf::BufferView::extensions_json_string);
        BufferView.def_readwrite("draco_decoded", &tinygltf::BufferView::dracoDecoded);
        BufferView.def(py::init<>());
        BufferView.def(py::init<const tinygltf::BufferView &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::BufferView, BufferView)

    PYCLASS_BEGIN(_gltf, tinygltf::Accessor, Accessor)
        Accessor.def_readwrite("buffer_view", &tinygltf::Accessor::bufferView);
        Accessor.def_readwrite("name", &tinygltf::Accessor::name);
        Accessor.def_readwrite("byte_offset", &tinygltf::Accessor::byteOffset);
        Accessor.def_readwrite("normalized", &tinygltf::Accessor::normalized);
        Accessor.def_readwrite("component_type", &tinygltf::Accessor::componentType);
        Accessor.def_readwrite("count", &tinygltf::Accessor::count);
        Accessor.def_readwrite("type", &tinygltf::Accessor::type);
        Accessor.def_readwrite("extras", &tinygltf::Accessor::extras);
        Accessor.def_readwrite("extensions", &tinygltf::Accessor::extensions);
        Accessor.def_readwrite("extras_json_string", &tinygltf::Accessor::extras_json_string);
        Accessor.def_readwrite("extensions_json_string", &tinygltf::Accessor::extensions_json_string);
        Accessor.def_readwrite("min_values", &tinygltf::Accessor::minValues);
        Accessor.def_readwrite("max_values", &tinygltf::Accessor::maxValues);
        PYCLASS_BEGIN(_gltf, tinygltf::Accessor::Sparse, AccessorSparse)
            AccessorSparse.def_readwrite("count", &tinygltf::Accessor::Sparse::count);
            AccessorSparse.def_readwrite("is_sparse", &tinygltf::Accessor::Sparse::isSparse);
            PYCLASS_BEGIN(_gltf, tinygltf::Accessor::Sparse::Indices, AccessorSparseIndices)
                AccessorSparseIndices.def_readwrite("byte_offset", &tinygltf::Accessor::Sparse::Indices::byteOffset);
                AccessorSparseIndices.def_readwrite("buffer_view", &tinygltf::Accessor::Sparse::Indices::bufferView);
                AccessorSparseIndices.def_readwrite("component_type", &tinygltf::Accessor::Sparse::Indices::componentType);
                AccessorSparseIndices.def_readwrite("extras", &tinygltf::Accessor::Sparse::Indices::extras);
                AccessorSparseIndices.def_readwrite("extensions", &tinygltf::Accessor::Sparse::Indices::extensions);
                AccessorSparseIndices.def_readwrite("extras_json_string", &tinygltf::Accessor::Sparse::Indices::extras_json_string);
                AccessorSparseIndices.def_readwrite("extensions_json_string", &tinygltf::Accessor::Sparse::Indices::extensions_json_string);
            PYCLASS_END(_gltf, tinygltf::Accessor::Sparse::Indices, AccessorSparseIndices)

            AccessorSparse.def_readwrite("indices", &tinygltf::Accessor::Sparse::indices);
            PYCLASS_BEGIN(_gltf, tinygltf::Accessor::Sparse::Values, AccessorSparseValues)
                AccessorSparseValues.def_readwrite("buffer_view", &tinygltf::Accessor::Sparse::Values::bufferView);
                AccessorSparseValues.def_readwrite("byte_offset", &tinygltf::Accessor::Sparse::Values::byteOffset);
                AccessorSparseValues.def_readwrite("extras", &tinygltf::Accessor::Sparse::Values::extras);
                AccessorSparseValues.def_readwrite("extensions", &tinygltf::Accessor::Sparse::Values::extensions);
                AccessorSparseValues.def_readwrite("extras_json_string", &tinygltf::Accessor::Sparse::Values::extras_json_string);
                AccessorSparseValues.def_readwrite("extensions_json_string", &tinygltf::Accessor::Sparse::Values::extensions_json_string);
            PYCLASS_END(_gltf, tinygltf::Accessor::Sparse::Values, AccessorSparseValues)

            AccessorSparse.def_readwrite("values", &tinygltf::Accessor::Sparse::values);
            AccessorSparse.def_readwrite("extras", &tinygltf::Accessor::Sparse::extras);
            AccessorSparse.def_readwrite("extensions", &tinygltf::Accessor::Sparse::extensions);
            AccessorSparse.def_readwrite("extras_json_string", &tinygltf::Accessor::Sparse::extras_json_string);
            AccessorSparse.def_readwrite("extensions_json_string", &tinygltf::Accessor::Sparse::extensions_json_string);
        PYCLASS_END(_gltf, tinygltf::Accessor::Sparse, AccessorSparse)

        Accessor.def_readwrite("sparse", &tinygltf::Accessor::sparse);
        Accessor.def("byte_stride", &tinygltf::Accessor::ByteStride
        , py::arg("buffer_view_object")
        , py::return_value_policy::automatic_reference);

        Accessor.def(py::init<>());
        Accessor.def(py::init<const tinygltf::Accessor &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Accessor, Accessor)

    PYCLASS_BEGIN(_gltf, tinygltf::PerspectiveCamera, PerspectiveCamera)
        PerspectiveCamera.def_readwrite("aspect_ratio", &tinygltf::PerspectiveCamera::aspectRatio);
        PerspectiveCamera.def_readwrite("yfov", &tinygltf::PerspectiveCamera::yfov);
        PerspectiveCamera.def_readwrite("zfar", &tinygltf::PerspectiveCamera::zfar);
        PerspectiveCamera.def_readwrite("znear", &tinygltf::PerspectiveCamera::znear);
        PerspectiveCamera.def(py::init<>());
        PerspectiveCamera.def(py::init<const tinygltf::PerspectiveCamera &>()
        , py::arg("")
        );
        PerspectiveCamera.def_readwrite("extensions", &tinygltf::PerspectiveCamera::extensions);
        PerspectiveCamera.def_readwrite("extras", &tinygltf::PerspectiveCamera::extras);
        PerspectiveCamera.def_readwrite("extras_json_string", &tinygltf::PerspectiveCamera::extras_json_string);
        PerspectiveCamera.def_readwrite("extensions_json_string", &tinygltf::PerspectiveCamera::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::PerspectiveCamera, PerspectiveCamera)

    PYCLASS_BEGIN(_gltf, tinygltf::OrthographicCamera, OrthographicCamera)
        OrthographicCamera.def_readwrite("xmag", &tinygltf::OrthographicCamera::xmag);
        OrthographicCamera.def_readwrite("ymag", &tinygltf::OrthographicCamera::ymag);
        OrthographicCamera.def_readwrite("zfar", &tinygltf::OrthographicCamera::zfar);
        OrthographicCamera.def_readwrite("znear", &tinygltf::OrthographicCamera::znear);
        OrthographicCamera.def(py::init<>());
        OrthographicCamera.def(py::init<const tinygltf::OrthographicCamera &>()
        , py::arg("")
        );
        OrthographicCamera.def_readwrite("extensions", &tinygltf::OrthographicCamera::extensions);
        OrthographicCamera.def_readwrite("extras", &tinygltf::OrthographicCamera::extras);
        OrthographicCamera.def_readwrite("extras_json_string", &tinygltf::OrthographicCamera::extras_json_string);
        OrthographicCamera.def_readwrite("extensions_json_string", &tinygltf::OrthographicCamera::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::OrthographicCamera, OrthographicCamera)

    PYCLASS_BEGIN(_gltf, tinygltf::Camera, Camera)
        Camera.def_readwrite("type", &tinygltf::Camera::type);
        Camera.def_readwrite("name", &tinygltf::Camera::name);
        Camera.def_readwrite("perspective", &tinygltf::Camera::perspective);
        Camera.def_readwrite("orthographic", &tinygltf::Camera::orthographic);
        Camera.def(py::init<>());
        Camera.def(py::init<const tinygltf::Camera &>()
        , py::arg("")
        );
        Camera.def_readwrite("extensions", &tinygltf::Camera::extensions);
        Camera.def_readwrite("extras", &tinygltf::Camera::extras);
        Camera.def_readwrite("extras_json_string", &tinygltf::Camera::extras_json_string);
        Camera.def_readwrite("extensions_json_string", &tinygltf::Camera::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::Camera, Camera)

    PYCLASS_BEGIN(_gltf, tinygltf::Primitive, Primitive)
        Primitive.def_readwrite("attributes", &tinygltf::Primitive::attributes);
        Primitive.def_readwrite("material", &tinygltf::Primitive::material);
        Primitive.def_readwrite("indices", &tinygltf::Primitive::indices);
        Primitive.def_readwrite("mode", &tinygltf::Primitive::mode);
        Primitive.def_readwrite("targets", &tinygltf::Primitive::targets);
        Primitive.def_readwrite("extensions", &tinygltf::Primitive::extensions);
        Primitive.def_readwrite("extras", &tinygltf::Primitive::extras);
        Primitive.def_readwrite("extras_json_string", &tinygltf::Primitive::extras_json_string);
        Primitive.def_readwrite("extensions_json_string", &tinygltf::Primitive::extensions_json_string);
        Primitive.def(py::init<>());
        Primitive.def(py::init<const tinygltf::Primitive &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Primitive, Primitive)

    PYCLASS_BEGIN(_gltf, tinygltf::Mesh, Mesh)
        Mesh.def_readwrite("name", &tinygltf::Mesh::name);
        Mesh.def_readwrite("primitives", &tinygltf::Mesh::primitives);
        Mesh.def_readwrite("weights", &tinygltf::Mesh::weights);
        Mesh.def_readwrite("extensions", &tinygltf::Mesh::extensions);
        Mesh.def_readwrite("extras", &tinygltf::Mesh::extras);
        Mesh.def_readwrite("extras_json_string", &tinygltf::Mesh::extras_json_string);
        Mesh.def_readwrite("extensions_json_string", &tinygltf::Mesh::extensions_json_string);
        Mesh.def(py::init<>());
        Mesh.def(py::init<const tinygltf::Mesh &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Mesh, Mesh)

    PYCLASS_BEGIN(_gltf, tinygltf::Node, Node)
        Node.def(py::init<>());
        Node.def(py::init<const tinygltf::Node &>()
        , py::arg("")
        );
        Node.def_readwrite("camera", &tinygltf::Node::camera);
        Node.def_readwrite("name", &tinygltf::Node::name);
        Node.def_readwrite("skin", &tinygltf::Node::skin);
        Node.def_readwrite("mesh", &tinygltf::Node::mesh);
        Node.def_readwrite("light", &tinygltf::Node::light);
        Node.def_readwrite("emitter", &tinygltf::Node::emitter);
        Node.def_readwrite("children", &tinygltf::Node::children);
        Node.def_readwrite("rotation", &tinygltf::Node::rotation);
        Node.def_readwrite("scale", &tinygltf::Node::scale);
        Node.def_readwrite("translation", &tinygltf::Node::translation);
        Node.def_readwrite("matrix", &tinygltf::Node::matrix);
        Node.def_readwrite("weights", &tinygltf::Node::weights);
        Node.def_readwrite("extensions", &tinygltf::Node::extensions);
        Node.def_readwrite("extras", &tinygltf::Node::extras);
        Node.def_readwrite("extras_json_string", &tinygltf::Node::extras_json_string);
        Node.def_readwrite("extensions_json_string", &tinygltf::Node::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::Node, Node)

    PYCLASS_BEGIN(_gltf, tinygltf::Buffer, Buffer)
        Buffer.def_readwrite("name", &tinygltf::Buffer::name);
        Buffer.def_readwrite("data", &tinygltf::Buffer::data);
        Buffer.def_readwrite("uri", &tinygltf::Buffer::uri);
        Buffer.def_readwrite("extras", &tinygltf::Buffer::extras);
        Buffer.def_readwrite("extensions", &tinygltf::Buffer::extensions);
        Buffer.def_readwrite("extras_json_string", &tinygltf::Buffer::extras_json_string);
        Buffer.def_readwrite("extensions_json_string", &tinygltf::Buffer::extensions_json_string);
        Buffer.def(py::init<>());
        Buffer.def(py::init<const tinygltf::Buffer &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Buffer, Buffer)

    PYCLASS_BEGIN(_gltf, tinygltf::Asset, Asset)
        Asset.def_readwrite("version", &tinygltf::Asset::version);
        Asset.def_readwrite("generator", &tinygltf::Asset::generator);
        Asset.def_readwrite("min_version", &tinygltf::Asset::minVersion);
        Asset.def_readwrite("copyright", &tinygltf::Asset::copyright);
        Asset.def_readwrite("extensions", &tinygltf::Asset::extensions);
        Asset.def_readwrite("extras", &tinygltf::Asset::extras);
        Asset.def_readwrite("extras_json_string", &tinygltf::Asset::extras_json_string);
        Asset.def_readwrite("extensions_json_string", &tinygltf::Asset::extensions_json_string);
        Asset.def(py::init<>());
        Asset.def(py::init<const tinygltf::Asset &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Asset, Asset)

    PYCLASS_BEGIN(_gltf, tinygltf::Scene, Scene)
        Scene.def_readwrite("name", &tinygltf::Scene::name);
        Scene.def_readwrite("nodes", &tinygltf::Scene::nodes);
        Scene.def_readwrite("audio_emitters", &tinygltf::Scene::audioEmitters);
        Scene.def_readwrite("extensions", &tinygltf::Scene::extensions);
        Scene.def_readwrite("extras", &tinygltf::Scene::extras);
        Scene.def_readwrite("extras_json_string", &tinygltf::Scene::extras_json_string);
        Scene.def_readwrite("extensions_json_string", &tinygltf::Scene::extensions_json_string);
        Scene.def(py::init<>());
        Scene.def(py::init<const tinygltf::Scene &>()
        , py::arg("")
        );
    PYCLASS_END(_gltf, tinygltf::Scene, Scene)

    PYCLASS_BEGIN(_gltf, tinygltf::SpotLight, SpotLight)
        SpotLight.def_readwrite("inner_cone_angle", &tinygltf::SpotLight::innerConeAngle);
        SpotLight.def_readwrite("outer_cone_angle", &tinygltf::SpotLight::outerConeAngle);
        SpotLight.def(py::init<>());
        SpotLight.def(py::init<const tinygltf::SpotLight &>()
        , py::arg("")
        );
        SpotLight.def_readwrite("extensions", &tinygltf::SpotLight::extensions);
        SpotLight.def_readwrite("extras", &tinygltf::SpotLight::extras);
        SpotLight.def_readwrite("extras_json_string", &tinygltf::SpotLight::extras_json_string);
        SpotLight.def_readwrite("extensions_json_string", &tinygltf::SpotLight::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::SpotLight, SpotLight)

    PYCLASS_BEGIN(_gltf, tinygltf::Light, Light)
        Light.def_readwrite("name", &tinygltf::Light::name);
        Light.def_readwrite("color", &tinygltf::Light::color);
        Light.def_readwrite("intensity", &tinygltf::Light::intensity);
        Light.def_readwrite("type", &tinygltf::Light::type);
        Light.def_readwrite("range", &tinygltf::Light::range);
        Light.def_readwrite("spot", &tinygltf::Light::spot);
        Light.def(py::init<>());
        Light.def(py::init<const tinygltf::Light &>()
        , py::arg("")
        );
        Light.def_readwrite("extensions", &tinygltf::Light::extensions);
        Light.def_readwrite("extras", &tinygltf::Light::extras);
        Light.def_readwrite("extras_json_string", &tinygltf::Light::extras_json_string);
        Light.def_readwrite("extensions_json_string", &tinygltf::Light::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::Light, Light)

    PYCLASS_BEGIN(_gltf, tinygltf::PositionalEmitter, PositionalEmitter)
        PositionalEmitter.def_readwrite("cone_inner_angle", &tinygltf::PositionalEmitter::coneInnerAngle);
        PositionalEmitter.def_readwrite("cone_outer_angle", &tinygltf::PositionalEmitter::coneOuterAngle);
        PositionalEmitter.def_readwrite("cone_outer_gain", &tinygltf::PositionalEmitter::coneOuterGain);
        PositionalEmitter.def_readwrite("max_distance", &tinygltf::PositionalEmitter::maxDistance);
        PositionalEmitter.def_readwrite("ref_distance", &tinygltf::PositionalEmitter::refDistance);
        PositionalEmitter.def_readwrite("rolloff_factor", &tinygltf::PositionalEmitter::rolloffFactor);
        PositionalEmitter.def(py::init<>());
        PositionalEmitter.def(py::init<const tinygltf::PositionalEmitter &>()
        , py::arg("")
        );
        PositionalEmitter.def_readwrite("extensions", &tinygltf::PositionalEmitter::extensions);
        PositionalEmitter.def_readwrite("extras", &tinygltf::PositionalEmitter::extras);
        PositionalEmitter.def_readwrite("extras_json_string", &tinygltf::PositionalEmitter::extras_json_string);
        PositionalEmitter.def_readwrite("extensions_json_string", &tinygltf::PositionalEmitter::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::PositionalEmitter, PositionalEmitter)

    PYCLASS_BEGIN(_gltf, tinygltf::AudioEmitter, AudioEmitter)
        AudioEmitter.def_readwrite("name", &tinygltf::AudioEmitter::name);
        AudioEmitter.def_readwrite("gain", &tinygltf::AudioEmitter::gain);
        AudioEmitter.def_readwrite("loop", &tinygltf::AudioEmitter::loop);
        AudioEmitter.def_readwrite("playing", &tinygltf::AudioEmitter::playing);
        AudioEmitter.def_readwrite("type", &tinygltf::AudioEmitter::type);
        AudioEmitter.def_readwrite("distance_model", &tinygltf::AudioEmitter::distanceModel);
        AudioEmitter.def_readwrite("positional", &tinygltf::AudioEmitter::positional);
        AudioEmitter.def_readwrite("source", &tinygltf::AudioEmitter::source);
        AudioEmitter.def(py::init<>());
        AudioEmitter.def(py::init<const tinygltf::AudioEmitter &>()
        , py::arg("")
        );
        AudioEmitter.def_readwrite("extensions", &tinygltf::AudioEmitter::extensions);
        AudioEmitter.def_readwrite("extras", &tinygltf::AudioEmitter::extras);
        AudioEmitter.def_readwrite("extras_json_string", &tinygltf::AudioEmitter::extras_json_string);
        AudioEmitter.def_readwrite("extensions_json_string", &tinygltf::AudioEmitter::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::AudioEmitter, AudioEmitter)

    PYCLASS_BEGIN(_gltf, tinygltf::AudioSource, AudioSource)
        AudioSource.def_readwrite("name", &tinygltf::AudioSource::name);
        AudioSource.def_readwrite("uri", &tinygltf::AudioSource::uri);
        AudioSource.def_readwrite("buffer_view", &tinygltf::AudioSource::bufferView);
        AudioSource.def_readwrite("mime_type", &tinygltf::AudioSource::mimeType);
        AudioSource.def(py::init<>());
        AudioSource.def(py::init<const tinygltf::AudioSource &>()
        , py::arg("")
        );
        AudioSource.def_readwrite("extras", &tinygltf::AudioSource::extras);
        AudioSource.def_readwrite("extensions", &tinygltf::AudioSource::extensions);
        AudioSource.def_readwrite("extras_json_string", &tinygltf::AudioSource::extras_json_string);
        AudioSource.def_readwrite("extensions_json_string", &tinygltf::AudioSource::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::AudioSource, AudioSource)

    PYCLASS_BEGIN(_gltf, tinygltf::Model, Model)
        Model.def(py::init<>());
        Model.def(py::init<const tinygltf::Model &>()
        , py::arg("")
        );
        Model.def_readwrite("accessors", &tinygltf::Model::accessors);
        Model.def_readwrite("animations", &tinygltf::Model::animations);
        Model.def_readwrite("buffers", &tinygltf::Model::buffers);
        Model.def_readwrite("buffer_views", &tinygltf::Model::bufferViews);
        Model.def_readwrite("materials", &tinygltf::Model::materials);
        Model.def_readwrite("meshes", &tinygltf::Model::meshes);
        Model.def_readwrite("nodes", &tinygltf::Model::nodes);
        Model.def_readwrite("textures", &tinygltf::Model::textures);
        Model.def_readwrite("images", &tinygltf::Model::images);
        Model.def_readwrite("skins", &tinygltf::Model::skins);
        Model.def_readwrite("samplers", &tinygltf::Model::samplers);
        Model.def_readwrite("cameras", &tinygltf::Model::cameras);
        Model.def_readwrite("scenes", &tinygltf::Model::scenes);
        Model.def_readwrite("lights", &tinygltf::Model::lights);
        Model.def_readwrite("audio_emitters", &tinygltf::Model::audioEmitters);
        Model.def_readwrite("audio_sources", &tinygltf::Model::audioSources);
        Model.def_readwrite("default_scene", &tinygltf::Model::defaultScene);
        Model.def_readwrite("extensions_used", &tinygltf::Model::extensionsUsed);
        Model.def_readwrite("extensions_required", &tinygltf::Model::extensionsRequired);
        Model.def_readwrite("asset", &tinygltf::Model::asset);
        Model.def_readwrite("extras", &tinygltf::Model::extras);
        Model.def_readwrite("extensions", &tinygltf::Model::extensions);
        Model.def_readwrite("extras_json_string", &tinygltf::Model::extras_json_string);
        Model.def_readwrite("extensions_json_string", &tinygltf::Model::extensions_json_string);
    PYCLASS_END(_gltf, tinygltf::Model, Model)

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
            .export_values();

    _gltf.def("uri_decode", &tinygltf::URIDecode
    , py::arg("in_uri")
    , py::arg("out_uri")
    , py::arg("user_data")
    , py::return_value_policy::automatic_reference);

    _gltf.def("load_image_data", &tinygltf::LoadImageData
    , py::arg("image")
    , py::arg("image_idx")
    , py::arg("err")
    , py::arg("warn")
    , py::arg("req_width")
    , py::arg("req_height")
    , py::arg("bytes")
    , py::arg("size")
    , py::arg("")
    , py::return_value_policy::automatic_reference);

    _gltf.def("write_image_data", &tinygltf::WriteImageData
    , py::arg("basepath")
    , py::arg("filename")
    , py::arg("image")
    , py::arg("embed_images")
    , py::arg("uri_cb")
    , py::arg("out_uri")
    , py::arg("")
    , py::return_value_policy::automatic_reference);

    _gltf.def("file_exists", &tinygltf::FileExists
    , py::arg("abs_filename")
    , py::arg("")
    , py::return_value_policy::automatic_reference);

    _gltf.def("expand_file_path", &tinygltf::ExpandFilePath
    , py::arg("filepath")
    , py::arg("userdata")
    , py::return_value_policy::automatic_reference);

    _gltf.def("read_whole_file", &tinygltf::ReadWholeFile
    , py::arg("out")
    , py::arg("err")
    , py::arg("filepath")
    , py::arg("")
    , py::return_value_policy::automatic_reference);

    _gltf.def("write_whole_file", &tinygltf::WriteWholeFile
    , py::arg("err")
    , py::arg("filepath")
    , py::arg("contents")
    , py::arg("")
    , py::return_value_policy::automatic_reference);

    PYCLASS_BEGIN(_gltf, tinygltf::TinyGLTF, TinyGLTF)
        TinyGLTF.def(py::init<>());
        TinyGLTF.def("load_ascii_from_string", &tinygltf::TinyGLTF::LoadASCIIFromString
        , py::arg("model")
        , py::arg("err")
        , py::arg("warn")
        , py::arg("str")
        , py::arg("length")
        , py::arg("base_dir")
        , py::arg("check_sections") = SectionCheck::REQUIRE_VERSION
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("load_binary_from_file", &tinygltf::TinyGLTF::LoadBinaryFromFile
        , py::arg("model")
        , py::arg("err")
        , py::arg("warn")
        , py::arg("filename")
        , py::arg("check_sections") = SectionCheck::REQUIRE_VERSION
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("load_binary_from_memory", &tinygltf::TinyGLTF::LoadBinaryFromMemory
        , py::arg("model")
        , py::arg("err")
        , py::arg("warn")
        , py::arg("bytes")
        , py::arg("length")
        , py::arg("base_dir") = ""
        , py::arg("check_sections") = SectionCheck::REQUIRE_VERSION
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("write_gltf_scene_to_file", &tinygltf::TinyGLTF::WriteGltfSceneToFile
        , py::arg("model")
        , py::arg("filename")
        , py::arg("embed_images")
        , py::arg("embed_buffers")
        , py::arg("pretty_print")
        , py::arg("write_binary")
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("set_parse_strictness", &tinygltf::TinyGLTF::SetParseStrictness
        , py::arg("strictness")
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("remove_image_loader", &tinygltf::TinyGLTF::RemoveImageLoader
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("set_uri_callbacks", &tinygltf::TinyGLTF::SetURICallbacks
        , py::arg("callbacks")
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("set_fs_callbacks", &tinygltf::TinyGLTF::SetFsCallbacks
        , py::arg("callbacks")
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("set_serialize_default_values", &tinygltf::TinyGLTF::SetSerializeDefaultValues
        , py::arg("enabled")
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("get_serialize_default_values", &tinygltf::TinyGLTF::GetSerializeDefaultValues
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("set_store_original_json_for_extras_and_extensions", &tinygltf::TinyGLTF::SetStoreOriginalJSONForExtrasAndExtensions
        , py::arg("enabled")
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("get_store_original_json_for_extras_and_extensions", &tinygltf::TinyGLTF::GetStoreOriginalJSONForExtrasAndExtensions
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("set_preserve_image_channels", &tinygltf::TinyGLTF::SetPreserveImageChannels
        , py::arg("onoff")
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("set_max_external_file_size", &tinygltf::TinyGLTF::SetMaxExternalFileSize
        , py::arg("max_bytes")
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("get_max_external_file_size", &tinygltf::TinyGLTF::GetMaxExternalFileSize
        , py::return_value_policy::automatic_reference);

        TinyGLTF.def("get_preserve_image_channels", &tinygltf::TinyGLTF::GetPreserveImageChannels
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_gltf, tinygltf::TinyGLTF, TinyGLTF)


}