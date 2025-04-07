import requests

class BrevoEmailService:
    """
    A service class to send emails using the Brevo REST API.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.brevo.com/v3/smtp/email"  # Brevo API endpoint for sending emails

    def send_email(self, subject, recipient_email, sender_email, sender_name="Your Name", body="This is a test email."):
        """
        Sends an email using the Brevo REST API.
        """
        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }
        payload = {
            "sender": {"name": sender_name, "email": sender_email},
            "to": [{"email": recipient_email}],
            "subject": subject,
            "htmlContent": body,
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            if response.status_code == 201:  # 201 indicates the email was successfully sent
                return True, response.json()
            else:
                return False, response.text
        except Exception as e:
            return False, str(e)

from django.test import TestCase

class TestEmailService(TestCase):  # Ensure the class name starts with 'Test'
    def test_send_email(self):  # Ensure the method name starts with 'test_'
        # Use environment variable or a placeholder for tests
        api_key = "YOUR_API_KEY_HERE"  # For tests, use a placeholder or mock
        email_service = BrevoEmailService(api_key)  # Use the correct class name

        # Test email details
        subject = "LEcture ALert Notification"
        recipient_email = "vincentmutua02@gmail.com"  # Replace with a valid recipient email
        sender_email = "vinniebrevo@gmail.com"  # Replace with your verified sender email
        sender_name = "Lecture Alert"
        body = f"""
        <div style="font-family: Arial, sans-serif; text-align: left; padding: 20px; background-color: #f4f4f4; border: 1px solid #ddd; border-radius: 10px; max-width: 600px; margin: auto;">
            <header style="background-color: #4CAF50; color: white; padding: 10px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0;">Lecture Alert Notification</h1>
            </header>
            <section style="padding: 20px; color: #333;">
                <p style="font-size: 16px;">Dear Vincent Musyoki Mutua,</p>
                <p style="font-size: 16px;">You have an upcoming lesson scheduled. Here are the details:</p>
                <ul style="list-style-type: none; padding: 0; font-size: 16px;">
                    <li style="margin-bottom: 10px;"><strong>Course:</strong> Data Structures</li>
                    <li style="margin-bottom: 10px;"><strong>Date:</strong> Monday April 04/07</li>
                    <li style="margin-bottom: 10px;"><strong>Time:</strong> 9:30:00 -  11:30:00</li>
                    <li style="margin-bottom: 10px;"><strong>Venue:</strong>S504</li>
                </ul>
                <p style="font-size: 16px;">Please ensure you are prepared for the lesson. If you have any questions, feel free to reach out to the administration.</p>
            </section>
            <footer style="background-color: #f9f9f9; color: #888; text-align: center; padding: 10px; border-top: 1px solid #ddd; border-radius: 0 0 10px 10px;">
                <p style="margin: 0; font-size: 12px;">Thank you for using Lecture Alert System!</p>
                <p style="margin: 0; font-size: 12px;">&copy; 07/04/2025 Lecture Alert System</p>
            </footer>
        </div>
        """

        # Send the email
        success, response = email_service.send_email(subject, recipient_email, sender_email, sender_name, body)

        # Assert the result
        self.assertTrue(success, f"Email sending failed: {response}")

if __name__ == "__main__":
    # Use environment variable or a placeholder for tests
    api_key = "YOUR_API_KEY_HERE"  # For tests, use a placeholder or mock
    email_service = BrevoEmailService(api_key)

    # Test email details
    subject = "Test Email"
    recipient_email = "vincentmutua02@gmail.com"  # Replace with a valid recipient email
    sender_email = "vinniebrevo@gmail.com"  # Replace with your verified sender email
    sender_name = "Lecture Alert"
    body = f"""
        <div style="font-family: Arial, sans-serif; text-align: left; padding: 20px; background-color: #f4f4f4; border: 1px solid #ddd; border-radius: 10px; max-width: 600px; margin: auto;">
            <header style="background-color: #4CAF50; color: white; padding: 10px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0;">Lecture Alert Notification</h1>
            </header>
            <section style="padding: 20px; color: #333;">
                <p style="font-size: 16px;">Dear Vincent Musyoki Mutua,</p>
                <p style="font-size: 16px;">You have an upcoming lesson scheduled. Here are the details:</p>
                <ul style="list-style-type: none; padding: 0; font-size: 16px;">
                    <li style="margin-bottom: 10px;"><strong>Course:</strong> Data Structures</li>
                    <li style="margin-bottom: 10px;"><strong>Date:</strong> Monday April 04/07</li>
                    <li style="margin-bottom: 10px;"><strong>Time:</strong> 9:30:00 -  11:30:00</li>
                    <li style="margin-bottom: 10px;"><strong>Venue:</strong>S504</li>
                </ul>
                <p style="font-size: 16px;">Please ensure you are prepared for the lesson. If you have any questions, feel free to reach out to the administration.</p>
            </section>
            <footer style="background-color: #f9f9f9; color: #888; text-align: center; padding: 10px; border-top: 1px solid #ddd; border-radius: 0 0 10px 10px;">
                <p style="margin: 0; font-size: 12px;">Thank you for using Lecture Alert System!</p>
                <p style="margin: 0; font-size: 12px;">&copy; 07/04/2025 Lecture Alert System</p>
            </footer>
        </div>
        """
    # Send the email
    success, response = email_service.send_email(subject, recipient_email, sender_email, sender_name, body)

    # Print the result
    if success:
        print("Email sent successfully!")
        print(response)
    else:
        print("Failed to send email.")
        print(response)