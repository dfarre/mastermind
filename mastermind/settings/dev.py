from mastermind.settings.base import *  # noqa


ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append('django.contrib.postgres')  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'HOST': 'db',
        'PASSWORD': 'postgres',
        'PORT': 5433,
        'USER': 'postgres',
    }
}


REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += (  # noqa
    'rest_framework.renderers.BrowsableAPIRenderer',)
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (  # noqa
    'rest_framework.authentication.SessionAuthentication',)
