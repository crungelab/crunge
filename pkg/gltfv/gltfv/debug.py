from loguru import logger

def debug_node(model, node):
    logger.debug(f"node: {node}")
    logger.debug(f"node.name: {node.name}")
    logger.debug(f"node.children: {node.children}")
    logger.debug(f"node.mesh: {node.mesh}")
    logger.debug(f"node.rotation: {node.rotation}")
    logger.debug(f"node.scale: {node.scale}")
    logger.debug(f"node.translation: {node.translation}")
    logger.debug(f"node.matrix: {node.matrix}")
    logger.debug(f"node.weights: {node.weights}")
    logger.debug(f"node.camera: {node.camera}")
    logger.debug(f"node.skin: {node.skin}")
    logger.debug(f"node.extensions: {node.extensions}")
    logger.debug(f"node.extras: {node.extras}")
    logger.debug(f"node.extras_json_string: {node.extras_json_string}")
    logger.debug(f"node.extensions_json_string: {node.extensions_json_string}")

def debug_mesh(model, mesh):
    logger.debug(f"mesh: {mesh}")
    logger.debug(f"mesh.name: {mesh.name}")
    logger.debug(f"mesh.primitives: {mesh.primitives}")
    logger.debug(f"mesh.weights: {mesh.weights}")
    logger.debug(f"mesh.extensions: {mesh.extensions}")
    logger.debug(f"mesh.extras: {mesh.extras}")
    logger.debug(f"mesh.extras_json_string: {mesh.extras_json_string}")
    logger.debug(f"mesh.extensions_json_string: {mesh.extensions_json_string}")

def debug_primitive(primitive):
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

def debug_accessor(accessor):
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

def debug_attribute(attribute):
    logger.debug(f"attribute: {attribute}")
