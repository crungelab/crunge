from pathlib import Path

from loguru import logger
import trimesh as tm

class Scene:
    def __init__(self) -> None:
        pass
    
    def load(self, path:Path):
        self.scene = scene = tm.load(str(path))
        logger.debug(scene.__dict__)
        logger.debug(scene.graph.__dict__)
        logger.debug(scene.graph.transforms.edge_data)
        logger.debug(scene.graph.transforms.node_data)
        #print(scene)
        #print(scene.geometry)
        graph = scene.graph.to_networkx()
        logger.debug(graph.edges)
        logger.debug(graph.nodes)
