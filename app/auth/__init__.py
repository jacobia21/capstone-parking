""" This package holds the blueprints for all authentication. """

from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')

from app.auth import routes