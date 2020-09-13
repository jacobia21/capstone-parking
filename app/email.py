from flask import current_app, render_template
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import db
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(msg)
        sg.send(msg)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        
def send_email(subject, sender, recipients, text_body, html_body):
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        html_content=html_body)
    try:
        Thread(target=send_async_email,
           args=(current_app._get_current_object(), message)).start()
        
    except Exception as e:
        print(e)