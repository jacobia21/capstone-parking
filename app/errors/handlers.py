"""This module holds all error handlers."""
import traceback
from flask import render_template, current_app

from app import db
from app.errors import bp
from app.email import send_email


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
    error_tb = traceback.format_exc()
    send_email('[Soar High Parking] System Failure',
               sender=current_app.config['ADMIN'],
               recipients=current_app.config['ADMIN'],
               html_body=render_template('error_message_email.html',
                                         error=error_tb))
    db.session.rollback()
    return render_template('500.html'), 500
