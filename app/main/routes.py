""" This module holds the route controllers for the main blueprint. """

from flask import render_template, flash

from app.admin.utils import log_error_to_database
from app.main import bp
from app.models import Zone


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
    try:
        zone = Zone.query.get_or_404(zone_id)
        lots = zone.lots

        available_spaces = {}

        for lot in lots:
            available_spaces[lot.name] = lot.get_available_spaces(zone_id)

        children = zone.children.split(',') if zone.children != '' else None
        child_zones = []
        if children is not None:
            for child in children:
                zone = Zone.query.get_or_404(int(child))
                child_zones.append(zone.name)
                for lot in zone.lots:
                    if lot.name in available_spaces:
                        available_spaces[lot.name] = available_spaces[lot.name] + lot.get_available_spaces(zone.id)
                    else:
                        available_spaces[lot.name] = lot.get_available_spaces(zone.id)
    except Exception as error:
        log_error_to_database(error)
        flash("Something went wrong, try again later.")
    return render_template("lots.html", title='Lots', available_spaces=available_spaces, zone=Zone.query.get_or_404(zone_id), child_zones=child_zones)
