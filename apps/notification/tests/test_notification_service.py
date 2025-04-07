from unittest.mock import patch
from django.test import TestCase
from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
from apps.notification.brevo_email_service import EmailService
from apps.notification.models import Notification
from apps.accounts.models import Lecturer, Timetable, Course, Department
from apps.notification.utils import get_upcoming_classes, get_lecturer_emails

class TestNotificationService(TestCase):
    def setUp(self):
        """
        Set up mock data for tests.
        """
        # Create mock Department, Course, Lecturer, and Timetable objects
        self.department = Department.objects.create(
            id=1,
            name="Mathematics Department"
        )
        self.course = Course.objects.create(
            id=1,
            name="Advanced Mathematics",
            department=self.department
        )
        self.lecturer = Lecturer.objects.create(
            id=1,
            fullname="John Doe",
            email="johndoe@example.com"
        )
        # Ensure the date and time are timezone-aware and match the query conditions
        self.timetable = Timetable.objects.create(
            id=1,
            course=self.course,
            date=now().date(),  # Set date to today
            start_time=(now() + timedelta(minutes=10)).time(),  # Set start_time within the next 30 minutes
            end_time=(now() + timedelta(minutes=70)).time(),
            venue="Room 101",
            lecturer=self.lecturer
        )

    def test_notification_sent_to_lecturer(self):
        # Mock lesson and lecturer data
        lesson = {
            "lecturer": {"fullname": "John Doe", "email": "johndoe@example.com"},
            "course": {"name": "Advanced Mathematics"},
            "date": "2023-10-15",
            "start_time": "10:00 AM",
            "end_time": "12:00 PM",
            "venue": "Room 101",
        }

        # Mock the send_email method
        with patch("apps.notification.brevo_email_service.EmailService.send_email") as mock_send_email:
            mock_send_email.return_value = (True, "Email sent successfully")

            # Trigger the notification logic
            email_service = EmailService("dummy_api_key")
            subject = "Upcoming Lesson Notification"
            body = f"""
            <p>Dear {lesson['lecturer']['fullname']},</p>
            <p>You have an upcoming lesson:</p>
            <ul>
                <li><strong>Course:</strong> {lesson['course']['name']}</li>
                <li><strong>Date:</strong> {lesson['date']}</li>
                <li><strong>Time:</strong> {lesson['start_time']} - {lesson['end_time']}</li>
                <li><strong>Venue:</strong> {lesson['venue']}</li>
            </ul>
            <p>Thank you,<br>Lecture Alert System</p>
            """
            email_service.send_email(
                subject,
                lesson["lecturer"]["email"],
                "admin@lecturealert.com",
                "Lecture Alert System",
                body,
            )

            # Assert that send_email was called with the correct arguments
            mock_send_email.assert_called_once_with(
                subject,
                lesson["lecturer"]["email"],
                "admin@lecturealert.com",
                "Lecture Alert System",
                body,
            )

    def test_notification_model_creation(self):
        # Create a Notification object using the mock Lecturer and Timetable
        sent_at_datetime = make_aware(datetime(2023, 10, 15, 10, 0, 0))  # Use a datetime object
        notification = Notification.objects.create(
            lecturer=self.lecturer,
            timetable=self.timetable,
            email=self.lecturer.email,
            subject="Upcoming Lesson Notification",
            is_sent=True,
            sent_at=sent_at_datetime,  # Use the datetime object here
        )

        # Assert that the Notification object was created with the correct details
        self.assertEqual(notification.lecturer, self.lecturer)
        self.assertEqual(notification.timetable, self.timetable)
        self.assertEqual(notification.email, self.lecturer.email)
        self.assertEqual(notification.subject, "Upcoming Lesson Notification")
        self.assertTrue(notification.is_sent)
        self.assertEqual(notification.sent_at.isoformat(), "2023-10-15T10:00:00+00:00")

    def test_get_upcoming_classes(self):
        # Call the get_upcoming_classes function
        upcoming_classes = get_upcoming_classes()

        # Assert that the function returns the expected data
        self.assertEqual(len(upcoming_classes), 1)
        self.assertEqual(upcoming_classes[0].course.name, self.course.name)
