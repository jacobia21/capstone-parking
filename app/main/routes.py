from app.main import bp
from flask import render_template, url_for
from app.models import Zone, Lot, ParkingSpace
from sqlalchemy import func
from app.enums import SpaceAvailability

@bp.route('/')
@bp.route('/index')
def index():
    4/0
    return render_template("index.html", title='Home')

@bp.route('/zones')
def zones():
    zones = Zone.query.all()
    return render_template("zones.html", title='Zones', zones=zones)

@bp.route('/lots/<zone_id>')
def lots(zone_id):
    lots = Zone.query.get(zone_id).lots
    return render_template("lots.html", title='Lots', lots=lots)
