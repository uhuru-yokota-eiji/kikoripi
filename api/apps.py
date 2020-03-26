from django.apps import AppConfig
from django.conf import settings


class ApiConfig(AppConfig):
    name = "api"

    @classmethod
    def is_env_local(cls):
        return settings.ENV_NAME == "local"

    @classmethod
    def is_env_raspi(cls):
        return settings.ENV_NAME == "raspi"
