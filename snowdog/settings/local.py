import sys

from .base import *

print('>>>>>>>>>> local <<<<<<<<<<')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache:11211',
    }
}


if 'test' in sys.argv:

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
