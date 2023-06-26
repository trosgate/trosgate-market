from django.apps import AppConfig

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'

    verbose_name = "Realtime Chat System"
    verbose_name_plural = "Realtime Chat System"

    def ready(self):
        import notification.signals