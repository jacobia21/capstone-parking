from app.main import bp
from flask import render_template, url_for
from app.models import Zone, Lot, ParkingSpace
from sqlalchemy import func

@bp.route('/')
@bp.route('/index')
def index():
    return render_template("main/index.html", title='Home')

@bp.route('/zones')
def zones():
    zones = Zone.query.all()
    return render_template("main/zones.html", title='Zones', zones=zones)

@bp.route('/lots/<zone_id>')
def lots(zone_id):
    lots = Lot.query.join(ParkingSpace, Lot.id==ParkingSpace.lot_id).add_columns(Lot.name,func.count(ParkingSpace.availability).label("available_spaces")).filter(ParkingSpace.zone_id==zone_id).filter(ParkingSpace.availability == "Available").group_by(Lot.id).all()
    
    return render_template("main/lots.html", title='Lots', lots=lots)
