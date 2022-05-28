from django.apps import AppConfig


class TeamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teams'
    # verbose_name = 'teams manager'


    def ready(self):
        import teams.signals