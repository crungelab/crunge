from crunge import imgui
from crunge.engine import App, colors
from crunge.demo import Page, PageChannel


class Button(Page):
    def reset(self):
        self.message = ""

    def _draw(self):
        imgui.begin("Example: buttons")

        if imgui.button("Button 1"):
            self.message = "You pressed 1!"
        if imgui.button("Button 2"):
            self.message = "You pressed 2!"
        imgui.text(self.message)
        imgui.end()
        super()._draw()


class ColorButton(Page):
    def reset(self):
        self.color = colors.BLACK
        self.color_name = ""

    def _draw(self):
        imgui.begin("Example: color button")
        if imgui.color_button("Button 1", colors.RED, 0, (10, 10)):
            self.color = colors.RED
            self.color_name = "Red"
        if imgui.color_button("Button 2", colors.GREEN, 0, (10, 10)):
            self.color = colors.GREEN
            self.color_name = "Green"
        if imgui.color_button("Wide Button", colors.BLUE, 0, (20, 10)):
            self.color = colors.BLUE
            self.color_name = "Blue"
        if imgui.color_button("Tall Button", colors.MAGENTA, 0, (10, 20)):
            self.color = colors.MAGENTA
            self.color_name = "Magenta"

        imgui.text_colored(self.color, f"You chose {self.color_name}")
        imgui.end()
        super()._draw()


class RadioButtonPage(Page):
    def reset(self):
        self.radio_active = False

    def _draw(self):
        imgui.begin(self.title)

        if imgui.radio_button("Radio button", self.radio_active):
            self.radio_active = not self.radio_active

        imgui.end()
        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(Button, "button", "Buttons"))
    app.add_channel(PageChannel(ColorButton, "colorbutton", "Buttons - Color"))
    app.add_channel(PageChannel(RadioButtonPage, "radiobutton", "Buttons - Radio"))
