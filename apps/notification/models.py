from django.db import models

class Notification(models.Model):
    lecturer = models.ForeignKey('accounts.Lecturer', on_delete=models.CASCADE, related_name='notifications')
    subject = models.CharField(max_length=255, null=True, blank=True)  # Subject field
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        db_table = 'notifications'
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.lecturer.fullname} - {self.sent_at}"

    @property
    def email(self):
        return self.lecturer.email

