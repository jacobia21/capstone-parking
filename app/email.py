from flask import current_app, render_template
import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, sender, recipients, text_body, html_body):
    print(sender)
    print(recipients)
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        html_content=html_body)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Soar High Parking] Reset Your Password',
               sender=current_app.config['ADMIN'],
               recipients=user.email,
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))