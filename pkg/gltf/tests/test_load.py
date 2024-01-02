from pathlib import Path

from loguru import logger

from crunge import gltf

resource_root = Path(__file__).parent.parent.parent / "gltfv" / "resources"

scene_path = resource_root / "models" / "BoxVertexColors" / "glTF" / "BoxVertexColors.gltf"
#scene_path = resource_root / "models" / "BoxTextured" / "glTF" / "BoxTextured.gltf"
#scene_path = resource_root / "models" / "Cube" / "glTF" / "Cube.gltf"
#scene_path = resource_root / "models" / "SimpleMeshes" / "glTF" / "SimpleMeshes.gltf"
#scene_path = resource_root / "models" / "CesiumMilkTruck" / "glTF" / "CesiumMilkTruck.gltf"
#scene_path = resource_root / "models" / "DamagedHelmet" / "glTF" / "DamagedHelmet.gltf"
#scene_path = resource_root / "models" / "Character" / "Character.gltf"
#scene_path = resource_root / "models" / "RobotCopernicus" / "scene.gltf"

loader = gltf.TinyGLTF()
logger.debug(f"loader: {loader}")

tg_model = gltf.Model()
logger.debug(f"tg_model_: {tg_model}")

err = ''
warn = ''

#res = loader.load_ascii_from_file(tg_model, err, warn, str(scene_path), gltf.SectionCheck.REQUIRE_VERSION)
res = loader.load_ascii_from_file(tg_model, err, warn, str(scene_path))
logger.debug(f"res: {res}")

if not warn:
    logger.debug(f"warn: {warn}")

if not err:
    logger.debug(f"err: {err}")

if not res:
    logger.debug(f"Failed to load glTF: {scene_path}")
else:
    logger.debug(f"Loaded glTF: {scene_path}")

tg_scene = tg_model.scenes[tg_model.default_scene]
logger.debug(f"tg_scene: {tg_scene}")

'''
for i in range(len(tg_scene.nodes)):
    assert (tg_scene.nodes[i] >= 0) and (tg_scene.nodes[i] < len(tg_model.nodes))
    node = tg_model.nodes[tg_scene.nodes[i]]
    logger.debug(f"node: {node}")
'''

'''
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
'''

for node in tg_model.nodes:
    logger.debug(f"node: {node}")
    logger.debug(f"node.camera: {node.camera}")
    logger.debug(f"node.name: {node.name}")
    logger.debug(f"node.skin: {node.skin}")
    logger.debug(f"node.mesh: {node.mesh}")
    logger.debug(f"node.light: {node.light}")
    logger.debug(f"node.emitter: {node.emitter}")
    logger.debug(f"node.children: {node.children}")
    logger.debug(f"node.rotation: {node.rotation}")
    logger.debug(f"node.scale: {node.scale}")
    logger.debug(f"node.translation: {node.translation}")
    logger.debug(f"node.matrix: {node.matrix}")
    logger.debug(f"node.weights: {node.weights}")
    logger.debug(f"node.extensions: {node.extensions}")
    logger.debug(f"node.extras: {node.extras}")
    logger.debug(f"node.extras_json_string: {node.extras_json_string}")
    logger.debug(f"node.extensions_json_string: {node.extensions_json_string}")

    if node.mesh >= 0 and node.mesh < len(tg_model.meshes):
        logger.debug(f"node.mesh: {node.mesh}")
        mesh = tg_model.meshes[node.mesh]
        logger.debug(f"mesh: {mesh}")

        for primitive in mesh.primitives:
            logger.debug(f"primitive: {primitive}")
            logger.debug(f"primitive.attributes: {primitive.attributes}")
            logger.debug(f"primitive.indices: {primitive.indices}")
            logger.debug(f"primitive.material: {primitive.material}")
            logger.debug(f"primitive.mode: {primitive.mode}")
            logger.debug(f"primitive.targets: {primitive.targets}")
            logger.debug(f"primitive.extensions: {primitive.extensions}")
            logger.debug(f"primitive.extras: {primitive.extras}")
            logger.debug(f"primitive.extras_json_string: {primitive.extras_json_string}")
            logger.debug(f"primitive.extensions_json_string: {primitive.extensions_json_string}")

            if primitive.indices >= 0 and primitive.indices < len(tg_model.accessors):
                logger.debug(f"primitive.indices: {primitive.indices}")
                accessor = tg_model.accessors[primitive.indices]
                logger.debug(f"accessor: {accessor}")
                logger.debug(f"accessor.buffer_view: {accessor.buffer_view}")
                logger.debug(f"accessor.byte_offset: {accessor.byte_offset}")
                logger.debug(f"accessor.component_type: {accessor.component_type}")
                logger.debug(f"accessor.normalized: {accessor.normalized}")
                logger.debug(f"accessor.count: {accessor.count}")
                logger.debug(f"accessor.type: {accessor.type}")
                logger.debug(f"accessor.max_values: {accessor.max_values}")
                logger.debug(f"accessor.min_values: {accessor.min_values}")
                logger.debug(f"accessor.sparse: {accessor.sparse}")
                logger.debug(f"accessor.extensions: {accessor.extensions}")
                logger.debug(f"accessor.extras: {accessor.extras}")
                logger.debug(f"accessor.extras_json_string: {accessor.extras_json_string}")
                logger.debug(f"accessor.extensions_json_string: {accessor.extensions_json_string}")

            for attribute in primitive.attributes:
                logger.debug(f"attribute: {attribute}")
                logger.debug(f"primitive.attributes[attribute]: {primitive.attributes[attribute]}")
                if primitive.attributes[attribute] >= 0 and primitive.attributes[attribute] < len(tg_model.accessors):
                    logger.debug(f"primitive.attributes[attribute]: {primitive.attributes[attribute]}")
                    accessor = tg_model.accessors[primitive.attributes[attribute]]
                    logger.debug(f"accessor: {accessor}")
                    #logger.debug(f"accessor.buffer_view: {access