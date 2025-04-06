from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('lecturer', 'email', 'subject', 'is_sent', 'sent_at')
    list_filter = ('is_sent', 'sent_at')
    search_fields = ('lecturer__fullname', 'email', 'subject')

