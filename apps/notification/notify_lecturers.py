import logging
import os  # Import os to access environment variables
from apps.notification.brevo_email_service import EmailService
from apps.notification.utils import get_lecturer_emails

# Initialize logger
logger = logging.getLogger(__name__)

def notify_lecturers(subject, body):
    try:
        # Load API key and sender email from environment variables
        api_key = os.getenv("BREVO_API_KEY")
        sender_email = os.getenv("DEFAULT_FROM_EMAIL")

        if not api_key or not sender_email:
            logger.error("API key or sender email is not set in environment variables.")
            return

        email_service = EmailService(api_key)  # Initialize EmailService with the API key
        lecturer_emails = get_lecturer_emails()  # Get recipient emails

        if not lecturer_emails:
            logger.warning("No lecturer emails found to send notifications.")
            return

        for email in lecturer_emails:
            success, response = email_service.send_email(
                subject=subject,
                recipient_email=email,
                sender_email=sender_email,  # Sender email is passed here
                body=body
            )
            if not success:
                logger.error(f"Failed to send email to {email}: {response}")
            else:
                logger.info(f"Email successfully sent to {email}.")
    except Exception as e:
        logger.exception(f"An error occurred while notifying lecturers: {e}")
