from django import apps


class MastermindConfig(apps.AppConfig):
    name = 'mastermind'

    def ready(self):
        from mastermind import signals  # noqa
