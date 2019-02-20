from flask import Flask, request
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy

from makecelery import make_celery

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

# if app.config['TEST']:
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:19950707@localhost/automltest'
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:19950707@localhost/automl'

CORS(app, supports_credentials=True)
db = SQLAlchemy(app=app)
celery = make_celery(app)
req = request

import automl.router
