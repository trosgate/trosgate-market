from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'

    verbose_name = "Inbox System"
    verbose_name_plural = "Inbox System"

    def ready(self):
        import notification.signals