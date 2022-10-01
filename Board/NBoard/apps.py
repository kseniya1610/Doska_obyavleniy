from django.apps import AppConfig


class NBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NBoard'

    def ready(self):
        pass
        