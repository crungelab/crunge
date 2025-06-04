from crunge import yoga

from .style_builder import StyleBuilder


class LayoutBuilder(StyleBuilder):
    def build(self):
        layout = yoga.Layout()
        layout.set_style(self.style)
        return layout