from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from time import time
import jwt
from flask import current_app

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class LotZone(db.Model):
    __tablename__ = 'lotzone'
    lot_id = db.Column('lot_id', db.Integer, db.ForeignKey('lot.id'),primary_key=True)
    zone_id = db.Column('zone_id', db.Integer, db.ForeignKey('zone.id'), primary_key=True)

    def __repr__(self):
        return '<LotZone {}>'.format(self.id)

   
class Zone(db.Model):
    __tablename__ = 'zone'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),index=True, unique=True)
    color = db.Column(db.String(100),index=True, unique=True)

    lots = db.relationship('Lot', secondary='lotzone', backref=db.backref('zones', lazy='dynamic'))

    def __repr__(self):
        return '<Zone {}>'.format(self.id)

class Lot(db.Model):
    __tablename__ = 'lot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),index=True, unique=True)

    def __repr__(self):
        return '<Lot {}>'.format(self.id)

class ParkingSpace(db.Model):
    __tablename__ = 'space'
    id = db.Column(db.Integer, primary_key=True)
    availability = db.Column(db.String(100))
    lot_id = db.Column(db.Integer, db.ForeignKey('lotzone.lot_id'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('lotzone.zone_id'), nullable=False)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)

    def __repr__(self):
        return '<Lot {}>'.format(self.id)

class Camera(db.Model):
    __tablename__ = 'camera'
    id = db.Column(db.Integer, primary_key=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)  

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