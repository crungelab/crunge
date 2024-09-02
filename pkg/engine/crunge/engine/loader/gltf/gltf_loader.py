from typing import List
from pathlib import Path

from loguru import logger
from jinja2 import Environment, BaseLoader, ChoiceLoader, PackageLoader, select_autoescape

from crunge import gltf

from ...d3.scene_3d import Scene3D

from ..loader import Loader

from .builder.builder_context import BuilderContext
from .builder.scene_builder import SceneBuilder


class GltfLoader(Loader):
    def __init__(self, template_loaders: List[BaseLoader] = []) -> None:
        super().__init__()
        self.template_loader_stack: List[BaseLoader] = [PackageLoader("crunge.engine.loader.gltf", "templates")]
        self.template_loader_stack.extend(template_loaders)
        self.tf_model = None

    def push_template_loader(self, loader: BaseLoader):
        self.template_loader_stack.append(loader)

    def create_context(self) -> BuilderContext:
        loaders = list(reversed(self.template_loader_stack))
        logger.debug(f"loaders: {loaders}")
        template_env = Environment(
            loader = ChoiceLoader(loaders),
            autoescape=select_autoescape()
        )

        scene = Scene3D()
        self.context = BuilderContext(scene, self.tf_model, template_env)

    def load(self, scene_path:Path) -> Scene3D:
        loader = gltf.TinyGLTF()
        logger.debug(f"loader: {loader}")

        self.tf_model = tf_model = gltf.Model()
        logger.debug(f"tf_model_: {self.tf_model}")

        self.create_context()

        res, err, warn = loader.load_ascii_from_file(tf_model, str(scene_path))

        logger.debug(f"res: {res}")

        if warn:
            logger.debug(f"warn: {warn}")

        if err:
            logger.debug(f"err: {err}")

        if not res:
            logger.debug(f"Failed to load glTF: {scene_path}")
            exit()
        else:
            logger.debug(f"Loaded glTF: {scene_path}")

        self.tf_scene = tf_scene = tf_model.scenes[tf_model.default_scene]
        logger.debug(f"tf_scene: {tf_scene}")

        scene = SceneBuilder(self.context, tf_scene).build()
        return scene