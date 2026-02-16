from .bucket_phase import BucketPhase
from .render_item import FilterItem

class FilterPhase(BucketPhase[FilterItem]):
    def render(self) -> None:
        self.render_items()

    def render_items(self):
        for d in self.items:
            #logger.debug(f"FilterPhase: drawing item for {d.node}")
            d.callback()
