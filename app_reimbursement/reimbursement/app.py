# -*- coding: utf-8 -*-

import logging.config
import os

from flask import Flask
from reimbursement import settings
from reimbursement.database import db
from reimbursement.v1 import blueprint as api_v1

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
LOG = logging.getLogger(__name__)

def initialize_app(flask_app):
    app.config.from_object(settings.cur_config)
    flask_app.register_blueprint(api_v1)
    db.init_app(app)

def main():
    initialize_app(app)
    LOG.info('>>>>> Starting development server at http://%s/api/v1/ <<<<<' \
            % (app.config['SERVER_NAME']))
    app.run()

if __name__ == "__main__":
    main()

