"""
This module defines the models that represent the database tables and relationships.
We use the Flask-SQLAlchemy extension to create these models, and the Flask-Migrate extension
to manage database changes. When changes or made to the structure of a table or field in the model,
running the `flask db migrate` command will pick up the changes and create a new migration file in the
migrations directory. Then running the `flask db upgrade` command will make the changes to the database
that is currently set up using the SQLALCHEMY_DATABASE_URI config environment variable.
"""

from datetime import datetime, timedelta
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login
from app.enums import CameraStatus, SpaceAvailability, LogStatus, LogType


@login.user_loader
def load_admin(user_id):
    """
    Tells  :mod:`flask_login`  how a user should be loaded. This function should not be called directly.
    It is used internally so the Flask-Login LoginManager can determine if a user is logged in or not, and
    keep track of who the current user is.


    :param user_id: The id of the administrator being loaded.
    :type user_id:
    :return: The administrator from the database.
    :rtype: Administrator
    """
    return Administrator.query.get(int(user_id))


class LotZone(db.Model):
    """
    Model representation of the lotzone table.
    """
    # Database table name
    __tablename__ = 'lotzone'

    # Table attributes
    lot_id = db.Column('lot_id', db.Integer,
                       db.ForeignKey('lot.id', ondelete="cascade"), primary_key=True)
    zone_id = db.Column('zone_id', db.Integer,
                        db.ForeignKey('zone.id', ondelete="cascade"), primary_key=True)

    # Formats string representation of a lotzone record
    def __repr__(self):
        return '<LotZone: Lot {}, Zone{}>'.format(self.lot_id, self.zone_id)


class Zone(db.Model):
    """
        Model representation of the zone table.
    """
    # Database table name
    __tablename__ = 'zone'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    color = db.Column(db.String(100), index=True, unique=True)
    children = db.Column(db.String(100))

    # Table relationships
    lots = db.relationship('Lot', secondary='lotzone',
                           backref=db.backref('zones', lazy='dynamic'))

    # Formats string representation of a zone record
    def __repr__(self):
        return '<Zone {}>'.format(self.id)

    # Returns a zone record as a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color
        }

    # Takes in a dictionary representation of a zone and returns the record as a Zone.
    def from_dict(self, data):
        for field in ['name', 'color']:
            if field in data:
                setattr(self, field, data[field])


class Lot(db.Model):
    # Database table name
    __tablename__ = 'lot'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)

    # Formats string representation of a lot record
    def __repr__(self):
        return '<Lot {}>'.format(self.id)

    # Calculates the number of available spaces for the Lot and returns the count.
    def get_available_spaces(self, zone_id):
        return self.spaces.filter(ParkingSpace.zone_id == zone_id).filter(ParkingSpace.availability == SpaceAvailability.AVAILABLE).count()


class ParkingSpace(db.Model):
    # Database table name
    __tablename__ = 'space'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    availability = db.Column(db.Enum(SpaceAvailability))
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'), nullable=False)
    camera_id = db.Column(db.Integer, db.ForeignKey(
        'camera.id', ondelete="cascade"), nullable=False)

    # Table relationships
    lot = db.relationship('Lot', backref=db.backref('spaces', lazy='dynamic', cascade="all"))
    zone = db.relationship(
        'Zone', backref=db.backref('spaces', lazy='dynamic', cascade="all"))

    # Formats string representation of a space record
    def __repr__(self):
        return '<Space {}>'.format(self.id)


class SpaceDimensions(db.Model):
    # Database table name
    __tablename__ = 'space_dimensions'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    start_x = db.Column(db.Float)
    start_y = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id', ondelete="cascade"), nullable=False)

    # Table relationships
    space = db.relationship(
        'ParkingSpace', backref=db.backref('dimensions', uselist=False, cascade="all, delete"))

    # Formats a string representation of a space_coordinate record
    def __repr__(self):
        return '<Space Coordinates {}>'.format(self.id)


class Camera(db.Model):
    # Database table name
    __tablename__ = 'camera'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer)
    status = db.Column(db.Enum(CameraStatus))
    ip_address = db.Column(db.String(20))
    lot_id = db.Column(db.Integer, db.ForeignKey("lot.id", ondelete="cascade"), nullable=False)

    # Table relationships
    lot = db.relationship(
        'Lot', backref=db.backref('cameras', lazy='dynamic'))
    spaces = db.relationship('ParkingSpace', cascade="all, delete")

    # Formats a string representation of a camera record
    def __repr__(self):
        return '<Camera {}>'.format(self.id)

    # Returns a camera record as a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "status": self.status.value,
            "lot_id": self.lot_id
        }

    # Takes in a dictionary representation of a camera and returns the record as a Camera.
    def from_dict(self, data):
        for field in ['location', 'status', "lot_id"]:
            if field in data:
                setattr(self, field, data[field])


class ControlPoints(db.Model):
    # Database table name
    __tablename__ = 'control_points'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    start_x = db.Column(db.Float)
    start_y = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    camera_id = db.Column(db.Integer, db.ForeignKey(
        'camera.id', ondelete="cascade"), nullable=False)

    # Table relationships
    camera = db.relationship(
        'Camera', backref=db.backref('control', uselist=False, cascade="all, delete"))


class AdminGroup(db.Model):
    # Database table name
    __tablename__ = 'admin_group'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class SystemLog(db.Model):
    # Database table name
    __tablename__ = 'logs'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    status = db.Column(db.Enum(LogStatus))
    type = db.Column(db.Enum(LogType), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)


class Notifications(db.Model):
    # Database table name
    __tablename__ = "notifications"

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    updates = db.Column(db.String(255), default="", nullable=False)


class Administrator(UserMixin, db.Model):
    # Database table name
    __tablename__ = 'administrators'

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(255), index=True)
    last_name = db.Column(db.String(255), index=True)
    middle_initial = db.Column(db.String(1), index=True)
    password_hash = db.Column(db.String(128))
    group_id = db.Column(db.Integer, db.ForeignKey('admin_group.id'))

    # Table relationships
    group = db.relationship('AdminGroup', backref=db.backref(
        'administrators', lazy='dynamic'))

    # Table constraint, 2 administrators can't have the same first name, last name, and middle initial combination
    __table_args__ = (db.UniqueConstraint(
        'first_name', 'last_name', 'middle_initial'),)

    # Formats the string representation of an administrator record
    def __repr__(self):
        return '<User {}>'.format(self.first_name)

    # Generates hash of the given password string and updates the password_hash attribute for the administrator.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Compares the given password to the hashed version stored for the administrator. Returns true or false.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Generates and returns a JWT token for resetting a password, with a default expiration of 10 minutes.
    def get_reset_password_token(self, expires_in=timedelta(minutes=10)):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # Takes in a JWT token and verifies that is a valid, unexpired reset password token.
    # Returns the administrator the token was assigned to, or None if invalid.
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Administrator.query.get(id)

    # Generates and returns a JWT token for activating a new administrator, with a default expiration of 10 minutes.
    def get_activation_token(self, expires_in=600):
        return jwt.encode(
            {'activation': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # Takes in a JWT token and verifies that is a valid, unexpired activation password token.
    # Returns the administrator the token was assigned to, or None if invalid.
    @staticmethod
    def verify_activation_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['activation']
        except:
            return
        return Administrator.query.get(id)
