import os
import sys
from flask import Flask
from mongoengine import connect


app = Flask(__name__)

if os.environ.get('SOURCERER_SETTINGS'):
    app.config.from_envvar("SOURCERER_SETTINGS")
else:
    app.logger.warn("SOURCERER_SETTINGS environment not declared "
                    "defaulting to the test environment...")
    app.config.from_pyfile(os.path.abspath('./config/config-local.py'))


connect(
    host='mongodb://localhost/kndb'
)
