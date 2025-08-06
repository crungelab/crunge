from typing import List
from pathlib import Path

from .image_loader import ImageLoader
from ...resource.image import Image


class MultiImageLoader:
    def __init__(self, image_loader: ImageLoader = ImageLoader()) -> None:
        self.image_loader = image_loader

    def load(self, paths: List[Path]) -> List[Image]:
        images = []
        for path in paths:
            image = self.image_loader.load(path)
            if image is not None:
                images.append(image)
        return images