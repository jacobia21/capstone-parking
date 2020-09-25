"""This module allows for sending asynchronous emails."""

from flask import current_app, render_template
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import db
from threading import Thread


def send_async_email(app, msg):
    """
    Sends an email in the background.

    :param app: The subject line of the email
    :type app: Flask
    :param msg: The email object to send.
    :type msg: Mail

    """
    with app.app_context():
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(msg)
        sg.send(msg)


def send_email(subject, sender, recipients, html_body):
    """
    Prepares a new SendGrid Mail object from inputs and calls :func:`~send_async_email` to send the asynchronous message.

    :param subject: The subject line of the email
    :type subject: str
    :param sender: The email address of the sender.
    :type sender: str
    :param recipients: An array of recipients. Min length 1.
    :type recipients: list[str]
    :param html_body: The file name of the html file that contains the body of the email.
    :type html_body: str

    """
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
