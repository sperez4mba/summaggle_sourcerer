import os
import sys
from flask import Flask
from mongoengine import connect
import logging


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


formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(pathname)s %(funcName)s %(message)s")
log_handler = logging.FileHandler(
        '/var/log/summaggle.log'
)
log_handler.setFormatter(formatter)
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(log_handler)
logger = logging.getLogger('summaggle')
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


from sourcerer.cli import *
import sourcerer.views
