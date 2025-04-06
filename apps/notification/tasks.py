from celery import shared_task
from django.utils.timezone import now, timedelta
from apps.accounts.models import Timetable
from .email_service import EmailService
from .models import Notification

@shared_task
def send_upcoming_class_notifications():
    """Send email notifications to lecturers about their upcoming classes."""
    email_service = EmailService()
    current_time = now()
    upcoming_classes = Timetable.objects.filter(
        date=current_time.date(),
        start_time__gte=current_time.time(),
        start_time__lte=(current_time + timedelta(hours=1)).time()
    ).select_related('lecturer')

    for timetable in upcoming_classes:
        lecturer = timetable.lecturer
        if lecturer.email:
            subject = "Upcoming Class Notification"
            message = (
                f"Dear {lecturer.fullname},\n\n"
                f"You have an upcoming class:\n"
                f"Course: {timetable.course.name}\n"
                f"Department: {timetable.department.name}\n"
                f"Date: {timetable.date}\n"
                f"Time: {timetable.start_time} - {timetable.end_time}\n"
                f"Venue: {timetable.venue}\n\n"
                f"Best regards,\nLecture Alert System"
            )
            success, response = email_service.send_email(lecturer.email, subject, message)
            Notification.objects.create(
                lecturer=lecturer,
                message=message,
                is_sent=success
            )
            if success:
                print(f"Email sent to {lecturer.fullname} ({lecturer.email})")
            else:
                print(f"Failed to send email to {lecturer.fullname}: {response}")