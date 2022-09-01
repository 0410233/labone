from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = '6.微信用户'

    def ready(self):
        from .signals import receivers
