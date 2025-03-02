# from django.db import models
# from accounts.models import Lecturer

# class Notification(models.Model):
#     id = models.AutoField(primary_key=True)
#     lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='notifications')
#     message = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)
#     is_sent = models.BooleanField(default=False)

#     class Meta:
#         db_table = 'notifications'
#         ordering = ['-sent_at']

#     def __str__(self):
#         return f"{self.lecturer.fullname} - {self.sent_at}"
