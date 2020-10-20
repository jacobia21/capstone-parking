""" This module includes the logic for emails sent from the auth package """

from flask import current_app, render_template

from app import db
from app.email import send_email


def send_password_reset_email(user):
    """
    Sends a email to an administrator with instructions on resetting their password.

    :param user: The user who will receive the email.
    :type user: User

    """
    token = user.get_reset_password_token()
    db.session.commit()
    send_email('[Soar High Parking] Reset Your Password',
               sender=current_app.config['ADMIN'],
               recipients=user.email,
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_activation_email(user):
    """
    Sends an email to a newly added administrator to set their password.

    :param user: The user who will receive the email.
    :type user: User

    """
    token = user.get_activation_token()
    send_email('[Soar High Parking] Activate User',
               sender=current_app.config['ADMIN'],
               recipients=[user.email],
               html_body=render_template('email/activate_user.html',
                                         user=user, token=token))
