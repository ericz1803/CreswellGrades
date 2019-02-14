import os
basedir = os.path.abspath(os.path.dirname(__file__))
import warnings


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    if not SECRET_KEY:
        warnings.warn("Secret Key not set.")


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True