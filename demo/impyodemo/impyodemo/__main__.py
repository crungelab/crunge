import os, sys

sys.path.append(os.getcwd())

from impyodemo import App


app = App().create()

app.use('help')
app.use('intro')
app.use('controls')
app.use('generators')
app.use('soundfiles')
app.use('envelopes')
app.use('filters')
app.use('effects')
app.use('dynamics')
app.use('callbacks')
app.use('tables')
app.use('midi')
#app.use('osc')
app.use('multirate')
app.use('multicore')
app.use('utilities')
app.use('events')

app.show('about')

app.run()
