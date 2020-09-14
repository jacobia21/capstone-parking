import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.environ.get('CLEARDB_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True,
    "pool_recycle": 10,
    "pool_size": 0}

    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_PORT=os.environ.get('MAIL_PORT')
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')

    ADMIN = os.environ.get('ADMIN')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')