import django_heroku
from memcacheify import memcacheify

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['https://snowdog-pokemonapp.herokuapp.com/']

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

CACHES = memcacheify()
django_heroku.settings(locals())

