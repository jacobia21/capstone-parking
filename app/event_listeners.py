from flask_login import current_user

from app import db
from app.models import Zone, Lot, Camera, Notifications, User


def send_insert_notification(item, target, name):
    administrator = "{} {}".format(current_user.first_name, current_user.last_name)
    title = "New {}".format(item)
    message = "{} {} was added by {}".format(item, name, administrator)

    new_notification = Notifications(title=title, message=message)
    db.session.add(new_notification)


def send_remove_notification(item, target, name):
    administrator = "{} {}".format(current_user.first_name, current_user.last_name)
    title = "{} Deleted".format(item)
    message = "{} {} was removed by {}".format(item, name, administrator)

    new_notification = Notifications(title=title, message=message)
    db.session.add(new_notification)


def send_update_notification(item, target, name):
    changes = get_changes(target)
    if changes:
        changes_list = []
        for change in changes:
            attribute_name = change.replace("_"," ")
            attribute_name = attribute_name.title()
            phrase = "{} changed from {} to {}".format(attribute_name, changes[change][0], changes[change][1])
            changes_list.append(phrase)

        change_csv = ",".join(changes_list)
        administrator = "{} {}".format(current_user.first_name, current_user.last_name)
        title = "Updated {}".format(item)
        message = "{} {} was updated by {}".format(item, name, administrator)

        new_notification = Notifications(title=title, message=message,updates=change_csv)
        db.session.add(new_notification)


def get_changes(model):
    state = db.inspect(model)
    changes = {}
    for attr in state.attrs:
        hist = state.get_history(attr.key, True)

        if not hist.has_changes():
            continue

        old_value = hist.deleted[0] if hist.deleted else None
        new_value = hist.added[0] if hist.added else None
        changes[attr.key] = [old_value, new_value]

    return changes


@db.event.listens_for(Zone, "after_insert")
def on_insert_zone(mapper, connection, target):
    send_insert_notification("Zone", target, target.name)


@db.event.listens_for(Zone, "after_delete")
def on_delete_zone(mapper, connection, target):
    send_remove_notification("Zone", target, target.name)


@db.event.listens_for(Zone, "after_update")
def on_update_zone(mapper, connection, target):
    send_update_notification("Zone", target, target.name)


@db.event.listens_for(Lot, "after_insert")
def on_insert_lot(mapper, connection, target):
    send_insert_notification("Lot", target, target.name)


@db.event.listens_for(Lot, "after_delete")
def on_delete_lot(mapper, connection, target):
    send_remove_notification("Lot", target, target.name)


@db.event.listens_for(Lot, "after_update")
def on_update_lot(mapper, connection, target):
    send_update_notification("Lot", target, target.name)


@db.event.listens_for(Camera, "after_insert")
def on_insert_camera(mapper, connection, target):
    send_insert_notification("Camera", target, target.ip_address)


@db.event.listens_for(Camera, "after_delete")
def on_delete_camera(mapper, connection, target):
    send_remove_notification("Camera", target, target.id)


@db.event.listens_for(Camera, "after_update")
def on_update_camera(mapper, connection, target):
    send_update_notification("Camera", target, target.id)


@db.event.listens_for(User, "after_insert")
def on_insert_administrator(mapper, connection, target):
    send_insert_notification("Administrator", target, "{} {}".format(target.first_name, target.last_name))


@db.event.listens_for(User, "after_delete")
def on_delete_administrator(mapper, connection, target):
    send_remove_notification("Administrator", target, "{} {}".format(target.first_name, target.last_name))


@db.event.listens_for(User, "after_update")
def on_update_administrator(mapper, connection, target):
    send_update_notification("Administrator", target, "{} {}".format(target.first_name, target.last_name))
