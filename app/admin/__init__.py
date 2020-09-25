from app.admin import routes
from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='', template_folder='templates')
