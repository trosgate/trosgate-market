from django.apps import AppConfig


class GeneralSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'general_settings'
    verbose_name = 'Settings'

    def ready(self):
        import general_settings.signals
