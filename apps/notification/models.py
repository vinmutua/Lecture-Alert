from django.db import models
from apps.accounts.models import Lecturer, Timetable

class Notification(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    timetable = models.ForeignKey(
        Timetable,
        on_delete=models.CASCADE,
        default=1 
    )
    email = models.EmailField(default="default@example.com")
    subject = models.CharField(max_length=255, default="No Subject")
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(null=True, blank=True)  # Added field to store failure reason

    def __str__(self):
        return f"Notification to {self.lecturer.fullname} - {self.subject}"

