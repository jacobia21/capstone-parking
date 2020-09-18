""" This module holds the route controllers for the main module """

from app.main import bp
from flask import render_template, url_for
from app.models import Zone, Lot, ParkingSpace
from sqlalchemy import func
from app.enums import SpaceAvailability

@bp.route('/')
@bp.route('/index')
def index():
    """ Returns the home page of the site."""

    return render_template("index.html", title='Home')

@bp.route('/zones')
def zones():
    """ Retrieves all parking zone and displays them on the zones page. """
    zones = Zone.query.all()
    return render_template("zones.html", title='Zones', zones=zones)

@bp.route('/lots/<zone_id>')
def lots(zone_id):
    """ 
    Retrieves all the lots available in selected zone to display.

    :param zone_id: The id of the selected zone to look for lots in.
    :type zone_id: int
    
    """

    lots = Zone.query.get(zone_id).lots
    return render_template("lots.html", title='Lots', lots=lots)
