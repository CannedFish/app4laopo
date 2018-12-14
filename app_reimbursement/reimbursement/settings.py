# -*- coding: utf8 -*-

class Config(object):
    # Flask settings
    DEBUG = False
    TESTING = False

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_NATIVE_UNICODE = 'utf8'

    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False

class ProductionConfig(Config):
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SERVER_NAME = '0.0.0.0:8888'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    TESTING = True

cur_config = DevelopmentConfig

