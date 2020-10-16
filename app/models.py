""" This module defines the models that represent the database tables and relationships. """
from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login
from app.enums import CameraStatus, SpaceAvailability, LogStatus, LogType


@login.user_loader
def load_user(id):
    """Tells  :mod:`flask_login`  how a user should be loaded. This method should not be called directly."""
    return User.query.get(int(id))


class APIMixin(object):
    @staticmethod
    def to_collection_dict(query):
        resources = query.paginate()
        data = {
            'items': [item.to_dict() for item in resources.items],
        }
        return data


class LotZone(db.Model):
    __tablename__ = 'lotzone'
    lot_id = db.Column('lot_id', db.Integer,
                       db.ForeignKey('lot.id', ondelete="cascade"), primary_key=True)
    zone_id = db.Column('zone_id', db.Integer,
                        db.ForeignKey('zone.id', ondelete="cascade"), primary_key=True)

    def __repr__(self):
        return '<LotZone: Lot {}, Zone{}>'.format(self.lot_id, self.zone_id)


class Zone(APIMixin, db.Model):
    __tablename__ = 'zone'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    color = db.Column(db.String(100), index=True, unique=True)

    lots = db.relationship('Lot', secondary='lotzone',
                           backref=db.backref('zones', lazy='dynamic'))

    def __repr__(self):
        return '<Zone {}>'.format(self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color
        }

    def from_dict(self, data):
        for field in ['name', 'color']:
            if field in data:
                setattr(self, field, data[field])


class Lot(db.Model):
    __tablename__ = 'lot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)

    def __repr__(self):
        return '<Lot {}>'.format(self.id)

    def get_available_spaces(self):
        return self.spaces.filter(ParkingSpace.availability == SpaceAvailability.AVAILABLE).count()


class ParkingSpace(db.Model):
    __tablename__ = 'space'
    id = db.Column(db.Integer, primary_key=True)
    availability = db.Column(db.Enum(SpaceAvailability))
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'), nullable=False)
    camera_id = db.Column(db.Integer, db.ForeignKey(
        'camera.id', ondelete="cascade"), nullable=False)

    lot = db.relationship('Lot', backref=db.backref('spaces', lazy='dynamic'))
    zone = db.relationship(
        'Zone', backref=db.backref('spaces', lazy='dynamic'))
    camera = db.relationship(
        'Camera', backref=db.backref('spaces', lazy='dynamic'))

    def __repr__(self):
        return '<Space {}>'.format(self.id)


class SpaceDimensions(db.Model):
    __tablename__ = 'space_dimensions'
    id = db.Column(db.Integer, primary_key=True)
    start_x = db.Column(db.Integer)
    start_y = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id', ondelete="cascade"), nullable=False)

    space = db.relationship(
        'ParkingSpace', backref=db.backref('dimensions', lazy='dynamic'))

    def __repr__(self):
        return '<Space Coordinates {}>'.format(self.id)


class Camera(db.Model):
    __tablename__ = 'camera'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer)
    status = db.Column(db.Enum(CameraStatus))
    ip_address = db.Column(db.String(20))
    lot_id = db.Column(db.Integer, db.ForeignKey("lot.id", ondelete="cascade"), nullable=False)

    lot = db.relationship(
        'Lot', backref=db.backref('cameras', lazy='dynamic'))

    def __repr__(self):
        return '<Camera {}>'.format(self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "status": self.status.value,
            "lot_id": self.lot_id
        }

    def from_dict(self, data):
        for field in ['location', 'status', "lot_id"]:
            if field in data:
                setattr(self, field, data[field])


class ControlPoints(db.Model):
    __tablename__ = 'control_points'
    id = db.Column(db.Integer, primary_key=True)
    start_x = db.Column(db.Integer)
    start_y = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    camera_id = db.Column(db.Integer, db.ForeignKey(
        'camera.id', ondelete="cascade"), nullable=False)

    camera = db.relationship(
        'Camera', backref=db.backref('control', lazy='dynamic', cascade="all, delete-orphan"))


class AdminGroup(db.Model):
    __tablename__ = 'admin_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class SystemLog(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    status = db.Column(db.Enum(LogStatus))
    type = db.Column(db.Enum(LogType), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(255), index=True)
    last_name = db.Column(db.String(255), index=True)
    middle_initial = db.Column(db.String(1), index=True)
    password_hash = db.Column(db.String(128))
    group_id = db.Column(db.Integer, db.ForeignKey('admin_group.id'))

    group = db.relationship('AdminGroup', backref=db.backref(
        'administrators', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint(
        'first_name', 'last_name', 'middle_initial'),)

    def __repr__(self):
        return '<User {}>'.format(self.first_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_activation_token(self, expires_in=600):
        return jwt.encode(
            {'activation': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_activation_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['activation']
        except:
            return
        return User.query.get(id)
