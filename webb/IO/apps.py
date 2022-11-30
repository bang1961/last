from django.apps import AppConfig


class IoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IO'
    
    def ready(self):
        import IO.signals
