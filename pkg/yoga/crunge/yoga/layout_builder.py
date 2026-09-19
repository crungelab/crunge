from crunge import yoga

from .style_builder import StyleBuilder


class LayoutBuilder(StyleBuilder):
    def build(self):
        layout = yoga.LayoutNode()
        layout.set_style(self.style)
        return layout