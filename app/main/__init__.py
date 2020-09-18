""" This package holds all the blueprints for the users view of the site """
from flask import Blueprint

bp = Blueprint('main', __name__,template_folder='templates')

from app.main import routes
