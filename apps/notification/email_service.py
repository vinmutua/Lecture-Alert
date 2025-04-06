import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

class EmailService:
    def send_email(self, recipient_email, subject, message):
        brevo_api_key = os.getenv("BREVO_API_KEY")
        if not brevo_api_key:
            return False, "BREVO_API_KEY not found in environment"

        # Set up the Brevo API client configuration for transactional emails
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = brevo_api_key
        api_client = sib_api_v3_sdk.ApiClient(configuration)
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

        # Prepare the transactional email payload
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": recipient_email}],
            sender={"email": settings.DEFAULT_FROM_EMAIL, "name": "SoftAlert"},
            subject=subject,
            html_content=f"<html><body><p>{message}</p></body></html>"
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            return True, "Email sent successfully"
        except ApiException as e:
            return False, f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}"