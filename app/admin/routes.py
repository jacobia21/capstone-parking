import base64
from datetime import datetime
import calendar
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
from app.models import ControlPoints, SpaceDimensions, Administrator, Zone, Camera, ParkingSpace, Lot, SystemLog, AdminGroup, \
    Notifications


@bp.route('/home')
@login_required
def home():
    user_count = Administrator.query.count()
    camera_count = Camera.query.count()
    zone_count = Zone.query.count()
    lot_count = Lot.query.count()

    notifications_query = Notifications.query.order_by(Notifications.timestamp.desc()).limit(3).all()
    notifications = []
    for notification in notifications_query:
        title = notification.title
        month = calendar.month_abbr[notification.timestamp.month]
        day = notification.timestamp.day
        message = notification.message
        updates = notification.updates if notification.updates != "" else None

        notification = {
            'title': title,
            'month': month,
            'day': day,
            'message': message,
        }
        if updates:
            updates_list = updates.split(",")
            notification['updates'] = updates_list

        notifications.append(notification)

    return render_template("home.html", title='Command Center', users=user_count, cameras=camera_count,
                           zones=zone_count, lots=lot_count, notifications=notifications)


@bp.route('/administrators')
@login_required
def administrators():
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
    admin = Administrator.query.all()
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
            user = Administrator(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
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
            admin = Administrator.query.get(user_id)
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
                                   admin=Administrator.query.get(user_id), error=1)

        return redirect(url_for('admin.administrators'))

    admin = Administrator.query.get(user_id)
    form.group.data = admin.group_id
    return render_template("administrators/edit_administrator.html", title='Edit Administrator', form=form, admin=admin)


@bp.route('/administrators/delete/<user_id>', methods=['POST'])
@login_required
def delete_administrator(user_id):
    if current_user.group.name != Groups.SUPER.value:
        return redirect('/')
    try:
        admin = Administrator.query.get(user_id)
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
        camera = Camera.query.get(camera_id)
        # Camera.query.delete(camera_id)
        db.session.delete(camera)
        db.session.commit()
        flash("Camera removed")
    except Exception as error:
        current_app.logger.error(error)
        db.session.rollback()
        flash("Something went wrong! Try again later")
        return render_template('cameras/cameras.html', error=1)

    return redirect(url_for('admin.cameras'))


@bp.route('/zones')
@login_required
def zones():
    zones = Zone.query.all()
    return render_template("zones/zones.html", title='Parking Zones', zones=zones)


@bp.route('/zones/add', methods=['GET', 'POST'])
@login_required
def add_zone():
    form = AddZoneForm()
    form.additional_zones.choices = [(z.id, z.name) for z in Zone.query.order_by('name')]
    form.additional_zones.render_kw = {'style': 'height: fit-content; list-style: none;'}

    form.lots.choices = [(l.id, l.name) for l in Lot.query.order_by('name')]
    form.lots.render_kw = {'style': 'height: fit-content; list-style: none;'}
    if form.validate_on_submit():
        try:
            new_zone = Zone(name=form.name.data, color=form.color.data)
            children = []
            for z in form.additional_zones.data:
                children.append(z)

            converted_list = [str(child) for child in children]
            children_csv = ",".join(converted_list)
            new_zone.children = children_csv

            for lot_id in form.lots.data:
                lot = Lot.query.get(lot_id)
                new_zone.lots.append(lot)

            db.session.add(new_zone)
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
    form.additional_zones.choices = [(z.id, z.name) for z in Zone.query.order_by('id').filter(Zone.id != zone_id)]
    form.additional_zones.render_kw = {'style': 'height: fit-content; list-style: none;'}

    form.lots.choices = [(l.id, l.name) for l in Lot.query.order_by('id')]
    form.lots.render_kw = {'style': 'height: fit-content; list-style: none;'}
    if form.validate_on_submit():
        try:
            zone = Zone.query.get(zone_id)
            zone.name = form.name.data
            zone.color = form.color.data

            children = []
            for z in form.additional_zones.data:
                children.append(z)
            converted_list = [str(child) for child in children]
            children_csv = ",".join(converted_list)
            zone.children = children_csv

            lots = []
            for lot_id in form.lots.data:
                lots.append(Lot.query.get(lot_id))
            zone.lots = lots

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
    form.additional_zones.data = [int(s) for s in zone.children.split(',')] if zone.children != "" else []
    form.lots.data = [int(l.id) for l in zone.lots]
    return render_template("zones/edit_zone.html", title='Edit Zone', form=form, zone=zone)


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
    return render_template("lots/lots.html", title='Parking Lots', lots=lots)


@bp.route('/lots/add', methods=['GET', 'POST'])
@login_required
def add_lot():
    form = AddLotForm()
    if form.validate_on_submit():
        try:
            lot = Lot(name=form.name.data)

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

    if form.validate_on_submit():
        try:
            lot = Lot.query.get(lot_id)
            lot.name = form.name.data

            db.session.commit()
            flash('Lot updated successfully!')
        except Exception as error:
            flash("Something went wrong! Try again later")
            return render_template("lots/edit_lot.html", title='Edit Lot', form=form, lot=Lot.query.get(lot_id),
                                   error=1)

        return redirect(url_for('admin.lots'))

    return render_template("lots/edit_lot.html", title='Edit Lot', form=form, lot=Lot.query.get(lot_id))


@bp.route('/lots/delete/<lot_id>', methods=['POST'])
@login_required
def delete_lot(lot_id):
    try:
        lot = Lot.query.get(lot_id)
        db.session.delete(lot)
        db.session.commit()
        flash("Lot removed")
    except Exception as error:
        current_app.logger.error(error)
        db.session.rollback()
        flash("Something went wrong! Try again later")
        return render_template("lots/lots.html", title='Lots', lots=Lot.query.all(), error=1)
    return redirect(url_for('admin.lots'))


@bp.route('/spaces/add', methods=['POST'])
@login_required
def add_spaces():
    data = request.json
    camera = json.loads(data.get("camera"))
    camera = camera.get("cameraInfo")
    canvas = json.loads(data.get("canvas"))
    objects = canvas.get("objects")

    for object in objects:
        if object.get("type") == "ParkingSpace":
            parking_space = ParkingSpace(lot_id=camera["lot_id"], zone_id=object["zoneId"],
                camera_id=camera["id"])

            zone = Zone.query.get(parking_space.zone_id)
            if zone.name == "Reserved":
                parking_space.availability = SpaceAvailability.RESERVED.value
            else:
                parking_space.availability = SpaceAvailability.NOT_AVAILABLE.value

            db.session.add(parking_space)
            db.session.commit()

            parking_space_coordinates = SpaceDimensions(
                start_x=object["left"], start_y=object["top"], width=(object["width"] * object["scaleX"]), height=(object["height"] * object["scaleY"]),
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


@bp.route('/spaces/update', methods=['POST'])
@login_required
def update_spaces():
    data = request.json
    camera = json.loads(data.get("camera"))
    camera = camera.get("cameraInfo")
    canvas = json.loads(data.get("canvas"))
    objects = canvas.get("objects")

    spacesToRemove = data.get("spacesToRemove")
    for space in spacesToRemove:
        space = ParkingSpace.query.get(int(space))
        db.session.delete(space)
        db.session.commit()

    for object in objects:
        if object.get("type") == "ParkingSpace":
            if object.get("id") == 0:
                parking_space = ParkingSpace(lot_id=camera["lot_id"], zone_id=object["zoneId"],
                                             camera_id=camera["id"])

                zone = Zone.query.get(parking_space.zone_id)
                if zone.name == "Reserved":
                    parking_space.availability = SpaceAvailability.RESERVED.value
                else:
                    parking_space.availability = SpaceAvailability.NOT_AVAILABLE.value

                db.session.add(parking_space)
                db.session.commit()

                parking_space_coordinates = SpaceDimensions(
                    start_x=object["left"], start_y=object["top"], width=(object["width"] * object["scaleX"]),
                    height=(object["height"] * object["scaleY"]),
                    space_id=parking_space.id)

                db.session.add(parking_space_coordinates)
                db.session.commit()
            else:
                old_space_id = object.get("id")
                old_parking_space = ParkingSpace.query.get(int(old_space_id))
                old_parking_space.zone_id = object["zoneId"]

                dimensions = old_parking_space.dimensions
                dimensions.start_x = object["left"]
                dimensions.start_y = object["top"]
                dimensions.width = object["width"] * object["scaleX"]
                dimensions.height = object["height"] * object["scaleY"]

                db.session.commit()

        if object.get("type") == "ControlPoint":
            controlPoint = Camera.query.get(camera["id"]).control
            controlPoint.start_x = object["left"]
            controlPoint.start_y = object["top"]
            controlPoint.width = object["width"]
            controlPoint.height = object["height"]

            db.session.commit()

    flash("Spaces and control point updated successfully!")
    return {"result": "success"}


@bp.route('/spaces/edit/<camera_id>', methods=['GET', 'POST'])
@login_required
def edit_spaces(camera_id):
    dropbox_access_token = current_app.config["DROPBOX_ACCESS_TOKEN"]

    camera = Camera.query.get(camera_id)
    # TODO: error handling needed here
    dbx = dropbox.Dropbox(dropbox_access_token)
    ip_address = camera.ip_address
    download_result = download(dbx, "", "", "{}.jpg".format(camera.ip_address))
    download_bytes = base64.b64encode(download_result)
    download_string = download_bytes.decode('ascii')
    lot = camera.lot
    zones = lot.zones.all()

    control_point = {
        "left": camera.control.start_x,
        "top": camera.control.start_y
    }

    spaces = []

    for space in camera.spaces:
        space_dimensions = space.dimensions

        spaces.append({
            "id": space.id,
            "zoneId": space.zone.id,
            "width": space_dimensions.width,
            "height": space_dimensions.height,
            "left": space_dimensions.start_x,
            "top": space_dimensions.start_y
        })

    data = {'cameraInfo': camera.to_dict(), 'canvasImage': download_string, "spaces": spaces,"controlPoint": control_point}

    return render_template("spaces/view_spaces.html", title="View & Edit Spaces", zones=zones, data=data)


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
    try:
        dropbox_access_token = current_app.config["DROPBOX_ACCESS_TOKEN"]

        camera = Camera.query.get(camera_id)
        dbx = dropbox.Dropbox(dropbox_access_token)
        download_result = download(dbx, "", "", "{}.jpg".format(camera.ip_address))
        download_bytes = base64.b64encode(download_result)
        download_string = download_bytes.decode('ascii')
        lot = Lot.query.get(lot_id)
        zones = lot.zones.all()
        camera = (Camera.query.get_or_404(camera_id)).to_dict()

        data = {'cameraInfo': camera, 'canvasImage': download_string}
    except Exception as error:
        flash("Could not find an image for the camera with this IP address. Please make sure the camera is set up "
              "properly and the IP address is correct.")
        db.session.delete(camera)
        db.session.commit()
        return render_template("cameras/add_camera.html", title='Add Camera', form=AddCameraForm(), error=1)

    return render_template("spaces/mark_spaces.html", title="Mark Spaces", zones=zones, data=data)
