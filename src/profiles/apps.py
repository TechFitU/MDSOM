from __future__ import unicode_literals
from django.apps import AppConfig


class ProfileConfig(AppConfig):
    name = "profiles"
    label = 'profiles'
    verbose_name = 'User Profiles'

    def ready(self):
        from . import signals   # noqa
