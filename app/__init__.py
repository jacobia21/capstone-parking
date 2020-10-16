""" This is the main app package for the Soar High Parking website. It creates and initializes the flask app. """

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
toolbar = DebugToolbarExtension()

import app.event_listeners
def create_app(config_class=None):
    """
    Creates and initializes flask app.

    :param config_class: The Config object to use when initializing the app
    :type config_class: Config

    :returns: The configured Flask object for the app
    :rtype: Flask

    """
    app = Flask(__name__)

    environment = os.environ.get('FLASK_ENV')
    if config_class is not None:
        app.config.from_object(config_class)
    elif environment == 'testing':
        app.config.from_object('config.TestingConfig')
    elif environment == 'development':
        app.config.from_object('config.DevelopmentConfig')
    elif environment == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        raise Exception("No configuration object was passed and could not determine from environment")

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    if app.debug and not app.testing:
        toolbar.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['ADMIN'],
                toaddrs=app.config['ADMIN'], subject='[Soar High Parking] System Failure',
                credentials=auth, secure=secure, timeout=10.0)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/soarhighparking.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Soar High Parking - startup')

    return app
