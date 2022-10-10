from django.apps import AppConfig


class ControlSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'control_settings'

    def ready(self):
        import control_settings.signals