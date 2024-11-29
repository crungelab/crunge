import os, sys

sys.path.append(os.getcwd())

from imflodemo import App

app = App().create()

app.use('basic')
app.use('connect')
app.use('sine')
#app.use('sparks')

app.show_channel('basic')

app.run()
