from app import db
from app.models import Zone


@db.event.listens_for(Zone, "after_insert")
def on_insert_zone(mapper, connection, target):
    # TODO add logic to add to notifications table
    pass
