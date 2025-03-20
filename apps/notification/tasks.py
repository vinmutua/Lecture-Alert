from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from accounts.models import Timetable
from .models import Notification
from .infobip_service import InfobipService

@shared_task
def check_and_send_notifications():
    # Get current time and 30min threshold
    now = timezone.now()
    thirty_mins_later = now + timedelta(minutes=30)

    # Find upcoming lectures
    upcoming_lectures = Timetable.objects.filter(
        date=now.date(),
        start_time__gte=now.time(),
        start_time__lte=thirty_mins_later.time()
    ).select_related('lecturer')

    # Initialize InfoBip service
    sms_service = InfobipService()

    for lecture in upcoming_lectures:
        # Check if notification already sent
        notification_exists = Notification.objects.filter(
            lecturer=lecture.lecturer,
            sent_at__date=now.date(),
            is_sent=True
        ).exists()

        if not notification_exists:
            # Prepare message
            message = (
                f"Reminder: You have a {lecture.course} lecture "
                f"scheduled for {lecture.start_time} "
                f"at {lecture.venue}"
            )

            # Send SMS
            success, response = sms_service.send_sms(
                lecture.lecturer.phone,
                message
            )

            # Record notification
            Notification.objects.create(
                lecturer=lecture.lecturer,
                message=message,
                is_sent=success
            )