"""This module holds all error handlers."""
from app.errors import bp
from flask import render_template
from app import db


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Handles all 404 errors, displaying the 404.html page.

    :param error: The error that triggered the handler.
    """
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Handles all 500, internal errors, displaying the 500.html page.

    :param error: The error that triggered the handler.
    """
    db.session.rollback()
    return render_template('500.html'), 500
