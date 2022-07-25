from django.apps import AppConfig


class PinderappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pinderApp'

    def ready(self):
        import pinderApp.signals
