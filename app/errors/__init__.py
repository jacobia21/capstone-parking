"""This package holds all the blueprints for error handlers."""

from app.errors import handlers
from flask import Blueprint

bp = Blueprint('errors', __name__, template_folder='templates')
