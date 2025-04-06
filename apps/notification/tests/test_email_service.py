from __future__ import print_function

import sys
import os

# Add the project root directory (f:\Lecture_alert) to sys.path BEFORE any other imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from apps.notification.email_service import EmailService

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.mail import send_mail



def test_smtp_email():
    subject = "Test Email via Brevo SMTP"
    message = "This is a test email sent using Brevo's SMTP relay."
    recipient = "recipient@example.com"  # Replace with a valid recipient email

    success = send_mail(subject, message, None, [recipient])
    print("Emails sent:", success)

if __name__ == "__main__":

    test_smtp_email()