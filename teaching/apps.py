from django.apps import AppConfig


class TeachingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teaching'
    verbose_name = '3.教学'
    
    def ready(self):
        from .signals import receivers
