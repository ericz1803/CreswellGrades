import os
basedir = os.path.abspath(os.path.dirname(__file__))
import warnings
import redis

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY", default=b'\xa4U\xb4]\x1a\x84\xfef\xb8\xaf)71vC#\x19PO\x9e\xf72l\x00\x9cG\x01\xb7\xa0\x1d/ \x9f\x0c\x86B\x17\x80\x1d\xb5\xb4A\xa8\x1eS\xd8\xaa\xd18\xad')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'creswellgrades@gmail.com'
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER='creswellgrades@gmail.com'
    SESSION_TYPE = 'null'

    if not SECRET_KEY:
        warnings.warn("Secret Key not set.")


class ProductionConfig(Config):
    DEBUG = False
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(os.environ.get("REDISCLOUD_URL")) if os.environ.get("REDISCLOUD_URL") else redis.Redis(host='localhost', port=6379, db=0)
    SCOUT_MONITOR = True
    SCOUT_KEY = os.environ.get("SCOUT_KEY")
    SCOUT_NAME = "Creswell Grades"

class DevelopmentConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True