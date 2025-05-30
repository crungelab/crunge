from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Columns(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: Columns - File list")
        imgui.columns(4, 'fileList')
        imgui.separator()
        imgui.text("ID")
        imgui.next_column()
        imgui.text("File")
        imgui.next_column()
        imgui.text("Size")
        imgui.next_column()
        imgui.text("Last Modified")
        imgui.next_column()
        imgui.separator()
        imgui.set_column_offset(1, 40)

        imgui.next_column()
        imgui.text('FileA.txt')
        imgui.next_column()
        imgui.text('57 Kb')
        imgui.next_column()
        imgui.text('12th Feb, 2016 12:19:01')
        imgui.next_column()

        imgui.next_column()
        imgui.text('ImageQ.png')
        imgui.next_column()
        imgui.text('349 Kb')
        imgui.next_column()
        imgui.text('1st Mar, 2016 06:38:22')
        imgui.next_column()

        imgui.columns(1)
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(Columns, "columns", "Columns"))
