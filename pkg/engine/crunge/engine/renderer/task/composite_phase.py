from .bucket_phase import BucketPhase
from .render_item import CompositeItem

class CompositePhase(BucketPhase[CompositeItem]):
    def render(self) -> None:
        self.render_items()

    def render_items(self):
        for d in self.items:
            #logger.debug(f"CompositePhase: drawing item for {d.node}")
            d.callback()
