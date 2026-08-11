import os, sys

sys.path.append(os.getcwd())

from spine_demo import SpineDemo

app = SpineDemo().create()

app.use('spineboy')

app.show_channel('spineboy')

app.run()
