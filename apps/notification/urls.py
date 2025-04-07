from django.urls import path
from .views import send_notification_to_lecturers

urlpatterns = [
    path('send-notifications/', send_notification_to_lecturers, name='send_notifications'),
]