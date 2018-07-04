from flask import Flask




app = Flask('amazon')
app.secret_key = 'ilovemymom'

from amazon import api

