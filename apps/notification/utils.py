from datetime import timedelta
from django.utils.timezone import now, localtime
from apps.accounts.models import Timetable, Lecturer
from apps.notification.brevo_email_service import EmailService  # Import EmailService
import os

def get_upcoming_classes(min_window_minutes=30, max_window_minutes=60):
    """
    Fetch upcoming classes within a specific time window.

    Args:
        min_window_minutes: Minimum minutes from now (e.g., 30 means don't include classes starting sooner than 30 minutes)
        max_window_minutes: Maximum minutes from now (e.g., 60 means don't include classes starting later than 60 minutes)

    This approach ensures we don't miss any classes due to the cron job schedule.
    For example, if the cron job runs every 5 minutes and we want to notify about classes 30 minutes before they start,
    we should check for classes starting between 30 and 35 minutes from now.
    """
    import logging
    logger = logging.getLogger(__name__)

    now = localtime()  # Get current time in local timezone
    logger.debug(f"Looking for classes between {min_window_minutes} and {max_window_minutes} minutes from now ({now})")

    # Get all classes for today
    today_classes = Timetable.objects.filter(date=now.date())
    logger.debug(f"Found {today_classes.count()} total classes scheduled for today")

    upcoming_classes = []

    # Manually filter classes within the time window to handle time zones correctly
    for cls in today_classes:
        # Convert class start time to datetime for accurate comparison
        from datetime import datetime
        cls_datetime = datetime.combine(now.date(), cls.start_time)

        # Calculate minutes until class starts
        time_diff = (cls_datetime - now.replace(tzinfo=None)).total_seconds() / 60

        logger.debug(f"Class ID {cls.id}: {cls.course.name} at {cls.start_time} - {time_diff:.1f} minutes away")

        # Check if class is within the specified window
        if min_window_minutes <= time_diff <= max_window_minutes:
            upcoming_classes.append(cls.id)
            logger.debug(f"Class ID {cls.id} is within the {min_window_minutes}-{max_window_minutes} minute window")

    # Return QuerySet of classes within the time window
    result = Timetable.objects.filter(id__in=upcoming_classes)
    logger.debug(f"Returning {result.count()} classes within the {min_window_minutes}-{max_window_minutes} minute window")
    return result

def get_lecturer_emails(upcoming_classes):
    """
    Fetch emails of lecturers associated with the upcoming classes.
    """
    lecturer_ids = upcoming_classes.values_list('lecturer_id', flat=True).distinct()
    return list(Lecturer.objects.filter(id__in=lecturer_ids).values_list('email', flat=True))
