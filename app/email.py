"""This module allows for sending asynchronous emails."""

import os
from threading import Thread

from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_async_email(app, msg):
    """
    Sends an email in the background.

    :param app: The subject line of the email
    :type app: Flask
    :param msg: The email object to send.
    :type msg: Mail

    """

    # The function is called on a custom Thread, so we need to get the application context before sending a message.
    with app.app_context():

        # Instantiate the SendGridAPIClient with API key and send message
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(msg)


def send_email(subject, sender, recipients, html_body):
    """
    Prepares a new SendGrid Mail object from inputs and calls
    :func:`send_async_email` to send the asynchronous message.

    :param subject: The subject line of the email
    :type subject: str
    :param sender: The email address of the sender.
    :type sender: str
    :param recipients: An array of recipients. Min length 1.
    :type recipients: list[str]
    :param html_body: The file name of the html file that contains the body of the email.
    :type html_body: str

    """

    try:
        # Create a new SendGrid Mail object with the arguments given
        message = Mail(
            from_email=sender,
            to_emails=recipients,
            subject=subject,
            html_content=html_body)

        # We prepare a new Thread here to send the email in the background. This takes in the send_async_email
        # function as its target and runs the function with the parameters passed through args.
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), message)).start()

    except Exception as e:
        print(e)
        # FIXME: should do some type of error handling here or allow error to bubble up
