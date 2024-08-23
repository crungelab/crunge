import os, sys

sys.path.append(os.getcwd())

from implotdemo import App

app = App().create()

app.use('index')
app.use('demo')
app.use('line')
app.use('bar')
app.use('scatter')
app.use('shaded')

app.show('shaded')

app.run()
