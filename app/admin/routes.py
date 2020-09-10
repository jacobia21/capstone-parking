from app.admin import bp
from flask import render_template, url_for, flash, redirect
from flask_login import login_required
from app.models import User, Zone, Camera, ParkingSpace, Lot, SystemLog
from app.admin.forms import AddAdminForm, EditAdminForm
from app import db

@bp.route('/home')
@login_required
def home():
    user_count = User.query.count()
    camera_count = Camera.query.count()
    zone_count = Zone.query.count()
    lot_count = Lot.query.count()
    return render_template("admin/index.html", title='Command Center', users=user_count, cameras=camera_count, zones=zone_count, lots=lot_count)

@bp.route('/administrators')
@login_required
def administrators():
    administrators = User.query.all()
    return render_template("admin/administrators/administrators.html", title='Administrators', administrators=administrators)

@bp.route('/administrators/add', methods=['GET', 'POST'])
@login_required
def add_administrator():
    form = AddAdminForm()
    if form.validate_on_submit():
        # form.validate_name(form.first_name.data, form.last_name.data,form.middle_initial.data)
        try:
            user = User( email=form.email.data, first_name = form.first_name.data,last_name = form.last_name.data,middle_initial = form.middle_initial.data)
            #TODO send activiation message to the new user
            flash("New Admin Added")
            return redirect(url_for('admin.administrators'))
        except:
            flash("Something went wrong! Try again later")
            return render_template("admin/administrators/add_administrator.html", title='Add Administrator', form=form, error=1)
    return render_template("admin/administrators/add_administrator.html", title='Add Administrator', form=form)

@bp.route('/administrators/edit/<user_id>',  methods=['GET', 'POST'])
@login_required
def edit_administrator(user_id):
    form = EditAdminForm()
    if form.validate_on_submit():
        try:
            admin = User.query.get(user_id)
            admin.email = form.email.data
            admin.first_name = form.first_name.data
            admin.last_name = form.last_name.data
            admin.middle_initial = form.middle_initial.data
            db.session.commit()
        except Exception as error:
            print(error)
            flash("Something went wrong! Try again later")
            return render_template("admin/administrators/edit_administrator.html", title='Administrators', form=form, admin=User.query.get(user_id), error=1)

        return redirect(url_for('admin.administrators'))
    
    admin = User.query.get(user_id)
    return render_template("admin/administrators/edit_administrator.html", title='Administrators', form=form, admin=admin)


@bp.route('/administrators/delete/<user_id>',  methods=['POST'])
@login_required
def delete_administrator(user_id):
    try:
        admin = User.query.get(user_id)
        db.session.delete(admin)
        db.session.commit()
        flash("Administrator removed")
    except Exception as error: 
        print(error)
        flash("Something went wrong! Try again later")
        return redirect(url_for('admin.administrators', error=1))
    return redirect(url_for('admin.administrators'))

@bp.route('/cameras')
@login_required
def cameras():
    cameras = Camera.query.all()
    return render_template("admin/cameras/cameras.html", title='Cameras', cameras=cameras)

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
    zones = Zone.query.all()
    return render_template("admin/zones/zones.html", title='Zones', zones=zones)

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
    lots = Lot.query.all()
    return render_template("admin/lots/lots.html", title='Lots', lots= lots)

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
    spaces = ParkingSpace.query.all()
    return render_template("admin/spaces/spaces.html", title='Parking Spaces',spaces=spaces)

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
    logs = SystemLog.query.all()
    return render_template("admin/system_log/system_log.html", title='System Log', logs=logs)
