import base64
from datetime import datetime

import dropbox
from flask import json
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import current_user
from flask_login import login_required
from sqlalchemy import func

from app import db
from app.admin import bp
from app.admin.forms import AddAdminForm, EditAdminForm, AddZoneForm, EditZoneForm, AddLotForm, EditLotForm, \
    AddCameraForm, EditCameraZone
from app.admin.utils import download
from app.auth.email import send_activation_email
from app.enums import Groups, LogStatus, CameraStatus, SpaceAvailability
from app.models import ControlPoints, SpaceDimensions, User, Zone, Camera, ParkingSpace, Lot, SystemLog, AdminGroup


@bp.route('/home')
@login_required
def home():
    user_count = User.query.count()
    camera_count = Camera.query.count()
    zone_count = Zone.query.count()
    lot_count = Lot.query.count()
    return render_template("home.html", title='Command Center', users=user_count, cameras=camera_count,
                           zones=zone_count, lots=lot_count)


@bp.route('/administrators')
@login_required
def administrators():
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
    admin = User.query.all()
    return render_template("administrators/administrators.html", title='Administrators', administrators=admin)


@bp.route('/administrators/add', methods=['GET', 'POST'])
@login_required
def add_administrator():
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
    form = AddAdminForm()
    form.group.choices = [(g.id, g.name)
                          for g in AdminGroup.query.order_by('name')]

    if form.validate_on_submit():
        try:
            user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        middle_initial=form.middle_initial.data, group_id=form.group.data)

            db.session.add(user)
            db.session.commit()
            send_activation_email(user)
            flash("New Admin Added")
            return redirect(url_for('admin.administrators'))
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            flash("Something went wrong! Try again later")
            return render_template("administrators/add_administrator.html", title='Add Administrator', form=form,
                                   error=1)
    return render_template("administrators/add_administrator.html", title='Add Administrator', form=form)


@bp.route('/administrators/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_administrator(user_id):
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
    form = EditAdminForm(user_id=user_id)
    form.group.choices = [(g.id, g.name)
                          for g in AdminGroup.query.order_by('name')]

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
            current_app.logger.error(error)
            db.session.rollback()
            flash("Something went wrong! Try again later")
            return render_template("administrators/edit_administrator.html", title='Edit Administrator', form=form,
                                   admin=User.query.get(user_id), error=1)

        return redirect(url_for('admin.administrators'))

    admin = User.query.get(user_id)
    form.group.data = admin.group_id
    return render_template("administrators/edit_administrator.html", title='Edit Administrator', form=form, admin=admin)


@bp.route('/administrators/delete/<user_id>', methods=['POST'])
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
        current_app.logger.error(error)
        db.session.rollback()
        flash("Something went wrong! Try again later")
        return redirect(url_for('admin.administrators', error=1))
    return redirect(url_for('admin.administrators'))


@bp.route('/cameras')
@login_required
def cameras():
    # cameras = Camera.query.all()
    cameras = Camera.query.all()
    lots = Lot.query.with_entities(Lot.name).all()
    return render_template("cameras/cameras.html", title='Cameras', cameras=cameras, lots=lots)


@bp.route('/cameras/add', methods=['GET', 'POST'])
@login_required
def add_camera():
    form = AddCameraForm()
    form.lot.choices = [(lot.id, lot.name)
                        for lot in Lot.query.order_by('name')]
    form.status.choices = [(s.name, s.name) for s in CameraStatus]

    form.lot.render_kw = {'style': 'height: fit-content; list-style: none;'}
    form.status.render_kw = {'style': 'height: fit-content; list-style: none;'}

    if form.validate_on_submit():
        try:
            camera = Camera(location=form.location.data,
                            lot_id=form.lot.data, status=form.status.data, ip_address=form.ip_address.data)
            db.session.add(camera)
            db.session.commit()

            return redirect(url_for('.mark_spaces', lot_id=camera.lot_id, camera_id=camera.id))
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            flash("Something went wrong! Try again later")
            return render_template("cameras/add_camera.html", title='Add Camera', form=form, error=1)
    return render_template("cameras/add_camera.html", title='Add Camera', form=form)


@bp.route('/cameras/edit/<camera_id>', methods=['GET', 'POST'])
@login_required
def edit_camera(camera_id):
    form = EditCameraZone(camera_id=camera_id)
    form.lot.choices = [(lot.id, lot.name)
                        for lot in Lot.query.order_by('name')]
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
            current_app.logger.error(error)
            db.session.rollback()
            flash("Something went wrong! Try again later")
            return render_template("cameras/edit_camera.html", title='Edit Camera', form=form,
                                   camera=Camera.query.get(camera_id), error=1)

        return redirect(url_for('admin.cameras'))

    camera = Camera.query.with_entities(Camera.id, Camera.lot_id, func.lpad(
        Camera.location, 4, 0).label("location"), Camera.status).filter_by(id=camera_id).first()
    form.lot.data = camera.lot_id
    form.status.data = camera.status.value
    form.location.data = camera.location
    return render_template("cameras/edit_camera.html", title='Edit Camera', form=form,
                           camera=Camera.query.get(camera_id))


@bp.route('/cameras/delete/<camera_id>', methods=['POST'])
@login_required
def delete_camera(camera_id):
    try:
        Camera.query.filter(Camera.id == camera_id).delete()
        db.session.commit()
        flash("Camera removed")
    except Exception as error:
        current_app.logger.error(error)
        db.session.rollback()
        db.session.rollback()
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
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            flash("Something went wrong! Try again later")
            return render_template("zones/add_zones.html", title='Add Zone', form=form, error=1)
    return render_template("zones/add_zones.html", title='Add Zone', form=form)


@bp.route('/zones/edit/<zone_id>', methods=['GET', 'POST'])
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
            current_app.logger.error(error)
            db.session.rollback()
            flash("Something went wrong! Try again later")
            return render_template("zones/edit_zone.html", title='Edit Zone', form=form, zone=Zone.query.get(zone_id),
                                   error=1)

        return redirect(url_for('admin.zones'))

    zone = Zone.query.get(zone_id)
    return render_template("zones/edit_zone.html", title='Edit Zone', form=form, zone=Zone.query.get(zone_id))


@bp.route('/zones/delete/<zone_id>', methods=['POST'])
@login_required
def delete_zone(zone_id):
    try:
        zone = Zone.query.get(zone_id)
        db.session.delete(zone)
        db.session.commit()
        flash("Zone removed")
    except Exception as error:
        current_app.logger.error(error)
        db.session.rollback()
        flash("Something went wrong! Try again later")
        return render_template("zones/zones.html", title='Zones', zones=Zone.query.all(), error=1)
    return redirect(url_for('admin.zones'))


@bp.route('/lots')
@login_required
def lots():
    lots = Lot.query.all()
    return render_template("lots/lots.html", title='Lots', lots=lots)


@bp.route('/lots/add', methods=['GET', 'POST'])
@login_required
def add_lot():
    form = AddLotForm()
    form.zones.choices = [(z.id, z.name) for z in Zone.query.order_by('name')]
    form.zones.render_kw = {'style': 'height: fit-content; list-style: none;'}
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
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            flash("Something went wrong! Try again later")
            return render_template("lots/add_lot.html", title='Add Lot', form=form, error=1)
    return render_template("lots/add_lot.html", title='Add Lot', form=form)


@bp.route('/lots/edit/<lot_id>', methods=['GET', 'POST'])
@login_required
def edit_lot(lot_id):
    lot = Lot.query.get(lot_id)
    form = EditLotForm(lot_id=lot_id)
    form.zones.choices = [(z.id, z.name) for z in Zone.query.order_by('id')]
    form.zones.render_kw = {'style': 'height: fit-content; list-style: none;'}

    if form.validate_on_submit():
        try:
            lot = Lot.query.get(lot_id)
            lot.name = form.name.data

            zones = []
            for zone_id in form.zones.data:
                zones.append(Zone.query.get(zone_id))
            lot.zones = zones

            db.session.commit()
            flash('Lot updated successfully!')
        except Exception as error:
            flash("Something went wrong! Try again later")
            return render_template("lots/edit_lot.html", title='Edit Lot', form=form, lot=Lot.query.get(lot_id),
                                   error=1)

        return redirect(url_for('admin.lots'))

    form.zones.data = [zone.id for zone in lot.zones]
    return render_template("lots/edit_lot.html", title='Edit Lot', form=form, lot=Lot.query.get(lot_id))


@bp.route('/lots/delete/<lot_id>', methods=['POST'])
@login_required
def delete_lot(lot_id):
    try:
        Lot.query.filter(Lot.id == lot_id).delete()
        db.session.commit()
        flash("Lot removed")
    except Exception as error:
        current_app.logger.error(error)
        db.session.rollback()
        flash("Something went wrong! Try again later")
        return render_template("lots/lots.html", title='Lots', lots=Lot.query.all(), error=1)
    return redirect(url_for('admin.lots'))


@bp.route('/spaces')
@login_required
def spaces():
    spaces = ParkingSpace.query.all()
    return render_template("spaces/spaces.html", title='Parking Spaces', spaces=spaces)


@bp.route('/spaces/add', methods=['POST'])
@login_required
def add_space():
    data = request.json
    camera = json.loads(data.get("camera"))
    canvas = json.loads(data.get("canvas"))
    objects = canvas.get("objects")

    for object in objects:
        if object.get("type") == "ParkingSpace":
            parking_space = ParkingSpace(
                availability=SpaceAvailability.NOT_AVAILABLE, lot_id=camera["lot_id"], zone_id=object["zones"][0],
                camera_id=camera["id"])

            db.session.add(parking_space)
            db.session.commit()

            parking_space_coordinates = SpaceDimensions(
                start_x=object["left"], start_y=object["top"], width=object["width"], height=object["height"],
                space_id=parking_space.id)
            db.session.add(parking_space_coordinates)
            db.session.commit()


        if object.get("type") == "ControlPoint":
            controlPoint = ControlPoints(start_x=object["left"], start_y=object["top"],
                                         width=object["width"], height=object["height"], camera_id=camera["id"])
            db.session.add(controlPoint)
            db.session.commit()

    flash("Spaces and control point added successfully!")
    return {"result": "success"}


@bp.route('/spaces/edit/<camera_id>', methods=['GET', 'POST'])
@login_required
def edit_space(camera_id):
    camera = Camera.query.get_or_404(camera_id)
    spaces = []

    for space in camera.spaces.all():
        space_dimensions = space.dimensions.first()

        spaces.append({
            "id": space.id,
            "zones": [space.zone.name],
            "width": space_dimensions.width,
            "height": space_dimensions.height,
            "left": space_dimensions.start_x,
            "top": space_dimensions.start_y
        })

    return render_template("spaces/view_spaces.html", title='Edit Parking Spaces', data={"spaces": spaces})


@bp.route('/spaces/delete', methods=['POST'])
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


@bp.route('/mark_spaces/<lot_id>/<camera_id>')
@login_required
def mark_spaces(lot_id, camera_id):
    
    dropbox_access_token = current_app.config["DROPBOX_ACCESS_TOKEN"]
    
    # TODO: error handling needed here
    dbx = dropbox.Dropbox(dropbox_access_token)
    download_result = download(dbx, "", "", "photo.jpg")
    download_bytes = base64.b64encode(download_result)
    download_string = download_bytes.decode('ascii')
    lot = Lot.query.get(lot_id)
    zones = lot.zones.all()
    camera = (Camera.query.get_or_404(camera_id)).to_dict()

    data = {'cameraInfo': camera, 'canvasImage': download_string }
    return render_template("spaces/mark_spaces.html", title="Mark Spaces", zones=zones, data=data)
