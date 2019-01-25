# -*- coding: utf-8 -*-

import logging.config
import os

from flask import Flask
from reimbursement import settings
from reimbursement.database import db
from reimbursement.v1 import blueprint as api_v1

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
LOG = logging.getLogger(__name__)

def create_app(config_name):
    app = Flask(__name__)

    config = getattr(settings, config_name)
    app.config.from_object(config)
    app.register_blueprint(api_v1)
    db.init_app(app)

    return app

if __name__ == "__main__":
    create_app('DevelopmentConfig').run()

