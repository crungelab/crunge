from ....vu import Vu
from ....renderer.task.filter_phase import FilterItem, FilterPhase

class FilterVu(Vu):
    def _render(self):
        phase: FilterPhase = self.current_renderer.plan.get_phase(FilterPhase)
        phase.add(FilterItem(self, self._draw))
