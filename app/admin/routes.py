from app.admin import bp
from flask import render_template, url_for
from flask_login import login_required

@bp.route('/home')
@login_required
def home():
    return render_template("admin/index.html", title='Command Center')

@bp.route('/administrators')
@login_required
def administrators():
    return render_template("admin/administrators/administrators.html", title='Administrators')

@bp.route('/administrators/add', methods=['GET', 'POST'])
@login_required
def add_administrator():
    return render_template("admin/administrators/administrators.html", title='Administrators')

@bp.route('/administrators/edit',  methods=['GET', 'POST'])
@login_required
def edit_administrator():
    return render_template("admin/administrators/administrators.html", title='Administrators')


@bp.route('/administrators/delete',  methods=['POST'])
@login_required
def delete_administrator():
    return render_template("admin/administrators/administrators.html", title='Administrators')

@bp.route('/cameras')
@login_required
def cameras():
    return render_template("admin/cameras/cameras.html", title='Cameras')

@bp.route('/cameras/add', methods=['GET', 'POST'])
@login_required
def add_camera():
    return render_template("admin/cameras/cameras.html", title='Cameras')

@bp.route('/cameras/edit',  methods=['GET', 'POST'])
@login_required
def edit_camera():
    return render_template("admin/cameras/cameras.html", title='Cameras')


@bp.route('/cameras/delete',  methods=['POST'])
@login_required
def delete_camera():
    return render_template("admin/cameras/cameras.html", title='Cameras')

@bp.route('/zones')
@login_required
def zones():
    return render_template("admin/zones/zones.html", title='Zones')

@bp.route('/zones/add', methods=['GET', 'POST'])
@login_required
def add_zone():
    return render_template("admin/zones/zones.html", title='Zones')

@bp.route('/zones/edit',  methods=['GET', 'POST'])
@login_required
def edit_zone():
    return render_template("admin/zones/zones.html", title='Zones')


@bp.route('/zones/delete',  methods=['POST'])
@login_required
def delete_zone():
    return render_template("admin/zones/zones.html", title='Zones')


@bp.route('/lots')
@login_required
def lots():
    return render_template("admin/lots/lots.html", title='Lots')

@bp.route('/lots/add', methods=['GET', 'POST'])
@login_required
def add_lot():
    return render_template("admin/lots/lots.html", title='Lots')

@bp.route('/lots/edit',  methods=['GET', 'POST'])
@login_required
def edit_lot():
    return render_template("admin/lots/lots.html", title='Lots')


@bp.route('/lots/delete',  methods=['POST'])
@login_required
def delete_lot():
    return render_template("admin/lots/lots.html", title='Lots')

@bp.route('/spaces')
@login_required
def spaces():
    return render_template("admin/spaces/spaces.html", title='Parking Spaces')

# FIXME: is this needed?
# @bp.route('/spaces/add', methods=['GET', 'POST'])
# @login_required
# def add_space():
#     return render_template("admin/spaces/spaces.html", title='Parking Spaces')

@bp.route('/spaces/edit',  methods=['GET', 'POST'])
@login_required
def edit_space():
    return render_template("admin/spaces/spaces.html", title='Parking Spaces')


@bp.route('/spaces/delete',  methods=['POST'])
@login_required
def delete_space():
    return render_template("admin/spaces/spaces.html", title='Parking Spaces')

@bp.route('/system_log')
@login_required
def system_log():
    return render_template("admin/system_log/system_log.html", title='System Log')
