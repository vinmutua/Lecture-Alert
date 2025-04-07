import os
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailService:
    """
    A service class to send emails using the Brevo REST API.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("BREVO_API_KEY")
        self.base_url = "https://api.brevo.com/v3/smtp/email"

    def send_email(self, subject, recipient_email, sender_email=None, sender_name="Lect Alert", html_content=None, body=None, debug=False):
        """
        Sends an email using the Brevo REST API.

        Args:
            subject: Email subject
            recipient_email: Recipient's email address
            sender_email: Sender's email address (optional)
            sender_name: Sender's name (optional)
            html_content: HTML content of the email (optional)
            body: Alias for html_content (deprecated, use html_content instead)
            debug: Whether to print debug information (optional)
        """
        # Use html_content if provided, otherwise use body, otherwise use default
        email_content = html_content or body or "This is a test email."

        if debug:
            print(f"DEBUG: Sending email with parameters:")
            print(f"  Subject: {subject}")
            print(f"  Recipient: {recipient_email}")
            print(f"  Sender: {sender_name} <{sender_email}>")
            print(f"  Content length: {len(email_content)} characters")

        sender_email = sender_email or os.getenv("DEFAULT_FROM_EMAIL")
        headers = {
            "accept": "application/json",
            "api-key": self.api_key,  # API key is used here
            "content-type": "application/json",
        }
        payload = {
            "sender": {"name": sender_name, "email": sender_email},  # Sender email is included here
            "to": [{"email": recipient_email}],
            "subject": subject,
            "htmlContent": email_content,
        }

        if debug:
            print(f"DEBUG: API URL: {self.base_url}")
            print(f"DEBUG: Headers: {headers}")
            print(f"DEBUG: Payload: {payload}")

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            if response.status_code == 201:  # 201 indicates the email was successfully sent
                return True, response.json()
            else:
                logger.error(f"Failed to send email to {recipient_email} with subject '{subject}': {response.text}")
                return False, response.text
        except Exception as e:
            logger.error(f"Exception occurred while sending email to {recipient_email} with subject '{subject}': {str(e)}")
            return False, str(e)