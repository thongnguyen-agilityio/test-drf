import os

from app.settings.components import BASE_DIR

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = False

ALLOWED_HOSTS += [
    '127.0.0.1',
    '0.0.0.0',
    'drf-ecs-alb-159461053.us-east-1.elb.amazonaws.com'
]
