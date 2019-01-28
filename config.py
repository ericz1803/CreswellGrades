import os
import warnings

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = None
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    DEBUG = True
    DEVELOPMENT = True

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    DEBUG=False
    TESTING=False
    if not SECRET_KEY:
        warnings.warn("No secret key set.")
