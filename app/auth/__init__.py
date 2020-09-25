""" This package holds the blueprints for all authentication. """

from app.auth import routes
from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')
