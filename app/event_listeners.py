"""
    This module holds the logic for listening to certain database changes and creating notifications. These
    notifications are then add to the Notifications table. Currently, each event listener will call either the
    send_insert_notification(), send_update_notification(), or send_remove_notification() based on the type of listener
    it is. For example, @db.event.listens_for(Zone, "after_insert") listens for inserts in the Zone table, and therefore
    calls send_insert_notification().
"""

from flask_login import current_user

from app import db
from app.models import Zone, Lot, Camera, Notifications, Administrator


def send_insert_notification(item, name):
    """
    Creates a new notification when an insertion is made to the database.Adds the notification to the Notifications
    table. This function is not automatically triggered and should be called in an event listener (typically an
    "after_insert" listener) to work as expected.


    :param item: The name of the item that was added to the database. (ex: "Zone")
    :type item: str
    :param name: A string identifier for the object that was inserted. This is typically the object name or id.
                This is used in the notification message to state what object was inserted.
    :type name: str

    """

    # Get the name of the administrator who made the change.
    administrator = "{} {}".format(current_user.first_name, current_user.last_name)

    # Format the title that for the notification.
    title = "New {}".format(item)

    # Format the message for the notification.
    message = "{} {} was added by {}".format(item, name, administrator)

    # Create the new notification and add to the database.
    new_notification = Notifications(title=title, message=message)
    db.session.add(new_notification)


def send_remove_notification(item, name):
    """
    Creates a new notification when an deletion is made to the database. Adds the notification to the Notifications
    table. This function is not automatically triggered and should be called in an event listener (typically an
    "after_delete" listener) to work as expected.

    :param item: The name of the item that was removed from the database. (ex: "Zone")
    :type item: str
    :param name: A string identifier for the object that was removed. This is typically the object name or id.
                This is used in the notification message to state what object was removed.
    :type name: str
    """

    # Get the name of the administrator who made the change.
    administrator = "{} {}".format(current_user.first_name, current_user.last_name)

    # Format the title for the notification.
    title = "{} Deleted".format(item)

    # Format the message for the notification.
    message = "{} {} was removed by {}".format(item, name, administrator)

    # Create the new notification and add to the database.
    new_notification = Notifications(title=title, message=message)
    db.session.add(new_notification)


def send_update_notification(item, target, name):
    """
    Creates a new notification when a row in the database is updated. Adds the notification to the Notifications
    table. This function is not automatically triggered and should be called in an event listener (typically an
    "after_update" listener) to work as expected.

    :param item: The name of the item that was removed from the database. (ex: "Zone")
    :type item: str
    :param target: The object model representation of the row that has been updated.
    :type target: object
    :param name: A string identifier for the object that was updated. This is typically the object name or id.
                This is used in the notification message to state what object was updated.
    :type name: str
    """

    # Get all the changes that were made on the target row.
    changes = get_changes(target)

    # If no changes are found, then we do not need to create a notification.
    # Therefore, we check to see if there are changes before continuing.
    if changes:

        # Iterate over all changes, create a phrase describing each change, and add each phrase to the changes_list.
        changes_list = []
        for change in changes:
            attribute_name = change.replace("_", " ")
            attribute_name = attribute_name.title()
            phrase = "{} changed from {} to {}".format(attribute_name, changes[change][0], changes[change][1])
            changes_list.append(phrase)

        # Join all the phrases in the changes_list as a string with each phrase separated by a comma.
        # This sentence will be added to the Notifications table as the updates column.
        updates = ",".join(changes_list)

        # Get the name of the administrator who made the change.
        administrator = "{} {}".format(current_user.first_name, current_user.last_name)

        # Format the title for the notification.
        title = "Updated {}".format(item)

        # Format the title for the notification.
        message = "{} {} was updated by {}".format(item, name, administrator)

        # Create the new notification and add to the database.
        new_notification = Notifications(title=title, message=message, updates=updates)
        db.session.add(new_notification)


def get_changes(model_object):
    """
    Returns any changes that have been made to a row in the database.

    :param model_object: The object representation (model) of the database row to get the changes for.
    :type model_object: object

    :return: A dictionary with the attributes that was changed as the key and a list holding the old and new value of
    the attribute respectively as the value.
    :rtype: dict
    """

    # Grab the current state of the model_object
    state = db.inspect(model_object)
    changes = {}

    for attr in state.attrs:

        # We skip checking if the password_hash has changed for security reasons.
        # Even if it is being updated, we will not create a notification for this.
        if attr.key == "password_hash":
            continue

        # Check if attribute has changed. Continue to next attribute if it has not.
        hist = state.get_history(attr.key, True)
        if not hist.has_changes():
            continue

        # Get the old and new value and add the information to the changes dictionary.
        old_value = hist.deleted[0] if hist.deleted else None
        new_value = hist.added[0] if hist.added else None
        changes[attr.key] = [old_value, new_value]

    return changes


"""
    The remainder of this file sets up the event listeners and calls the appropriate function to create and add a 
    notification to the database. Each listener has three parts. 
    
    First, define what the listener should listen for: 
        @db.event.listens_for(<Insert db.Model to listen to here>, <Insert the action to listen for (ex. after_insert)>
    
    Second, create a function that takes in the mapper, connection, and target passed automatically by Flask-SQLAlchemy:
        def on_insert_zone(mapper, connection, target):
    
    Third, call the appropriate function to create and send the notification:
        send_insert_notification("Zone", target.name)       
"""


@db.event.listens_for(Zone, "after_insert")
def on_insert_zone(mapper, connection, target):
    send_insert_notification("Zone", target.name)


@db.event.listens_for(Zone, "after_delete")
def on_delete_zone(mapper, connection, target):
    send_remove_notification("Zone", target.name)


@db.event.listens_for(Zone, "after_update")
def on_update_zone(mapper, connection, target):
    send_update_notification("Zone", target, target.name)


@db.event.listens_for(Lot, "after_insert")
def on_insert_lot(mapper, connection, target):
    send_insert_notification("Lot", target.name)


@db.event.listens_for(Lot, "after_delete")
def on_delete_lot(mapper, connection, target):
    send_remove_notification("Lot", target.name)


@db.event.listens_for(Lot, "after_update")
def on_update_lot(mapper, connection, target):
    send_update_notification("Lot", target, target.name)


@db.event.listens_for(Camera, "after_insert")
def on_insert_camera(mapper, connection, target):
    send_insert_notification("Camera", target.ip_address)


@db.event.listens_for(Camera, "after_delete")
def on_delete_camera(mapper, connection, target):
    send_remove_notification("Camera", target.ip_address)


@db.event.listens_for(Camera, "after_update")
def on_update_camera(mapper, connection, target):
    send_update_notification("Camera", target, target.id)


@db.event.listens_for(Administrator, "after_insert")
def on_insert_administrator(mapper, connection, target):
    send_insert_notification("Administrator", "{} {}".format(target.first_name, target.last_name))


@db.event.listens_for(Administrator, "after_delete")
def on_delete_administrator(mapper, connection, target):
    send_remove_notification("Administrator", "{} {}".format(target.first_name, target.last_name))


@db.event.listens_for(Administrator, "after_update")
def on_update_administrator(mapper, connection, target):
    send_update_notification("Administrator", target, "{} {}".format(target.first_name, target.last_name))
