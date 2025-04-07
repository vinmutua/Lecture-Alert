import logging
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from datetime import datetime
from django.utils.timezone import localtime
from apps.notification.brevo_email_service import EmailService
from .utils import get_lecturer_emails, get_upcoming_classes
from django.conf import settings
from apps.notification.models import Notification

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_upcoming_class_notifications(self):
    """
    Send email notifications to lecturers about their upcoming classes.
    """
    now = localtime()
    logger.info(f"[NOTIFICATION TASK] Running at {now}")

    api_key = settings.BREVO_API_KEY
    email_service = EmailService(api_key=api_key)

    # Fetch upcoming lessons using utility function
    # We'll use two time windows to ensure we don't miss any classes:
    # 1. Classes starting between 30 and 31 minutes from now (normal notifications)
    # 2. Classes starting between 0 and 30 minutes from now that haven't been notified yet (catch-up)

    # Regular notification window (30-31 minutes)
    upcoming_classes_regular = get_upcoming_classes(min_window_minutes=30, max_window_minutes=31)
    logger.info(f"[NOTIFICATION TASK] Found {upcoming_classes_regular.count()} classes in regular window (30-31 min)")

    # Check if notifications have already been sent for regular window classes
    regular_notified_ids = Notification.objects.filter(
        timetable__in=upcoming_classes_regular,
        is_sent=True
    ).values_list('timetable_id', flat=True)

    regular_classes_to_notify = upcoming_classes_regular.exclude(id__in=regular_notified_ids)

    # Log detailed information about regular window classes
    for cls in upcoming_classes_regular:
        already_notified = cls.id in regular_notified_ids
        status = "Already notified" if already_notified else "Needs notification"
        logger.info(f"[NOTIFICATION TASK] Regular window class: {cls.course.name} by {cls.lecturer.fullname} at {cls.start_time} - {status}")

    # Catch-up for any missed classes (0-30 minutes)
    upcoming_classes_catchup = get_upcoming_classes(min_window_minutes=0, max_window_minutes=30)
    logger.info(f"[NOTIFICATION TASK] Found {upcoming_classes_catchup.count()} classes in catch-up window (0-30 min)")

    # Filter out classes that already have notifications
    catchup_notified_ids = Notification.objects.filter(
        timetable__in=upcoming_classes_catchup,
        is_sent=True
    ).values_list('timetable_id', flat=True)

    missed_classes = upcoming_classes_catchup.exclude(id__in=catchup_notified_ids)
    logger.info(f"[NOTIFICATION TASK] Found {missed_classes.count()} missed classes that need notifications")

    # Log detailed information about catch-up window classes
    for cls in upcoming_classes_catchup:
        already_notified = cls.id in catchup_notified_ids
        status = "Already notified" if already_notified else "Needs notification"
        logger.info(f"[NOTIFICATION TASK] Catch-up window class: {cls.course.name} by {cls.lecturer.fullname} at {cls.start_time} - {status}")

        # Additional details for classes that need notifications
        if not already_notified:
            from datetime import datetime
            now_local = localtime()
            cls_datetime = datetime.combine(now_local.date(), cls.start_time)
            time_diff = (cls_datetime - now_local.replace(tzinfo=None)).total_seconds() / 60
            logger.info(f"[NOTIFICATION TASK] Missed class details: ID={cls.id}, Minutes until start: {time_diff:.1f}")

    # Combine regular and missed classes
    upcoming_classes = list(regular_classes_to_notify) + list(missed_classes)
    logger.info(f"[NOTIFICATION TASK] Total classes to notify: {len(upcoming_classes)} ({len(regular_classes_to_notify)} from regular window, {len(missed_classes)} from catch-up window)")

    for lesson in upcoming_classes:
        # Use a more distinctive subject line with a timestamp to avoid filtering
        from datetime import datetime
        now_time = datetime.now()
        subject = f"Upcoming Class: {lesson.course.name} at {lesson.start_time} - {now_time.strftime('%H:%M:%S')}"
        recipient_email = lesson.lecturer.email
        sender_email = settings.DEFAULT_FROM_EMAIL

        # Simplified email template to avoid Brevo API length limitations
        body = f"""
        <html>
        <body>
            <h2>Upcoming Class Reminder</h2>
            <p>Dear {lesson.lecturer.fullname},</p>
            <p>This is a reminder that you have a class scheduled soon:</p>
            <ul>
                <li><strong>Course:</strong> {lesson.course.name}</li>
                <li><strong>Date:</strong> {lesson.date}</li>
                <li><strong>Time:</strong> {lesson.start_time} - {lesson.end_time}</li>
                <li><strong>Venue:</strong> {lesson.venue}</li>
            </ul>
            <p>Please be prepared for your class.</p>
            <p>Thank you!</p>
        </body>
        </html>
        """

        try:
            logger.info(f"[NOTIFICATION TASK] Attempting to send email to {recipient_email} for class {lesson.course.name} at {lesson.start_time}")
            success, response = email_service.send_email(
                subject=subject,
                recipient_email=recipient_email,
                sender_email=sender_email,
                html_content=body
            )
            if success:
                logger.info(f"[NOTIFICATION TASK] Successfully sent email to {recipient_email}")
                notification = Notification.objects.create(
                    lecturer=lesson.lecturer,
                    timetable=lesson,
                    email=recipient_email,
                    subject=subject,
                    is_sent=True,
                    sent_at=now
                )
                logger.info(f"[NOTIFICATION TASK] Created notification record: ID={notification.id}")
            else:
                logger.error(f"[NOTIFICATION TASK] Failed to send email to {recipient_email}: {response}")
                raise Exception(response)
        except Exception as e:
            logger.error(f"[NOTIFICATION TASK] Failed to send email to {recipient_email} for lesson {lesson.id}: {str(e)}")
            try:
                logger.info(f"[NOTIFICATION TASK] Retrying email to {recipient_email} in 60 seconds")
                self.retry(countdown=60)
            except MaxRetriesExceededError:
                logger.error(f"[NOTIFICATION TASK] Max retries exceeded for {recipient_email}")
                notification = Notification.objects.create(
                    lecturer=lesson.lecturer,
                    timetable=lesson,
                    email=recipient_email,
                    subject=subject,
                    is_sent=False,
                    failure_reason=str(e)
                )
                logger.error(f"[NOTIFICATION TASK] Created failed notification record: ID={notification.id}")

@shared_task
def send_class_reminder_emails():
    """
    Send reminder emails to lecturers about their upcoming classes.
    """
    now = localtime()
    logger.info(f"[REMINDER TASK] Running at {now}")

    api_key = settings.BREVO_API_KEY
    email_service = EmailService(api_key)

    # Fetch upcoming classes and lecturer emails using the same improved logic
    # Regular notification window (30-31 minutes)
    upcoming_classes_regular = get_upcoming_classes(min_window_minutes=30, max_window_minutes=31)
    logger.info(f"[REMINDER TASK] Found {upcoming_classes_regular.count()} classes in regular window (30-31 min)")

    # Catch-up for any missed classes (0-30 minutes)
    upcoming_classes_catchup = get_upcoming_classes(min_window_minutes=0, max_window_minutes=30)
    logger.info(f"[REMINDER TASK] Found {upcoming_classes_catchup.count()} classes in catch-up window (0-30 min)")

    # Filter out classes that already have notifications
    notified_timetable_ids = Notification.objects.filter(
        timetable__in=upcoming_classes_catchup,
        is_sent=True
    ).values_list('timetable_id', flat=True)

    missed_classes = upcoming_classes_catchup.exclude(id__in=notified_timetable_ids)
    logger.info(f"[REMINDER TASK] Found {missed_classes.count()} missed classes that need notifications")

    # Combine regular and missed classes
    upcoming_classes = list(upcoming_classes_regular) + list(missed_classes)
    lecturer_emails = get_lecturer_emails(upcoming_classes)
    logger.info(f"[REMINDER TASK] Total lecturers to notify: {len(lecturer_emails)}")

    subject = "Class Reminder"
    sender_email = settings.DEFAULT_FROM_EMAIL

    for email in lecturer_emails:
        logger.info(f"[REMINDER TASK] Attempting to send email to {email}")
        success, message = email_service.send_email(
            subject=subject,
            recipient_email=email,
            sender_email=sender_email
        )
        if success:
            logger.info(f"[REMINDER TASK] Email sent successfully to {email}")
        else:
            logger.error(f"[REMINDER TASK] Failed to send email to {email}: {message}")