""" This is the main app package for the Soar High Parking website. It creates and initializes the flask app. """

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# We use Flask-SQLAlchemy as an Object Relational Mapper(ORM) to simplify database interactions.
db = SQLAlchemy()

# We use Flask-Migrate to handle database migrations.
migrate = Migrate(compare_type=True)

# We use Flask_Login's LoginManager to handle logging user's in and out, restrict views, and track the current user.
# We also tell the LoginManager what view holds our Login Form here.
login = LoginManager()
login.login_view = 'auth.login'

# We use Flask-DebugToolbar in the development environment to aid in development.
toolbar = DebugToolbarExtension()


def create_app(config_class=None):
    """
    Creates and initializes flask app.

    :param config_class: The Config object to use when initializing the app. If none is passed, we look for the
                         FLASK_ENV environment variable and select a config class based on the current environment.
                         For example, if FLASK_ENV = 'testing', then the app will use the TestingConfig class
                         in initialization.
    :type config_class: Config

    :returns: The configured Flask object for the application.
    :rtype: Flask

    """

    app = Flask(__name__)

    # Set up the proper app configurations based on the Flask environment or passed in config_class.
    # Raises an exception if config_class is None and FLASK_ENV is not set.
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

    # Pass the app to the the extensions we set up at the top of the file.
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Only set up the Debug Toolbar if FLASK_DEBUG=True and TESTING=False in config.
    if app.debug and not app.testing:
        toolbar.init_app(app)

    # Only import the event listeners if TESTING = False in config. These event listeners create notifications on
    # database changes and add them to the Notifications table in the database. However, they currently cause tests
    # to fail, so we skip importing them when testing.
    if not app.testing:
        from app import event_listeners

    # Register the errors blueprint, which holds all the routes and logic for handling 400 and 500 website errors.
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Register the auth blueprint, which holds all the routes and logic for the administrator portion of the site.
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Register the main blueprint, which holds all the routes and logic for the user portion of the site.
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Register the auth blueprint, which holds all the routes and logic for handling authenticating administrators.
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Set up the correct log handler when in production environment.
    if not app.debug and not app.testing:
        # If the LOG_TO_STDOUT environment variable is set, we use a StreamHandler to log information.
        # This allows us to log messages and have them appear in Heroku's Application Log window.
        # Currently, this environment variable is only set in the Heroku Config Vars, as it is not necessary
        # for local development.
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)

        # If LOG_TO_STDOUT is not set, we simply create a logs directory and write our log messages to a file.
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

        # Log all messages marked INFO level and up.
        app.logger.setLevel(logging.INFO)

    return app
