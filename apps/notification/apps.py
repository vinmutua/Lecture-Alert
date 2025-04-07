from django.apps import AppConfig

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field type for models in this app.
    name = 'apps.notification'  # Specifies the full Python path to the app.
