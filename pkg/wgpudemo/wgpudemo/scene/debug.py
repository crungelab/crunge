from loguru import logger

def debug_mesh(model, mesh):
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

        if primitive.indices >= 0 and primitive.indices < len(model.accessors):
            logger.debug(f"primitive.indices: {primitive.indices}")
            accessor = model.accessors[primitive.indices]
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
            if primitive.attributes[attribute] >= 0 and primitive.attributes[attribute] < len(model.accessors):
                logger.debug(f"primitive.attributes[attribute]: {primitive.attributes[attribute]}")
                accessor = model.accessors[primitive.attributes[attribute]]
                logger.debug(f"accessor: {accessor}")
                #logger.debug(f"accessor.buffer_view: {access