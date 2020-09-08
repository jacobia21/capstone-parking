from app.admin import bp
from flask import render_template, url_for
from flask_login import login_required

@bp.route('/home')
@login_required
def home():
    return render_template("admin/home.html", title='Admin Home')