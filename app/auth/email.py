from app.email import send_email
from app import db
from flask import current_app, render_template
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    db.session.commit()
    send_email('[Soar High Parking] Reset Your Password',
               sender=current_app.config['ADMIN'],
               recipients=user.email,
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_activation_email(user):
    token = user.get_activation_token()
    send_email('[Soar High Parking] Activate User',
               sender=current_app.config['ADMIN'],
               recipients=[user.email],
               html_body=render_template('email/activate_user.html',
                                         user=user, token=token))