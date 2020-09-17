from app.admin import bp
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required
from app.models import User, Zone, Camera, ParkingSpace, Lot, SystemLog, AdminGroup
from app.admin.forms import AddAdminForm, EditAdminForm, AddZoneForm, EditZoneForm, AddLotForm, EditLotForm, AddCameraForm, EditCameraZone
from app.auth.email import send_activation_email
from app import db
from app.enums import Groups, LogStatus, CameraStatus
from flask_login import current_user
from datetime import datetime

@bp.route('/home')
@login_required
def home():
    user_count = User.query.count()
    camera_count = Camera.query.count()
    zone_count = Zone.query.count()
    lot_count = Lot.query.count()
    return render_template("home.html", title='Command Center', users=user_count, cameras=camera_count, zones=zone_count, lots=lot_count)

@bp.route('/administrators')
@login_required
def administrators():
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
    administrators = User.query.all()
    return render_template("administrators/administrators.html", title='Administrators', administrators=administrators)

@bp.route('/administrators/add', methods=['GET', 'POST'])
@login_required
def add_administrator():
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
    form = AddAdminForm()
    form.group.choices = [(g.id, g.name) for g in AdminGroup.query.order_by('name')]

    if form.validate_on_submit():
        # form.validate_name(form.first_name.data, form.last_name.data,form.middle_initial.data)
        try:
            user = User( email=form.email.data, first_name = form.first_name.data,last_name = form.last_name.data,middle_initial = form.middle_initial.data, group_id=form.group.data)

            db.session.add(user)
            db.session.commit()
            send_activation_email(user)
            flash("New Admin Added")
            return redirect(url_for('admin.administrators'))
        except Exception as err:
            print(err)
            flash("Something went wrong! Try again later")
            return render_template("administrators/add_administrator.html", title='Add Administrator', form=form, error=1)
    return render_template("administrators/add_administrator.html", title='Add Administrator', form=form)

@bp.route('/administrators/edit/<user_id>',  methods=['GET', 'POST'])
@login_required
def edit_administrator(user_id):
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
    form = EditAdminForm()
    form.group.choices = [(g.id, g.name) for g in AdminGroup.query.order_by('name')]

    if form.validate_on_submit():
        try:
            admin = User.query.get(user_id)
            admin.email = form.email.data
            admin.first_name = form.first_name.data
            admin.last_name = form.last_name.data
            admin.middle_initial = form.middle_initial.data
            admin.group_id = form.group.data
            db.session.commit()
            flash('Administrator updated successfully!')
        except Exception as error:
            print(error)
            flash("Something went wrong! Try again later")
            return render_template("administrators/edit_administrator.html", title='Edit Adminstrator', form=form, admin=User.query.get(user_id), error=1)

        return redirect(url_for('admin.administrators'))
    
    admin = User.query.get(user_id)
    form.group.data = admin.group_id
    return render_template("administrators/edit_administrator.html", title='Edit Administrator', form=form, admin=admin)


@bp.route('/administrators/delete/<user_id>',  methods=['POST'])
@login_required
def delete_administrator(user_id):
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
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
    return render_template("cameras/cameras.html", title='Cameras', cameras=cameras)

@bp.route('/cameras/add', methods=['GET', 'POST'])
@login_required
def add_camera():
    form = AddCameraForm()
    form.lot.choices = [(lot.id, lot.name) for lot in Lot.query.order_by('name')]
    form.status.choices = [(s.name, s.name) for s in CameraStatus]
    
    form.lot.render_kw={'style': 'height: fit-content; list-style: none;'}
    form.status.render_kw={'style': 'height: fit-content; list-style: none;'}

    if form.validate_on_submit():
        try:
            camera = Camera(location=form.location.data, lot_id=form.lot.data, status=form.status.data)
            db.session.add(camera)
            db.session.commit()
            return redirect(url_for('.mark_spaces'))
        except Exception as err:
            print(err)
            flash("Something went wrong! Try again later")
            return render_template("cameras/add_camera.html", title='Add Camera', form=form, error=1)
    return render_template("cameras/add_camera.html", title='Add Camera', form=form)

@bp.route('/cameras/edit/<camera_id>',  methods=['GET', 'POST'])
@login_required
def edit_camera(camera_id):
    form = EditCameraZone(camera_id=camera_id)
    form.lot.choices = [(lot.id, lot.name) for lot in Lot.query.order_by('name')]
    form.status.choices = [(s.name, s.name) for s in CameraStatus]
    
    if form.validate_on_submit():
        try:
            camera = Camera.query.get(camera_id)
            camera.location = form.location.data
            camera.status = form.status.data
            camera.lot = form.lot.data
            db.session.commit()
            flash('Camera updated successfully!')
            # TODO either send directly to edit spaces page or ask if they would like to edit spaces
        except Exception as error:
            print(error)
            flash("Something went wrong! Try again later")
            return render_template("cameras/edit_camera/html", title='Edit Camera', form=form, camera=Camera.query.get(camera_id),error=1)

        return redirect(url_for('admin.cameras'))
        
    camera = Camera.query.get(camera_id)
    form.lot.data = camera.lot_id
    form.status.data = camera.status.value
    return render_template("cameras/edit_camera.html", title='Edit Camera', form=form, camera=Camera.query.get(camera_id))

@bp.route('/cameras/delete/<camera_id>',  methods=['POST'])
@login_required
def delete_camera(camera_id):
    try:
        camera = Camera.query.get(camera_id)
        db.session.delete(camera)
        db.session.commit()
        flash("Camera removed")
    except Exception as error: 
        print(error)
        flash("Something went wrong! Try again later")
    return redirect(url_for('admin.cameras'))


@bp.route('/zones')
@login_required
def zones():
    zones = Zone.query.all()
    return render_template("zones/zones.html", title='Zones', zones=zones)

@bp.route('/zones/add', methods=['GET', 'POST'])
@login_required
def add_zone():
    form = AddZoneForm()

    if form.validate_on_submit():
        try:
            zone = Zone(name=form.name.data, color=form.color.data)

            db.session.add(zone)
            db.session.commit()
            flash("New Zone Added")
            return redirect(url_for('admin.zones'))
        except Exception as err:
            print(err)
            flash("Something went wrong! Try again later")
            return render_template("zones/add_zones.html", title='Add Zone', form=form, error=1)
    return render_template("zones/add_zones.html", title='Add Zone', form=form)

@bp.route('/zones/edit/<zone_id>',  methods=['GET', 'POST'])
@login_required
def edit_zone(zone_id):
    form = EditZoneForm(zone_id=zone_id)

    if form.validate_on_submit():
        try:
            zone = Zone.query.get(zone_id)
            zone.name = form.name.data
            zone.color = form.color.data
            db.session.commit()
            flash('Zone updated successfully!')
        except Exception as error:
            print(error)
            flash("Something went wrong! Try again later")
            return render_template("zones/edit_zone.html", title='Edit Zone', form=form, zone=Zone.query.get(zone_id),error=1)

        return redirect(url_for('admin.zones'))
    
    zone = Zone.query.get(zone_id)
    return render_template("zones/edit_zone.html", title='Edit Zone', form=form, zone=Zone.query.get(zone_id))


@bp.route('/zones/delete/<zone_id>',  methods=['POST'])
@login_required
def delete_zone(zone_id):
    try:
        zone = Zone.query.get(zone_id)
        db.session.delete(zone)
        db.session.commit()
        flash("Zone removed")
    except Exception as error: 
        print(error)
        flash("Something went wrong! Try again later")
        return render_template("zones/zones.html", title='Zones', zones=Zone.query.all(), error=1)
    return redirect(url_for('admin.zones'))


@bp.route('/lots')
@login_required
def lots():
    lots = Lot.query.all()
    return render_template("lots/lots.html", title='Lots', lots= lots)

@bp.route('/lots/add', methods=['GET', 'POST'])
@login_required
def add_lot():
    form = AddLotForm()
    form.zones.choices = [(z.id, z.name) for z in Zone.query.order_by('name')]
    form.zones.render_kw={'style': 'height: fit-content; list-style: none;'}
    if form.validate_on_submit():
        try:
            lot = Lot(name=form.name.data)
            for z in form.zones.data:
                zone = Zone.query.get(z)
                lot.zones.append(zone)

            db.session.add(lot)
            db.session.commit()
            flash("New Lot Added")
            return redirect(url_for('admin.lots'))
        except Exception as err:
            print(err)
            flash("Something went wrong! Try again later")
            return render_template("lots/add_lot.html", title='Add Lot', form=form, error=1)
    return render_template("lots/add_lot.html", title='Add Lot', form=form)

@bp.route('/lots/edit/<lot_id>',  methods=['GET', 'POST'])
@login_required
def edit_lot(lot_id):
    lot = Lot.query.get(lot_id)
    form = EditLotForm(lot_id=lot_id)
    form.zones.choices = [(z.id, z.name) for z in Zone.query.order_by('id')]
    form.zones.render_kw={'style': 'height: fit-content; list-style: none;'}
    form.zones.data = [zone.id for zone in lot.zones]
    
    if form.validate_on_submit():
        try:
            lot = Lot.query.get(lot_id)
            lot.name = form.name.data
            lot.zone = form.zones.data
            db.session.commit()
            flash('Lot updated successfully!')
        except Exception as error:
            print(error)
            flash("Something went wrong! Try again later")
            return render_template("lots/edit_lot.html", title='Edit Lot', form=form, lot=Lot.query.get(lot_id),error=1)

        return redirect(url_for('admin.lots'))
    
    return render_template("lots/edit_lot.html", title='Edit Lot',form=form, lot=Lot.query.get(lot_id))


@bp.route('/lots/delete/<lot_id>',  methods=['POST'])
@login_required
def delete_lot(lot_id):
    try:
        lot = Lot.query.get(lot_id)
        db.session.delete(lot)
        db.session.commit()
        flash("Lot removed")
    except Exception as error: 
        print(error)
        flash("Something went wrong! Try again later")
        return render_template("lots/lots.html", title='Lots', lots=Lot.query.all(), error=1)
    return redirect(url_for('admin.lots'))

@bp.route('/spaces')
@login_required
def spaces():
    spaces = ParkingSpace.query.all()
    return render_template("spaces/spaces.html", title='Parking Spaces',spaces=spaces)

# FIXME: is this needed?
# @bp.route('/spaces/add', methods=['GET', 'POST'])
# @login_required
# def add_space():
#     return render_template("spaces/spaces.html", title='Parking Spaces')

@bp.route('/spaces/edit',  methods=['GET', 'POST'])
@login_required
def edit_space():
    return render_template("spaces/spaces.html", title='Edit Parking Spaces')


@bp.route('/spaces/delete',  methods=['POST'])
@login_required
def delete_space():
    return render_template("spaces/spaces.html", title='Parking Spaces')

@bp.route('/system_log')
@login_required
def system_log():
    logs = SystemLog.query.all()
    return render_template("system_log/system_log.html", title='System Log', logs=logs)

@bp.route('/resolve_log', methods=['POST'])
@login_required
def resolve_log():
    logsToResolve = request.form['logs'].split(',')
    updated_at = datetime.now()
    for l_id in logsToResolve:
        log = SystemLog.query.get(l_id)
        log.updated_at = updated_at
        log.status = LogStatus.RESOLVED
        db.session.add(log)
    db.session.commit()
    return redirect(url_for('.system_log'))


@bp.route('/mark_spaces')
@login_required
def mark_spaces():
    return render_template("spaces/mark_spaces.html", title ="Mark Spaces")
    